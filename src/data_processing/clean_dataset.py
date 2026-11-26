# -*- coding: utf-8 -*-
"""
Módulo de Limpeza e Sanitização do Dataset de Fluxos de Rede.
Referência: Issue #18 e Seção 3.2.4 do TCC.

Remove valores nulos (NaN), infinitos (+/-Inf), registros duplicados
e fluxos incompletos com volume insuficiente de pacotes (< 3), garantindo
integridade numérica estrita para os algoritmos de Machine Learning (RF03, RNF02).
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, Union, List

import numpy as np
import pandas as pd

logger = logging.getLogger("clean_dataset")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def sanitize_dataframe(
    df: pd.DataFrame,
    min_packets: int = 3,
    inf_strategy: str = "drop",
    drop_duplicates: bool = True,
    duplicate_subset: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Executa a limpeza vetorizada de um DataFrame de fluxos de rede.

    Args:
        df: DataFrame original de fluxos extraídos.
        min_packets: Limiar mínimo de pacotes por fluxo (default: 3).
        inf_strategy: Estratégia de tratamento de Inf: 'drop', 'impute_max', 'impute_zero'.
        drop_duplicates: Se True, remove linhas duplicadas exatas.
        duplicate_subset: Lista opcional de colunas para verificação de duplicidade.

    Returns:
        Tupla (df_sanitizado, relatorio_estatistico).
    """
    total_original = len(df)
    current_df = df.copy()

    # Caso DataFrame esteja vazio
    if total_original == 0:
        return current_df, {
            "total_original": 0,
            "nan_inf_removed": 0,
            "duplicates_removed": 0,
            "insufficient_pkts_removed": 0,
            "total_removed": 0,
            "total_preserved": 0,
            "retention_rate_pct": 0.0
        }

    # 1. Identificação e tratamento de valores Infinitos e NaN
    numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()

    # Substitui Inf e -Inf por NaN em colunas numéricas para tratamento unificado
    if numeric_cols:
        inf_mask = np.isinf(current_df[numeric_cols])
        has_inf_per_row = inf_mask.any(axis=1)
    else:
        has_inf_per_row = pd.Series(False, index=current_df.index)

    has_nan_per_row = current_df.isna().any(axis=1)
    nan_or_inf_mask = has_inf_per_row | has_nan_per_row
    nan_inf_count = int(nan_or_inf_mask.sum())

    if inf_strategy == "drop":
        # Descarte de todas as linhas que contêm NaN ou Inf
        current_df = current_df[~nan_or_inf_mask].copy()

    elif inf_strategy == "impute_max":
        # Substitui +Inf pelo máximo finito e -Inf pelo mínimo finito; NaNs pela mediana/0
        for col in numeric_cols:
            col_series = current_df[col]
            finite_vals = col_series[np.isfinite(col_series)]
            if len(finite_vals) > 0:
                max_val = finite_vals.max()
                min_val = finite_vals.min()
                median_val = finite_vals.median()
            else:
                max_val = 0.0
                min_val = 0.0
                median_val = 0.0

            current_df[col] = current_df[col].replace(np.inf, max_val)
            current_df[col] = current_df[col].replace(-np.inf, min_val)
            current_df[col] = current_df[col].fillna(median_val)

        # Para colunas não numéricas que contenham NaN, preenche com 'unknown'
        non_numeric_cols = [c for c in current_df.columns if c not in numeric_cols]
        for col in non_numeric_cols:
            current_df[col] = current_df[col].fillna("unknown")

    elif inf_strategy == "impute_zero":
        for col in numeric_cols:
            current_df[col] = current_df[col].replace([np.inf, -np.inf], 0.0).fillna(0.0)
        non_numeric_cols = [c for c in current_df.columns if c not in numeric_cols]
        for col in non_numeric_cols:
            current_df[col] = current_df[col].fillna("unknown")

    else:
        raise ValueError(f"Estratégia inf_strategy não suportada: '{inf_strategy}'. Opções: drop, impute_max, impute_zero")

    # 2. Remoção de Linhas Duplicadas
    dup_count = 0
    if drop_duplicates and len(current_df) > 0:
        dup_mask = current_df.duplicated(subset=duplicate_subset, keep="first")
        dup_count = int(dup_mask.sum())
        current_df = current_df[~dup_mask].copy()

    # 3. Filtragem de Fluxos Incompletos / Pacotes Insuficientes (< min_packets)
    insuf_count = 0
    if min_packets > 1 and len(current_df) > 0:
        if "flow_pkts_tot" in current_df.columns:
            insuf_mask = pd.to_numeric(current_df["flow_pkts_tot"], errors="coerce") < min_packets
            insuf_count = int(insuf_mask.sum())
            current_df = current_df[~insuf_mask].copy()
        elif "fwd_pkts_tot" in current_df.columns and "bwd_pkts_tot" in current_df.columns:
            tot_pkts = (
                pd.to_numeric(current_df["fwd_pkts_tot"], errors="coerce").fillna(0) +
                pd.to_numeric(current_df["bwd_pkts_tot"], errors="coerce").fillna(0)
            )
            insuf_mask = tot_pkts < min_packets
            insuf_count = int(insuf_mask.sum())
            current_df = current_df[~insuf_mask].copy()

    # 4. Asserções Matemáticas de Integridade (DoD e Seção 3.2.4)
    nan_remaining = current_df.isna().sum().sum()
    assert nan_remaining == 0, f"Falha de integridade: {nan_remaining} valores NaN residuais no dataset sanitizado"

    if numeric_cols:
        curr_numeric = current_df.select_dtypes(include=[np.number])
        if not curr_numeric.empty:
            inf_remaining = np.isinf(curr_numeric.to_numpy()).sum()
            assert inf_remaining == 0, f"Falha de integridade: {inf_remaining} valores Infinitos residuais no dataset sanitizado"

    total_preserved = len(current_df)
    total_removed = total_original - total_preserved
    retention_pct = round((total_preserved / total_original * 100.0), 2) if total_original > 0 else 0.0

    report = {
        "total_original": total_original,
        "nan_inf_identified": nan_inf_count,
        "duplicates_identified": dup_count,
        "insufficient_pkts_identified": insuf_count,
        "total_removed": total_removed,
        "total_preserved": total_preserved,
        "retention_rate_pct": retention_pct
    }

    return current_df, report


