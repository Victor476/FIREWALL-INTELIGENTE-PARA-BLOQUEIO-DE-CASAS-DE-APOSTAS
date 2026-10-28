import json
import struct
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.collector.verify_pcaps import (
    check_pcap_header,
    count_packets_streaming,
    validate_pcap,
    infer_class_from_filename,
    resolve_directories,
    run_validation,
    parse_args
)

def create_synthetic_pcap(packet_count: int, packet_size: int = 64, corrupt_payload: bool = False) -> bytes:
    """Gera um binário PCAP sintético válido ou propositalmente truncado para testes."""
    # Cabeçalho global Libpcap (24 bytes, little-endian, Ethernet DLT 1)
    global_header = struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)
    packets = b""
    for i in range(packet_count):
        ph = struct.pack("<IIII", 1700000000 + i, 0, packet_size, packet_size)
        payload = b"\x00" * packet_size
        packets += ph + payload

    if corrupt_payload and packet_count > 0:
        # Trunca os últimos bytes para gerar erro de EOF prematuro
        packets = packets[:-20]

    return global_header + packets


# -------------------------------------------------------------
# Testes de infer_class_from_filename
# -------------------------------------------------------------
def test_infer_class_from_filename():
    """Valida o mapeamento de classes por prefixo de arquivo."""
    assert infer_class_from_filename("apostas_bet365_123.pcap") == "apostas"
    assert infer_class_from_filename("classe1_betano_456.pcap") == "apostas"
    assert infer_class_from_filename("benigno_youtube_789.pcap") == "benigno"
    assert infer_class_from_filename("classe0_uol_101.pcap") == "benigno"
    assert infer_class_from_filename("outro_arquivo.pcap") == "outros"


# -------------------------------------------------------------
# Testes de check_pcap_header
# -------------------------------------------------------------
def test_check_pcap_header_non_existent():
    """Retorna False para arquivo inexistente."""
    ok, msg = check_pcap_header(Path("inexistente.pcap"))
    assert ok is False
    assert "não encontrado" in msg


def test_check_pcap_header_too_small(tmp_path):
    """Retorna False para arquivo menor que 24 bytes."""
    small = tmp_path / "small.pcap"
    small.write_bytes(b"\x00" * 10)
    ok, msg = check_pcap_header(small)
    assert ok is False
    assert "menor que o cabeçalho" in msg


def test_check_pcap_header_invalid_magic(tmp_path):
    """Retorna False quando o magic number for inválido."""
    bad_magic = tmp_path / "bad_magic.pcap"
    bad_magic.write_bytes(b"\x12\x34\x56\x78" + b"\x00" * 20)
    ok, msg = check_pcap_header(bad_magic)
    assert ok is False
    assert "Magic number inválido" in msg


def test_check_pcap_header_valid(tmp_path):
    """Retorna True para cabeçalho Libpcap válido."""
    valid_pcap = tmp_path / "valid_hdr.pcap"
    valid_pcap.write_bytes(create_synthetic_pcap(packet_count=0))
    ok, msg = check_pcap_header(valid_pcap)
    assert ok is True
    assert "válido" in msg


# -------------------------------------------------------------
# Testes de validate_pcap
# -------------------------------------------------------------
def test_validate_pcap_insufficient_packets(tmp_path):
    """Rejeita PCAP com volume de pacotes abaixo do mínimo (ex: 5 < 15)."""
    pcap = tmp_path / "low_packets.pcap"
    pcap.write_bytes(create_synthetic_pcap(packet_count=5))

    is_valid, count, reason = validate_pcap(pcap, min_packets=15)
    assert is_valid is False
    assert count == 5
    assert "Volume insuficiente" in reason


def test_validate_pcap_sufficient_packets(tmp_path):
    """Aprova PCAP íntegro com volume suficiente (ex: 20 >= 15)."""
    pcap = tmp_path / "good.pcap"
    pcap.write_bytes(create_synthetic_pcap(packet_count=20))

    is_valid, count, reason = validate_pcap(pcap, min_packets=15)
    assert is_valid is True
    assert count >= 15
    assert "validados com sucesso" in reason


def test_validate_pcap_truncated_corrupted(tmp_path):
    """Detecta PCAP truncado com EOF prematuro."""
    pcap = tmp_path / "corrupted.pcap"
    pcap.write_bytes(create_synthetic_pcap(packet_count=20, corrupt_payload=True))

    is_valid, count, reason = validate_pcap(pcap, min_packets=15)
    assert is_valid is False
    assert ("truncad" in reason.lower() or "error" in reason.lower() or "eof" in reason.lower())


