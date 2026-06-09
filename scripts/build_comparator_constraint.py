#!/usr/bin/env python3
"""Join gnomAD constraint metrics to comparator pathway genes (heme, CoQ).

Reuses the same gnomAD v4.1 file as the N-glycosylation constraint analysis
but operates on data/processed/comparator_gene_table.tsv.

Outputs
-------
- data/processed/comparator_constraint_metrics.tsv
- results/tables/comparator_constraint_join_audit.tsv
- results/tables/comparator_constraint_summary.tsv

Usage
-----
    python scripts/build_comparator_constraint.py

Run from the repository root.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


GNOMAD_PATH = "data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv"
GENE_TABLE = "data/processed/comparator_gene_table.tsv"

LOEUF_CONSTRAINED_THRESHOLD = 0.6


def load_gnomad(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", low_memory=False)
    # Keep canonical transcripts only
    canonical = df[df["canonical"].astype(str).str.lower() == "true"].copy()
    # Prefer MANE select when available
    mane = canonical[canonical["mane_select"].astype(str).str.lower() == "true"]
    non_mane = canonical[canonical["mane_select"].astype(str).str.lower() != "true"]
    canonical = pd.concat([mane, non_mane]).drop_duplicates(subset=["gene_id"], keep="first")
    return canonical


def main() -> None:
    genes = pd.read_csv(GENE_TABLE, sep="\t")
    print(f"Comparator genes: {len(genes)}")

    gnomad = load_gnomad(GNOMAD_PATH)
    print(f"gnomAD canonical rows: {len(gnomad)}")

    # Normalise Ensembl IDs (strip version)
    genes["ensembl_gene_id_base"] = genes["ensembl_gene_id"].astype(str).str.split(".").str[0]
    gnomad["gene_id_base"] = gnomad["gene_id"].astype(str).str.split(".").str[0]

    # Detect key columns (gnomAD v4.1 uses dot notation)
    loeuf_col = next((c for c in gnomad.columns if c in ("lof.oe_ci.upper", "loeuf")), None)
    oe_lof_col = next((c for c in gnomad.columns if c in ("lof.oe", "oe_lof")), None)
    mis_z_col = next((c for c in gnomad.columns if c in ("mis.z_score", "mis_z")), None)

    # Find actual column names
    print("Detected columns:")
    for label, col in [("LOEUF", loeuf_col), ("oe_lof", oe_lof_col), ("mis_z", mis_z_col)]:
        print(f"  {label}: {col}")

    # Try joining by Ensembl ID first, then by symbol
    merged = genes.merge(
        gnomad[["gene_id_base", "gene"] + [c for c in [loeuf_col, mis_z_col, oe_lof_col] if c]],
        left_on="ensembl_gene_id_base",
        right_on="gene_id_base",
        how="left",
    )

    # For unmatched, try symbol join
    unmatched = merged[merged["gene_id_base"].isna()]["symbol"].tolist()
    if unmatched:
        sym_join = genes[genes["symbol"].isin(unmatched)].merge(
            gnomad[["gene"] + [c for c in [loeuf_col, mis_z_col, oe_lof_col] if c]],
            left_on="symbol", right_on="gene", how="left",
        )
        for _, row in sym_join.iterrows():
            idx = merged.index[merged["symbol"] == row["symbol"]]
            for col in [loeuf_col, mis_z_col, oe_lof_col]:
                if col and col in row:
                    merged.loc[idx, col] = row[col]

    # Rename for clarity
    rename = {}
    if loeuf_col:
        rename[loeuf_col] = "loeuf"
    if mis_z_col:
        rename[mis_z_col] = "missense_z"
    if oe_lof_col and oe_lof_col != loeuf_col:
        rename[oe_lof_col] = "oe_lof"
    merged = merged.rename(columns=rename)

    if "loeuf" in merged.columns:
        merged["loeuf_constrained"] = merged["loeuf"].apply(
            lambda x: "yes" if pd.notna(x) and float(x) < LOEUF_CONSTRAINED_THRESHOLD else (
                "no" if pd.notna(x) else None
            )
        )

    # Join status
    has_loeuf = merged["loeuf"].notna() if "loeuf" in merged.columns else pd.Series(False, index=merged.index)
    merged["constraint_join_status"] = has_loeuf.map({True: "matched", False: "unmatched"})

    # Write outputs
    out_cols = ["symbol", "ensembl_gene_id", "pathway_name", "primary_region",
                "pathway_step_order", "pathway_step", "constraint_join_status",
                "loeuf", "missense_z", "loeuf_constrained"]
    out_cols = [c for c in out_cols if c in merged.columns]
    out = merged[out_cols].copy()

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    Path("results/tables").mkdir(parents=True, exist_ok=True)

    out.to_csv("data/processed/comparator_constraint_metrics.tsv", sep="\t", index=False)

    # Audit
    audit_cols = ["symbol", "ensembl_gene_id", "pathway_name", "primary_region",
                  "constraint_join_status", "loeuf", "missense_z"]
    audit_cols = [c for c in audit_cols if c in merged.columns]
    merged[audit_cols].to_csv("results/tables/comparator_constraint_join_audit.tsv",
                              sep="\t", index=False)

    # Summary by pathway and region
    def iqr(s):
        return float(s.quantile(0.75) - s.quantile(0.25))

    summary_rows = []
    for (pathway, region), grp in out.groupby(["pathway_name", "primary_region"]):
        row = {"pathway_name": pathway, "primary_region": region,
               "n_genes": len(grp)}
        for col in ["loeuf", "missense_z"]:
            if col in grp.columns:
                vals = grp[col].dropna()
                row[f"n_{col}"] = len(vals)
                row[f"median_{col}"] = round(vals.median(), 4) if len(vals) else None
                row[f"iqr_{col}"] = round(iqr(vals), 4) if len(vals) > 1 else None
        if "loeuf_constrained" in grp.columns:
            row["n_loeuf_constrained"] = int((grp["loeuf_constrained"] == "yes").sum())
        summary_rows.append(row)

    summary = pd.DataFrame(summary_rows)
    summary.to_csv("results/tables/comparator_constraint_summary.tsv", sep="\t", index=False)

    # Print summary
    n_matched = int((merged["constraint_join_status"] == "matched").sum())
    print(f"\nJoined: {n_matched}/{len(merged)} genes with constraint data")
    print("\nSummary by pathway and region:")
    print(summary.to_string(index=False))

    unmatched_genes = merged[merged["constraint_join_status"] == "unmatched"]["symbol"].tolist()
    if unmatched_genes:
        print(f"\nUnmatched genes: {unmatched_genes}")

    print(f"\nWrote data/processed/comparator_constraint_metrics.tsv")
    print(f"Wrote results/tables/comparator_constraint_join_audit.tsv")
    print(f"Wrote results/tables/comparator_constraint_summary.tsv")


if __name__ == "__main__":
    main()
