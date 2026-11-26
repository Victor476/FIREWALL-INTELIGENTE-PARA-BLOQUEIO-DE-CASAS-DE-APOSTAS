# -*- coding: utf-8 -*-
"""
Suíte de Testes Unitários para a Issue #18: Limpeza e Sanitização do Dataset de Fluxos.
Cobre tratamento vetorizado de NaN/Inf, duplicatas, limiar de pacotes e auditoria.
"""

import sys
import json
import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from src.data_processing.clean_dataset import (
    sanitize_dataframe,
    clean_dataset,
    main
)


@pytest.fixture
def sample_flow_dataframe() -> pd.DataFrame:
    """Cria um DataFrame sintético representativo de fluxos de rede."""
    data = {
        "flow_id": [
            "10.0.0.1:1000-1.1.1.1:443-6",
            "10.0.0.2:2000-2.2.2.2:443-6",
            "10.0.0.3:3000-3.3.3.3:443-6",
            "10.0.0.4:4000-4.4.4.4:443-6",
            "10.0.0.5:5000-5.5.5.5:443-6",
            "10.0.0.6:6000-6.6.6.6:443-6",
            "10.0.0.1:1000-1.1.1.1:443-6",
        ],
        "flow_duration": [1.5, 0.0, 2.0, 0.5, 3.0, 1.0, 1.5],
        "flow_pkts_tot": [10, 1, 15, 2, 20, 8, 10],  # 1 e 2 são insuficientes (< 3)
        "fwd_pkts_tot": [5, 1, 8, 1, 10, 4, 5],
        "bwd_pkts_tot": [5, 0, 7, 1, 10, 4, 5],
        "flow_bytes_tot": [1500, 60, 2000, 120, 3000, 800, 1500],
        "flow_pkts_per_sec": [6.66, np.inf, 7.5, 4.0, 6.66, 8.0, 6.66],  # linha 1 tem inf
        "flow_iat_mean": [0.15, np.nan, 0.13, 0.25, 0.15, 0.12, 0.15],   # linha 1 tem nan
        "pkt_len_mean": [150.0, 60.0, 133.3, 60.0, 150.0, 100.0, 150.0],
        "label": ["betting", "benign", "betting", "benign", "betting", "benign", "betting"]
    }
    # A última linha (índice 6) é uma duplicata exata da linha 0 em todas as colunas
    return pd.DataFrame(data)


