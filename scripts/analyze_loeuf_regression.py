#!/usr/bin/env python3
"""Regression analysis: does the LOEUF inversion survive covariate control?

The primary constraint result shows that upstream-core genes have HIGHER median
LOEUF (less constrained) than downstream-diversification genes, which is the
OPPOSITE of the naive architecture prediction. This script tests whether that
pattern is explained by confounders:

  LOEUF ~ analysis_group + paralog_count + expression_breadth + log(gene_length)

Covariates:
  - paralog_count: number of human paralogs from Ensembl REST API
  - expression_breadth: number of GTEx tissues with nTPM >= 1 (Human Protein Atlas)
  - gene_length: genomic span (end - start) from the gene table

If analysis_group drops out after covariate control → the inversion is explained
by composition (e.g. downstream genes have more paralogs or narrower expression).
If analysis_group persists → the inversion is genuinely interesting.

Outputs
-------
data/processed/nglyco_loeuf_covariates.tsv   — joined covariate table
results/tables/loeuf_regression_results.txt  — OLS summary
results/tables/loeuf_covariate_summary.tsv   — per-group covariate summary

Usage
-----
    python scripts/analyze_loeuf_regression.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
import zipfile
import io

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import mannwhitneyu, spearmanr

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

GENE_TABLE = "data/processed/nglyco_gene_table.tsv"
ARCH_TABLE = "data/processed/nglyco_architecture_features.tsv"
CONSTRAINT_TABLE = "data/processed/nglyco_constraint_metrics.tsv"
HPA_CACHE = "data/raw/hpa_rna_tissue_gtex.tsv"
PARALOG_CACHE = "data/raw/ensembl_paralog_counts.tsv"
COVAR_OUT = "data/processed/nglyco_loeuf_covariates.tsv"
REG_OUT = "results/tables/loeuf_regression_results.txt"
SUM_OUT = "results/tables/loeuf_covariate_summary.tsv"

HPA_URL = "https://www.proteinatlas.org/download/tsv/rna_tissue_gtex.tsv.zip"
ENSEMBL_REST = "https://rest.ensembl.org"
EXPRESSION_THRESHOLD = 1.0  # nTPM >= 1 counts as "expressed"


# ---------------------------------------------------------------------------
# Fetch Human Protein Atlas GTEx expression breadth
# ---------------------------------------------------------------------------

def fetch_hpa_expression_breadth(gene_ids: list[str], cache_path: str) -> pd.DataFrame:
    """Return a DataFrame with symbol and n_tissues_expressed from HPA GTEx data."""
    cache = Path(cache_path)
    if not cache.exists():
        print(f"Downloading Human Protein Atlas GTEx RNA data (~30 MB)...")
        cache.parent.mkdir(parents=True, exist_ok=True)
        req = Request(HPA_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=120) as resp:
            data = resp.read()
        # It's a zip containing rna_tissue_gtex.tsv
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            tsv_name = [n for n in zf.namelist() if n.endswith(".tsv")][0]
            with zf.open(tsv_name) as f:
                hpa = pd.read_csv(f, sep="\t")
        hpa.to_csv(cache, sep="\t", index=False)
        print(f"  Saved {len(hpa)} rows to {cache}")
    else:
        print(f"Loading HPA GTEx data from cache: {cache}")
        hpa = pd.read_csv(cache, sep="\t")

    print(f"  HPA columns: {list(hpa.columns[:6])}...")

    # Expected columns: Gene, Gene name, Tissue, TPM or nTPM
    # Normalise column names
    hpa.columns = [c.strip() for c in hpa.columns]
    gene_col = next((c for c in hpa.columns if c.lower() in ("gene name", "gene_name", "gene name")), None)
    if gene_col is None:
        # Try 'Gene name' or second column
        gene_col = hpa.columns[1] if len(hpa.columns) > 1 else hpa.columns[0]
    expr_col = next((c for c in hpa.columns if "ntpm" in c.lower() or "tpm" in c.lower()), None)
    if expr_col is None:
        expr_col = hpa.columns[-1]

    print(f"  Using gene column='{gene_col}', expression column='{expr_col}'")

    # Filter to our genes
    hpa_filt = hpa[hpa[gene_col].isin(gene_ids)].copy()
    hpa_filt["expressed"] = hpa_filt[expr_col].fillna(0) >= EXPRESSION_THRESHOLD

    breadth = (
        hpa_filt.groupby(gene_col)["expressed"]
        .sum()
        .reset_index()
        .rename(columns={gene_col: "symbol", "expressed": "n_tissues_expressed"})
    )
    breadth["n_tissues_expressed"] = breadth["n_tissues_expressed"].astype(int)
    print(f"  Expression breadth computed for {len(breadth)} genes")
    return breadth


# ---------------------------------------------------------------------------
# Fetch paralog counts from Ensembl REST
# ---------------------------------------------------------------------------

def fetch_paralog_count(ensembl_id: str, retries: int = 3) -> int | None:
    """Return number of human paralogs for one gene via Ensembl REST."""
    url = f"{ENSEMBL_REST}/homology/id/human/{ensembl_id}?type=paralogues&target_species=homo_sapiens&content-type=application/json"
    for attempt in range(retries):
        try:
            req = Request(url, headers={"Accept": "application/json", "Content-Type": "application/json"})
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            entries = data.get("data", [])
            if not entries:
                return 0
            homologies = entries[0].get("homologies", [])
            return len(homologies)
        except Exception as exc:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                print(f"    Paralog fetch failed for {ensembl_id}: {exc}")
                return None


def fetch_all_paralog_counts(gene_df: pd.DataFrame, cache_path: str) -> pd.DataFrame:
    """Return DataFrame with ensembl_gene_id and paralog_count_ensembl."""
    cache = Path(cache_path)
    if cache.exists():
        print(f"Loading paralog counts from cache: {cache}")
        return pd.read_csv(cache, sep="\t")

    print(f"Fetching paralog counts for {len(gene_df)} genes from Ensembl REST...")
    records = []
    for i, row in gene_df.iterrows():
        eid = row["ensembl_gene_id"]
        sym = row["symbol"]
        count = fetch_paralog_count(eid)
        print(f"  [{i+1}/{len(gene_df)}] {sym}: {count} paralogs")
        records.append({"symbol": sym, "ensembl_gene_id": eid, "paralog_count_ensembl": count})
        time.sleep(0.15)  # Respect Ensembl rate limits

    df = pd.DataFrame(records)
    cache.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache, sep="\t", index=False)
    print(f"Saved paralog counts to {cache}")
    return df


# ---------------------------------------------------------------------------
# Build paralog family size from architecture table (within-dataset proxy)
# ---------------------------------------------------------------------------

def build_within_dataset_paralog_size(arch: pd.DataFrame) -> pd.DataFrame:
    """Count how many genes in the 101-gene set share each paralog family label."""
    family_size = (
        arch[arch["has_paralog_family"] == "yes"]
        .groupby("paralog_family_name")["symbol"]
        .count()
        .reset_index()
        .rename(columns={"symbol": "family_size_in_dataset"})
    )
    arch2 = arch[["symbol", "has_paralog_family", "paralog_family_name"]].merge(
        family_size, on="paralog_family_name", how="left"
    )
    arch2["family_size_in_dataset"] = arch2["family_size_in_dataset"].fillna(1).astype(int)
    return arch2[["symbol", "has_paralog_family", "paralog_family_name", "family_size_in_dataset"]]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    for path in [COVAR_OUT, REG_OUT, SUM_OUT]:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    # Load base tables
    gene_table = pd.read_csv(GENE_TABLE, sep="\t")
    arch = pd.read_csv(ARCH_TABLE, sep="\t")
    constraint = pd.read_csv(CONSTRAINT_TABLE, sep="\t")

    # Gene length from coordinates
    gene_table["gene_length_bp"] = (
        gene_table["grch38_end"].astype(float) - gene_table["grch38_start"].astype(float)
    ).abs()

    # --- Covariate 1: expression breadth ---
    symbols = gene_table["symbol"].tolist()
    try:
        expr_breadth = fetch_hpa_expression_breadth(symbols, HPA_CACHE)
    except Exception as exc:
        print(f"WARNING: HPA fetch failed ({exc}). Using NA for expression breadth.")
        expr_breadth = pd.DataFrame({"symbol": symbols, "n_tissues_expressed": [np.nan] * len(symbols)})

    # --- Covariate 2: Ensembl genome-wide paralog count ---
    paralog_df = fetch_all_paralog_counts(gene_table[["symbol", "ensembl_gene_id"]], PARALOG_CACHE)

    # --- Covariate 3: within-dataset paralog family size ---
    family_size_df = build_within_dataset_paralog_size(arch)

    # --- Join everything ---
    df = (
        constraint[
            ["symbol", "ensembl_gene_id", "primary_region", "analysis_group",
             "include_primary", "loeuf", "mis_z", "cds_length",
             "pLI", "oe_lof", "oe_mis"]
        ]
        .merge(gene_table[["symbol", "gene_length_bp"]], on="symbol", how="left")
        .merge(expr_breadth, on="symbol", how="left")
        .merge(paralog_df[["symbol", "paralog_count_ensembl"]], on="symbol", how="left")
        .merge(family_size_df[["symbol", "has_paralog_family", "family_size_in_dataset"]], on="symbol", how="left")
    )

    df["paralog_count_ensembl"] = pd.to_numeric(df["paralog_count_ensembl"], errors="coerce")
    df["log_gene_length"] = np.log10(df["gene_length_bp"].clip(lower=1))
    df["log_cds_length"] = np.log10(df["cds_length"].clip(lower=1))
    df["log_paralog_count"] = np.log10(df["paralog_count_ensembl"].fillna(0).clip(lower=1))

    df.to_csv(COVAR_OUT, sep="\t", index=False)
    print(f"\nCovariate table: {COVAR_OUT}  ({len(df)} genes × {df.shape[1]} cols)")
    print(df[["symbol", "analysis_group", "loeuf", "n_tissues_expressed",
              "paralog_count_ensembl", "family_size_in_dataset", "gene_length_bp"]].head(10).to_string())

    # --- Regression analysis ---
    primary = df[df["include_primary"] == "yes"].copy()
    primary = primary[primary["analysis_group"].isin(["upstream_core", "downstream_diversification"])].copy()
    primary_complete = primary.dropna(subset=["loeuf", "n_tissues_expressed",
                                               "paralog_count_ensembl", "log_gene_length"])

    print(f"\nPrimary contrast: {len(primary_complete)} genes with complete data "
          f"({primary_complete['analysis_group'].value_counts().to_dict()})")

    results_lines = []

    def log_section(title: str) -> None:
        results_lines.append(f"\n{'='*70}")
        results_lines.append(title)
        results_lines.append('='*70)

    # --- 1. Raw group comparison (baseline) ---
    log_section("1. RAW GROUP COMPARISON (no covariates)")
    up = primary_complete[primary_complete["analysis_group"] == "upstream_core"]["loeuf"]
    dn = primary_complete[primary_complete["analysis_group"] == "downstream_diversification"]["loeuf"]
    stat, p = mannwhitneyu(up, dn, alternative="two-sided")
    rbc = 1 - 2 * stat / (len(up) * len(dn))
    results_lines += [
        f"  Upstream (n={len(up)}): median LOEUF = {up.median():.4f}  IQR [{up.quantile(.25):.3f}, {up.quantile(.75):.3f}]",
        f"  Downstream (n={len(dn)}): median LOEUF = {dn.median():.4f}  IQR [{dn.quantile(.25):.3f}, {dn.quantile(.75):.3f}]",
        f"  Mann-Whitney U = {stat:.1f}, p = {p:.4f}, rank-biserial r = {rbc:.3f}",
        f"  Direction: {'Upstream HIGHER (less constrained) — opposite of naive prediction' if up.median() > dn.median() else 'Upstream LOWER (more constrained) — consistent with naive prediction'}",
    ]

    # --- 2. Covariate summaries by group ---
    log_section("2. COVARIATE SUMMARY BY GROUP")
    covars = ["n_tissues_expressed", "paralog_count_ensembl", "family_size_in_dataset",
              "gene_length_bp", "cds_length"]
    summary_rows = []
    for grp, grpdf in primary_complete.groupby("analysis_group"):
        row = {"analysis_group": grp, "n": len(grpdf)}
        for c in covars:
            vals = grpdf[c].dropna()
            row[f"{c}_median"] = round(float(vals.median()), 2) if len(vals) else np.nan
        summary_rows.append(row)
        lines = [f"  {grp} (n={len(grpdf)}):"]
        for c in covars:
            vals = grpdf[c].dropna()
            if len(vals):
                lines.append(f"    {c}: median={vals.median():.2f}, IQR=[{vals.quantile(.25):.2f},{vals.quantile(.75):.2f}]")
        results_lines += lines
    pd.DataFrame(summary_rows).to_csv(SUM_OUT, sep="\t", index=False)

    # Spearman correlations with LOEUF
    log_section("3. SPEARMAN CORRELATIONS WITH LOEUF (primary genes)")
    for c in covars + ["log_paralog_count", "log_gene_length"]:
        vals = primary_complete[["loeuf", c]].dropna()
        if len(vals) > 5:
            rho, pval = spearmanr(vals["loeuf"], vals[c])
            results_lines.append(f"  LOEUF ~ {c}: rho={rho:.3f}, p={pval:.4f}")

    # --- 3. OLS regressions ---
    log_section("4. OLS REGRESSIONS")

    models = {
        "Null (group only)":
            "loeuf ~ C(analysis_group, Treatment('upstream_core'))",
        "Partial (group + log_gene_length)":
            "loeuf ~ C(analysis_group, Treatment('upstream_core')) + log_gene_length",
        "Partial (group + log_paralog_count)":
            "loeuf ~ C(analysis_group, Treatment('upstream_core')) + log_paralog_count",
        "Partial (group + n_tissues_expressed)":
            "loeuf ~ C(analysis_group, Treatment('upstream_core')) + n_tissues_expressed",
        "Full (group + all covariates)":
            "loeuf ~ C(analysis_group, Treatment('upstream_core')) + log_gene_length + log_paralog_count + n_tissues_expressed",
    }

    for name, formula in models.items():
        try:
            fit = smf.ols(formula, data=primary_complete.dropna(
                subset=["loeuf", "log_gene_length", "log_paralog_count", "n_tissues_expressed"]
            )).fit()
            # Extract group coefficient
            coef_col = [c for c in fit.params.index if "downstream" in c]
            coef = fit.params[coef_col[0]] if coef_col else np.nan
            pval_group = fit.pvalues[coef_col[0]] if coef_col else np.nan
            results_lines += [
                f"\n  Model: {name}",
                f"  Formula: {formula}",
                f"  N = {int(fit.nobs)}, R² = {fit.rsquared:.4f}, Adj R² = {fit.rsquared_adj:.4f}",
                f"  Downstream coef = {coef:.4f}, p = {pval_group:.4f}",
                f"  {'*** GROUP SURVIVES COVARIATE CONTROL' if pval_group < 0.05 else '--- Group not significant after covariate control'}",
                fit.summary().as_text(),
            ]
        except Exception as exc:
            results_lines.append(f"\n  Model: {name} — FAILED: {exc}")

    # --- Write output ---
    output_text = "\n".join(results_lines)
    with open(REG_OUT, "w") as f:
        f.write(output_text)
    print(f"\nRegression results: {REG_OUT}")
    # Also print key findings to stdout
    for line in results_lines[:40]:
        print(line)


if __name__ == "__main__":
    main()
