# -*- coding: utf-8 -*-
"""
Módulo de Extração de Fluxos Bidirecionais (Conversão PCAP para CSV).
Referência: Issue #17 e Seção 3.2.2 do TCC.

Converte arquivos PCAP em fluxos bidirecionais delimitados pela 5-tupla
(src_ip, src_port, dst_ip, dst_port, protocol) com timeout de inatividade
configurável, extraindo 40+ atributos estatísticos e temporais sem DPI (RNF02).
"""

import os
import sys
import csv
import math
import struct
import socket
import logging
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Generator, Any, Union

logger = logging.getLogger("flow_extractor")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class OnlineStats:
    """
    Acumulador estatístico online baseado no algoritmo de Welford e momentos
    de ordem superior (m2, m3) para cálculo de média, variância, desvio padrão,
    mínimo, máximo e assimetria (skewness) em complexidade O(1) de memória (RNF02).
    """

    def __init__(self) -> None:
        self.count: int = 0
        self.total: float = 0.0
        self.mean: float = 0.0
        self.m2: float = 0.0
        self.m3: float = 0.0
        self.min_val: float = float("inf")
        self.max_val: float = float("-inf")

    def update(self, x: float) -> None:
        """Atualiza os momentos estatísticos com um novo valor numérico."""
        self.count += 1
        self.total += x
        if x < self.min_val:
            self.min_val = x
        if x > self.max_val:
            self.max_val = x

        delta = x - self.mean
        delta_n = delta / self.count
        term1 = delta * delta_n * (self.count - 1)

        self.mean += delta_n
        self.m3 += term1 * delta_n * (self.count - 2) - 3.0 * delta_n * self.m2
        self.m2 += term1

    @property
    def variance(self) -> float:
        """Variância amostral com correção de Bessel (N-1)."""
        if self.count < 2:
            return 0.0
        return max(0.0, self.m2 / (self.count - 1))

    @property
    def std(self) -> float:
        """Desvio padrão amostral."""
        return math.sqrt(self.variance)

    @property
    def skewness(self) -> float:
        """
        Assimetria populacional (Fisher-Pearson standardized third moment).
        Retorna 0.0 se count < 3 ou se variância for nula.
        """
        if self.count < 3 or self.m2 <= 0.0:
            return 0.0
        var_pop = self.m2 / self.count
        if var_pop <= 0.0:
            return 0.0
        return (self.m3 / self.count) / (var_pop ** 1.5)


@dataclass(slots=True)
class PacketRecord:
    """Representação leve de cabeçalho de pacote de rede para agregação de fluxo."""
    timestamp: float
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    protocol: int
    length: int


