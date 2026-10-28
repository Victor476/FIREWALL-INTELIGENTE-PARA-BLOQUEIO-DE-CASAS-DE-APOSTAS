import os
import re
import sys
import time
import signal
import logging
import argparse
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, Any, Optional, Union, Callable

from src.collector.stealth_config import get_stealth_driver
from src.collector.human_behavior import simulate_human_session
from src.collector.bpf_filter import build_tcpdump_command, get_active_bpf_filter

# Diretório padrão para armazenamento de tráfego bruto (.pcap)
DEFAULT_RAW_DIR = Path(os.environ.get("RAW_DATA_DIR", "/data/raw"))

# Configuração de Logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("SessionOrchestrator")


def clean_url_domain(url: str) -> str:
    """
    Extrai e sanitiza o domínio ou hostname a partir de uma URL para uso seguro no nome de arquivos.
    Exemplo: 'https://betano.pt/sports/futebol' -> 'betano.pt'
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split("/")[0]
    # Remove porta se presente
    domain = domain.split(":")[0]
    # Remove prefixo www. para padronização de nomenclatura
    if domain.startswith("www."):
        domain = domain[4:]
    # Sanitiza caracteres que não sejam alfanuméricos, hífen ou ponto
    sanitized = re.sub(r"[^\w\.-]", "_", domain)
    return sanitized.strip("._") or "unknown_domain"


def generate_pcap_filename(
    label: str,
    url: str,
    timestamp: Optional[int] = None,
    output_dir: Optional[Union[str, Path]] = None
) -> Path:
    """
    Gera o caminho completo do arquivo PCAP seguindo o padrão estruturado:
    <classe>_<dominio>_<timestamp>.pcap
    Exemplo: apostas_betano.pt_1793158000.pcap
    """
    base_dir = Path(output_dir) if output_dir is not None else DEFAULT_RAW_DIR
    clean_domain = clean_url_domain(url)
    clean_label = re.sub(r"[^\w-]", "_", label.lower().strip())
    ts = timestamp if timestamp is not None else int(time.time())

    filename = f"{clean_label}_{clean_domain}_{ts}.pcap"
    return base_dir / filename


def start_packet_capture(
    output_pcap: Union[str, Path],
    interface: str = "eth0",
    bpf_filter: Optional[str] = None,
    stabilization_delay: float = 2.0
) -> subprocess.Popen:
    """
    Inicia o processo de captura do tcpdump em segundo plano com filtros BPF.
    Aguarda o tempo de estabilização para garantir que o filtro foi anexado ao kernel.
    """
    pcap_path = Path(output_pcap)
    pcap_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = build_tcpdump_command(
        output_file=str(pcap_path),
        interface=interface,
        bpf_filter=bpf_filter
    )

    logger.info("Inicializando captura para sessao de treino...")
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError as e:
        logger.error(f"Binário tcpdump não encontrado no sistema: {e}")
        raise

    logger.info(f"Processo tcpdump iniciado (PID: {proc.pid}).")

    # Verifica se o processo morreu imediatamente (ex: erro de interface ou permissões)
    time.sleep(stabilization_delay)
    if proc.poll() is not None:
        raise RuntimeError(f"O processo tcpdump encerrou inesperadamente com código de saída {proc.returncode}")

    return proc


def stop_packet_capture(proc: subprocess.Popen, timeout: float = 5.0) -> None:
    """
    Envia sinal de término gracioso (SIGINT) ao tcpdump para forçar descarga de buffers (flush)
    e fechamento correto do cabeçalho do arquivo PCAP.
    """
    if proc.poll() is not None:
        logger.debug("Processo de captura já havia sido encerrado.")
        return

    logger.info("Sinal SIGINT enviado ao sniffer. Finalizando gravacao...")
    try:
        # No Unix/Linux, SIGINT é o sinal padrão que o tcpdump espera para escrever metadados e fechar
        sig = getattr(signal, "SIGINT", signal.SIGTERM)
        proc.send_signal(sig)
    except Exception as e:
        logger.warning(f"Falha ao enviar sinal para PID {proc.pid}: {e}. Tentando terminate().")
        proc.terminate()

    try:
        proc.wait(timeout=timeout)
        logger.info("Processo tcpdump encerrado com sucesso.")
    except subprocess.TimeoutExpired:
        logger.warning(f"tcpdump (PID {proc.pid}) não encerrou em {timeout}s. Forçando kill().")
        proc.kill()
        proc.wait()


def run_collection_session(
    url: str,
    label: str,
    duration: int = 45,
    interface: str = "eth0",
    output_dir: Optional[Union[str, Path]] = None,
    bpf_filter: Optional[str] = None,
    headless: bool = True,
    driver_factory: Optional[Callable[[], Any]] = None,
    stabilization_delay: float = 2.0
) -> Dict[str, Any]:
    """
    Orquestra o ciclo completo sincronizado:
    1. Inicia tcpdump com BPF no nó de rede
    2. Aguarda estabilização do socket de escuta
    3. Inicializa o browser e emula comportamento humano
    4. Encerra o browser com segurança
    5. Finaliza o sniffer via SIGINT (flush de pacotes)
    6. Valida arquivo PCAP resultante
    """
    if duration <= 0:
        raise ValueError("A duração da sessão deve ser maior que 0 segundos.")

    target_dir = Path(output_dir) if output_dir is not None else DEFAULT_RAW_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    start_timestamp = int(time.time())
    pcap_path = generate_pcap_filename(
        label=label,
        url=url,
        timestamp=start_timestamp,
        output_dir=target_dir
    )

    sniffer_proc = start_packet_capture(
        output_pcap=pcap_path,
        interface=interface,
        bpf_filter=bpf_filter,
        stabilization_delay=stabilization_delay
    )

    driver = None
    behavior_stats = {}
    session_success = False

    try:
        logger.info(f"Navegador ativo em {url}. Simulando comportamento...")
        if driver_factory:
            driver = driver_factory()
        else:
            driver = get_stealth_driver(headless=headless)

        behavior_stats = simulate_human_session(driver, url, duration_seconds=duration)
        session_success = True
    except Exception as e:
        logger.error(f"Erro durante a navegação interativa na URL {url}: {e}")
        raise
    finally:
        # Encerramento gracioso do navegador
        if driver is not None:
            try:
                driver.quit()
                logger.info("Navegador encerrado com sucesso.")
            except Exception as e:
                logger.warning(f"Erro ao encerrar navegador: {e}")

        # Encerramento garantido do sniffer (sem deixar processos zumbis)
        stop_packet_capture(sniffer_proc)

    # Verificação do arquivo PCAP gerado
    file_size = pcap_path.stat().st_size if pcap_path.exists() else 0
    logger.info(f"[OK] Sessao finalizada. Arquivo gerado: {pcap_path} ({file_size} bytes)")

    return {
        "success": session_success,
        "url": url,
        "label": label,
        "pcap_file": str(pcap_path),
        "file_size_bytes": file_size,
        "duration_seconds": duration,
        "behavior_stats": behavior_stats,
        "timestamp": start_timestamp
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Orquestrador de Coleta e Sincronia de Tráfego (Issue #12)"
    )
    parser.add_argument("url", nargs="?", default="https://betano.pt", help="URL do site alvo")
    parser.add_argument("--label", "-l", default="apostas", choices=["apostas", "benigno"], help="Rótulo da classe da sessão")
    parser.add_argument("--duration", "-d", type=int, default=45, help="Duração da sessão em segundos")
    parser.add_argument("--interface", "-i", default="eth0", help="Interface de rede para escuta do tcpdump")
    parser.add_argument("--output-dir", "-o", default=str(DEFAULT_RAW_DIR), help="Diretório destino dos arquivos PCAP")
    parser.add_argument("--bpf", default=None, help="Expressão BPF customizada")
    parser.add_argument("--no-headless", action="store_true", help="Desativa modo headless do navegador")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print("=========================================================")
    print("🎬 Orquestrador de Sessão de Coleta (Issue #12)")
    print("=========================================================")
    print(f"🎯 Alvo: {args.url}")
    print(f"🏷️  Classe: {args.label}")
    print(f"⏱️  Duração: {args.duration}s")
    print(f"📁 Diretório de Saída: {args.output_dir}")
    print("=========================================================")

    try:
        results = run_collection_session(
            url=args.url,
            label=args.label,
            duration=args.duration,
            interface=args.interface,
            output_dir=args.output_dir,
            bpf_filter=args.bpf,
            headless=not args.no_headless
        )
        print("=========================================================")
        print("📊 Resumo da Sessão:")
        for k, v in results.items():
            print(f"   └─ {k}: {v}")
        print("=========================================================")
    except Exception as err:
        logger.error(f"Falha na execução da sessão de coleta: {err}")
        sys.exit(1)
