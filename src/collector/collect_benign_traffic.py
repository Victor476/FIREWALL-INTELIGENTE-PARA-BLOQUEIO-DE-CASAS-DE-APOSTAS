import os
import sys
import time
import json
import random
import shutil
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Callable

from src.collector.session_orchestrator import run_collection_session, DEFAULT_RAW_DIR

# Lista diversificada de sítios de controlo benigno cobrindo múltiplos domínios e categorias (AC3)
# (Streaming, notícias, enciclopédias, esportes e tecnologia)
DEFAULT_BENIGN_TARGETS = [
    # Streaming & Vídeo / Áudio (8 alvos)
    {"name": "youtube", "domain": "https://www.youtube.com", "category": "streaming"},
    {"name": "vimeo", "domain": "https://vimeo.com", "category": "streaming"},
    {"name": "twitch", "domain": "https://www.twitch.tv", "category": "streaming"},
    {"name": "dailymotion", "domain": "https://www.dailymotion.com", "category": "streaming"},
    {"name": "soundcloud", "domain": "https://soundcloud.com", "category": "audio_streaming"},
    {"name": "spotify", "domain": "https://open.spotify.com", "category": "audio_streaming"},
    {"name": "ted", "domain": "https://www.ted.com", "category": "streaming"},
    {"name": "bandcamp", "domain": "https://bandcamp.com", "category": "audio_streaming"},

    # Notícias & Portais de Informação (12 alvos)
    {"name": "g1_noticias", "domain": "https://g1.globo.com", "category": "news"},
    {"name": "uol", "domain": "https://www.uol.com.br", "category": "portal"},
    {"name": "bbc_noticias", "domain": "https://www.bbc.com/portuguese", "category": "news"},
    {"name": "cnn_brasil", "domain": "https://www.cnnbrasil.com.br", "category": "news"},
    {"name": "globo_esporte", "domain": "https://ge.globo.com", "category": "sports_news"},
    {"name": "folha_sp", "domain": "https://www.folha.uol.com.br", "category": "news"},
    {"name": "estadao", "domain": "https://www.estadao.com.br", "category": "news"},
    {"name": "r7_noticias", "domain": "https://www.r7.com", "category": "portal"},
    {"name": "terra", "domain": "https://www.terra.com.br", "category": "portal"},
    {"name": "reuters", "domain": "https://www.reuters.com", "category": "news"},
    {"name": "elpais_brasil", "domain": "https://brasil.elpais.com", "category": "news"},
    {"name": "lance", "domain": "https://www.lance.com.br", "category": "sports_news"},

    # Enciclopédias, Educação & Ciência (8 alvos)
    {"name": "wikipedia", "domain": "https://pt.wikipedia.org", "category": "reference"},
    {"name": "internet_archive", "domain": "https://archive.org", "category": "reference"},
    {"name": "wikihow", "domain": "https://pt.wikihow.com", "category": "education"},
    {"name": "khan_academy", "domain": "https://pt.khanacademy.org", "category": "education"},
    {"name": "coursera", "domain": "https://www.coursera.org", "category": "education"},
    {"name": "mit_ocw", "domain": "https://ocw.mit.edu", "category": "education"},
    {"name": "sciencedirect", "domain": "https://www.sciencedirect.com", "category": "science"},
    {"name": "britannica", "domain": "https://www.britannica.com", "category": "reference"},

    # Tecnologia, Blogs & Fóruns de Discussão (10 alvos)
    {"name": "github", "domain": "https://github.com", "category": "tech"},
    {"name": "stackoverflow", "domain": "https://stackoverflow.com", "category": "tech"},
    {"name": "techcrunch", "domain": "https://techcrunch.com", "category": "tech_news"},
    {"name": "canaltech", "domain": "https://canaltech.com.br", "category": "tech_news"},
    {"name": "techtudo", "domain": "https://www.techtudo.com.br", "category": "tech_news"},
    {"name": "medium", "domain": "https://medium.com", "category": "blogs"},
    {"name": "reddit", "domain": "https://www.reddit.com", "category": "community"},
    {"name": "quora", "domain": "https://pt.quora.com", "category": "community"},
    {"name": "dev_to", "domain": "https://dev.to", "category": "tech"},
    {"name": "hacker_news", "domain": "https://news.ycombinator.com", "category": "tech_news"},

    # E-commerce, Marketplace & Serviços de Viagem (8 alvos)
    {"name": "mercadolivre", "domain": "https://www.mercadolivre.com.br", "category": "ecommerce"},
    {"name": "amazon_br", "domain": "https://www.amazon.com.br", "category": "ecommerce"},
    {"name": "magazineluiza", "domain": "https://www.magazineluiza.com.br", "category": "ecommerce"},
    {"name": "shopee", "domain": "https://shopee.com.br", "category": "ecommerce"},
    {"name": "olx", "domain": "https://www.olx.com.br", "category": "marketplace"},
    {"name": "booking", "domain": "https://www.booking.com", "category": "travel"},
    {"name": "tripadvisor", "domain": "https://www.tripadvisor.com.br", "category": "travel"},
    {"name": "airbnb", "domain": "https://www.airbnb.com.br", "category": "travel"},

    # Institucional, Governamental & Clima (4 alvos)
    {"name": "gov_br", "domain": "https://www.gov.br", "category": "government"},
    {"name": "ibge", "domain": "https://www.ibge.gov.br", "category": "government"},
    {"name": "receita_federal", "domain": "https://www.gov.br/receitafederal", "category": "government"},
    {"name": "climatempo", "domain": "https://www.climatempo.com.br", "category": "weather"},
]

