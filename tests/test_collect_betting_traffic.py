import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

from src.collector.collect_betting_traffic import (
    DEFAULT_BETTING_TARGETS,
    resolve_output_dir,
    load_targets_from_file,
    check_disk_space,
    execute_betting_batch,
    parse_args
)

# -------------------------------------------------------------
# Testes da lista de alvos de apostas
# -------------------------------------------------------------
def test_default_betting_targets_diversity():
    """Garante que a lista padrão cobre pelo menos 10 plataformas distintas (AC3)."""
    assert len(DEFAULT_BETTING_TARGETS) >= 10
    names = set()
    for t in DEFAULT_BETTING_TARGETS:
        assert "name" in t and isinstance(t["name"], str)
        assert "domain" in t and t["domain"].startswith(("http://", "https://"))
        names.add(t["name"])
    # Garante que os nomes de plataformas são únicos
    assert len(names) == len(DEFAULT_BETTING_TARGETS)


# -------------------------------------------------------------
# Testes de resolução de diretório e carregamento de alvos
# -------------------------------------------------------------
def test_resolve_output_dir_custom(tmp_path):
    """Garante que o caminho customizado é resolvido e criado."""
    custom = tmp_path / "custom_pcap_dir"
    res = resolve_output_dir(custom)
    assert res == custom
    assert custom.exists()


def test_load_targets_from_valid_json(tmp_path):
    """Valida o carregamento correto de alvos a partir de um JSON."""
    targets_data = [
        {"name": "siteA", "domain": "https://siteA.com"},
        {"name": "siteB", "domain": "https://siteB.com"}
    ]
    json_file = tmp_path / "targets.json"
    json_file.write_text(json.dumps(targets_data), encoding="utf-8")

    loaded = load_targets_from_file(json_file)
    assert loaded == targets_data


def test_load_targets_file_not_found():
    """Lança FileNotFoundError para arquivo inexistente."""
    with pytest.raises(FileNotFoundError):
        load_targets_from_file("non_existent_file.json")


def test_load_targets_invalid_json_format(tmp_path):
    """Lança ValueError para JSON que não contenha uma lista não-vazia."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="lista JSON não-vazia"):
        load_targets_from_file(bad_file)


# -------------------------------------------------------------
# Testes de verificação de espaço em disco
# -------------------------------------------------------------
@patch("src.collector.collect_betting_traffic.shutil.disk_usage")
def test_check_disk_space_sufficient(mock_usage, tmp_path):
    """Retorna True quando há espaço suficiente."""
    # 5 GB livres
    mock_usage.return_value = MagicMock(free=5 * 1024 * 1024 * 1024)
    assert check_disk_space(tmp_path, min_free_mb=500.0) is True


@patch("src.collector.collect_betting_traffic.shutil.disk_usage")
def test_check_disk_space_insufficient(mock_usage, tmp_path):
    """Retorna False quando o espaço em disco é crítico."""
    # 100 MB livres (abaixo de 500 MB)
    mock_usage.return_value = MagicMock(free=100 * 1024 * 1024)
    assert check_disk_space(tmp_path, min_free_mb=500.0) is False


# -------------------------------------------------------------
# Testes de execute_betting_batch
# -------------------------------------------------------------
@patch("src.collector.collect_betting_traffic.time.sleep")
def test_execute_betting_batch_success(mock_sleep, tmp_path):
    """Valida a execução completa do lote de apostas com múltiplas repetições."""
    sample_targets = [
        {"name": "bet365", "domain": "https://www.bet365.com"},
        {"name": "betano", "domain": "https://www.betano.pt"}
    ]

    mock_runner = MagicMock()
    mock_runner.side_effect = lambda url, label, duration, **kwargs: {
        "success": True,
        "pcap_file": str(tmp_path / f"{label}_123.pcap"),
        "file_size_bytes": 10240,
        "url": url
    }

    summary = execute_betting_batch(
        targets=sample_targets,
        iterations_per_site=2,
        duration_per_session=45,
        output_dir=tmp_path,
        min_cooldown=0.1,
        max_cooldown=0.2,
        session_runner=mock_runner,
        save_manifest=True
    )

    assert summary["batch_type"] == "apostas"
    assert summary["total_targets"] == 2
    assert summary["iterations_per_site"] == 2
    assert summary["successful_sessions"] == 4
    assert summary["failed_sessions"] == 0
    assert summary["total_files_generated"] == 4
    assert mock_runner.call_count == 4

    # Verifica se os rótulos das chamadas usam prefixo apostas_<target>
    calls = mock_runner.call_args_list
    assert calls[0].kwargs["label"] == "apostas_bet365"
    assert calls[1].kwargs["label"] == "apostas_bet365"
    assert calls[2].kwargs["label"] == "apostas_betano"
    assert calls[3].kwargs["label"] == "apostas_betano"

    # Verifica geração do manifesto
    manifest_files = list(tmp_path.glob("manifest_betting_batch_*.json"))
    assert len(manifest_files) == 1


@patch("src.collector.collect_betting_traffic.time.sleep")
def test_execute_betting_batch_error_resilience(mock_sleep, tmp_path):
    """Garante que falhas em um site não interrompem a recolha nos demais alvos."""
    sample_targets = [
        {"name": "fail_site", "domain": "https://fail.com"},
        {"name": "success_site", "domain": "https://ok.com"}
    ]

    def mock_runner_fn(url, label, **kwargs):
        if "fail" in url:
            raise RuntimeError("Cloudflare / WAF block")
        return {
            "success": True,
            "pcap_file": str(tmp_path / f"{label}_123.pcap"),
            "file_size_bytes": 5000
        }

    summary = execute_betting_batch(
        targets=sample_targets,
        iterations_per_site=1,
        duration_per_session=30,
        output_dir=tmp_path,
        session_runner=mock_runner_fn,
        save_manifest=False
    )

    assert summary["successful_sessions"] == 1
    assert summary["failed_sessions"] == 1
    assert summary["total_files_generated"] == 1
    assert summary["sessions"][0]["status"] == "failed"
    assert summary["sessions"][1]["status"] == "success"


def test_execute_betting_batch_invalid_parameters():
    """Valida rejeição de parâmetros inválidos."""
    with pytest.raises(ValueError, match="iterations_per_site"):
        execute_betting_batch(iterations_per_site=0)
    with pytest.raises(ValueError, match="duration_per_session"):
        execute_betting_batch(duration_per_session=-10)


# -------------------------------------------------------------
# Testes do CLI
# -------------------------------------------------------------
def test_parse_args_defaults():
    """Valida argumentos padrão do CLI."""
    with patch("sys.argv", ["collect_betting_traffic.py"]):
        args = parse_args()
        assert args.iterations == 5
        assert args.duration == 60
        assert args.interface == "eth0"
        assert args.targets_file is None
        assert args.single_target is None


def test_parse_args_custom():
    """Valida argumentos customizados passados por linha de comando."""
    custom_argv = [
        "collect_betting_traffic.py",
        "--iterations", "2",
        "--duration", "45",
        "--output-dir", "/data/custom",
        "--single-target", "betano"
    ]
    with patch("sys.argv", custom_argv):
        args = parse_args()
        assert args.iterations == 2
        assert args.duration == 45
        assert args.output_dir == "/data/custom"
        assert args.single_target == "betano"
