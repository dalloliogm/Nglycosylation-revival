#!/usr/bin/env python3
"""Compute per-gene Weir-Cockerham FST and PBS for N-glycosylation pathway genes.

Uses scikit-allel for FST computation from the per-gene VCF slices fetched by
scripts/fetch_popgen_data.py. No external tools (vcftools, plink) required.

Statistics computed
-------------------
- Pairwise Weir-Cockerham FST for all 10 superpopulation pairs
- PBS (Population Branch Statistic; Yi et al. 2010) for key population trios
- Per-gene summary: mean FST, max FST, n SNPs, fraction FST > 0.3

Outputs
-------
- data/processed/nglyco_fst_per_gene.tsv
- data/processed/nglyco_pbs_per_gene.tsv
- results/tables/popgen_fst_summary.tsv
- results/tables/popgen_join_audit.tsv

Usage
-----
    python scripts/compute_fst_pbs.py [--vcf-dir data/raw/popgen/vcf_slices]

Run from the repository root after fetch_popgen_data.py has completed.
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import math
from pathlib import Path
from typing import Any

import allel
import numpy as np
import pandas as pd

SUPERPOPULATIONS = ["AFR", "AMR", "EAS", "EUR", "SAS"]

# PBS trios: (focal_pop, pop_B, pop_C) — PBS is computed for the focal pop
PBS_TRIOS = [
    ("AFR", "EUR", "EAS"),
    ("EUR", "AFR", "EAS"),
    ("EAS", "AFR", "EUR"),
    ("SAS", "AFR", "EUR"),
    ("AMR", "AFR", "EUR"),
]

# Variant filters
MIN_MAF = 0.01        # global MAF filter
MAX_MISSING = 0.05    # max missingness fraction


# ---------------------------------------------------------------------------
# Load population panel
# ---------------------------------------------------------------------------

def load_panel(panel_path: str) -> dict[str, list[str]]:
    """Return dict mapping superpopulation → list of sample IDs."""
    panel = pd.read_csv(panel_path, sep="\t")
    # columns: sample, pop, super_pop, gender
    sup_col = next(c for c in panel.columns if "super" in c.lower())
    sam_col = panel.columns[0]
    result: dict[str, list[str]] = {}
    for sup, grp in panel.groupby(sup_col):
        result[str(sup)] = grp[sam_col].tolist()
    return result


# ---------------------------------------------------------------------------
# Parse VCF and extract genotype array
# ---------------------------------------------------------------------------

def parse_vcf_gz(vcf_path: Path) -> tuple[list[str], allel.GenotypeArray, np.ndarray] | None:
    """Parse a gzipped VCF and return (samples, genotypes, positions).

    Applies biallelic SNP filter. Returns None on failure or empty.
    """
    try:
        callset = allel.read_vcf(
            str(vcf_path),
            fields=["samples", "calldata/GT", "variants/POS",
                    "variants/REF", "variants/ALT", "variants/FILTER_PASS",
                    "variants/is_snp"],
            alt_number=1,
        )
    except Exception as exc:
        print(f"    VCF parse error: {exc}")
        return None

    if callset is None:
        return None

    gt_raw = callset.get("calldata/GT")
    if gt_raw is None or gt_raw.shape[0] == 0:
        return None

    samples = list(callset["samples"])
    gt = allel.GenotypeArray(gt_raw)
    pos = callset["variants/POS"]
    is_snp = callset.get("variants/is_snp", np.ones(gt.shape[0], dtype=bool))
    pass_filter = callset.get("variants/FILTER_PASS", np.ones(gt.shape[0], dtype=bool))

    # Keep biallelic SNPs that pass filter
    mask = is_snp & pass_filter
    gt = gt[mask]
    pos = pos[mask]

    if gt.shape[0] == 0:
        return None

    return samples, gt, pos


# ---------------------------------------------------------------------------
# FST computation
# ---------------------------------------------------------------------------

def wc_fst_per_variant(
    gt: allel.GenotypeArray,
    subpops: list[list[int]],
) -> np.ndarray:
    """Weir-Cockerham FST per variant across subpopulation indices."""
    ac = gt.count_alleles_subpops(
        {i: sp for i, sp in enumerate(subpops)}
    )
    ac_list = [ac[i] for i in range(len(subpops))]
    fst, _ = allel.weir_cockerham_fst(gt, subpops, max_allele=1)
    return fst


def pairwise_fst_summary(
    gt: allel.GenotypeArray,
    samples: list[str],
    panel: dict[str, list[str]],
    min_maf: float = MIN_MAF,
) -> dict[str, Any]:
    """Compute pairwise FST for all superpopulation pairs for one gene."""
    # Build sample index lists per superpopulation
    sample_index = {s: i for i, s in enumerate(samples)}
    pop_indices: dict[str, list[int]] = {}
    for sup, sids in panel.items():
        idxs = [sample_index[s] for s in sids if s in sample_index]
        if idxs:
            pop_indices[sup] = idxs

    present_pops = sorted(pop_indices.keys())
    if len(present_pops) < 2:
        return {}

    # Global MAF filter
    ac_all = gt.count_alleles()
    n_called = ac_all.sum(axis=1)
    af = ac_all[:, 1] / np.where(n_called > 0, n_called, 1)
    maf = np.minimum(af, 1 - af)
    missingness = (gt.is_missing().sum(axis=1) / gt.shape[1])
    keep = (maf >= min_maf) & (missingness <= MAX_MISSING)
    gt_filt = gt[keep]

    if gt_filt.shape[0] < 5:
        return {"n_snps_used": int(keep.sum()), "note": "too_few_snps"}

    result: dict[str, Any] = {"n_snps_used": int(keep.sum())}

    for pop_a, pop_b in itertools.combinations(present_pops, 2):
        pair_key = f"{pop_a}_{pop_b}"
        idxs_a = pop_indices[pop_a]
        idxs_b = pop_indices[pop_b]
        gt_pair = gt_filt.take(idxs_a + idxs_b, axis=1)
        subpops = [list(range(len(idxs_a))),
                   list(range(len(idxs_a), len(idxs_a) + len(idxs_b)))]
        try:
            # weir_cockerham_fst returns (a, b, c) components;
            # per-variant FST = a / (a + b + c)
            a, b, c = allel.weir_cockerham_fst(gt_pair, subpops, max_allele=1)
            denom = a + b + c
            with np.errstate(invalid="ignore", divide="ignore"):
                fst_vals = np.where(denom > 0, a / denom, np.nan)
            # Clip to valid FST range; values outside [0,1] are numerical artefacts
            fst_vals = np.clip(fst_vals, 0.0, 1.0)
            valid = fst_vals[np.isfinite(fst_vals)]
            if len(valid) == 0:
                continue
            result[f"fst_mean_{pair_key}"] = round(float(np.mean(valid)), 5)
            result[f"fst_max_{pair_key}"] = round(float(np.max(valid)), 5)
            result[f"fst_gt0.3_frac_{pair_key}"] = round(
                float((valid > 0.3).sum() / len(valid)), 5
            )
        except Exception as exc:
            result[f"fst_error_{pair_key}"] = str(exc)[:80]

    return result


# ---------------------------------------------------------------------------
# PBS
# ---------------------------------------------------------------------------

def compute_pbs(fst_result: dict, trios: list[tuple]) -> dict[str, float]:
    """Compute PBS from pairwise FST values for specified trios.

    PBS_focal = ( T(focal,B) + T(focal,C) - T(B,C) ) / 2
    where T(A,B) = -log(1 - FST(A,B))
    """
    def t(pop_a: str, pop_b: str) -> float | None:
        key = f"fst_mean_{pop_a}_{pop_b}"
        alt_key = f"fst_mean_{pop_b}_{pop_a}"
        fst = fst_result.get(key, fst_result.get(alt_key))
        if fst is None or not math.isfinite(fst):
            return None
        fst_clipped = min(max(fst, 0.0), 0.9999)
        return -math.log(1 - fst_clipped)

    pbs: dict[str, float] = {}
    for focal, pop_b, pop_c in trios:
        t_fb = t(focal, pop_b)
        t_fc = t(focal, pop_c)
        t_bc = t(pop_b, pop_c)
        if t_fb is None or t_fc is None or t_bc is None:
            continue
        pbs_val = (t_fb + t_fc - t_bc) / 2.0
        trio_key = f"pbs_{focal}_vs_{pop_b}_{pop_c}"
        pbs[trio_key] = round(pbs_val, 5)
    return pbs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gene-table",
                        default="data/processed/nglyco_gene_table.tsv")
    parser.add_argument("--hg19-table",
                        default="data/processed/nglyco_gene_table_hg19.tsv")
    parser.add_argument("--vcf-dir",
                        default="data/raw/popgen/vcf_slices")
    parser.add_argument("--panel",
                        default="data/raw/popgen/1000g_phase3_panel.tsv")
    parser.add_argument("--fst-out",
                        default="data/processed/nglyco_fst_per_gene.tsv")
    parser.add_argument("--pbs-out",
                        default="data/processed/nglyco_pbs_per_gene.tsv")
    parser.add_argument("--summary-out",
                        default="results/tables/popgen_fst_summary.tsv")
    parser.add_argument("--audit-out",
                        default="results/tables/popgen_join_audit.tsv")
    args = parser.parse_args()

    gene_table = pd.read_csv(args.gene_table, sep="\t")
    hg19_table = pd.read_csv(args.hg19_table, sep="\t")
    manifest = pd.read_csv(
        Path(args.vcf_dir) / "vcf_manifest.tsv", sep="\t"
    )
    panel = load_panel(args.panel)

    print(f"Genes: {len(gene_table)}")
    print(f"Populations: {sorted(panel.keys())}")
    print(f"VCF slices available: {(manifest['vcf_status'] == 'ok').sum()}")

    fst_records = []
    pbs_records = []
    audit_records = []

    for _, gene_row in gene_table.iterrows():
        symbol = gene_row["symbol"]
        mrow = manifest[manifest["symbol"] == symbol]

        if mrow.empty or mrow.iloc[0]["vcf_status"] != "ok":
            status = mrow.iloc[0]["vcf_status"] if not mrow.empty else "not_in_manifest"
            print(f"  [{symbol}] Skipping: {status}")
            audit_records.append({"symbol": symbol, "status": status,
                                  "n_snps_used": 0})
            continue

        vcf_path = Path(mrow.iloc[0]["vcf_path"])
        print(f"  [{symbol}] Parsing {vcf_path.name}...")

        parsed = parse_vcf_gz(vcf_path)
        if parsed is None:
            print(f"    Empty or unreadable VCF")
            audit_records.append({"symbol": symbol, "status": "parse_failed",
                                  "n_snps_used": 0})
            continue

        samples, gt, pos = parsed
        fst_res = pairwise_fst_summary(gt, samples, panel)
        pbs_res = compute_pbs(fst_res, PBS_TRIOS)

        n_snps = fst_res.get("n_snps_used", 0)
        print(f"    {n_snps} SNPs, {len(pbs_res)} PBS values")

        fst_row = {"symbol": symbol, **fst_res}
        pbs_row = {"symbol": symbol, **pbs_res}
        fst_records.append(fst_row)
        pbs_records.append(pbs_row)
        audit_records.append({"symbol": symbol, "status": "ok",
                              "n_snps_used": n_snps})

    # Merge with gene table metadata
    meta_cols = ["symbol", "ensembl_gene_id", "primary_region", "analysis_group",
                 "include_primary", "include_sensitivity"]
    meta = gene_table[meta_cols]

    fst_df = pd.DataFrame(fst_records)
    pbs_df = pd.DataFrame(pbs_records)
    audit_df = pd.DataFrame(audit_records)

    fst_out = meta.merge(fst_df, on="symbol", how="left")
    pbs_out = meta.merge(pbs_df, on="symbol", how="left")
    audit_out = meta.merge(audit_df, on="symbol", how="left")

    for path in [args.fst_out, args.pbs_out, args.summary_out, args.audit_out]:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    fst_out.to_csv(args.fst_out, sep="\t", index=False)
    pbs_out.to_csv(args.pbs_out, sep="\t", index=False)
    audit_out.to_csv(args.audit_out, sep="\t", index=False)

    # Region-level FST summary
    primary = fst_out[fst_out["include_primary"] == "yes"]
    fst_cols = [c for c in fst_out.columns if c.startswith("fst_mean_")]
    if fst_cols:
        summary_rows = []
        for grp_name, grp in primary.groupby("analysis_group"):
            row = {"analysis_group": grp_name, "n_genes": len(grp)}
            for col in fst_cols:
                vals = grp[col].dropna()
                if len(vals):
                    row[f"median_{col}"] = round(float(vals.median()), 5)
                    row[f"max_{col}"] = round(float(vals.max()), 5)
            summary_rows.append(row)
        pd.DataFrame(summary_rows).to_csv(args.summary_out, sep="\t", index=False)

    print(f"\nWrote {args.fst_out}")
    print(f"Wrote {args.pbs_out}")
    print(f"Wrote {args.summary_out}")
    print(f"Wrote {args.audit_out}")
    n_ok = int((audit_df["status"] == "ok").sum())
    print(f"\nSuccessfully processed: {n_ok}/{len(audit_df)} genes")


if __name__ == "__main__":
    main()