# -------------------------------------------------------------
# Testes de run_validation e isolamento em quarentena
# -------------------------------------------------------------
def test_run_validation_moves_corrupted_to_quarantine(tmp_path):
    """Garante que arquivos corrompidos/insuficientes são movidos para quarentena e válidos permanecem."""
    raw_dir = tmp_path / "raw"
    corrupted_dir = tmp_path / "corrupted"
    raw_dir.mkdir()
    corrupted_dir.mkdir()

    # Cria 1 válido de apostas (20 pacotes)
    good_bet = raw_dir / "apostas_betano_123.pcap"
    good_bet.write_bytes(create_synthetic_pcap(packet_count=20))

    # Cria 1 válido benigno (25 pacotes)
    good_benign = raw_dir / "benigno_youtube_456.pcap"
    good_benign.write_bytes(create_synthetic_pcap(packet_count=25))

    # Cria 1 corrompido de apostas (truncado)
    bad_bet = raw_dir / "apostas_bad_789.pcap"
    bad_bet.write_bytes(create_synthetic_pcap(packet_count=20, corrupt_payload=True))

    # Cria 1 com pacotes insuficientes benigno (3 pacotes < 15)
    low_benign = raw_dir / "benigno_empty_101.pcap"
    low_benign.write_bytes(create_synthetic_pcap(packet_count=3))

    summary = run_validation(
        raw_dir=raw_dir,
        corrupted_dir=corrupted_dir,
        min_packets=15,
        dry_run=False,
        save_report=True
    )

    assert summary["total_inspected"] == 4
    assert summary["valid_count"] == 2
    assert summary["invalid_count"] == 2

    # Verifica persistência dos arquivos válidos em raw
    assert (raw_dir / "apostas_betano_123.pcap").exists()
    assert (raw_dir / "benigno_youtube_456.pcap").exists()

    # Verifica isolamento dos arquivos inválidos em quarentena (AC3)
    assert not (raw_dir / "apostas_bad_789.pcap").exists()
    assert (corrupted_dir / "apostas_bad_789.pcap").exists()
    assert not (raw_dir / "benigno_empty_101.pcap").exists()
    assert (corrupted_dir / "benigno_empty_101.pcap").exists()

    # Verifica relatório de anomalias gravado
    reports = list(corrupted_dir.glob("anomaly_report_*.json"))
    assert len(reports) == 1

    # Verifica estatísticas por classe (AC4)
    assert summary["class_stats"]["apostas"]["valid"] == 1
    assert summary["class_stats"]["apostas"]["invalid"] == 1
    assert summary["class_stats"]["benigno"]["valid"] == 1
    assert summary["class_stats"]["benigno"]["invalid"] == 1


def test_run_validation_dry_run(tmp_path):
    """Garante que no modo dry-run nenhum arquivo é movido fisicamente."""
    raw_dir = tmp_path / "raw"
    corrupted_dir = tmp_path / "corrupted"
    raw_dir.mkdir()
    corrupted_dir.mkdir()

    bad_pcap = raw_dir / "apostas_fail.pcap"
    bad_pcap.write_bytes(b"\x00" * 5)  # Inválido

    summary = run_validation(raw_dir=raw_dir, corrupted_dir=corrupted_dir, dry_run=True)

    assert summary["invalid_count"] == 1
    # Arquivo deve continuar no raw_dir porque dry_run=True
    assert bad_pcap.exists()
    assert not (corrupted_dir / "apostas_fail.pcap").exists()


# -------------------------------------------------------------
# Testes do CLI
# -------------------------------------------------------------
def test_parse_args_defaults():
    """Valida argumentos padrão do CLI."""
    with patch("sys.argv", ["verify_pcaps.py"]):
        args = parse_args()
        assert args.raw_dir is None
        assert args.corrupted_dir is None
        assert args.min_packets == 15
        assert args.dry_run is False
        assert args.no_report is False


def test_parse_args_custom():
    """Valida argumentos customizados passados por CLI."""
    custom = [
        "verify_pcaps.py",
        "--raw-dir", "/data/custom_raw",
        "--corrupted-dir", "/data/custom_corrupted",
        "--min-packets", "30",
        "--dry-run",
        "--no-report"
    ]
    with patch("sys.argv", custom):
        args = parse_args()
        assert args.raw_dir == "/data/custom_raw"
        assert args.corrupted_dir == "/data/custom_corrupted"
        assert args.min_packets == 30
        assert args.dry_run is True
        assert args.no_report is True
