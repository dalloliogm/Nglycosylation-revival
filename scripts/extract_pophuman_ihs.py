#!/usr/bin/env python3
"""Download PopHuman iHS BigWig tracks and extract per-gene windowed summaries.

PopHuman provides pre-computed iHS scores (selscan) for all 26 1000 Genomes
Phase 3 populations in 10 kb windows at hg19. Files are ~1.6 MB each.

This script:
1. Downloads iHS BigWig files for all 26 populations (~42 MB total).
2. For each gene (± flank, hg19 coords), extracts the 10 kb windows that
   overlap the gene body and records: mean |iHS|, max |iHS|, fraction of
   windows with |iHS| > 2 (a conventional soft threshold).
3. Summarises per superpopulation by taking the max across constituent
   populations (reflects the strongest signal in any population of that group).

Outputs
-------
- data/raw/popgen/pophuman_ihs/iHS_{POP}_10kb.bw  (downloaded, one per population)
- data/processed/nglyco_ihs_per_gene.tsv           (per-gene per-population summary)
- results/tables/popgen_ihs_summary.tsv            (region-level group summary)

Usage
-----
    python scripts/extract_pophuman_ihs.py [--skip-download]

Requires: pyBigWig (pip install pyBigWig)
Run from repository root.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import numpy as np
import pandas as pd

POPHUMAN_BASE = "http://pophuman.uab.cat/files/wig"
BW_PATTERN = "{base}/iHS_{pop}_10kb.bw"

POPULATIONS = [
    # AFR
    "YRI", "ESN", "GWD", "LWK", "MSL", "ACB", "ASW",
    # AMR
    "CLM", "MXL", "PEL", "PUR",
    # EAS
    "CHB", "CDX", "CHS", "JPT", "KHV",
    # EUR
    "CEU", "GBR", "FIN", "IBS", "TSI",
    # SAS
    "BEB", "GIH", "ITU", "PJL", "STU",
]

SUPERPOP_MAP = {
    "AFR": ["YRI", "ESN", "GWD", "LWK", "MSL", "ACB", "ASW"],
    "AMR": ["CLM", "MXL", "PEL", "PUR"],
    "EAS": ["CHB", "CDX", "CHS", "JPT", "KHV"],
    "EUR": ["CEU", "GBR", "FIN", "IBS", "TSI"],
    "SAS": ["BEB", "GIH", "ITU", "PJL", "STU"],
}

IHS_THRESHOLD = 2.0   # |iHS| > 2 considered a soft positive-selection candidate


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def download_bw(pop: str, out_dir: Path, retries: int = 3) -> Path | None:
    dest = out_dir / f"iHS_{pop}_10kb.bw"
    if dest.exists() and dest.stat().st_size > 100_000:
        return dest
    url = BW_PATTERN.format(base=POPHUMAN_BASE, pop=pop)
    for attempt in range(retries):
        try:
            print(f"  Downloading {pop}... ", end="", flush=True)
            req = Request(url)
            with urlopen(req, timeout=60) as resp, open(dest, "wb") as fh:
                while True:
                    chunk = resp.read(1024 * 512)
                    if not chunk:
                        break
                    fh.write(chunk)
            print(f"{dest.stat().st_size // 1024} KB")
            return dest
        except HTTPError as exc:
            print(f"HTTP {exc.code}")
            if attempt < retries - 1:
                time.sleep(5)
        except Exception as exc:
            print(f"Error: {exc}")
            if attempt < retries - 1:
                time.sleep(5)
    return None


# ---------------------------------------------------------------------------
# Extract iHS for one gene from one BigWig
# ---------------------------------------------------------------------------

def extract_gene_ihs(
    bw,           # open pyBigWig object
    chrom: str,
    start: int,
    end: int,
) -> dict:
    """Return iHS summary stats for a genomic interval from an open BigWig."""
    result = {
        "mean_abs_ihs": None, "max_abs_ihs": None,
        "frac_gt_threshold": None, "n_windows": 0,
    }
    chrom_str = str(chrom) if str(chrom).startswith("chr") else "chr" + str(chrom)
    try:
        vals = bw.values(chrom_str, int(start), int(end), numpy=True)
    except Exception:
        return result
    if vals is None or len(vals) == 0:
        return result
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return result
    abs_vals = np.abs(vals)
    result["mean_abs_ihs"] = round(float(np.mean(abs_vals)), 4)
    result["max_abs_ihs"] = round(float(np.max(abs_vals)), 4)
    result["frac_gt_threshold"] = round(float((abs_vals > IHS_THRESHOLD).mean()), 4)
    result["n_windows"] = int(len(abs_vals))
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hg19-table",
                        default="data/processed/nglyco_gene_table_hg19.tsv")
    parser.add_argument("--gene-table",
                        default="data/processed/nglyco_gene_table.tsv")
    parser.add_argument("--bw-dir",
                        default="data/raw/popgen/pophuman_ihs")
    parser.add_argument("--ihs-out",
                        default="data/processed/nglyco_ihs_per_gene.tsv")
    parser.add_argument("--summary-out",
                        default="results/tables/popgen_ihs_summary.tsv")
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    try:
        import pyBigWig  # noqa
    except ImportError:
        print("ERROR: pyBigWig not installed. Run: uv add pyBigWig")
        raise SystemExit(1)
    import pyBigWig

    bw_dir = Path(args.bw_dir)
    bw_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Download BigWig files
    if not args.skip_download:
        print(f"--- Downloading {len(POPULATIONS)} iHS BigWig files ---")
        for pop in POPULATIONS:
            download_bw(pop, bw_dir)
    else:
        print("Skipping download (--skip-download).")

    # Step 2: Load gene coordinates (hg19)
    hg19 = pd.read_csv(args.hg19_table, sep="\t")
    gene_meta = pd.read_csv(args.gene_table, sep="\t")[
        ["symbol", "ensembl_gene_id", "primary_region", "analysis_group",
         "include_primary", "include_sensitivity"]
    ]

    # Step 3: Extract iHS per gene per population
    print(f"\n--- Extracting iHS for {len(hg19)} genes across {len(POPULATIONS)} populations ---")
    records = []

    for pop in POPULATIONS:
        bw_path = bw_dir / f"iHS_{pop}_10kb.bw"
        if not bw_path.exists():
            print(f"  [{pop}] BigWig not found, skipping")
            continue

        bw = pyBigWig.open(str(bw_path))
        pop_records = []
        for _, row in hg19.iterrows():
            if not row.get("grch37_chr"):
                pop_records.append({"symbol": row["symbol"], "population": pop,
                                    "mean_abs_ihs": None, "max_abs_ihs": None,
                                    "frac_gt_threshold": None, "n_windows": 0})
                continue
            r = extract_gene_ihs(
                bw, row["grch37_chr"],
                int(row["fetch_start"]), int(row["fetch_end"])
            )
            r["symbol"] = row["symbol"]
            r["population"] = pop
            pop_records.append(r)
        bw.close()

        n_ok = sum(1 for r in pop_records if r["mean_abs_ihs"] is not None)
        print(f"  [{pop}] {n_ok}/{len(pop_records)} genes with iHS data")
        records.extend(pop_records)

    ihs_long = pd.DataFrame(records)

    # Step 4: Pivot to wide format (one row per gene, one column set per population)
    ihs_wide_parts = []
    for pop in POPULATIONS:
        sub = ihs_long[ihs_long["population"] == pop][
            ["symbol", "mean_abs_ihs", "max_abs_ihs", "frac_gt_threshold", "n_windows"]
        ].rename(columns={
            "mean_abs_ihs": f"ihs_mean_{pop}",
            "max_abs_ihs": f"ihs_max_{pop}",
            "frac_gt_threshold": f"ihs_frac_gt2_{pop}",
            "n_windows": f"ihs_nwin_{pop}",
        })
        ihs_wide_parts.append(sub)

    ihs_wide = ihs_wide_parts[0]
    for part in ihs_wide_parts[1:]:
        ihs_wide = ihs_wide.merge(part, on="symbol", how="outer")

    # Add superpopulation max columns
    for sup, pops in SUPERPOP_MAP.items():
        max_cols = [f"ihs_max_{p}" for p in pops if f"ihs_max_{p}" in ihs_wide.columns]
        if max_cols:
            ihs_wide[f"ihs_max_{sup}"] = ihs_wide[max_cols].max(axis=1)
            ihs_wide[f"ihs_mean_{sup}"] = ihs_wide[
                [f"ihs_mean_{p}" for p in pops if f"ihs_mean_{p}" in ihs_wide.columns]
            ].mean(axis=1).round(4)

    out = gene_meta.merge(ihs_wide, on="symbol", how="left")

    for path in [args.ihs_out, args.summary_out]:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.ihs_out, sep="\t", index=False)

    # Step 5: Region-level summary
    primary = out[out["include_primary"] == "yes"]
    sup_max_cols = [f"ihs_max_{s}" for s in SUPERPOP_MAP if f"ihs_max_{s}" in out.columns]
    summary_rows = []
    for grp_name, grp in primary.groupby("analysis_group"):
        row = {"analysis_group": grp_name, "n_genes": len(grp)}
        for col in sup_max_cols:
            vals = grp[col].dropna()
            if len(vals):
                row[f"median_{col}"] = round(float(vals.median()), 4)
                row[f"max_{col}"] = round(float(vals.max()), 4)
        summary_rows.append(row)
    pd.DataFrame(summary_rows).to_csv(args.summary_out, sep="\t", index=False)

    print(f"\nWrote {args.ihs_out}  ({len(out)} genes × {len(out.columns)} cols)")
    print(f"Wrote {args.summary_out}")


if __name__ == "__main__":
    main()
