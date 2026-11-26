# -*- coding: utf-8 -*-
"""
Módulo de Extração de Metadados Brutos de Capturas PCAP.
Atende à Issue #16: [Backend] Extração de Metadados Brutos: Relatório de volume e duração por captura.

Requisitos relacionados:
- RF02: Sniffing Passivo (processamento de PCAP sem alterar payloads).
- RNF02: Restrição de Memória RAM (leitura por streaming sem carregar pacotes na memória).
- Seção 3.2.1 do TCC: Aquisição e Rotulagem (auditoria do balanceamento volumétrico e temporal).
"""

import os
import sys
import csv
import json
import math
import struct
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

# Configuração de logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("RawMetadataExtractor")

# Magic numbers da Libpcap (Big-Endian e Little-Endian, microsegundos e nanosegundos)
LIBPCAP_MAGIC_CONFIGS = {
    0xa1b2c3d4: (">", 1_000_000.0, "Libpcap Big-Endian (microsegundos)"),
    0xd4c3b2a1: ("<", 1_000_000.0, "Libpcap Little-Endian (microsegundos)"),
    0xa1b23c4d: (">", 1_000_000_000.0, "Libpcap Big-Endian (nanosegundos)"),
    0x4d3cb2a1: ("<", 1_000_000_000.0, "Libpcap Little-Endian (nanosegundos)"),
}


def infer_class_from_name(filename_or_path: Union[str, Path]) -> str:
    """
    Infere a classe da captura (betting ou benign) com base no nome do arquivo ou caminho.
    Retorna 'betting', 'benign' ou 'unknown'.
    """
    name = Path(filename_or_path).name.lower()
    parts = [p.lower() for p in Path(filename_or_path).parts]

    if "betting" in name or name.startswith("bet_") or "aposta" in name:
        return "betting"
    elif "benign" in name or "controle" in name or "noticia" in name or "stream" in name:
        return "benign"
    elif "betting" in parts:
        return "betting"
    elif "benign" in parts:
        return "benign"
    return "unknown"


