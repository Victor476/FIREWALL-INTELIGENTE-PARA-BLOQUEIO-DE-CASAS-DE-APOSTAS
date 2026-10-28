import os
import signal
import pytest
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch, call

from src.collector.session_orchestrator import (
    clean_url_domain,
    generate_pcap_filename,
    start_packet_capture,
    stop_packet_capture,
    run_collection_session,
    parse_args
)

# -------------------------------------------------------------
# Testes de sanitização de domínio e geração de nomes
# -------------------------------------------------------------
def test_clean_url_domain_variations():
    """Valida a extração e sanitização de domínio para múltiplos formatos de URL."""
    assert clean_url_domain("https://betano.pt") == "betano.pt"
    assert clean_url_domain("https://www.bet365.com/sports") == "bet365.com"
    assert clean_url_domain("http://sports.bwin.com:8080/live?id=123") == "sports.bwin.com"
    assert clean_url_domain("betfair.com/exchange") == "betfair.com"
    assert clean_url_domain("https://sub.domain-test.co.uk/") == "sub.domain-test.co.uk"


def test_generate_pcap_filename_format(tmp_path):
    """Garante a conformidade da nomenclatura com o padrão <classe>_<dominio>_<timestamp>.pcap."""
    pcap = generate_pcap_filename(
        label="apostas",
        url="https://betano.pt",
        timestamp=1793158000,
        output_dir=tmp_path
    )
    assert pcap.name == "apostas_betano.pt_1793158000.pcap"
    assert pcap.parent == tmp_path


def test_generate_pcap_filename_benign_label(tmp_path):
    """Valida geração de nome para tráfego benigno."""
    pcap = generate_pcap_filename(
        label="benigno",
        url="https://www.youtube.com/watch?v=abc",
        timestamp=1793159000,
        output_dir=tmp_path
    )
    assert pcap.name == "benigno_youtube.com_1793159000.pcap"


# -------------------------------------------------------------
# Testes de start_packet_capture
# -------------------------------------------------------------
@patch("src.collector.session_orchestrator.time.sleep")
@patch("src.collector.session_orchestrator.subprocess.Popen")
def test_start_packet_capture_success(mock_popen, mock_sleep, tmp_path):
    """Garante que o tcpdump é inicializado com comando correto e estabilização de socket."""
    mock_proc = MagicMock()
    mock_proc.pid = 4321
    mock_proc.poll.return_value = None  # Processo continua rodando
    mock_popen.return_value = mock_proc

    out_file = tmp_path / "test.pcap"
    proc = start_packet_capture(output_pcap=out_file, interface="eth0", stabilization_delay=1.5)

    assert proc == mock_proc
    mock_popen.assert_called_once()
    mock_sleep.assert_called_once_with(1.5)
    
    cmd_args = mock_popen.call_args[0][0]
    assert cmd_args[0] == "tcpdump"
    assert "-i" in cmd_args and "eth0" in cmd_args
    assert str(out_file) in cmd_args


@patch("src.collector.session_orchestrator.time.sleep")
@patch("src.collector.session_orchestrator.subprocess.Popen")
def test_start_packet_capture_premature_exit(mock_popen, mock_sleep, tmp_path):
    """Lança RuntimeError se o tcpdump falhar imediatamente após o disparo."""
    mock_proc = MagicMock()
    mock_proc.pid = 9999
    mock_proc.poll.return_value = 1  # Processo morreu imediatamente
    mock_proc.returncode = 1
    mock_popen.return_value = mock_proc

    out_file = tmp_path / "crash.pcap"
    with pytest.raises(RuntimeError, match="encerrou inesperadamente"):
        start_packet_capture(output_pcap=out_file, stabilization_delay=0.1)


# -------------------------------------------------------------
# Testes de stop_packet_capture
# -------------------------------------------------------------
def test_stop_packet_capture_graceful_sigint():
    """Garante que SIGINT é enviado para flush de pacotes do tcpdump."""
    mock_proc = MagicMock()
    mock_proc.poll.return_value = None
    mock_proc.pid = 1234

    stop_packet_capture(mock_proc, timeout=2.0)

    # Verifica envio de SIGINT (ou SIGTERM)
    mock_proc.send_signal.assert_called_once_with(signal.SIGINT)
    mock_proc.wait.assert_called_once_with(timeout=2.0)
    mock_proc.kill.assert_not_called()


def test_stop_packet_capture_already_terminated():
    """Não deve tentar enviar sinais se o processo já tiver encerrado."""
    mock_proc = MagicMock()
    mock_proc.poll.return_value = 0  # Já encerrado

    stop_packet_capture(mock_proc)
    mock_proc.send_signal.assert_not_called()
    mock_proc.wait.assert_not_called()


