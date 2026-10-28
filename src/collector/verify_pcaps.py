import os
import sys
import time
import json
import shutil
import struct
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, Union, Tuple, List

try:
    from scapy.all import PcapReader
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

# Diretórios padrão
DEFAULT_RAW_DIR = Path(os.environ.get("RAW_DATA_DIR", "/data/raw"))
DEFAULT_CORRUPTED_DIR = Path(os.environ.get("CORRUPTED_DATA_DIR", "/data/corrupted"))
DEFAULT_MIN_PACKETS = 15

# Magic numbers suportados da Libpcap (Big-Endian e Little-Endian, microsegundos e nanosegundos)
LIBPCAP_MAGIC_NUMBERS = {
    0xa1b2c3d4: "Libpcap padrão (Big-Endian, microsegundos)",
    0xd4c3b2a1: "Libpcap padrão (Little-Endian, microsegundos)",
    0xa1b23c4d: "Libpcap nanosegundos (Big-Endian)",
    0x4d3cb2a1: "Libpcap nanosegundos (Little-Endian)",
    0x0a0d0d0a: "PCAPNG Section Header Block",
}

# Configuração de Logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("PcapVerifier")


def resolve_directories(
    raw_path: Optional[Union[str, Path]] = None,
    corrupted_path: Optional[Union[str, Path]] = None
) -> Tuple[Path, Path]:
    """
    Resolve caminhos dos diretórios de dados brutos e quarentena,
    com suporte a caminhos no container (/data/raw) ou no host local (data/raw).
    """
    if raw_path:
        r_dir = Path(raw_path)
    elif os.environ.get("RAW_DATA_DIR"):
        r_dir = Path(os.environ["RAW_DATA_DIR"])
    elif Path("/app/data/raw").exists():
        r_dir = Path("/app/data/raw")
    elif Path("data/raw").exists():
        r_dir = Path("data/raw").resolve()
    else:
        r_dir = DEFAULT_RAW_DIR

    if corrupted_path:
        c_dir = Path(corrupted_path)
    elif os.environ.get("CORRUPTED_DATA_DIR"):
        c_dir = Path(os.environ["CORRUPTED_DATA_DIR"])
    elif Path("/app/data/corrupted").exists():
        c_dir = Path("/app/data/corrupted")
    elif Path("data/corrupted").exists():
        c_dir = Path("data/corrupted").resolve()
    else:
        # Se raw for data/raw relativo, coloca corrupted no mesmo nível
        if "raw" in r_dir.parts:
            c_dir = r_dir.parent / "corrupted"
        else:
            c_dir = DEFAULT_CORRUPTED_DIR

    r_dir.mkdir(parents=True, exist_ok=True)
    c_dir.mkdir(parents=True, exist_ok=True)
    return r_dir, c_dir


def check_pcap_header(filepath: Path) -> Tuple[bool, str]:
    """
    Verifica a integridade do cabeçalho global Libpcap (24 bytes) e o magic number.
    (Critério de Aceitação AC1).
    """
    if not filepath.exists() or not filepath.is_file():
        return False, "Arquivo não encontrado ou inacessível"

    size = filepath.stat().st_size
    if size < 24:
        return False, f"Arquivo vazio ou menor que o cabeçalho global Libpcap ({size} bytes < 24 bytes)"

    try:
        with open(filepath, "rb") as f:
            header_bytes = f.read(24)
            if len(header_bytes) < 24:
                return False, f"Cabeçalho truncado: leitura retornou apenas {len(header_bytes)} bytes"

            magic = struct.unpack("!I", header_bytes[:4])[0]
            if magic in LIBPCAP_MAGIC_NUMBERS:
                return True, f"Magic number válido: {hex(magic)} ({LIBPCAP_MAGIC_NUMBERS[magic]})"

            # Tenta verificar em little-endian se falhou no big-endian
            magic_le = struct.unpack("<I", header_bytes[:4])[0]
            if magic_le in LIBPCAP_MAGIC_NUMBERS:
                return True, f"Magic number válido: {hex(magic_le)} ({LIBPCAP_MAGIC_NUMBERS[magic_le]})"

            return False, f"Magic number inválido: {hex(magic)} / {hex(magic_le)}"
    except Exception as e:
        return False, f"Erro ao ler cabeçalho do arquivo: {e}"