class BidirectionalFlow:
    """
    Representação de um fluxo de rede bidirecional entre dois terminais IP.
    A direção 'forward' (direta) é fixada pelo primeiro pacote observado.
    """

    def __init__(self, first_pkt: PacketRecord) -> None:
        self.fwd_src_ip: str = first_pkt.src_ip
        self.fwd_src_port: int = first_pkt.src_port
        self.fwd_dst_ip: str = first_pkt.dst_ip
        self.fwd_dst_port: int = first_pkt.dst_port
        self.protocol: int = first_pkt.protocol

        self.start_time: float = first_pkt.timestamp
        self.end_time: float = first_pkt.timestamp
        self.last_seen: float = first_pkt.timestamp
        self.last_pkt_time: float = first_pkt.timestamp

        self.fwd_pkts: int = 1
        self.bwd_pkts: int = 0
        self.fwd_bytes: int = first_pkt.length
        self.bwd_bytes: int = 0

        self.last_fwd_time: Optional[float] = first_pkt.timestamp
        self.last_bwd_time: Optional[float] = None

        self.flow_iat_stats: OnlineStats = OnlineStats()
        self.fwd_iat_stats: OnlineStats = OnlineStats()
        self.bwd_iat_stats: OnlineStats = OnlineStats()

        self.pkt_len_stats: OnlineStats = OnlineStats()
        self.fwd_pkt_len_stats: OnlineStats = OnlineStats()
        self.bwd_pkt_len_stats: OnlineStats = OnlineStats()

        self.pkt_len_stats.update(first_pkt.length)
        self.fwd_pkt_len_stats.update(first_pkt.length)

    def add_packet(self, pkt: PacketRecord) -> None:
        """Adiciona um pacote subsequente ao fluxo bidirecional e recalcula métricas."""
        is_fwd = (pkt.src_ip == self.fwd_src_ip and pkt.src_port == self.fwd_src_port)

        iat = max(0.0, pkt.timestamp - self.last_pkt_time)
        self.flow_iat_stats.update(iat)
        self.pkt_len_stats.update(pkt.length)

        self.last_pkt_time = pkt.timestamp
        self.last_seen = pkt.timestamp
        if pkt.timestamp > self.end_time:
            self.end_time = pkt.timestamp
        if pkt.timestamp < self.start_time:
            self.start_time = pkt.timestamp

        if is_fwd:
            self.fwd_pkts += 1
            self.fwd_bytes += pkt.length
            self.fwd_pkt_len_stats.update(pkt.length)
            if self.last_fwd_time is not None:
                fwd_iat = max(0.0, pkt.timestamp - self.last_fwd_time)
                self.fwd_iat_stats.update(fwd_iat)
            self.last_fwd_time = pkt.timestamp
        else:
            self.bwd_pkts += 1
            self.bwd_bytes += pkt.length
            self.bwd_pkt_len_stats.update(pkt.length)
            if self.last_bwd_time is not None:
                bwd_iat = max(0.0, pkt.timestamp - self.last_bwd_time)
                self.bwd_iat_stats.update(bwd_iat)
            self.last_bwd_time = pkt.timestamp

    def to_dict(self, label: str = "unknown") -> Dict[str, Any]:
        """Converte as métricas do fluxo para um dicionário tabular (linha de CSV)."""
        duration = max(0.0, self.end_time - self.start_time)
        flow_pkts_tot = self.fwd_pkts + self.bwd_pkts
        flow_bytes_tot = self.fwd_bytes + self.bwd_bytes

        pkts_per_sec = (flow_pkts_tot / duration) if duration > 0.0 else 0.0
        bytes_per_sec = (flow_bytes_tot / duration) if duration > 0.0 else 0.0

        flow_id = f"{self.fwd_src_ip}:{self.fwd_src_port}-{self.fwd_dst_ip}:{self.fwd_dst_port}-{self.protocol}"

        return {
            "flow_id": flow_id,
            "src_ip": self.fwd_src_ip,
            "src_port": self.fwd_src_port,
            "dst_ip": self.fwd_dst_ip,
            "dst_port": self.fwd_dst_port,
            "protocol": self.protocol,
            "timestamp": round(self.start_time, 6),
            "flow_duration": round(duration, 6),
            "flow_pkts_tot": flow_pkts_tot,
            "fwd_pkts_tot": self.fwd_pkts,
            "bwd_pkts_tot": self.bwd_pkts,
            "flow_bytes_tot": flow_bytes_tot,
            "fwd_bytes_tot": self.fwd_bytes,
            "bwd_bytes_tot": self.bwd_bytes,
            "flow_pkts_per_sec": round(pkts_per_sec, 6),
            "flow_bytes_per_sec": round(bytes_per_sec, 6),
            # IAT Estatísticas Globais
            "flow_iat_mean": round(self.flow_iat_stats.mean, 6),
            "flow_iat_std": round(self.flow_iat_stats.std, 6),
            "flow_iat_min": round(self.flow_iat_stats.min_val, 6) if self.flow_iat_stats.count > 0 else 0.0,
            "flow_iat_max": round(self.flow_iat_stats.max_val, 6) if self.flow_iat_stats.count > 0 else 0.0,
            # IAT Forward
            "fwd_iat_mean": round(self.fwd_iat_stats.mean, 6),
            "fwd_iat_std": round(self.fwd_iat_stats.std, 6),
            "fwd_iat_min": round(self.fwd_iat_stats.min_val, 6) if self.fwd_iat_stats.count > 0 else 0.0,
            "fwd_iat_max": round(self.fwd_iat_stats.max_val, 6) if self.fwd_iat_stats.count > 0 else 0.0,
            # IAT Backward
            "bwd_iat_mean": round(self.bwd_iat_stats.mean, 6),
            "bwd_iat_std": round(self.bwd_iat_stats.std, 6),
            "bwd_iat_min": round(self.bwd_iat_stats.min_val, 6) if self.bwd_iat_stats.count > 0 else 0.0,
            "bwd_iat_max": round(self.bwd_iat_stats.max_val, 6) if self.bwd_iat_stats.count > 0 else 0.0,
            # Comprimento de Pacotes Global
            "pkt_len_mean": round(self.pkt_len_stats.mean, 2),
            "pkt_len_std": round(self.pkt_len_stats.std, 2),
            "pkt_len_min": int(self.pkt_len_stats.min_val) if self.pkt_len_stats.count > 0 else 0,
            "pkt_len_max": int(self.pkt_len_stats.max_val) if self.pkt_len_stats.count > 0 else 0,
            "pkt_len_skew": round(self.pkt_len_stats.skewness, 4),
            # Comprimento de Pacotes Forward
            "fwd_pkt_len_mean": round(self.fwd_pkt_len_stats.mean, 2),
            "fwd_pkt_len_std": round(self.fwd_pkt_len_stats.std, 2),
            "fwd_pkt_len_min": int(self.fwd_pkt_len_stats.min_val) if self.fwd_pkt_len_stats.count > 0 else 0,
            "fwd_pkt_len_max": int(self.fwd_pkt_len_stats.max_val) if self.fwd_pkt_len_stats.count > 0 else 0,
            # Comprimento de Pacotes Backward
            "bwd_pkt_len_mean": round(self.bwd_pkt_len_stats.mean, 2),
            "bwd_pkt_len_std": round(self.bwd_pkt_len_stats.std, 2),
            "bwd_pkt_len_min": int(self.bwd_pkt_len_stats.min_val) if self.bwd_pkt_len_stats.count > 0 else 0,
            "bwd_pkt_len_max": int(self.bwd_pkt_len_stats.max_val) if self.bwd_pkt_len_stats.count > 0 else 0,
            # Rótulo de Classe
            "label": label
        }


