# -*- coding: utf-8 -*-
"""
Suíte de Testes Unitários para a Issue #16: Extração de Metadados Brutos de PCAPs.
"""

import os
import sys
import csv
import json
import struct
import pytest
from pathlib import Path

from src.collector.extract_raw_metadata import (
    infer_class_from_name,
    extract_pcap_file_metadata,
    calculate_class_statistics,
    extract_raw_metadata_pipeline,
    main,
    LIBPCAP_MAGIC_CONFIGS
)


def create_mock_pcap(
    filepath: Path,
    packets: list,  # list of tuples: (ts_sec, ts_sub, payload_bytes)
    magic: int = 0xa1b2c3d4,  # default Little-Endian microsecond: 0xa1b2c3d4 in LE byte-order = \xd4\xc3\xb2\xa1
    endian: str = "<"
) -> Path:
    """
    Cria um arquivo PCAP sintético válido para testes unitários.
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        # Libpcap global header (24 bytes):
        # magic_number (4B), version_major (2B), version_minor (2B),
        # thiszone (4B), sigfigs (4B), snaplen (4B), network (4B)
        hdr = struct.pack(
            f"{endian}IHHiIII",
            magic,
            2, 4,
            0,
            0,
            65535,
            1  # LINKTYPE_ETHERNET
        )
        f.write(hdr)

        for ts_sec, ts_sub, payload in packets:
            incl_len = len(payload)
            orig_len = len(payload)
            pkt_hdr = struct.pack(f"{endian}IIII", ts_sec, ts_sub, incl_len, orig_len)
            f.write(pkt_hdr)
            f.write(payload)

    return filepath


class TestInferClassFromName:
    def test_betting_keywords(self):
        assert infer_class_from_name("betting_bet365_20261028.pcap") == "betting"
        assert infer_class_from_name("bet_betano_123.pcap") == "betting"
        assert infer_class_from_name("coleta_apostas_kto.pcap") == "betting"

    def test_benign_keywords(self):
        assert infer_class_from_name("benign_youtube_20261028.pcap") == "benign"
        assert infer_class_from_name("controle_g1_noticias.pcap") == "benign"
        assert infer_class_from_name("stream_twitch_test.pcap") == "benign"

    def test_subdirectory_inference(self):
        p1 = Path("/data/raw/betting/capture_01.pcap")
        assert infer_class_from_name(p1) == "betting"
        p2 = Path("/data/raw/benign/capture_02.pcap")
        assert infer_class_from_name(p2) == "benign"

    def test_unknown_name(self):
        assert infer_class_from_name("random_traffic_sample.pcap") == "unknown"


class TestExtractPcapFileMetadata:
    def test_nonexistent_file(self, tmp_path):
        assert extract_pcap_file_metadata(tmp_path / "nonexistent.pcap") is None

    def test_file_too_small(self, tmp_path):
        small_file = tmp_path / "small.pcap"
        small_file.write_bytes(b"\x00" * 10)
        assert extract_pcap_file_metadata(small_file) is None

    def test_invalid_magic_number(self, tmp_path):
        bad_magic = tmp_path / "bad_magic.pcap"
        bad_magic.write_bytes(b"\xde\xad\xbe\xef" + b"\x00" * 20)
        assert extract_pcap_file_metadata(bad_magic) is None

    def test_synthetic_valid_pcap(self, tmp_path):
        pcap_path = tmp_path / "betting_bet365_test.pcap"
        packets = [
            (1000, 100000, b"packet_1_data_12345"),
            (1001, 200000, b"packet_2_data_short"),
            (1002, 500000, b"packet_3_data_longer_payload"),
        ]
        create_mock_pcap(pcap_path, packets, magic=0xa1b2c3d4, endian="<")

        meta = extract_pcap_file_metadata(pcap_path)
        assert meta is not None
        assert meta["filename"] == "betting_bet365_test.pcap"
        assert meta["label_class"] == "betting"
        assert meta["packet_count"] == 3
        assert meta["duration_seconds"] == pytest.approx(2.4, 0.01)
        assert meta["first_timestamp"] == pytest.approx(1000.1, 0.01)
        assert meta["last_timestamp"] == pytest.approx(1002.5, 0.01)
        expected_wire = sum(len(p[2]) for p in packets)
        assert meta["total_wire_bytes"] == expected_wire
        assert meta["avg_packet_size_bytes"] == pytest.approx(expected_wire / 3, 0.01)
        assert meta["packets_per_second"] == pytest.approx(3 / 2.4, 0.05)

    def test_nanosecond_magic_pcap(self, tmp_path):
        pcap_path = tmp_path / "benign_nanoseconds.pcap"
        # Nanosecond magic: 0xa1b23c4d
        packets = [
            (2000, 500_000_000, b"nano_pkt_1"),
            (2005, 500_000_000, b"nano_pkt_2"),
        ]
        create_mock_pcap(pcap_path, packets, magic=0xa1b23c4d, endian="<")

        meta = extract_pcap_file_metadata(pcap_path)
        assert meta is not None
        assert meta["label_class"] == "benign"
        assert meta["packet_count"] == 2
        assert meta["duration_seconds"] == pytest.approx(5.0, 0.01)
        assert meta["first_timestamp"] == pytest.approx(2000.5, 0.01)
        assert meta["last_timestamp"] == pytest.approx(2005.5, 0.01)

    def test_single_packet_pcap(self, tmp_path):
        pcap_path = tmp_path / "betting_single.pcap"
        packets = [(5000, 0, b"single_packet")]
        create_mock_pcap(pcap_path, packets)

        meta = extract_pcap_file_metadata(pcap_path)
        assert meta is not None
        assert meta["packet_count"] == 1
        assert meta["duration_seconds"] == 0.0
        assert meta["packets_per_second"] == 0.0
        assert meta["bytes_per_second"] == 0.0

    def test_unordered_timestamps(self, tmp_path):
        pcap_path = tmp_path / "benign_unordered.pcap"
        packets = [
            (1005, 0, b"first_pkt_in_file_later_time"),
            (1001, 0, b"second_pkt_in_file_earlier_time"),
            (1010, 0, b"third_pkt_in_file_latest_time"),
        ]
        create_mock_pcap(pcap_path, packets)

        meta = extract_pcap_file_metadata(pcap_path)
        assert meta is not None
        assert meta["packet_count"] == 3
        assert meta["first_timestamp"] == 1001.0
        assert meta["last_timestamp"] == 1010.0
        assert meta["duration_seconds"] == 9.0

    def test_empty_pcap_no_packets(self, tmp_path):
        pcap_path = tmp_path / "empty_valid_hdr.pcap"
        create_mock_pcap(pcap_path, [])

        meta = extract_pcap_file_metadata(pcap_path)
        assert meta is not None
        assert meta["packet_count"] == 0
        assert meta["duration_seconds"] == 0.0
        assert meta["total_wire_bytes"] == 0

    def test_truncated_packet_record(self, tmp_path):
        pcap_path = tmp_path / "betting_truncated.pcap"
        packets = [
            (1000, 0, b"pkt_complete_1"),
            (1001, 0, b"pkt_complete_2"),
        ]
        create_mock_pcap(pcap_path, packets)
        # Anexa 8 bytes de cabeçalho incompleto (menos que os 16 bytes necessários)
        with open(pcap_path, "ab") as f:
            f.write(b"\x00" * 8)

        meta = extract_pcap_file_metadata(pcap_path)
        assert meta is not None
        # Deve ter lido com sucesso os 2 pacotes íntegros anteriores
        assert meta["packet_count"] == 2


class TestCalculateClassStatistics:
    def test_empty_records(self):
        stats = calculate_class_statistics([])
        assert stats["file_count"] == 0
        assert stats["total_packets"] == 0
        assert stats["avg_duration_seconds"] == 0.0
        assert stats["std_duration_seconds"] == 0.0

    def test_single_record(self):
        rec = [{
            "duration_seconds": 60.0,
            "packet_count": 1000,
            "file_size_bytes": 1024 * 1024,
            "total_wire_bytes": 1000000,
        }]
        stats = calculate_class_statistics(rec)
        assert stats["file_count"] == 1
        assert stats["total_packets"] == 1000
        assert stats["avg_duration_seconds"] == 60.0
        assert stats["std_duration_seconds"] == 0.0
        assert stats["min_duration_seconds"] == 60.0
        assert stats["max_duration_seconds"] == 60.0
        assert stats["avg_volume_mb_per_file"] == 1.0

    def test_multiple_records(self):
        records = [
            {"duration_seconds": 50.0, "packet_count": 1000, "file_size_bytes": 500000, "total_wire_bytes": 480000},
            {"duration_seconds": 70.0, "packet_count": 2000, "file_size_bytes": 1500000, "total_wire_bytes": 1400000},
        ]
        stats = calculate_class_statistics(records)
        assert stats["file_count"] == 2
        assert stats["total_packets"] == 3000
        assert stats["avg_duration_seconds"] == 60.0
        assert stats["std_duration_seconds"] == pytest.approx(14.14, 0.05)
        assert stats["min_duration_seconds"] == 50.0
        assert stats["max_duration_seconds"] == 70.0
        assert stats["avg_packets_per_file"] == 1500.0


class TestExtractRawMetadataPipeline:
    def test_pipeline_execution(self, tmp_path):
        raw_dir = tmp_path / "raw"
        raw_dir.mkdir()
        out_json = tmp_path / "reports" / "report.json"
        out_csv = tmp_path / "reports" / "report.csv"

        # Cria 2 capturas de apostas e 2 benignas
        create_mock_pcap(
            raw_dir / "betting_bet365.pcap",
            [(1000, 0, b"bet1"), (1060, 0, b"bet2")]
        )
        create_mock_pcap(
            raw_dir / "betting_betano.pcap",
            [(2000, 0, b"betano1"), (2050, 0, b"betano2")]
        )
        create_mock_pcap(
            raw_dir / "benign_youtube.pcap",
            [(3000, 0, b"yt1"), (3090, 0, b"yt2"), (3100, 0, b"yt3")]
        )
        create_mock_pcap(
            raw_dir / "benign_g1.pcap",
            [(4000, 0, b"g1_1"), (4080, 0, b"g1_2")]
        )

        result = extract_raw_metadata_pipeline(
            input_dir=raw_dir,
            output_json=out_json,
            output_csv=out_csv,
            recursive=True,
            min_packets=1
        )

        assert result["total_files_analyzed"] == 4
        assert "betting" in result["summary_by_class"]
        assert "benign" in result["summary_by_class"]
        assert result["summary_by_class"]["betting"]["file_count"] == 2
        assert result["summary_by_class"]["benign"]["file_count"] == 2

        # Validação do arquivo JSON exportado
        assert out_json.exists()
        with open(out_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["total_files_analyzed"] == 4
            assert len(data["files"]) == 4

        # Validação do arquivo CSV exportado
        assert out_csv.exists()
        with open(out_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 4
            assert set(r["label_class"] for r in rows) == {"betting", "benign"}

    def test_pipeline_with_min_packets_filter(self, tmp_path):
        raw_dir = tmp_path / "raw"
        create_mock_pcap(raw_dir / "betting_tiny.pcap", [(100, 0, b"p1")])  # 1 pkt
        create_mock_pcap(
            raw_dir / "betting_good.pcap",
            [(100, 0, b"p1"), (105, 0, b"p2"), (110, 0, b"p3")]
        )  # 3 pkts

        res = extract_raw_metadata_pipeline(
            input_dir=raw_dir,
            min_packets=2
        )
        # O arquivo com apenas 1 pacote deve ter sido filtrado
        assert res["total_files_analyzed"] == 1
        assert res["files"][0]["filename"] == "betting_good.pcap"

    def test_pipeline_empty_directory(self, tmp_path):
        empty_dir = tmp_path / "empty_dir"
        empty_dir.mkdir()
        out_json = tmp_path / "report_empty.json"

        res = extract_raw_metadata_pipeline(
            input_dir=empty_dir,
            output_json=out_json
        )
        assert res["total_files_analyzed"] == 0
        assert out_json.exists()


class TestCliMain:
    def test_cli_execution(self, tmp_path, monkeypatch):
        raw_dir = tmp_path / "raw"
        create_mock_pcap(raw_dir / "betting_test.pcap", [(10, 0, b"data")])
        json_path = tmp_path / "cli_report.json"
        csv_path = tmp_path / "cli_report.csv"

        test_args = [
            "extract_raw_metadata.py",
            "--input-dir", str(raw_dir),
            "--output-json", str(json_path),
            "--output-csv", str(csv_path),
            "--min-packets", "1"
        ]
        monkeypatch.setattr(sys, "argv", test_args)

        main()

        assert json_path.exists()
        assert csv_path.exists()
