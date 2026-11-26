# -*- coding: utf-8 -*-
"""
Suíte de Testes Unitários para a Issue #17: Extração de fluxos bidirecionais (PCAP para CSV).
Cobre agregador 5-tupla, Welford online, decodificação L2/L3/L4 sem DPI e exportação CSV.
"""

import os
import sys
import csv
import struct
import socket
import pytest
from pathlib import Path

from src.data_processing.flow_extractor import (
    OnlineStats,
    PacketRecord,
    BidirectionalFlow,
    FlowExtractor,
    parse_raw_packet,
    infer_class_from_name,
    process_pcap_file,
    process_directory,
    extract_flows_pipeline,
    main,
    CSV_FIELDNAMES
)


def create_mock_pcap_with_raw_packets(
    filepath: Path,
    packets: list,  # list of tuples: (ts_sec, ts_sub, raw_bytes)
    magic: int = 0xa1b2c3d4,  # Little-Endian microsecond
    endian: str = "<",
    linktype: int = 1  # LINKTYPE_ETHERNET
) -> Path:
    """Cria um arquivo PCAP sintético com pacotes binários brutos para testes."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        hdr = struct.pack(
            f"{endian}IHHiIII",
            magic,
            2, 4,
            0,
            0,
            65535,
            linktype
        )
        f.write(hdr)
        for ts_sec, ts_sub, raw_payload in packets:
            incl_len = len(raw_payload)
            orig_len = incl_len
            pkt_hdr = struct.pack(f"{endian}IIII", ts_sec, ts_sub, incl_len, orig_len)
            f.write(pkt_hdr)
            f.write(raw_payload)
    return filepath


def build_raw_ipv4_packet(
    src_ip: str,
    dst_ip: str,
    sport: int,
    dport: int,
    protocol: int = 6,  # TCP
    payload: bytes = b"test_payload_bytes",
    vlan_id: int = None
) -> bytes:
    """Monta um frame Ethernet com IPv4 e TCP/UDP sintético."""
    ip_proto = protocol
    src_bytes = socket.inet_aton(src_ip)
    dst_bytes = socket.inet_aton(dst_ip)

    if protocol == 6:  # TCP
        l4_hdr = struct.pack("!HHIIBBHHH", sport, dport, 1000, 0, 0x50, 0x18, 8192, 0, 0)
    elif protocol == 17:  # UDP
        udp_len = 8 + len(payload)
        l4_hdr = struct.pack("!HHHH", sport, dport, udp_len, 0)
    else:  # ICMP ou genérico
        l4_hdr = b"\x08\x00\x00\x00\x00\x00\x00\x00"

    total_ip_len = 20 + len(l4_hdr) + len(payload)
    ip_hdr = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0, total_ip_len, 1, 0, 64, ip_proto, 0, src_bytes, dst_bytes
    )

    if vlan_id is not None:
        eth_hdr = struct.pack("!6s6sHH", b"\xaa" * 6, b"\xbb" * 6, 0x8100, vlan_id) + struct.pack("!H", 0x0800)
    else:
        eth_hdr = struct.pack("!6s6sH", b"\xaa" * 6, b"\xbb" * 6, 0x0800)

    return eth_hdr + ip_hdr + l4_hdr + payload


class TestOnlineStats:
    """Testes para o acumulador estatístico online de Welford e momentos."""

    def test_empty_stats(self):
        stats = OnlineStats()
        assert stats.count == 0
        assert stats.mean == 0.0
        assert stats.variance == 0.0
        assert stats.std == 0.0
        assert stats.skewness == 0.0
        assert stats.min_val == float("inf")
        assert stats.max_val == float("-inf")

    def test_single_value(self):
        stats = OnlineStats()
        stats.update(42.0)
        assert stats.count == 1
        assert stats.mean == 42.0
        assert stats.variance == 0.0
        assert stats.std == 0.0
        assert stats.skewness == 0.0
        assert stats.min_val == 42.0
        assert stats.max_val == 42.0

    def test_known_distribution(self):
        stats = OnlineStats()
        values = [10.0, 20.0, 30.0, 40.0, 50.0]
        for v in values:
            stats.update(v)

        assert stats.count == 5
        assert stats.mean == pytest.approx(30.0)
        assert stats.min_val == 10.0
        assert stats.max_val == 50.0
        assert stats.variance == pytest.approx(250.0)  # sample variance
        assert stats.std == pytest.approx(15.811388, rel=1e-4)
        assert stats.skewness == pytest.approx(0.0, abs=1e-5)  # perfeitamente simétrica

    def test_constant_values(self):
        stats = OnlineStats()
        for _ in range(10):
            stats.update(100.0)
        assert stats.count == 10
        assert stats.mean == 100.0
        assert stats.variance == 0.0
        assert stats.std == 0.0
        assert stats.skewness == 0.0


class TestParseRawPacket:
    """Testes para decodificação ultra-rápida de pacotes L2/L3/L4."""

    def test_parse_valid_ipv4_tcp(self):
        raw = build_raw_ipv4_packet("192.168.1.100", "10.0.0.1", 54321, 443, protocol=6)
        pkt = parse_raw_packet(raw, linktype=1, ts=100.5, wire_len=len(raw))
        assert pkt is not None
        assert pkt.timestamp == 100.5
        assert pkt.src_ip == "192.168.1.100"
        assert pkt.dst_ip == "10.0.0.1"
        assert pkt.src_port == 54321
        assert pkt.dst_port == 443
        assert pkt.protocol == 6
        assert pkt.length == len(raw)

    def test_parse_valid_ipv4_udp(self):
        raw = build_raw_ipv4_packet("172.16.0.5", "8.8.8.8", 12345, 53, protocol=17)
        pkt = parse_raw_packet(raw, linktype=1, ts=200.0)
        assert pkt is not None
        assert pkt.protocol == 17
        assert pkt.src_port == 12345
        assert pkt.dst_port == 53

    def test_parse_vlan_tagged_packet(self):
        raw = build_raw_ipv4_packet("192.168.2.1", "10.1.1.1", 8080, 80, protocol=6, vlan_id=100)
        pkt = parse_raw_packet(raw, linktype=1, ts=300.0)
        assert pkt is not None
        assert pkt.src_ip == "192.168.2.1"
        assert pkt.dst_port == 80

    def test_parse_truncated_ethernet(self):
        assert parse_raw_packet(b"\x00" * 10, linktype=1) is None

    def test_parse_non_ip_packet(self):
        # Frame Ethernet com tipo ARP (0x0806)
        arp_frame = b"\x00" * 12 + b"\x08\x06" + b"\x00" * 28
        assert parse_raw_packet(arp_frame, linktype=1) is None

    def test_parse_linux_cooked_sll(self):
        # Linktype 113: SLL header (16 bytes), protocol 0x0800 em bytes 14..16
        sll_hdr = b"\x00" * 14 + b"\x08\x00"
        ip_raw = build_raw_ipv4_packet("10.0.0.2", "10.0.0.3", 1111, 2222)[14:]
        pkt = parse_raw_packet(sll_hdr + ip_raw, linktype=113, ts=400.0)
        assert pkt is not None
        assert pkt.src_ip == "10.0.0.2"
        assert pkt.src_port == 1111
        assert pkt.dst_port == 2222


class TestBidirectionalFlow:
    """Testes para a classe de agregação de fluxo bidirecional."""

    def test_single_forward_packet(self):
        pkt = PacketRecord(
            timestamp=1000.0,
            src_ip="192.168.1.10",
            src_port=50000,
            dst_ip="1.1.1.1",
            dst_port=443,
            protocol=6,
            length=100
        )
        flow = BidirectionalFlow(pkt)
        row = flow.to_dict(label="betting")

        assert row["flow_id"] == "192.168.1.10:50000-1.1.1.1:443-6"
        assert row["src_ip"] == "192.168.1.10"
        assert row["dst_port"] == 443
        assert row["flow_pkts_tot"] == 1
        assert row["fwd_pkts_tot"] == 1
        assert row["bwd_pkts_tot"] == 0
        assert row["flow_bytes_tot"] == 100
        assert row["flow_duration"] == 0.0
        assert row["label"] == "betting"
        assert all(k in row for k in CSV_FIELDNAMES)

    def test_bidirectional_exchange(self):
        # 1. Forward packet de A para B
        pkt1 = PacketRecord(1000.0, "192.168.1.10", 50000, "1.1.1.1", 443, 6, 60)
        # 2. Backward packet de B para A (resposta)
        pkt2 = PacketRecord(1000.2, "1.1.1.1", 443, "192.168.1.10", 50000, 6, 120)
        # 3. Forward packet de A para B
        pkt3 = PacketRecord(1000.6, "192.168.1.10", 50000, "1.1.1.1", 443, 6, 80)

        flow = BidirectionalFlow(pkt1)
        flow.add_packet(pkt2)
        flow.add_packet(pkt3)
        row = flow.to_dict(label="benign")

        assert row["flow_pkts_tot"] == 3
        assert row["fwd_pkts_tot"] == 2
        assert row["bwd_pkts_tot"] == 1
        assert row["flow_bytes_tot"] == 260
        assert row["fwd_bytes_tot"] == 140
        assert row["bwd_bytes_tot"] == 120
        assert row["flow_duration"] == pytest.approx(0.6, abs=1e-4)
        assert row["fwd_iat_mean"] == pytest.approx(0.6, abs=1e-4)  # 1000.6 - 1000.0
        assert row["flow_iat_mean"] == pytest.approx(0.3, abs=1e-4)  # (0.2 + 0.4)/2
        assert row["pkt_len_min"] == 60
        assert row["pkt_len_max"] == 120


class TestFlowExtractor:
    """Testes para o motor de agrupamento e expiração por inatividade."""

    def test_group_same_flow(self):
        extractor = FlowExtractor(flow_timeout=60.0)
        pkt1 = PacketRecord(10.0, "10.0.0.1", 1234, "10.0.0.2", 80, 6, 50)
        pkt2 = PacketRecord(15.0, "10.0.0.2", 80, "10.0.0.1", 1234, 6, 100)
        pkt3 = PacketRecord(20.0, "10.0.0.1", 1234, "10.0.0.2", 80, 6, 75)

        for p in (pkt1, pkt2, pkt3):
            emitted = extractor.add_packet(p)
            assert len(emitted) == 0

        flushed = extractor.flush_all()
        assert len(flushed) == 1
        assert flushed[0].fwd_pkts == 2
        assert flushed[0].bwd_pkts == 1

    def test_flow_timeout_expiration(self):
        extractor = FlowExtractor(flow_timeout=30.0)
        pkt1 = PacketRecord(10.0, "10.0.0.1", 1234, "10.0.0.2", 80, 6, 50)
        # Pacote após 40s (excede timeout de 30s)
        pkt2 = PacketRecord(50.0, "10.0.0.1", 1234, "10.0.0.2", 80, 6, 60)

        assert len(extractor.add_packet(pkt1)) == 0
        emitted = extractor.add_packet(pkt2)
        assert len(emitted) == 1
        assert emitted[0].fwd_pkts == 1
        assert emitted[0].start_time == 10.0

        flushed = extractor.flush_all()
        assert len(flushed) == 1
        assert flushed[0].start_time == 50.0

    def test_min_packets_filter(self):
        extractor = FlowExtractor(min_packets=2)
        single_pkt = PacketRecord(10.0, "1.1.1.1", 1111, "2.2.2.2", 2222, 6, 40)
        extractor.add_packet(single_pkt)

        # Como tem apenas 1 pacote e min_packets=2, deve ser filtrado
        flushed = extractor.flush_all()
        assert len(flushed) == 0


class TestInferClassFromName:
    """Testes de inferência de classe binária."""

    def test_betting_keywords(self):
        assert infer_class_from_name("apostas_bet365_20261028.pcap") == "betting"
        assert infer_class_from_name("capture_betano_live.pcap") == "betting"
        assert infer_class_from_name(Path("/data/raw/betting/traffic_01.pcap")) == "betting"

    def test_benign_keywords(self):
        assert infer_class_from_name("benign_youtube_stream.pcap") == "benign"
        assert infer_class_from_name("controle_g1_portal.pcap") == "benign"
        assert infer_class_from_name(Path("/data/raw/benign/traffic_02.pcap")) == "benign"

    def test_unknown_filename(self):
        assert infer_class_from_name("generic_capture.pcap") == "unknown"


class TestProcessPcapFile:
    """Testes de processamento de arquivo PCAP ponta a ponta."""

    def test_nonexistent_file(self, tmp_path):
        flows = list(process_pcap_file(tmp_path / "nao_existe.pcap"))
        assert len(flows) == 0

    def test_empty_or_too_small(self, tmp_path):
        small = tmp_path / "small.pcap"
        small.write_bytes(b"\x00" * 15)
        flows = list(process_pcap_file(small))
        assert len(flows) == 0

    def test_synthetic_valid_pcap(self, tmp_path):
        pcap_path = tmp_path / "betting_bet365_sample.pcap"
        # Criação de 4 pacotes alternando direções
        raw_fwd1 = build_raw_ipv4_packet("192.168.1.50", "104.18.2.1", 49152, 443, 6, b"syn")
        raw_bwd1 = build_raw_ipv4_packet("104.18.2.1", "192.168.1.50", 443, 49152, 6, b"syn_ack")
        raw_fwd2 = build_raw_ipv4_packet("192.168.1.50", "104.18.2.1", 49152, 443, 6, b"client_hello")
        raw_bwd2 = build_raw_ipv4_packet("104.18.2.1", "192.168.1.50", 443, 49152, 6, b"server_hello")

        packets = [
            (1000, 100000, raw_fwd1),
            (1000, 200000, raw_bwd1),
            (1000, 400000, raw_fwd2),
            (1000, 800000, raw_bwd2),
        ]
        create_mock_pcap_with_raw_packets(pcap_path, packets)

        flows = list(process_pcap_file(pcap_path))
        assert len(flows) == 1
        flow = flows[0]
        assert flow["label"] == "betting"
        assert flow["flow_pkts_tot"] == 4
        assert flow["fwd_pkts_tot"] == 2
        assert flow["bwd_pkts_tot"] == 2
        assert flow["flow_duration"] == pytest.approx(0.7, abs=1e-3)
        assert flow["protocol"] == 6

    def test_nanosecond_magic_pcap(self, tmp_path):
        pcap_path = tmp_path / "benign_nanoseconds.pcap"
        raw_pkt1 = build_raw_ipv4_packet("192.168.1.50", "8.8.8.8", 5353, 53, 17, b"dns_req")
        raw_pkt2 = build_raw_ipv4_packet("8.8.8.8", "192.168.1.50", 53, 5353, 17, b"dns_resp")

        packets = [
            (2000, 100_000_000, raw_pkt1),  # 2000.1s
            (2000, 500_000_000, raw_pkt2),  # 2000.5s
        ]
        create_mock_pcap_with_raw_packets(pcap_path, packets, magic=0xa1b23c4d)

        flows = list(process_pcap_file(pcap_path))
        assert len(flows) == 1
        assert flows[0]["label"] == "benign"
        assert flows[0]["flow_duration"] == pytest.approx(0.4, abs=1e-3)


class TestPipelineAndDirectory:
    """Testes de processamento em lote e CLI."""

    def test_process_empty_directory(self, tmp_path):
        empty_dir = tmp_path / "empty_dir"
        empty_dir.mkdir()
        out_csv = tmp_path / "output.csv"

        pcaps, flows = process_directory(empty_dir, out_csv)
        assert pcaps == 0
        assert flows == 0
        assert out_csv.exists()
        with open(out_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            assert header == CSV_FIELDNAMES

    def test_process_directory_with_multiple_pcaps(self, tmp_path):
        raw_dir = tmp_path / "raw"
        out_csv = tmp_path / "flows.csv"

        # PCAP 1 (Apostas)
        pcap1 = raw_dir / "apostas_kto.pcap"
        pkt1 = build_raw_ipv4_packet("10.0.0.1", "1.1.1.1", 1234, 443, 6, b"data1")
        pkt2 = build_raw_ipv4_packet("10.0.0.1", "1.1.1.1", 1234, 443, 6, b"data2")
        create_mock_pcap_with_raw_packets(pcap1, [(100, 0, pkt1), (101, 0, pkt2)])

        # PCAP 2 (Benigno)
        pcap2 = raw_dir / "benign_youtube.pcap"
        pkt3 = build_raw_ipv4_packet("10.0.0.2", "2.2.2.2", 5678, 443, 6, b"video1")
        pkt4 = build_raw_ipv4_packet("2.2.2.2", "10.0.0.2", 443, 5678, 6, b"video2")
        create_mock_pcap_with_raw_packets(pcap2, [(200, 0, pkt3), (201, 0, pkt4)])

        pcaps, flows = process_directory(raw_dir, out_csv, batch_size=2)
        assert pcaps == 2
        assert flows == 2
        assert out_csv.exists()

        with open(out_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2
            labels = {r["label"] for r in rows}
            assert labels == {"betting", "benign"}

    def test_extract_flows_pipeline_single_file(self, tmp_path):
        pcap_file = tmp_path / "apostas_single.pcap"
        pkt1 = build_raw_ipv4_packet("10.0.0.1", "1.1.1.1", 1234, 443, 6, b"d1")
        create_mock_pcap_with_raw_packets(pcap_file, [(100, 0, pkt1)])
        out_csv = tmp_path / "single_out.csv"

        pcaps, flows = extract_flows_pipeline(pcap_file, out_csv)
        assert pcaps == 1
        assert flows == 1
        assert out_csv.exists()

    def test_cli_execution(self, tmp_path, monkeypatch):
        pcap_file = tmp_path / "betting_cli_test.pcap"
        pkt1 = build_raw_ipv4_packet("10.0.0.1", "1.1.1.1", 1234, 443, 6, b"d1")
        create_mock_pcap_with_raw_packets(pcap_file, [(100, 0, pkt1)])
        out_csv = tmp_path / "cli_out.csv"

        test_args = [
            "flow_extractor.py",
            "--pcap-file", str(pcap_file),
            "--output-csv", str(out_csv),
            "--flow-timeout", "30.0"
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        ret = main()
        assert ret == 0
        assert out_csv.exists()


class TestAdditionalCoverageEdgeCases:
    """Testes adicionais de casos de borda e alta cobertura."""

    def test_parse_raw_ipv6_ethernet(self):
        src_v6 = socket.inet_pton(socket.AF_INET6, "2001:db8::1")
        dst_v6 = socket.inet_pton(socket.AF_INET6, "2001:db8::2")
        v6_hdr = struct.pack("!IHBB", 0x60000000, 20, 6, 64) + src_v6 + dst_v6
        tcp_hdr = struct.pack("!HHIIBBHHH", 8080, 443, 1, 0, 0x50, 0x02, 1024, 0, 0)
        eth_v6 = struct.pack("!6s6sH", b"\xaa" * 6, b"\xbb" * 6, 0x86dd) + v6_hdr + tcp_hdr

        pkt = parse_raw_packet(eth_v6, linktype=1, ts=500.0)
        assert pkt is not None
        assert pkt.protocol == 6
        assert pkt.src_port == 8080
        assert pkt.dst_port == 443
        assert "2001:db8" in pkt.src_ip

    def test_parse_raw_ip_linktypes(self):
        # Linktype 101 (LINKTYPE_RAW): sem cabeçalho Ethernet
        raw_ip = build_raw_ipv4_packet("192.168.1.1", "10.0.0.1", 1000, 2000)[14:]
        pkt = parse_raw_packet(raw_ip, linktype=101, ts=600.0)
        assert pkt is not None
        assert pkt.src_ip == "192.168.1.1"
        assert pkt.src_port == 1000

    def test_parse_icmp_protocol(self):
        raw = build_raw_ipv4_packet("192.168.1.1", "10.0.0.1", 0, 0, protocol=1)
        pkt = parse_raw_packet(raw, linktype=1, ts=700.0)
        assert pkt is not None
        assert pkt.protocol == 1
        assert pkt.src_port == 0
        assert pkt.dst_port == 0

    def test_flush_expired_method(self):
        extractor = FlowExtractor(flow_timeout=20.0)
        pkt1 = PacketRecord(100.0, "10.0.0.1", 1234, "10.0.0.2", 80, 6, 60)
        extractor.add_packet(pkt1)
        # flush_expired at t=110 (delta 10s <= 20s): not expired
        assert len(extractor.flush_expired(current_time=110.0)) == 0
        # flush_expired at t=130 (delta 30s > 20s): expired!
        expired = extractor.flush_expired(current_time=130.0)
        assert len(expired) == 1
        assert expired[0].start_time == 100.0

    def test_pcap_corrupted_magic_number(self, tmp_path):
        bad_magic = tmp_path / "bad_magic.pcap"
        bad_magic.write_bytes(b"\xde\xad\xbe\xef" + b"\x00" * 20)
        flows = list(process_pcap_file(bad_magic))
        assert len(flows) == 0

    def test_pcap_truncated_packet_data(self, tmp_path):
        pcap_path = tmp_path / "truncated_data.pcap"
        with open(pcap_path, "wb") as f:
            # global header
            f.write(struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1))
            # packet header claiming 100 bytes incl_len
            f.write(struct.pack("<IIII", 1000, 0, 100, 100))
            # write only 10 bytes
            f.write(b"\x00" * 10)
        flows = list(process_pcap_file(pcap_path))
        assert len(flows) == 0

    def test_pcap_truncated_packet_header(self, tmp_path):
        pcap_path = tmp_path / "truncated_hdr.pcap"
        with open(pcap_path, "wb") as f:
            f.write(struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1))
            # write partial packet header (8 bytes instead of 16)
            f.write(b"\x00" * 8)
        flows = list(process_pcap_file(pcap_path))
        assert len(flows) == 0

    def test_pcap_abnormal_packet_length(self, tmp_path):
        pcap_path = tmp_path / "abnormal_len.pcap"
        with open(pcap_path, "wb") as f:
            f.write(struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1))
            # abnormal incl_len > 65535*4
            f.write(struct.pack("<IIII", 1000, 0, 500000, 500000))
        flows = list(process_pcap_file(pcap_path))
        assert len(flows) == 0