CSV_FIELDNAMES = [
    "flow_id", "src_ip", "src_port", "dst_ip", "dst_port", "protocol",
    "timestamp", "flow_duration", "flow_pkts_tot", "fwd_pkts_tot", "bwd_pkts_tot",
    "flow_bytes_tot", "fwd_bytes_tot", "bwd_bytes_tot", "flow_pkts_per_sec", "flow_bytes_per_sec",
    "flow_iat_mean", "flow_iat_std", "flow_iat_min", "flow_iat_max",
    "fwd_iat_mean", "fwd_iat_std", "fwd_iat_min", "fwd_iat_max",
    "bwd_iat_mean", "bwd_iat_std", "bwd_iat_min", "bwd_iat_max",
    "pkt_len_mean", "pkt_len_std", "pkt_len_min", "pkt_len_max", "pkt_len_skew",
    "fwd_pkt_len_mean", "fwd_pkt_len_std", "fwd_pkt_len_min", "fwd_pkt_len_max",
    "bwd_pkt_len_mean", "bwd_pkt_len_std", "bwd_pkt_len_min", "bwd_pkt_len_max",
    "label"
]


def parse_raw_packet(
    raw_bytes: bytes,
    linktype: int = 1,
    ts: float = 0.0,
    wire_len: Optional[int] = None
) -> Optional[PacketRecord]:
    """
    Decodifica de forma ultra-rápida os cabeçalhos de enlace (L2), rede (L3: IPv4/IPv6)
    e transporte (L4: TCP/UDP) sem carregar o conteúdo da carga útil na memória (sem DPI).
    """
    if wire_len is None:
        wire_len = len(raw_bytes)

    offset = 0
    eth_proto = 0

    if linktype == 1:  # LINKTYPE_ETHERNET
        if len(raw_bytes) < 14:
            return None
        eth_proto = struct.unpack("!H", raw_bytes[12:14])[0]
        offset = 14
        if eth_proto == 0x8100:  # 802.1Q VLAN
            if len(raw_bytes) < 18:
                return None
            eth_proto = struct.unpack("!H", raw_bytes[16:18])[0]
            offset = 18
    elif linktype == 113:  # LINKTYPE_LINUX_SLL (cooked)
        if len(raw_bytes) < 16:
            return None
        eth_proto = struct.unpack("!H", raw_bytes[14:16])[0]
        offset = 16
    elif linktype in (101, 12):  # LINKTYPE_RAW / LINKTYPE_IPV4 / LINKTYPE_IPV6
        if len(raw_bytes) < 1:
            return None
        ip_ver = raw_bytes[0] >> 4
        eth_proto = 0x0800 if ip_ver == 4 else (0x86dd if ip_ver == 6 else 0)
        offset = 0
    else:
        # Fallback tentativa de parsing se o primeiro byte parecer IPv4
        if len(raw_bytes) >= 20 and (raw_bytes[0] >> 4) == 4:
            eth_proto = 0x0800
            offset = 0
        elif len(raw_bytes) >= 40 and (raw_bytes[0] >> 4) == 6:
            eth_proto = 0x86dd
            offset = 0
        else:
            return None

    src_ip: str
    dst_ip: str
    protocol: int
    l4_offset: int

    if eth_proto == 0x0800:  # IPv4
        if len(raw_bytes) < offset + 20:
            return None
        ver_ihl = raw_bytes[offset]
        ihl = (ver_ihl & 0x0f) * 4
        if ihl < 20 or len(raw_bytes) < offset + ihl:
            return None

        protocol = raw_bytes[offset + 9]
        src_ip = socket.inet_ntoa(raw_bytes[offset + 12: offset + 16])
        dst_ip = socket.inet_ntoa(raw_bytes[offset + 16: offset + 20])
        l4_offset = offset + ihl

    elif eth_proto == 0x86dd:  # IPv6
        if len(raw_bytes) < offset + 40:
            return None
        protocol = raw_bytes[offset + 6]
        src_ip = socket.inet_ntop(socket.AF_INET6, raw_bytes[offset + 8: offset + 24])
        dst_ip = socket.inet_ntop(socket.AF_INET6, raw_bytes[offset + 24: offset + 40])
        l4_offset = offset + 40
    else:
        return None

    sport = 0
    dport = 0
    if protocol in (6, 17):  # TCP ou UDP
        if len(raw_bytes) >= l4_offset + 4:
            sport, dport = struct.unpack("!HH", raw_bytes[l4_offset: l4_offset + 4])
    else:
        # Outros protocolos suportados (ex: ICMP=1, ESP=50), portas fixas em 0
        sport = 0
        dport = 0

    return PacketRecord(
        timestamp=ts,
        src_ip=src_ip,
        src_port=sport,
        dst_ip=dst_ip,
        dst_port=dport,
        protocol=protocol,
        length=wire_len
    )