def count_packets_streaming(filepath: Path, stop_at: Optional[int] = None) -> Tuple[bool, int, str]:
    """
    Conta os pacotes do arquivo PCAP utilizando leitura por fluxo (streaming)
    sem carregar o arquivo inteiro na memória (RNF02).
    Valida a integridade de cada registro de pacote contra truncamento prematuro.
    """
    count = 0
    try:
        with open(filepath, "rb") as f:
            header = f.read(24)
            if len(header) < 24:
                return False, 0, f"Cabeçalho truncado ({len(header)} bytes < 24 bytes)"

            magic = struct.unpack("<I", header[:4])[0]
            if magic in (0xa1b2c3d4, 0xa1b23c4d):
                endian = "<"
            else:
                endian = ">"

            while True:
                pkt_hdr = f.read(16)
                if not pkt_hdr:
                    break
                if len(pkt_hdr) < 16:
                    return False, count, f"Cabeçalho de pacote truncado (EOF prematuro após {count} pacotes)"

                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(f"{endian}IIII", pkt_hdr)
                if incl_len > 65535 * 4:
                    return False, count, f"Comprimento de pacote anormalmente grande ({incl_len} bytes)"

                packet_data = f.read(incl_len)
                if len(packet_data) < incl_len:
                    return False, count, f"Carga de pacote truncada (esperado {incl_len} bytes, lido {len(packet_data)} bytes)"

                count += 1
                if stop_at is not None and count >= stop_at:
                    break

        # Se Scapy estiver disponível, valida a compatibilidade com PcapReader (respeitando streaming)
        if HAS_SCAPY and count > 0:
            try:
                scapy_count = 0
                with PcapReader(str(filepath)) as reader:
                    for _ in reader:
                        scapy_count += 1
                        if stop_at is not None and scapy_count >= stop_at:
                            break
            except Exception as e:
                return False, count, f"Scapy pcap reading error: {e}"

        return True, count, "Sucesso na leitura de pacotes via streaming"
    except Exception as e:
        return False, count, f"Erro na análise de pacotes: {e}"


def validate_pcap(filepath: Path, min_packets: int = DEFAULT_MIN_PACKETS) -> Tuple[bool, int, str]:
    """
    Executa a validação completa de integridade de um arquivo PCAP:
    1. Validação do cabeçalho global Libpcap (AC1)
    2. Validação sintática e contagem mínima de pacotes via streaming (AC2)
    """
    # 1. Checagem de cabeçalho
    header_ok, header_msg = check_pcap_header(filepath)
    if not header_ok:
        return False, 0, header_msg

    # 2. Leitura de pacotes via streaming
    packets_ok, packet_count, stream_msg = count_packets_streaming(filepath)
    if not packets_ok:
        return False, packet_count, stream_msg

    # 3. Verificação do volume mínimo de pacotes
    if packet_count < min_packets:
        return False, packet_count, f"Volume insuficiente de pacotes ({packet_count} < {min_packets})"

    return True, packet_count, "Integridade e volume validados com sucesso"


def infer_class_from_filename(filename: str) -> str:
    """Extrai a classe da sessão a partir do prefixo do nome do arquivo."""
    name_lower = filename.lower()
    if name_lower.startswith("apostas_") or name_lower.startswith("classe1_"):
        return "apostas"
    elif name_lower.startswith("benigno_") or name_lower.startswith("classe0_"):
        return "benigno"
    return "outros"


