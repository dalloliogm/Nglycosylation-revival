#!/usr/bin/env python3
"""Compute expression deployment and optional essentiality metrics for N-glyco genes."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu


GENE_TABLE = Path("data/processed/nglyco_gene_table.tsv")
HPA_GTEX = Path("data/raw/hpa_rna_tissue_gtex.tsv")
DEFAULT_DEPMAP = Path("data/external/depmap/CRISPRGeneEffect.csv")

OUT_TABLE = Path("data/processed/nglyco_expression_essentiality.tsv")
EXPR_SUMMARY = Path("results/tables/interface_expression_summary.tsv")
ESS_SUMMARY = Path("results/tables/interface_essentiality_summary.tsv")
FIG_PNG = Path("results/figures/interface_expression_profile.png")
FIG_SVG = Path("results/figures/interface_expression_profile.svg")

EXPRESSION_THRESHOLD = 1.0

BARRIER_TISSUES = {
    "skin",
    "colon",
    "small intestine",
    "stomach",
    "esophagus",
    "lung",
    "breast",
    "cervix",
    "vagina",
    "urinary bladder",
}

IMMUNE_TISSUES = {
    "blood",
    "spleen",
}

PRIMARY_GROUPS = ["upstream_core", "downstream_diversification"]
GROUP_ORDER = [
    "substrate_support",
    "upstream_core",
    "checkpoint_layer",
    "downstream_diversification",
]


def ensure_dirs() -> None:
    for path in [OUT_TABLE, EXPR_SUMMARY, ESS_SUMMARY, FIG_PNG, FIG_SVG]:
        path.parent.mkdir(parents=True, exist_ok=True)


def tau(values: pd.Series) -> float:
    """Yanai tissue-specificity tau index."""
    clean = pd.to_numeric(values, errors="coerce").fillna(0).astype(float)
    if clean.empty:
        return np.nan
    max_expr = clean.max()
    if max_expr <= 0:
        return 0.0
    if len(clean) == 1:
        return 0.0
    return float(((1 - (clean / max_expr)).sum()) / (len(clean) - 1))


def load_expression_metrics(hpa_path: Path, symbols: set[str]) -> pd.DataFrame:
    if not hpa_path.exists():
        raise FileNotFoundError(
            f"Missing HPA GTEx table: {hpa_path}. See docs/methods/interface-layer-analysis.md."
        )

    hpa = pd.read_csv(hpa_path, sep="\t")
    required = {"Gene name", "Tissue", "nTPM"}
    missing = required.difference(hpa.columns)
    if missing:
        raise ValueError(f"HPA table missing required columns: {sorted(missing)}")

    hpa = hpa[hpa["Gene name"].isin(symbols)].copy()
    hpa["nTPM"] = pd.to_numeric(hpa["nTPM"], errors="coerce").fillna(0.0)
    hpa["tissue_lower"] = hpa["Tissue"].str.lower()

    records = []
    for symbol, group in hpa.groupby("Gene name", sort=True):
        all_expr = group["nTPM"]
        barrier = group[group["tissue_lower"].isin(BARRIER_TISSUES)]["nTPM"]
        immune = group[group["tissue_lower"].isin(IMMUNE_TISSUES)]["nTPM"]
        mean_expr = float(all_expr.mean())
        barrier_mean = float(barrier.mean()) if len(barrier) else np.nan
        immune_mean = float(immune.mean()) if len(immune) else np.nan
        records.append(
            {
                "symbol": symbol,
                "expression_source": "Human Protein Atlas GTEx RNA tissue nTPM",
                "expression_n_tissues_total": int(group["Tissue"].nunique()),
                "expression_n_tissues_ntpm_ge_1": int((all_expr >= EXPRESSION_THRESHOLD).sum()),
                "expression_mean_ntpm": mean_expr,
                "expression_median_ntpm": float(all_expr.median()),
                "expression_max_ntpm": float(all_expr.max()),
                "expression_tau": tau(all_expr),
                "barrier_tissue_mean_ntpm": barrier_mean,
                "immune_tissue_mean_ntpm": immune_mean,
                "barrier_to_all_expression_ratio": barrier_mean / mean_expr if mean_expr > 0 else np.nan,
                "immune_to_all_expression_ratio": immune_mean / mean_expr if mean_expr > 0 else np.nan,
            }
        )

    return pd.DataFrame(records)


def parse_depmap_gene_symbol(column: str) -> str:
    """Extract HGNC symbol from common DepMap column formats."""
    match = re.match(r"^(.+?)\s+\([^)]+\)$", column)
    if match:
        return match.group(1)
    return column


def load_depmap_metrics(depmap_path: Path, symbols: set[str]) -> pd.DataFrame:
    if not depmap_path.exists():
        return pd.DataFrame({"symbol": sorted(symbols), "essentiality_source": "not_available"})

    dep = pd.read_csv(depmap_path)
    if dep.empty:
        raise ValueError(f"DepMap file is empty: {depmap_path}")

    first_col = dep.columns[0]
    if first_col.lower() in {"modelid", "depmap_id", "cell_line", "cellline"}:
        gene_cols = dep.columns[1:]
    else:
        gene_cols = dep.columns

    rename = {col: parse_depmap_gene_symbol(col) for col in gene_cols}
    selected_original = [col for col in gene_cols if rename[col] in symbols]
    if not selected_original:
        raise ValueError(
            f"No N-glyco symbols matched DepMap columns in {depmap_path}. "
            "Expected columns like 'GENE (EntrezID)' or HGNC symbols."
        )

    records = []
    for original_col in selected_original:
        symbol = rename[original_col]
        vals = pd.to_numeric(dep[original_col], errors="coerce").dropna()
        records.append(
            {
                "symbol": symbol,
                "essentiality_source": str(depmap_path),
                "depmap_n_cell_lines": int(vals.shape[0]),
                "depmap_mean_gene_effect": float(vals.mean()) if len(vals) else np.nan,
                "depmap_median_gene_effect": float(vals.median()) if len(vals) else np.nan,
                "depmap_fraction_strongly_essential": float((vals <= -0.5).mean()) if len(vals) else np.nan,
                "depmap_fraction_common_essential": float((vals <= -1.0).mean()) if len(vals) else np.nan,
            }
        )

    return pd.DataFrame(records)


def summarize_by_group(df: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    rows = []
    for group_name, group_df in df.groupby("analysis_group", sort=False):
        row = {"analysis_group": group_name, "n_genes": int(len(group_df))}
        for metric in metrics:
            vals = pd.to_numeric(group_df[metric], errors="coerce").dropna()
            row[f"{metric}_median"] = float(vals.median()) if len(vals) else np.nan
            row[f"{metric}_mean"] = float(vals.mean()) if len(vals) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def primary_contrast(df: pd.DataFrame, metric: str) -> dict[str, object]:
    primary = df[
        (df["include_primary"] == "yes")
        & (df["analysis_group"].isin(PRIMARY_GROUPS))
    ].copy()
    up = pd.to_numeric(
        primary.loc[primary["analysis_group"] == "upstream_core", metric], errors="coerce"
    ).dropna()
    down = pd.to_numeric(
        primary.loc[primary["analysis_group"] == "downstream_diversification", metric], errors="coerce"
    ).dropna()
    row: dict[str, object] = {
        "metric": metric,
        "upstream_n": int(len(up)),
        "downstream_n": int(len(down)),
        "upstream_median": float(up.median()) if len(up) else np.nan,
        "downstream_median": float(down.median()) if len(down) else np.nan,
        "mannwhitney_p": np.nan,
        "rank_biserial_r": np.nan,
    }
    if len(up) and len(down):
        stat, pval = mannwhitneyu(up, down, alternative="two-sided")
        row["mannwhitney_p"] = float(pval)
        row["rank_biserial_r"] = float(1 - 2 * stat / (len(up) * len(down)))
    return row


def write_summaries(df: pd.DataFrame, has_depmap: bool) -> None:
    expression_metrics = [
        "expression_n_tissues_ntpm_ge_1",
        "expression_mean_ntpm",
        "expression_tau",
        "barrier_tissue_mean_ntpm",
        "immune_tissue_mean_ntpm",
        "barrier_to_all_expression_ratio",
        "immune_to_all_expression_ratio",
    ]
    expr_summary = summarize_by_group(df, expression_metrics)
    contrast_rows = [primary_contrast(df, metric) for metric in expression_metrics]
    contrast = pd.DataFrame(contrast_rows)
    expr_summary.to_csv(EXPR_SUMMARY, sep="\t", index=False)
    contrast.to_csv(EXPR_SUMMARY.with_name("interface_expression_primary_contrasts.tsv"), sep="\t", index=False)

    if has_depmap:
        essentiality_metrics = [
            "depmap_mean_gene_effect",
            "depmap_median_gene_effect",
            "depmap_fraction_strongly_essential",
            "depmap_fraction_common_essential",
        ]
        ess_summary = summarize_by_group(df, essentiality_metrics)
        ess_contrast = pd.DataFrame([primary_contrast(df, metric) for metric in essentiality_metrics])
        ess_summary.to_csv(ESS_SUMMARY, sep="\t", index=False)
        ess_contrast.to_csv(ESS_SUMMARY.with_name("interface_essentiality_primary_contrasts.tsv"), sep="\t", index=False)


def plot_expression(df: pd.DataFrame) -> None:
    plot_df = df[df["analysis_group"].isin(GROUP_ORDER)].copy()
    plot_df["analysis_group"] = pd.Categorical(plot_df["analysis_group"], GROUP_ORDER, ordered=True)
    plot_df = plot_df.sort_values("analysis_group")

    metrics = [
        ("expression_n_tissues_ntpm_ge_1", "Expression breadth\n(tissues nTPM >= 1)"),
        ("expression_tau", "Tissue specificity\n(tau)"),
        ("barrier_to_all_expression_ratio", "Barrier / all\nmean expression"),
        ("immune_to_all_expression_ratio", "Immune proxy / all\nmean expression"),
    ]

    colors = {
        "substrate_support": "#9aa0a6",
        "upstream_core": "#4c78a8",
        "checkpoint_layer": "#f58518",
        "downstream_diversification": "#54a24b",
    }

    fig, axes = plt.subplots(1, len(metrics), figsize=(13, 4), constrained_layout=True)
    for ax, (metric, title) in zip(axes, metrics, strict=True):
        groups = [g for g in GROUP_ORDER if g in set(plot_df["analysis_group"].dropna())]
        data = [
            pd.to_numeric(plot_df.loc[plot_df["analysis_group"] == group, metric], errors="coerce").dropna()
            for group in groups
        ]
        bp = ax.boxplot(data, tick_labels=[g.replace("_", "\n") for g in groups], patch_artist=True)
        for patch, group in zip(bp["boxes"], groups, strict=True):
            patch.set_facecolor(colors[group])
            patch.set_alpha(0.75)
        ax.set_title(title)
        ax.tick_params(axis="x", labelrotation=35)
        ax.grid(axis="y", alpha=0.25)

    fig.suptitle("N-glycosylation expression deployment by pathway layer", fontsize=12)
    fig.savefig(FIG_PNG, dpi=300)
    fig.savefig(FIG_SVG)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gene-table", type=Path, default=GENE_TABLE)
    parser.add_argument("--hpa-gtex", type=Path, default=HPA_GTEX)
    parser.add_argument("--depmap-gene-effect", type=Path, default=DEFAULT_DEPMAP)
    args = parser.parse_args()

    ensure_dirs()
    gene_table = pd.read_csv(args.gene_table, sep="\t")
    symbols = set(gene_table["symbol"])

    expression = load_expression_metrics(args.hpa_gtex, symbols)
    essentiality = load_depmap_metrics(args.depmap_gene_effect, symbols)
    has_depmap = args.depmap_gene_effect.exists()

    df = gene_table.merge(expression, on="symbol", how="left").merge(essentiality, on="symbol", how="left")
    df["interface_expression_essentiality_version"] = "v0.1_2026-06-15"
    df.to_csv(OUT_TABLE, sep="\t", index=False)

    write_summaries(df, has_depmap=has_depmap)
    plot_expression(df)

    print(f"Wrote {OUT_TABLE} ({len(df)} genes)")
    print(f"Wrote {EXPR_SUMMARY}")
    print(f"Wrote {FIG_PNG}")
    if has_depmap:
        print(f"Wrote {ESS_SUMMARY}")
    else:
        print(f"DepMap file not found at {args.depmap_gene_effect}; essentiality columns marked not_available.")


if __name__ == "__main__":
    main()