class FlowExtractor:
    """
    Agregador de pacotes em fluxos bidirecionais baseado na 5-tupla canônica
    e controle de timeout de inatividade.
    """

    def __init__(self, flow_timeout: float = 60.0, min_packets: int = 1) -> None:
        self.flow_timeout: float = max(1.0, float(flow_timeout))
        self.min_packets: int = max(1, int(min_packets))
        self.active_flows: Dict[Tuple[Tuple[str, int], Tuple[str, int], int], BidirectionalFlow] = {}

    def _get_canonical_key(self, pkt: PacketRecord) -> Tuple[Tuple[str, int], Tuple[str, int], int]:
        """Obtém chave imutável normalizada ordenando endpoints para chave bidirecional."""
        ep1 = (pkt.src_ip, pkt.src_port)
        ep2 = (pkt.dst_ip, pkt.dst_port)
        if ep1 <= ep2:
            return (ep1, ep2, pkt.protocol)
        return (ep2, ep1, pkt.protocol)

    def add_packet(self, pkt: PacketRecord) -> List[BidirectionalFlow]:
        """
        Insere um pacote. Se o fluxo anterior para esta 5-tupla expirou por inatividade,
        finaliza o fluxo antigo e inicia um novo. Retorna lista de fluxos expirados.
        """
        key = self._get_canonical_key(pkt)
        emitted: List[BidirectionalFlow] = []

        if key in self.active_flows:
            flow = self.active_flows[key]
            if (pkt.timestamp - flow.last_seen) > self.flow_timeout:
                if (flow.fwd_pkts + flow.bwd_pkts) >= self.min_packets:
                    emitted.append(flow)
                self.active_flows[key] = BidirectionalFlow(pkt)
            else:
                flow.add_packet(pkt)
        else:
            self.active_flows[key] = BidirectionalFlow(pkt)

        return emitted

    def flush_expired(self, current_time: float) -> List[BidirectionalFlow]:
        """Expira fluxos cuja última atividade ocorreu há mais de flow_timeout segundos."""
        emitted: List[BidirectionalFlow] = []
        expired_keys = [
            k for k, flow in self.active_flows.items()
            if (current_time - flow.last_seen) > self.flow_timeout
        ]
        for k in expired_keys:
            flow = self.active_flows.pop(k)
            if (flow.fwd_pkts + flow.bwd_pkts) >= self.min_packets:
                emitted.append(flow)
        return emitted

    def flush_all(self) -> List[BidirectionalFlow]:
        """Descarrega todos os fluxos ativos restantes ao final do processamento."""
        emitted: List[BidirectionalFlow] = []
        for flow in self.active_flows.values():
            if (flow.fwd_pkts + flow.bwd_pkts) >= self.min_packets:
                emitted.append(flow)
        self.active_flows.clear()
        return emitted