# Configuração de Logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("BenignCollector")


def resolve_output_dir(custom_path: Optional[Union[str, Path]] = None) -> Path:
    """
    Resolve o diretório de destino priorizando caminho explícito, variável de ambiente ou diretório padrão.
    """
    if custom_path:
        out = Path(custom_path)
    else:
        env_dir = os.environ.get("RAW_DATA_DIR")
        if env_dir:
            out = Path(env_dir)
        elif Path("/app/data/raw").exists():
            out = Path("/app/data/raw")
        elif Path("data/raw").exists():
            out = Path("data/raw").resolve()
        else:
            out = DEFAULT_RAW_DIR
    out.mkdir(parents=True, exist_ok=True)
    return out


def load_targets_from_file(filepath: Union[str, Path]) -> List[Dict[str, str]]:
    """Carrega lista de alvos de controlo a partir de um arquivo JSON estruturado."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo de alvos benignos não encontrado: {filepath}")
    with open(path, "r", encoding="utf-8") as f:
        targets = json.load(f)
    if not isinstance(targets, list) or not targets:
        raise ValueError("O arquivo de alvos deve conter uma lista JSON não-vazia de objetos.")
    return targets


def check_disk_space(path: Path, min_free_mb: float = 500.0) -> bool:
    """Verifica se há espaço suficiente em disco antes de gravar novas capturas de tráfego."""
    try:
        usage = shutil.disk_usage(path)
        free_mb = usage.free / (1024 * 1024)
        return free_mb >= min_free_mb
    except Exception as e:
        logger.warning(f"Não foi possível verificar espaço em disco: {e}")
        return True


def execute_benign_batch(
    targets: Optional[List[Dict[str, str]]] = None,
    iterations_per_site: int = 5,
    duration_per_session: int = 60,
    output_dir: Optional[Union[str, Path]] = None,
    interface: str = "eth0",
    min_cooldown: float = 5.0,
    max_cooldown: float = 12.0,
    bpf_filter: Optional[str] = None,
    session_runner: Optional[Callable] = None,
    save_manifest: bool = True
) -> Dict[str, Any]:
    """
    Executa a rotina automatizada de recolha de tráfego benigno de controlo (Issue #14).
    Gera arquivos PCAP estruturados com prefixo 'benigno_<servico>_' para a classe 0.
    """
    if iterations_per_site <= 0:
        raise ValueError("iterations_per_site deve ser maior ou igual a 1.")
    if duration_per_session <= 0:
        raise ValueError("duration_per_session deve ser maior ou igual a 1.")

    runner = session_runner or run_collection_session
    active_targets = targets if targets is not None else DEFAULT_BENIGN_TARGETS
    out_dir = resolve_output_dir(output_dir)

    print(f"[START] Iniciando recolha benigna para {len(active_targets)} alvos de controlo...")
    logger.info(
        f"Lote benigno configurado: {len(active_targets)} sítios x {iterations_per_site} iterações "
        f"({duration_per_session}s por sessão). Destino: {out_dir}"
    )

    batch_start_time = time.time()
    generated_files: List[str] = []
    successful_sessions = 0
    failed_sessions = 0
    session_records: List[Dict[str, Any]] = []

    for target in active_targets:
        target_name = target.get("name", "unknown")
        target_domain = target.get("domain", "")

        if not target_domain:
            logger.warning(f"Alvo benigno ignorado por URL ausente: {target}")
            continue

        for i in range(iterations_per_site):
            print(f"[EXEC] Recolhendo sessao benigna {i+1}/{iterations_per_site} em {target_name}...")

            # Verificação preventiva de espaço em disco
            if not check_disk_space(out_dir):
                logger.error(f"Espaço insuficiente em disco no diretório {out_dir}. Interrompendo lote.")
                break

            try:
                session_result = runner(
                    url=target_domain,
                    label=f"benigno_{target_name}",
                    duration=duration_per_session,
                    interface=interface,
                    output_dir=out_dir,
                    bpf_filter=bpf_filter
                )

                pcap_file = session_result.get("pcap_file", "")
                if pcap_file:
                    generated_files.append(pcap_file)
                successful_sessions += 1
                session_records.append({
                    "target": target_name,
                    "url": target_domain,
                    "category": target.get("category", "general"),
                    "iteration": i + 1,
                    "status": "success",
                    "pcap_file": pcap_file,
                    "file_size_bytes": session_result.get("file_size_bytes", 0)
                })

            except Exception as e:
                print(f"[WARN] Falha durante a recolha benigna em {target_name}: {e}")
                logger.warning(f"Erro ao capturar tráfego benigno de {target_name} ({target_domain}): {e}")
                failed_sessions += 1
                session_records.append({
                    "target": target_name,
                    "url": target_domain,
                    "category": target.get("category", "general"),
                    "iteration": i + 1,
                    "status": "failed",
                    "error": str(e)
                })

            # Intervalo aleatório de descanso (cooldown) para estabilização de buffers e anti-ban
            if i < (iterations_per_site - 1) or target != active_targets[-1]:
                cooldown = random.uniform(min_cooldown, max_cooldown)
                logger.debug(f"Pausa de estabilização entre sessões: {cooldown:.2f}s")
                time.sleep(cooldown)

    elapsed_time = round(time.time() - batch_start_time, 2)
    print(f"[OK] Lote de controlo benigno finalizado. Total de ficheiros gerados: {len(generated_files)}.")

    summary = {
        "batch_type": "benigno",
        "total_targets": len(active_targets),
        "iterations_per_site": iterations_per_site,
        "duration_per_session_seconds": duration_per_session,
        "successful_sessions": successful_sessions,
        "failed_sessions": failed_sessions,
        "total_files_generated": len(generated_files),
        "elapsed_time_seconds": elapsed_time,
        "output_directory": str(out_dir),
        "generated_files": generated_files,
        "sessions": session_records
    }

    if save_manifest and generated_files:
        manifest_path = out_dir / f"manifest_benign_batch_{int(batch_start_time)}.json"
        try:
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            logger.info(f"Manifesto de coleta benigna salvo em: {manifest_path}")
            summary["manifest_file"] = str(manifest_path)
        except Exception as e:
            logger.warning(f"Não foi possível salvar manifesto de lote benigno: {e}")

    return summary


def parse_args():
    parser = argparse.ArgumentParser(
        description="Coleta em Massa de Tráfego de Controle Benigno (Issue #14)"
    )
    parser.add_argument("--iterations", "-i", type=int, default=5, help="Iterações por sítio benigno (padrão: 5)")
    parser.add_argument("--duration", "-d", type=int, default=60, help="Duração de cada sessão em segundos (padrão: 60)")
    parser.add_argument("--output-dir", "-o", default=None, help="Diretório de destino dos arquivos PCAP")
    parser.add_argument("--interface", default="eth0", help="Interface de rede para o tcpdump (padrão: eth0)")
    parser.add_argument("--targets-file", default=None, help="Caminho para arquivo JSON com alvos benignos customizados")
    parser.add_argument("--min-cooldown", type=float, default=5.0, help="Tempo mínimo de descanso entre sessões (segundos)")
    parser.add_argument("--max-cooldown", type=float, default=12.0, help="Tempo máximo de descanso entre sessões (segundos)")
    parser.add_argument("--single-target", default=None, help="Executar coleta em apenas um sítio benigno específico")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    targets_to_run = DEFAULT_BENIGN_TARGETS
    if args.targets_file:
        targets_to_run = load_targets_from_file(args.targets_file)
    elif args.single_target:
        targets_to_run = [t for t in DEFAULT_BENIGN_TARGETS if t["name"] == args.single_target.lower()]
        if not targets_to_run:
            targets_to_run = [{"name": args.single_target, "domain": args.single_target, "category": "custom"}]

    print("=========================================================")
    print("🌐 Execução de Coleta de Tráfego Benigno (Issue #14)")
    print("=========================================================")
    print(f"📊 Alvos de controlo: {len(targets_to_run)}")
    print(f"🔄 Repetições por alvo: {args.iterations}")
    print(f"⏱️  Duração por sessão: {args.duration}s")
    print(f"🌐 Interface de rede: {args.interface}")
    print("=========================================================")

    results = execute_benign_batch(
        targets=targets_to_run,
        iterations_per_site=args.iterations,
        duration_per_session=args.duration,
        output_dir=args.output_dir,
        interface=args.interface,
        min_cooldown=args.min_cooldown,
        max_cooldown=args.max_cooldown
    )

    print("=========================================================")
    print("📊 Estatísticas Finais da Coleta Benigna:")
    for k in ["total_targets", "successful_sessions", "failed_sessions", "total_files_generated", "elapsed_time_seconds"]:
        print(f"   └─ {k}: {results.get(k)}")
    print("=========================================================")
