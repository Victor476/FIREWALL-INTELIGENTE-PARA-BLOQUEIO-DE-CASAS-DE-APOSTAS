import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.collector.collect_benign_traffic import (
    DEFAULT_BENIGN_TARGETS,
    resolve_output_dir,
    load_targets_from_file,
    check_disk_space,
    execute_benign_batch,
    parse_args
)

# -------------------------------------------------------------
# Testes da lista de alvos benignos de controlo
# -------------------------------------------------------------
def test_default_benign_targets_diversity():
    """Garante que a lista padrão cobre pelo menos 10 serviços distintos e categorizados (AC3)."""
    assert len(DEFAULT_BENIGN_TARGETS) >= 10
    names = set()
    categories = set()
    for t in DEFAULT_BENIGN_TARGETS:
        assert "name" in t and isinstance(t["name"], str)
        assert "domain" in t and t["domain"].startswith(("http://", "https://"))
        assert "category" in t and isinstance(t["category"], str)
        names.add(t["name"])
        categories.add(t["category"])

    # Garante nomes únicos e diversidade de categorias (streaming, notícias, referência, etc.)
    assert len(names) == len(DEFAULT_BENIGN_TARGETS)
    assert len(categories) >= 4


# -------------------------------------------------------------
# Testes de resolução de diretório e carregamento de alvos
# -------------------------------------------------------------
def test_resolve_output_dir_custom(tmp_path):
    """Garante que o caminho customizado é resolvido e criado."""
    custom = tmp_path / "custom_benign_pcap_dir"
    res = resolve_output_dir(custom)
    assert res == custom
    assert custom.exists()


def test_load_targets_from_valid_json(tmp_path):
    """Valida o carregamento correto de alvos a partir de um JSON."""
    targets_data = [
        {"name": "youtube", "domain": "https://www.youtube.com", "category": "streaming"},
        {"name": "wikipedia", "domain": "https://pt.wikipedia.org", "category": "reference"}
    ]
    json_file = tmp_path / "benign_targets.json"
    json_file.write_text(json.dumps(targets_data), encoding="utf-8")

    loaded = load_targets_from_file(json_file)
    assert loaded == targets_data


def test_load_targets_file_not_found():
    """Lança FileNotFoundError para arquivo inexistente."""
    with pytest.raises(FileNotFoundError):
        load_targets_from_file("non_existent_benign.json")


def test_load_targets_invalid_json_format(tmp_path):
    """Lança ValueError para JSON que não contenha uma lista não-vazia."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="lista JSON não-vazia"):
        load_targets_from_file(bad_file)


# -------------------------------------------------------------
# Testes de verificação de espaço em disco
# -------------------------------------------------------------
@patch("src.collector.collect_benign_traffic.shutil.disk_usage")
def test_check_disk_space_sufficient(mock_usage, tmp_path):
    """Retorna True quando há espaço suficiente."""
    mock_usage.return_value = MagicMock(free=5 * 1024 * 1024 * 1024)
    assert check_disk_space(tmp_path, min_free_mb=500.0) is True


@patch("src.collector.collect_benign_traffic.shutil.disk_usage")
def test_check_disk_space_insufficient(mock_usage, tmp_path):
    """Retorna False quando o espaço em disco é crítico."""
    mock_usage.return_value = MagicMock(free=100 * 1024 * 1024)
    assert check_disk_space(tmp_path, min_free_mb=500.0) is False


# -------------------------------------------------------------
# Testes de execute_benign_batch
# -------------------------------------------------------------
@patch("src.collector.collect_benign_traffic.time.sleep")
def test_execute_benign_batch_success(mock_sleep, tmp_path):
    """Valida a execução completa do lote benigno com múltiplas repetições."""
    sample_targets = [
        {"name": "youtube", "domain": "https://www.youtube.com", "category": "streaming"},
        {"name": "wikipedia", "domain": "https://pt.wikipedia.org", "category": "reference"}
    ]

    mock_runner = MagicMock()
    mock_runner.side_effect = lambda url, label, duration, **kwargs: {
        "success": True,
        "pcap_file": str(tmp_path / f"{label}_123.pcap"),
        "file_size_bytes": 102400,
        "url": url
    }

    summary = execute_benign_batch(
        targets=sample_targets,
        iterations_per_site=2,
        duration_per_session=45,
        output_dir=tmp_path,
        min_cooldown=0.1,
        max_cooldown=0.2,
        session_runner=mock_runner,
        save_manifest=True
    )

    assert summary["batch_type"] == "benigno"
    assert summary["total_targets"] == 2
    assert summary["iterations_per_site"] == 2
    assert summary["successful_sessions"] == 4
    assert summary["failed_sessions"] == 0
    assert summary["total_files_generated"] == 4
    assert mock_runner.call_count == 4

    # Verifica se os rótulos das chamadas usam prefixo benigno_<target> (AC4)
    calls = mock_runner.call_args_list
    assert calls[0].kwargs["label"] == "benigno_youtube"
    assert calls[1].kwargs["label"] == "benigno_youtube"
    assert calls[2].kwargs["label"] == "benigno_wikipedia"
    assert calls[3].kwargs["label"] == "benigno_wikipedia"

    # Verifica geração do manifesto
    manifest_files = list(tmp_path.glob("manifest_benign_batch_*.json"))
    assert len(manifest_files) == 1


@patch("src.collector.collect_benign_traffic.time.sleep")
def test_execute_benign_batch_error_resilience(mock_sleep, tmp_path):
    """Garante que falhas temporárias em um site benigno não interrompem os demais alvos."""
    sample_targets = [
        {"name": "youtube_error", "domain": "https://error.com", "category": "streaming"},
        {"name": "wikipedia_ok", "domain": "https://ok.com", "category": "reference"}
    ]

    def mock_runner_fn(url, label, **kwargs):
        if "error" in url:
            raise ConnectionResetError("Connection reset by peer")
        return {
            "success": True,
            "pcap_file": str(tmp_path / f"{label}_123.pcap"),
            "file_size_bytes": 50000
        }

    summary = execute_benign_batch(
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


def test_execute_benign_batch_invalid_parameters():
    """Valida rejeição de parâmetros inválidos."""
    with pytest.raises(ValueError, match="iterations_per_site"):
        execute_benign_batch(iterations_per_site=0)
    with pytest.raises(ValueError, match="duration_per_session"):
        execute_benign_batch(duration_per_session=-5)


# -------------------------------------------------------------
# Testes do CLI
# -------------------------------------------------------------
def test_parse_args_defaults():
    """Valida argumentos padrão do CLI benigno."""
    with patch("sys.argv", ["collect_benign_traffic.py"]):
        args = parse_args()
        assert args.iterations == 5
        assert args.duration == 60
        assert args.interface == "eth0"
        assert args.targets_file is None
        assert args.single_target is None


def test_parse_args_custom():
    """Valida argumentos customizados passados por linha de comando."""
    custom_argv = [
        "collect_benign_traffic.py",
        "--iterations", "3",
        "--duration", "50",
        "--output-dir", "/data/benign",
        "--single-target", "youtube"
    ]
    with patch("sys.argv", custom_argv):
        args = parse_args()
        assert args.iterations == 3
        assert args.duration == 50
        assert args.output_dir == "/data/benign"
        assert args.single_target == "youtube"