def infer_class_from_name(filepath: Union[str, Path]) -> str:
    """
    Infere a classe binária ('betting' ou 'benign') a partir do nome do arquivo
    ou da estrutura de diretórios (/data/raw/betting vs /data/raw/benign).
    """
    path_obj = Path(filepath)
    name_lower = path_obj.name.lower()
    parent_lower = path_obj.parent.name.lower()

    if parent_lower in ("betting", "apostas", "bets"):
        return "betting"
    if parent_lower in ("benign", "benigno", "controle", "control"):
        return "benign"

    betting_keywords = [
        "betting", "apostas", "aposta", "bet365", "betano", "blaze", "kto",
        "sportingbet", "betfair", "cassino", "casino", "poker", "roleta", "slots", "bet"
    ]
    for kw in betting_keywords:
        if kw in name_lower:
            return "betting"

    benign_keywords = [
        "benign", "benigno", "controle", "control", "youtube", "g1", "noticias",
        "globo", "uol", "wikipedia", "twitch", "stream", "github", "google"
    ]
    for kw in benign_keywords:
        if kw in name_lower:
            return "benign"

    return "unknown"


def process_pcap_file(
    filepath: Union[str, Path],
    flow_timeout: float = 60.0,
    min_packets: int = 1,
    label: Optional[str] = None
) -> Generator[Dict[str, Any], None, None]:
    """
    Lê um arquivo PCAP via streaming de pacotes e gera dicionários com
    atributos de fluxos bidirecionais delimitados pela 5-tupla.
    """
    path = Path(filepath)
    if not path.exists() or not path.is_file():
        logger.warning(f"Arquivo não localizado ou inacessível: {path}")
        return

    file_size = path.stat().st_size
    if file_size < 24:
        logger.warning(f"PCAP menor que cabeçalho Libpcap ({file_size} bytes): {path.name}")
        return

    effective_label = label if label is not None else infer_class_from_name(path)
    extractor = FlowExtractor(flow_timeout=flow_timeout, min_packets=min_packets)

    try:
        with open(path, "rb") as f:
            hdr_bytes = f.read(24)
            if len(hdr_bytes) < 24:
                return

            magic = struct.unpack("<I", hdr_bytes[:4])[0]
            if magic == 0xa1b2c3d4:
                endian, ts_div = "<", 1_000_000.0
            elif magic == 0xa1b23c4d:
                endian, ts_div = "<", 1_000_000_000.0
            elif magic == 0xd4c3b2a1:
                endian, ts_div = ">", 1_000_000.0
            elif magic == 0x4d3cb2a1:
                endian, ts_div = ">", 1_000_000_000.0
            else:
                logger.warning(f"Magic number desconhecido ({hex(magic)}) em {path.name}")
                return

            linktype = struct.unpack(f"{endian}I", hdr_bytes[20:24])[0]

            while True:
                pkt_hdr = f.read(16)
                if not pkt_hdr:
                    break
                if len(pkt_hdr) < 16:
                    logger.warning(f"Cabeçalho truncado em {path.name}.")
                    break

                ts_sec, ts_sub, incl_len, orig_len = struct.unpack(f"{endian}IIII", pkt_hdr)
                if incl_len > 65535 * 4:
                    logger.warning(f"Comprimento anormal ({incl_len} bytes) em {path.name}.")
                    break

                raw_bytes = f.read(incl_len)
                if len(raw_bytes) < incl_len:
                    logger.warning(f"Pacote truncado em {path.name}.")
                    break

                ts = ts_sec + (ts_sub / ts_div)
                wire_len = orig_len if orig_len > 0 else incl_len

                pkt = parse_raw_packet(raw_bytes, linktype=linktype, ts=ts, wire_len=wire_len)
                if pkt is not None:
                    expired = extractor.add_packet(pkt)
                    for flow in expired:
                        yield flow.to_dict(label=effective_label)

            # Esvazia os fluxos ativos restantes ao fim do arquivo
            for flow in extractor.flush_all():
                yield flow.to_dict(label=effective_label)

    except Exception as exc:
        logger.error(f"Erro ao processar PCAP {path.name}: {exc}")