class TestSanitizeDataframe:
    """Testes para a função de sanitização em memória."""

    def test_empty_dataframe(self):
        empty_df = pd.DataFrame(columns=["flow_id", "flow_pkts_tot", "flow_iat_mean"])
        cleaned, report = sanitize_dataframe(empty_df)
        assert len(cleaned) == 0
        assert report["total_original"] == 0
        assert report["total_removed"] == 0
        assert report["total_preserved"] == 0
        assert report["retention_rate_pct"] == 0.0

    def test_drop_inf_and_nan_strategy(self, sample_flow_dataframe):
        # Na amostra:
        # Linha 1 possui inf em flow_pkts_per_sec e nan em flow_iat_mean -> Removida
        cleaned, report = sanitize_dataframe(
            sample_flow_dataframe,
            min_packets=1,
            inf_strategy="drop",
            drop_duplicates=False
        )
        assert report["nan_inf_identified"] == 1
        assert not cleaned["flow_pkts_per_sec"].isin([np.inf, -np.inf]).any()
        assert cleaned.isna().sum().sum() == 0
        assert len(cleaned) == 6

    def test_impute_max_inf_strategy(self):
        df = pd.DataFrame({
            "val": [10.0, 50.0, np.inf, -np.inf, np.nan],
            "flow_pkts_tot": [10, 10, 10, 10, 10]
        })
        cleaned, report = sanitize_dataframe(df, min_packets=1, inf_strategy="impute_max", drop_duplicates=False)
        assert len(cleaned) == 5
        assert cleaned.isna().sum().sum() == 0
        assert not np.isinf(cleaned["val"]).any()
        # +inf vira 50.0 (max finito), -inf vira 10.0 (min finito), nan vira 30.0 (mediana)
        assert cleaned["val"].iloc[2] == 50.0
        assert cleaned["val"].iloc[3] == 10.0
        assert cleaned["val"].iloc[4] == 30.0

    def test_impute_zero_inf_strategy(self):
        df = pd.DataFrame({
            "val": [10.0, np.inf, -np.inf, np.nan],
            "flow_pkts_tot": [5, 5, 5, 5]
        })
        cleaned, report = sanitize_dataframe(df, min_packets=1, inf_strategy="impute_zero", drop_duplicates=False)
        assert len(cleaned) == 4
        assert cleaned["val"].iloc[1] == 0.0
        assert cleaned["val"].iloc[2] == 0.0
        assert cleaned["val"].iloc[3] == 0.0
        assert cleaned.isna().sum().sum() == 0

    def test_invalid_inf_strategy_raises_error(self, sample_flow_dataframe):
        with pytest.raises(ValueError, match="não suportada"):
            sanitize_dataframe(sample_flow_dataframe, inf_strategy="unsupported_mode")

    def test_drop_duplicate_rows(self, sample_flow_dataframe):
        # Linha 6 é duplicata exata de Linha 0
        cleaned, report = sanitize_dataframe(
            sample_flow_dataframe,
            min_packets=1,
            inf_strategy="impute_zero",
            drop_duplicates=True
        )
        assert report["duplicates_identified"] == 1
        assert len(cleaned) == 6

    def test_keep_duplicates_flag(self, sample_flow_dataframe):
        cleaned, report = sanitize_dataframe(
            sample_flow_dataframe,
            min_packets=1,
            inf_strategy="impute_zero",
            drop_duplicates=False
        )
        assert report["duplicates_identified"] == 0
        assert len(cleaned) == 7

    def test_insufficient_packets_filter(self, sample_flow_dataframe):
        # min_packets = 3:
        # Linha 1 tem 1 pacote, Linha 3 tem 2 pacotes -> Ambas descartadas
        cleaned, report = sanitize_dataframe(
            sample_flow_dataframe,
            min_packets=3,
            inf_strategy="impute_zero",
            drop_duplicates=False
        )
        assert report["insufficient_pkts_identified"] == 2
        assert (cleaned["flow_pkts_tot"] >= 3).all()

    def test_fallback_to_fwd_and_bwd_packets_sum(self):
        # DataFrame sem coluna flow_pkts_tot mas com fwd_pkts_tot e bwd_pkts_tot
        df = pd.DataFrame({
            "fwd_pkts_tot": [1, 2, 5],
            "bwd_pkts_tot": [0, 0, 5],
            "flow_duration": [1.0, 1.0, 1.0]
        })
        cleaned, report = sanitize_dataframe(df, min_packets=3, drop_duplicates=False)
        assert len(cleaned) == 1
        assert report["insufficient_pkts_identified"] == 2

    def test_full_pipeline_combination(self, sample_flow_dataframe):
        # Executa limpeza completa padrão:
        # - Linha 1: contém inf/nan -> removida
        # - Linha 3: tem 2 pacotes (< 3) -> removida
        # - Linha 6: duplicata exata da linha 0 -> removida
        # Restam 4 linhas limpas (linhas 0, 2, 4, 5)
        cleaned, report = sanitize_dataframe(
            sample_flow_dataframe,
            min_packets=3,
            inf_strategy="drop",
            drop_duplicates=True
        )
        assert report["total_original"] == 7
        assert report["nan_inf_identified"] == 1
        assert report["duplicates_identified"] == 1
        assert report["insufficient_pkts_identified"] == 1  # Linha 3 (pois Linha 1 já foi descartada no passo 1)
        assert report["total_preserved"] == 4
        assert report["retention_rate_pct"] == pytest.approx(57.14, abs=0.01)
        assert len(cleaned) == 4
        assert cleaned.isna().sum().sum() == 0
        assert not np.isinf(cleaned.select_dtypes(include=[np.number]).to_numpy()).any()


class TestCleanDatasetIO:
    """Testes de leitura, escrita em arquivo CSV e exportação de relatórios."""

    def test_file_io_clean_dataset(self, tmp_path, sample_flow_dataframe):
        in_csv = tmp_path / "raw_flows.csv"
        out_csv = tmp_path / "cleaned_flows.csv"
        rep_json = tmp_path / "audit_report.json"

        sample_flow_dataframe.to_csv(in_csv, index=False)

        cleaned_df, report = clean_dataset(
            input_source=in_csv,
            output_csv=out_csv,
            min_packets=3,
            inf_strategy="drop",
            drop_duplicates=True,
            report_json=rep_json
        )

        assert out_csv.exists()
        assert rep_json.exists()
        assert len(cleaned_df) == 4

        # Validação do arquivo CSV persistido
        saved_df = pd.read_csv(out_csv)
        assert len(saved_df) == 4
        assert saved_df.isna().sum().sum() == 0

        # Validação do arquivo JSON de auditoria
        with open(rep_json, "r", encoding="utf-8") as f:
            saved_rep = json.load(f)
            assert saved_rep["total_original"] == 7
            assert saved_rep["total_preserved"] == 4

    def test_nonexistent_file_raises_exception(self, tmp_path):
        bad_path = tmp_path / "non_existent.csv"
        with pytest.raises(FileNotFoundError):
            clean_dataset(bad_path)

    def test_cli_execution_success(self, tmp_path, sample_flow_dataframe, monkeypatch):
        in_csv = tmp_path / "cli_input.csv"
        out_csv = tmp_path / "cli_output.csv"
        rep_json = tmp_path / "cli_audit.json"
        sample_flow_dataframe.to_csv(in_csv, index=False)

        test_args = [
            "clean_dataset.py",
            "--input-csv", str(in_csv),
            "--output-csv", str(out_csv),
            "--min-packets", "3",
            "--inf-strategy", "drop",
            "--report-json", str(rep_json)
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        ret = main()
        assert ret == 0
        assert out_csv.exists()
        assert rep_json.exists()

    def test_cli_execution_missing_file_failure(self, tmp_path, monkeypatch):
        test_args = [
            "clean_dataset.py",
            "--input-csv", str(tmp_path / "missing.csv")
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        ret = main()
        assert ret == 1