def extract_pcap_file_metadata(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Lê os metadados brutos de um único arquivo PCAP via streaming de cabeçalhos
    sem carregar o conteúdo dos pacotes na memória RAM (RNF02).

    Retorna dicionário com os atributos brutos ou None se inválido/corrompido.
    """
    if not filepath.exists() or not filepath.is_file():
        logger.warning(f"Arquivo não localizado ou inacessível: {filepath}")
        return None

    file_size = filepath.stat().st_size
    if file_size < 24:
        logger.warning(f"Arquivo menor que cabeçalho global Libpcap ({file_size} bytes): {filepath.name}")
        return None

    try:
        with open(filepath, "rb") as f:
            header_bytes = f.read(24)
            if len(header_bytes) < 24:
                return None

            magic = struct.unpack("<I", header_bytes[:4])[0]
            if magic == 0xa1b2c3d4:
                endian, ts_divisor = "<", 1_000_000.0
            elif magic == 0xa1b23c4d:
                endian, ts_divisor = "<", 1_000_000_000.0
            elif magic == 0xd4c3b2a1:
                endian, ts_divisor = ">", 1_000_000.0
            elif magic == 0x4d3cb2a1:
                endian, ts_divisor = ">", 1_000_000_000.0
            else:
                logger.warning(f"Magic number não reconhecido em {filepath.name}: {hex(magic)}")
                return None

            packet_count = 0
            first_ts: Optional[float] = None
            last_ts: Optional[float] = None
            min_ts: Optional[float] = None
            max_ts: Optional[float] = None
            total_wire_bytes = 0
            total_captured_bytes = 0

            while True:
                pkt_hdr = f.read(16)
                if not pkt_hdr:
                    break
                if len(pkt_hdr) < 16:
                    logger.warning(f"Cabeçalho de pacote truncado em {filepath.name} após {packet_count} pacotes.")
                    break

                ts_sec, ts_sub, incl_len, orig_len = struct.unpack(f"{endian}IIII", pkt_hdr)

                # Validação de integridade do tamanho do pacote
                if incl_len > 65535 * 4:
                    logger.warning(f"Tamanho anormal de pacote ({incl_len} bytes) em {filepath.name}.")
                    break

                ts = ts_sec + (ts_sub / ts_divisor)

                if first_ts is None:
                    first_ts = ts
                    min_ts = ts
                    max_ts = ts
                else:
                    if ts < min_ts:
                        min_ts = ts
                    if ts > max_ts:
                        max_ts = ts
                last_ts = ts

                wire_len = orig_len if orig_len > 0 else incl_len
                total_wire_bytes += wire_len
                total_captured_bytes += incl_len
                packet_count += 1

                # Salto direto sem alocação de memória para o payload (RNF02)
                f.seek(incl_len, os.SEEK_CUR)

            if packet_count == 0:
                duration = 0.0
                first_ts_val = 0.0
                last_ts_val = 0.0
            else:
                first_ts_val = round(min_ts if min_ts is not None else first_ts, 6)
                last_ts_val = round(max_ts if max_ts is not None else last_ts, 6)
                duration = max(0.0, round(last_ts_val - first_ts_val, 6))

            avg_packet_size = round(total_wire_bytes / packet_count, 2) if packet_count > 0 else 0.0
            pps = round(packet_count / duration, 2) if duration > 0 else 0.0
            bps = round(total_wire_bytes / duration, 2) if duration > 0 else 0.0

            label_class = infer_class_from_name(filepath)

            return {
                "filename": filepath.name,
                "file_path": str(filepath.resolve()),
                "label_class": label_class,
                "file_size_bytes": file_size,
                "packet_count": packet_count,
                "first_timestamp": first_ts_val,
                "last_timestamp": last_ts_val,
                "duration_seconds": duration,
                "total_wire_bytes": total_wire_bytes,
                "total_captured_bytes": total_captured_bytes,
                "avg_packet_size_bytes": avg_packet_size,
                "packets_per_second": pps,
                "bytes_per_second": bps,
            }
    except Exception as e:
        logger.error(f"Erro ao processar arquivo {filepath.name}: {e}")
        return None


def calculate_class_statistics(file_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcula métricas estatísticas agregadas (média, variância, desvio padrão, min, max)
    para um grupo de arquivos de mesma classe.
    """
    n = len(file_records)
    if n == 0:
        return {
            "file_count": 0,
            "total_packets": 0,
            "total_file_bytes": 0,
            "total_wire_bytes": 0,
            "avg_duration_seconds": 0.0,
            "std_duration_seconds": 0.0,
            "min_duration_seconds": 0.0,
            "max_duration_seconds": 0.0,
            "avg_packets_per_file": 0.0,
            "std_packets_per_file": 0.0,
            "avg_volume_mb_per_file": 0.0,
            "avg_packet_size_bytes": 0.0,
            "avg_packets_per_second": 0.0,
        }

    durations = [r["duration_seconds"] for r in file_records]
    packet_counts = [r["packet_count"] for r in file_records]
    file_bytes = [r["file_size_bytes"] for r in file_records]
    wire_bytes = [r["total_wire_bytes"] for r in file_records]

    total_packets = sum(packet_counts)
    total_file_bytes = sum(file_bytes)
    total_wire_bytes = sum(wire_bytes)

    avg_dur = sum(durations) / n
    var_dur = sum((d - avg_dur) ** 2 for d in durations) / (n - 1) if n > 1 else 0.0
    std_dur = math.sqrt(var_dur)

    avg_pkts = total_packets / n
    var_pkts = sum((p - avg_pkts) ** 2 for p in packet_counts) / (n - 1) if n > 1 else 0.0
    std_pkts = math.sqrt(var_pkts)

    avg_vol_mb = (total_file_bytes / n) / (1024 * 1024)
    avg_pkt_sz = total_wire_bytes / total_packets if total_packets > 0 else 0.0

    total_dur_sum = sum(durations)
    avg_pps = total_packets / total_dur_sum if total_dur_sum > 0 else 0.0

    return {
        "file_count": n,
        "total_packets": total_packets,
        "total_file_bytes": total_file_bytes,
        "total_wire_bytes": total_wire_bytes,
        "avg_duration_seconds": round(avg_dur, 2),
        "std_duration_seconds": round(std_dur, 2),
        "min_duration_seconds": round(min(durations), 2),
        "max_duration_seconds": round(max(durations), 2),
        "avg_packets_per_file": round(avg_pkts, 1),
        "std_packets_per_file": round(std_pkts, 1),
        "avg_volume_mb_per_file": round(avg_vol_mb, 2),
        "avg_packet_size_bytes": round(avg_pkt_sz, 2),
        "avg_packets_per_second": round(avg_pps, 2),
    }


def extract_raw_metadata_pipeline(
    input_dir: Union[str, Path],
    output_json: Optional[Union[str, Path]] = None,
    output_csv: Optional[Union[str, Path]] = None,
    recursive: bool = True,
    min_packets: int = 1
) -> Dict[str, Any]:
    """
    Pipeline principal de extração de metadados brutos:
    1. Varre input_dir em busca de arquivos .pcap
    2. Extrai metadados individuais via streaming
    3. Agrupa e calcula estatísticas por classe (betting, benign)
    4. Gera relatórios JSON e CSV estruturados
    """
    in_path = Path(input_dir)
    logger.info(f"Iniciando extração de metadados brutos em {in_path}...")

    if not in_path.exists():
        logger.warning(f"Diretório de entrada não existe: {in_path}. Criando diretório vazio...")
        in_path.mkdir(parents=True, exist_ok=True)

    if recursive:
        pcap_files = sorted(list(in_path.rglob("*.pcap")))
    else:
        pcap_files = sorted(list(in_path.glob("*.pcap")))

    logger.info(f"Total de arquivos .pcap localizados: {len(pcap_files)}")

    file_records: List[Dict[str, Any]] = []
    classes_map: Dict[str, List[Dict[str, Any]]] = {}

    for pf in pcap_files:
        meta = extract_pcap_file_metadata(pf)
        if meta is not None:
            if meta["packet_count"] >= min_packets or min_packets <= 0:
                file_records.append(meta)
                cls_name = meta["label_class"]
                classes_map.setdefault(cls_name, []).append(meta)
                logger.info(
                    f"[OK] {meta['filename']} -> {meta['packet_count']:,} pacotes | "
                    f"{meta['file_size_bytes']:,} bytes | Duração: {meta['duration_seconds']}s "
                    f"[{meta['label_class']}]"
                )
            else:
                logger.warning(
                    f"[SKIP] {pf.name} ignorado por possuir menos que {min_packets} pacotes "
                    f"({meta['packet_count']} pacotes)."
                )

    # Cálculo dos resumos por classe
    summary_by_class: Dict[str, Any] = {}
    for cls_name, records in classes_map.items():
        summary_by_class[cls_name] = calculate_class_statistics(records)

    total_valid_files = len(file_records)
    total_packets = sum(r["packet_count"] for r in file_records)
    total_bytes = sum(r["file_size_bytes"] for r in file_records)
    total_mb = round(total_bytes / (1024 * 1024), 2)

    overall_summary = {
        "total_files": total_valid_files,
        "total_packets": total_packets,
        "total_volume_mb": total_mb,
        "classes_detected": sorted(list(classes_map.keys())),
    }

    report_payload = {
        "input_dir": str(in_path.resolve()),
        "total_files_analyzed": total_valid_files,
        "summary_by_class": summary_by_class,
        "overall_summary": overall_summary,
        "files": file_records,
    }

    # Exibição do resumo no terminal
    print("\n================ SÍNTESE METADADOS BRUTOS ================")
    for cls_name in ["betting", "benign"]:
        if cls_name in summary_by_class:
            stats = summary_by_class[cls_name]
            print(f"Classe '{cls_name}':")
            print(f"  - Arquivos válidos: {stats['file_count']}")
            print(f"  - Duração média: {stats['avg_duration_seconds']}s (DP: {stats['std_duration_seconds']}s)")
            print(f"  - Volume médio: {stats['avg_volume_mb_per_file']} MB por sessão")
            print(f"  - Média de pacotes: {stats['avg_packets_per_file']:,}")
            print(f"  - Taxa média de pacotes/s: {stats['avg_packets_per_second']}")

    for other_cls in summary_by_class:
        if other_cls not in ["betting", "benign"]:
            stats = summary_by_class[other_cls]
            print(f"Classe '{other_cls}':")
            print(f"  - Arquivos válidos: {stats['file_count']}")
            print(f"  - Média de pacotes: {stats['avg_packets_per_file']:,}")
    print("==========================================================\n")

    # Exportação JSON
    if output_json:
        json_path = Path(output_json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=2, ensure_ascii=False)
        logger.info(f"Relatório JSON exportado com sucesso: {json_path}")

    # Exportação CSV
    if output_csv:
        csv_path = Path(output_csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "filename",
            "file_path",
            "label_class",
            "file_size_bytes",
            "packet_count",
            "first_timestamp",
            "last_timestamp",
            "duration_seconds",
            "total_wire_bytes",
            "total_captured_bytes",
            "avg_packet_size_bytes",
            "packets_per_second",
            "bytes_per_second",
        ]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in file_records:
                writer.writerow(r)
        logger.info(f"Relatório CSV exportado com sucesso: {csv_path}")

    return report_payload


def main():
    parser = argparse.ArgumentParser(
        description="Extração de Metadados Brutos de Capturas PCAP (Volume e Duração por Captura)"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default=os.environ.get("RAW_DATA_DIR", "data/raw"),
        help="Diretório contendo os arquivos .pcap brutos (padrão: data/raw)"
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default="data/reports/raw_metadata_report.json",
        help="Caminho do arquivo de relatório JSON gerado"
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="data/reports/raw_metadata_report.csv",
        help="Caminho do arquivo de relatório CSV gerado"
    )
    parser.add_argument(
        "--min-packets",
        type=int,
        default=1,
        help="Filtro mínimo de pacotes por arquivo PCAP (padrão: 1)"
    )
    parser.add_argument(
        "--non-recursive",
        action="store_true",
        help="Desativa a busca recursiva em subpastas"
    )

    args = parser.parse_args()

    extract_raw_metadata_pipeline(
        input_dir=args.input_dir,
        output_json=args.output_json,
        output_csv=args.output_csv,
        recursive=not args.non_recursive,
        min_packets=args.min_packets
    )


if __name__ == "__main__":
    main()