def process_directory(
    input_dir: Union[str, Path],
    output_csv: Union[str, Path],
    flow_timeout: float = 60.0,
    min_packets: int = 1,
    batch_size: int = 1000,
    label: Optional[str] = None
) -> Tuple[int, int]:
    """
    Processa todos os arquivos .pcap em um diretório de entrada e exporta
    os fluxos bidirecionais consolidados diretamente para um arquivo CSV estruturado.
    Retorna (total_pcaps_processados, total_fluxos_extraidos).
    """
    in_path = Path(input_dir)
    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    pcap_files = sorted(list(in_path.glob("*.pcap")) + list(in_path.glob("**/*.pcap")))
    # Remover duplicatas mantendo ordem
    unique_pcaps = list(dict.fromkeys(pcap_files))

    if not unique_pcaps:
        logger.warning(f"Nenhum arquivo .pcap localizado em {in_path}")
        # Cria CSV vazio com cabeçalhos formais se não existir
        if not out_path.exists():
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
                writer.writeheader()
        return 0, 0

    total_pcaps = len(unique_pcaps)
    logger.info(f"Iniciando agrupamento de fluxos bidirecionais (Timeout: {flow_timeout}s)...")
    logger.info(f"Processando {total_pcaps} arquivos PCAP em {in_path}...")

    total_flows = 0
    buffer: List[Dict[str, Any]] = []

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()

        for idx, pcap_path in enumerate(unique_pcaps, start=1):
            flow_count_file = 0
            for flow_dict in process_pcap_file(pcap_path, flow_timeout=flow_timeout, min_packets=min_packets, label=label):
                buffer.append(flow_dict)
                flow_count_file += 1
                total_flows += 1

                if len(buffer) >= batch_size:
                    writer.writerows(buffer)
                    buffer.clear()

            if idx % max(1, total_pcaps // 4) == 0 or idx == total_pcaps:
                logger.info(f"[PROGRESS] {idx}/{total_pcaps} PCAPs analisados ({total_flows:,} fluxos gerados)...")

        if buffer:
            writer.writerows(buffer)
            buffer.clear()

    file_size_mb = out_path.stat().st_size / (1024 * 1024) if out_path.exists() else 0.0
    logger.info(f"[SUCCESS] Conversão concluída!")
    logger.info(f"  - Total de PCAPs processados: {total_pcaps}")
    logger.info(f"  - Total de fluxos extraídos: {total_flows:,}")
    logger.info(f"  - Atributos por fluxo: {len(CSV_FIELDNAMES)} colunas estatísticas")
    logger.info(f"  - Arquivo exportado: {out_path} ({file_size_mb:.2f} MB)")

    return total_pcaps, total_flows


def extract_flows_pipeline(
    input_source: Union[str, Path],
    output_csv: Union[str, Path],
    flow_timeout: float = 60.0,
    min_packets: int = 1,
    batch_size: int = 1000,
    label: Optional[str] = None
) -> Tuple[int, int]:
    """Ponto de entrada unificado para processamento de arquivo individual ou diretório."""
    src_path = Path(input_source)
    if src_path.is_file():
        out_path = Path(output_csv)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        total_flows = 0
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            for flow_dict in process_pcap_file(src_path, flow_timeout=flow_timeout, min_packets=min_packets, label=label):
                writer.writerow(flow_dict)
                total_flows += 1
        return 1, total_flows
    else:
        return process_directory(
            input_dir=src_path,
            output_csv=output_csv,
            flow_timeout=flow_timeout,
            min_packets=min_packets,
            batch_size=batch_size,
            label=label
        )


def main() -> int:
    """Interface de Linha de Comando (CLI) para extração de fluxos bidirecionais."""
    parser = argparse.ArgumentParser(
        description="Extrator de Fluxos Bidirecionais PCAP para CSV - Firewall Inteligente (RF03, RNF02)"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default="data/raw",
        help="Diretório contendo os arquivos PCAP brutos (padrão: data/raw)"
    )
    parser.add_argument(
        "--pcap-file",
        type=str,
        default=None,
        help="Arquivo PCAP individual para processamento isolado"
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="data/processed/flows_extracted.csv",
        help="Caminho do arquivo CSV de destino (padrão: data/processed/flows_extracted.csv)"
    )
    parser.add_argument(
        "--flow-timeout",
        type=float,
        default=60.0,
        help="Timeout de inatividade do fluxo em segundos (padrão: 60.0)"
    )
    parser.add_argument(
        "--min-packets",
        type=int,
        default=1,
        help="Volume mínimo de pacotes por fluxo para não descarte (padrão: 1)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Tamanho do lote de escrita em buffer para CSV (padrão: 1000)"
    )
    parser.add_argument(
        "--label",
        type=str,
        default=None,
        help="Força rótulo de classe para todos os fluxos (ex: betting ou benign)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Nível de detalhamento do log (padrão: INFO)"
    )

    args = parser.parse_args()
    logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))

    target_source = args.pcap_file if args.pcap_file else args.input_dir
    try:
        pcaps_proc, flows_proc = extract_flows_pipeline(
            input_source=target_source,
            output_csv=args.output_csv,
            flow_timeout=args.flow_timeout,
            min_packets=args.min_packets,
            batch_size=args.batch_size,
            label=args.label
        )
        return 0 if flows_proc >= 0 else 1
    except Exception as err:
        logger.error(f"Falha na execução do pipeline de extração de fluxos: {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