def clean_dataset(
    input_source: Union[str, Path, pd.DataFrame],
    output_csv: Optional[Union[str, Path]] = None,
    min_packets: int = 3,
    inf_strategy: str = "drop",
    drop_duplicates: bool = True,
    duplicate_subset: Optional[List[str]] = None,
    report_json: Optional[Union[str, Path]] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Função principal de sanitização do dataset com persistência em disco
    e emissão de relatório formal de auditoria.
    """
    if isinstance(input_source, pd.DataFrame):
        df = input_source.copy()
        src_name = "DataFrame em memória"
    else:
        src_path = Path(input_source)
        if not src_path.exists() or not src_path.is_file():
            raise FileNotFoundError(f"Arquivo CSV de entrada não localizado: {src_path}")
        logger.info(f"[INFO] Carregando {src_path}...")
        df = pd.read_csv(src_path)
        src_name = str(src_path)

    total_original = len(df)
    logger.info(f"[INFO] Carregando {src_name} ({total_original:,} linhas)...")

    cleaned_df, report = sanitize_dataframe(
        df=df,
        min_packets=min_packets,
        inf_strategy=inf_strategy,
        drop_duplicates=drop_duplicates,
        duplicate_subset=duplicate_subset
    )

    nan_inf_pct = (report["nan_inf_identified"] / total_original * 100.0) if total_original > 0 else 0.0
    dup_pct = (report["duplicates_identified"] / total_original * 100.0) if total_original > 0 else 0.0
    insuf_pct = (report["insufficient_pkts_identified"] / total_original * 100.0) if total_original > 0 else 0.0

    action_label = "Removidas" if inf_strategy == "drop" else "Imputadas"
    logger.info(f"[INFO] Linhas com NaN/Inf identificadas: {report['nan_inf_identified']:,} ({nan_inf_pct:.2f}%) -> {action_label}.")
    if drop_duplicates:
        logger.info(f"[INFO] Linhas duplicadas exatas: {report['duplicates_identified']:,} ({dup_pct:.2f}%) -> Removidas.")
    if min_packets > 1:
        logger.info(f"[INFO] Fluxos com pacotes insuficientes (< {min_packets}): {report['insufficient_pkts_identified']:,} ({insuf_pct:.2f}%) -> Removidos.")

    logger.info("================ RELATÓRIO DE LIMPEZA ================")
    logger.info(f"  - Registros originais: {report['total_original']:,}")
    logger.info(f"  - Registros removidos: {report['total_removed']:,}")
    logger.info(f"  - Registros limpos preservados: {report['total_preserved']:,} ({report['retention_rate_pct']}%)")

    if output_csv is not None:
        out_path = Path(output_csv)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cleaned_df.to_csv(out_path, index=False, encoding="utf-8")
        logger.info(f"[SUCCESS] Dataset limpo salvo em {out_path}")

    if report_json is not None:
        rep_path = Path(report_json)
        rep_path.parent.mkdir(parents=True, exist_ok=True)
        with open(rep_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        logger.info(f"[SUCCESS] Relatório de auditoria salvo em {rep_path}")

    return cleaned_df, report


def main() -> int:
    """Interface de Linha de Comando (CLI) para limpeza de dataset."""
    parser = argparse.ArgumentParser(
        description="Sanitizador e Limpador de Dataset de Fluxos de Rede - Firewall Inteligente (RF03, RNF02)"
    )
    parser.add_argument(
        "--input-csv",
        type=str,
        default="data/processed/flows_extracted.csv",
        help="Caminho do arquivo CSV de entrada bruto (padrão: data/processed/flows_extracted.csv)"
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="data/processed/flows_cleaned.csv",
        help="Caminho do arquivo CSV de saída limpo (padrão: data/processed/flows_cleaned.csv)"
    )
    parser.add_argument(
        "--min-packets",
        type=int,
        default=3,
        help="Volume mínimo de pacotes por fluxo para não descarte (padrão: 3)"
    )
    parser.add_argument(
        "--inf-strategy",
        type=str,
        default="drop",
        choices=["drop", "impute_max", "impute_zero"],
        help="Estratégia para tratamento de Infinitos/NaN (padrão: drop)"
    )
    parser.add_argument(
        "--keep-duplicates",
        action="store_true",
        default=False,
        help="Se informado, mantém linhas duplicadas em vez de descartá-las"
    )
    parser.add_argument(
        "--report-json",
        type=str,
        default=None,
        help="Caminho opcional para exportação do sumário de auditoria em JSON"
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

    try:
        _, report = clean_dataset(
            input_source=args.input_csv,
            output_csv=args.output_csv,
            min_packets=args.min_packets,
            inf_strategy=args.inf_strategy,
            drop_duplicates=not args.keep_duplicates,
            report_json=args.report_json
        )
        return 0 if report["total_preserved"] >= 0 else 1
    except Exception as err:
        logger.error(f"[ERRO] Falha na execução da limpeza do dataset: {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