def test_stop_packet_capture_timeout_triggers_kill():
    """Garante que processo travado é eliminado forçadamente via kill() após timeout."""
    mock_proc = MagicMock()
    mock_proc.poll.return_value = None
    mock_proc.pid = 5555
    mock_proc.wait.side_effect = [subprocess.TimeoutExpired(cmd="tcpdump", timeout=1.0), None]

    stop_packet_capture(mock_proc, timeout=1.0)

    mock_proc.send_signal.assert_called_once()
    mock_proc.kill.assert_called_once()


# -------------------------------------------------------------
# Testes de run_collection_session
# -------------------------------------------------------------
@patch("src.collector.session_orchestrator.start_packet_capture")
@patch("src.collector.session_orchestrator.stop_packet_capture")
@patch("src.collector.session_orchestrator.simulate_human_session")
def test_run_collection_session_success_lifecycle(mock_simulate, mock_stop, mock_start, tmp_path):
    """Valida o ciclo completo sincronizado de captura e navegação."""
    mock_proc = MagicMock()
    mock_start.return_value = mock_proc
    mock_simulate.return_value = {"completed": True, "scroll_count": 5}

    mock_driver = MagicMock()
    mock_driver_factory = MagicMock(return_value=mock_driver)

    result = run_collection_session(
        url="https://betano.pt",
        label="apostas",
        duration=30,
        interface="eth0",
        output_dir=tmp_path,
        driver_factory=mock_driver_factory,
        stabilization_delay=0.1
    )

    assert result["success"] is True
    assert result["url"] == "https://betano.pt"
    assert result["label"] == "apostas"
    assert result["duration_seconds"] == 30
    assert "betano.pt" in result["pcap_file"]
    assert result["behavior_stats"]["completed"] is True

    # 1. Captura iniciada antes do browser
    mock_start.assert_called_once()
    # 2. Browser navega e encerra
    mock_simulate.assert_called_once_with(mock_driver, "https://betano.pt", duration_seconds=30)
    mock_driver.quit.assert_called_once()
    # 3. Captura finalizada graciosamente
    mock_stop.assert_called_once_with(mock_proc)


@patch("src.collector.session_orchestrator.start_packet_capture")
@patch("src.collector.session_orchestrator.stop_packet_capture")
@patch("src.collector.session_orchestrator.simulate_human_session")
def test_run_collection_session_browser_exception_resilience(mock_simulate, mock_stop, mock_start, tmp_path):
    """Garante que mesmo em caso de erro no browser, o sniffer é finalizado sem deixar zumbis."""
    mock_proc = MagicMock()
    mock_start.return_value = mock_proc
    mock_simulate.side_effect = RuntimeError("Selenium crashed")

    mock_driver = MagicMock()
    mock_driver_factory = MagicMock(return_value=mock_driver)

    with pytest.raises(RuntimeError, match="Selenium crashed"):
        run_collection_session(
            url="https://bet365.com",
            label="apostas",
            duration=20,
            output_dir=tmp_path,
            driver_factory=mock_driver_factory,
            stabilization_delay=0.1
        )

    # Confirma que driver e sniffer foram fechados no bloco finally
    mock_driver.quit.assert_called_once()
    mock_stop.assert_called_once_with(mock_proc)


def test_run_collection_session_invalid_duration():
    """Valida rejeição de durações inválidas."""
    with pytest.raises(ValueError, match="maior que 0"):
        run_collection_session(url="https://betano.pt", label="apostas", duration=0)


# -------------------------------------------------------------
# Teste de parsing de CLI
# -------------------------------------------------------------
def test_parse_args_defaults():
    """Valida argumentos padrão da interface de comando."""
    with patch("sys.argv", ["session_orchestrator.py"]):
        args = parse_args()
        assert args.url == "https://betano.pt"
        assert args.label == "apostas"
        assert args.duration == 45
        assert args.interface == "eth0"
        assert args.no_headless is False


def test_parse_args_custom():
    """Valida argumentos customizados passados por linha de comando."""
    custom_argv = [
        "session_orchestrator.py",
        "https://youtube.com",
        "--label", "benigno",
        "--duration", "60",
        "--interface", "eth1",
        "--output-dir", "/custom/raw",
        "--no-headless"
    ]
    with patch("sys.argv", custom_argv):
        args = parse_args()
        assert args.url == "https://youtube.com"
        assert args.label == "benigno"
        assert args.duration == 60
        assert args.interface == "eth1"
        assert args.output_dir == "/custom/raw"
        assert args.no_headless is True