def run_validation(
    raw_dir: Optional[Union[str, Path]] = None,
    corrupted_dir: Optional[Union[str, Path]] = None,
    min_packets: int = DEFAULT_MIN_PACKETS,
    dry_run: bool = False,
    save_report: bool = True
) -> Dict[str, Any]:
    """
    Analisa em lote todos os arquivos PCAP no diretório bruto,
    isole os corrompidos/insuficientes na pasta de quarentena e gera sumário estatístico (AC3 e AC4).
    """
    r_dir, c_dir = resolve_directories(raw_dir, corrupted_dir)
    pcap_files = sorted(list(r_dir.glob("*.pcap")))

    print(f"[INFO] Iniciando verificação de integridade dos arquivos PCAP em {r_dir}...")
    logger.info(f"Arquivos PCAP localizados para inspeção: {len(pcap_files)} (Mínimo requerido: {min_packets} pacotes).")

    valid_count = 0
    invalid_count = 0
    class_stats = {
        "apostas": {"valid": 0, "invalid": 0},
        "benigno": {"valid": 0, "invalid": 0},
        "outros": {"valid": 0, "invalid": 0}
    }
    anomalies: List[Dict[str, Any]] = []

    for pcap_path in pcap_files:
        pcap_name = pcap_path.name
        cls_name = infer_class_from_filename(pcap_name)
        is_valid, pkt_count, reason = validate_pcap(pcap_path, min_packets=min_packets)

        if is_valid:
            valid_count += 1
            class_stats[cls_name]["valid"] += 1
            print(f"[OK] {pcap_name} validado com sucesso ({pkt_count} pacotes).")
        else:
            invalid_count += 1
            class_stats[cls_name]["invalid"] += 1
            print(f"[ERRO] Falha de integridade em {pcap_name}: {reason}.")

            dest_path = c_dir / pcap_name
            if not dry_run:
                try:
                    shutil.move(str(pcap_path), str(dest_path))
                    print(f"[QUARENTENA] Ficheiro movido: {pcap_name}")
                except Exception as e:
                    logger.error(f"Erro ao mover {pcap_name} para quarentena: {e}")
            else:
                print(f"[DRY-RUN] Ficheiro seria movido para quarentena: {pcap_name}")

            anomalies.append({
                "filename": pcap_name,
                "class": cls_name,
                "packet_count": pkt_count,
                "file_size_bytes": pcap_path.stat().st_size if pcap_path.exists() else 0,
                "reason": reason,
                "quarantine_path": str(dest_path)
            })

    # Exibição do sumário estatístico estruturado (AC4)
    print(f"\n[SUMÁRIO] Válidos: {valid_count} | Corrompidos/Insuficientes: {invalid_count}")
    print("=========================================================")
    print("📊 Sumário de Validação de Capturas por Classe:")
    print("=========================================================")
    for c_key in ["apostas", "benigno", "outros"]:
        v = class_stats[c_key]["valid"]
        inv = class_stats[c_key]["invalid"]
        total = v + inv
        if total > 0:
            pct = (v / total) * 100
            print(f"   ├─ {c_key.capitalize()}: {v} válidos / {inv} descartados ({pct:.1f}% aprovação)")
    print("=========================================================")

    summary = {
        "timestamp": int(time.time()),
        "raw_directory": str(r_dir),
        "corrupted_directory": str(c_dir),
        "total_inspected": len(pcap_files),
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "class_stats": class_stats,
        "anomalies": anomalies
    }

    if save_report and anomalies:
        report_path = c_dir / f"anomaly_report_{int(time.time())}.json"
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            logger.info(f"Relatório de anomalias gravado em: {report_path}")
            summary["report_file"] = str(report_path)
        except Exception as e:
            logger.warning(f"Não foi possível gravar relatório de anomalias: {e}")

    return summary


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validação de Integridade Estrutural de Arquivos PCAP (Issue #15)"
    )
    parser.add_argument("--raw-dir", "-r", default=None, help="Diretório contendo arquivos PCAP brutos")
    parser.add_argument("--corrupted-dir", "-c", default=None, help="Diretório de quarentena para arquivos corrompidos")
    parser.add_argument("--min-packets", "-m", type=int, default=DEFAULT_MIN_PACKETS, help="Volume mínimo de pacotes por sessão")
    parser.add_argument("--dry-run", action="store_true", help="Apenas inspeciona sem mover arquivos para quarentena")
    parser.add_argument("--no-report", action="store_true", help="Não grava arquivo JSON de anomalias")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_validation(
        raw_dir=args.raw_dir,
        corrupted_dir=args.corrupted_dir,
        min_packets=args.min_packets,
        dry_run=args.dry_run,
        save_report=not args.no_report
    )
