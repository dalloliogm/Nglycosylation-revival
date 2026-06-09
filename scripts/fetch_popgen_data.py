#!/usr/bin/env python3
"""Fetch population-genetics data for N-glycosylation pathway genes.

Step 1: Liftover gene coordinates from GRCh38 to GRCh37 (hg19) using the
        Ensembl REST API liftover endpoint.
Step 2: Download the 1000G population panel file.
Step 3: Fetch targeted VCF slices from the 1000 Genomes Phase 3 FTP using
        pysam (which bundles htslib/tabix — no separate tabix binary needed).

This script prepares the data needed for FST/PBS computation
(scripts/compute_fst_pbs.py) and iHS extraction (scripts/extract_pophuman_ihs.py).

Usage
-----
    python scripts/fetch_popgen_data.py [--flank 10000] [--skip-vcf]
    python scripts/fetch_popgen_data.py --skip-liftover  # if hg19 table exists

Requirements
------------
- pysam (pip install pysam — bundles htslib)
- Network access to rest.ensembl.org and ftp.1000genomes.ebi.ac.uk

Run from the repository root.
"""

from __future__ import annotations

import argparse
import gzip
import json
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pandas as pd

ENSEMBL_REST = "https://rest.ensembl.org"
KG_FTP_BASE = "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502"
KG_VCF_PATTERN = (
    "{base}/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5b"
    ".20130502.genotypes.vcf.gz"
)
KG_PANEL_URL = f"{KG_FTP_BASE}/integrated_call_samples_v3.20130502.ALL.panel"

SUPERPOPULATIONS = ["AFR", "AMR", "EAS", "EUR", "SAS"]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _get_json(url: str, timeout: int = 30, retries: int = 3) -> Any:
    for attempt in range(retries):
        try:
            req = Request(url, headers={"Content-Type": "application/json"})
            with urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except HTTPError as exc:
            if exc.code == 429:
                time.sleep(10 * (attempt + 1))
            elif exc.code in {500, 502, 503, 504} and attempt < retries - 1:
                time.sleep(5)
            else:
                raise
        except Exception:
            if attempt < retries - 1:
                time.sleep(5)
            else:
                raise
    raise RuntimeError(f"Failed: {url}")


def _download(url: str, dest: Path, timeout: int = 120) -> None:
    req = Request(url)
    with urlopen(req, timeout=timeout) as resp, open(dest, "wb") as fh:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            fh.write(chunk)


# ---------------------------------------------------------------------------
# Step 1: GRCh38 → GRCh37 liftover via Ensembl REST
# ---------------------------------------------------------------------------

def liftover_one(chrom: str, start: int, end: int, symbol: str) -> dict | None:
    chrom_str = str(chrom)
    region = f"{chrom_str}:{start}..{end}"
    url = (
        f"{ENSEMBL_REST}/map/human/GRCh38/{region}/GRCh37"
        f"?content-type=application/json"
    )
    try:
        data = _get_json(url, timeout=20)
        mappings = data.get("mappings", [])
        if not mappings:
            print(f"  [{symbol}] No liftover result")
            return None
        m = mappings[0]["mapped"]
        return {
            "symbol": symbol,
            "grch37_chr": str(m["seq_region_name"]),
            "grch37_start": int(m["start"]),
            "grch37_end": int(m["end"]),
            "grch37_strand": m.get("strand", 1),
        }
    except Exception as exc:
        print(f"  [{symbol}] Liftover error: {exc}")
        return None


def liftover_all(gene_table: pd.DataFrame, flank: int) -> pd.DataFrame:
    records = []
    n = len(gene_table)
    for i, row in enumerate(gene_table.itertuples(), start=1):
        print(f"  Liftover [{i}/{n}] {row.symbol}")
        result = liftover_one(
            row.grch38_chr,
            max(1, int(row.grch38_start) - flank),
            int(row.grch38_end) + flank,
            row.symbol,
        )
        if result:
            result["ensembl_gene_id"] = row.ensembl_gene_id
            result["grch38_chr"] = str(row.grch38_chr)
            result["grch38_start"] = int(row.grch38_start)
            result["grch38_end"] = int(row.grch38_end)
            result["flank_bp"] = flank
            result["fetch_start"] = max(1, int(result["grch37_start"]))
            result["fetch_end"] = int(result["grch37_end"])
        else:
            result = {
                "symbol": row.symbol, "ensembl_gene_id": row.ensembl_gene_id,
                "grch38_chr": str(row.grch38_chr),
                "grch38_start": int(row.grch38_start),
                "grch38_end": int(row.grch38_end),
                "grch37_chr": None, "grch37_start": None,
                "grch37_end": None, "grch37_strand": None,
                "flank_bp": flank, "fetch_start": None, "fetch_end": None,
            }
        records.append(result)
        time.sleep(0.1)
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Step 2: 1000G panel
# ---------------------------------------------------------------------------

def fetch_panel(out_dir: Path) -> Path:
    dest = out_dir / "1000g_phase3_panel.tsv"
    if dest.exists():
        print(f"  Panel already exists: {dest}")
        return dest
    print(f"  Downloading 1000G panel → {dest}")
    _download(KG_PANEL_URL, dest)
    print(f"  Done ({dest.stat().st_size // 1024} KB)")
    return dest


# ---------------------------------------------------------------------------
# Step 3: Per-gene VCF slices via pysam (htslib remote fetch)
# ---------------------------------------------------------------------------

def fetch_gene_vcf_pysam(
    symbol: str, chrom: str, start: int, end: int, out_dir: Path
) -> Path | None:
    """Fetch a VCF slice using pysam's remote tabix support.

    pysam can open a remote tabix-indexed VCF over HTTPS and iterate over
    records in a region, writing them to a local gzipped VCF file.
    """
    import pysam  # noqa: PLC0415

    out_path = out_dir / f"{symbol}.chr{chrom}_{start}_{end}.vcf.gz"
    if out_path.exists() and out_path.stat().st_size > 500:
        print(f"  [{symbol}] Already exists, skipping")
        return out_path

    remote_vcf = KG_VCF_PATTERN.format(base=KG_FTP_BASE, chrom=chrom)
    region = f"{chrom}:{start}-{end}"

    try:
        vcf_in = pysam.VariantFile(remote_vcf)  # opens remote + .tbi index
        header = vcf_in.header

        with gzip.open(out_path, "wt") as fh_out:
            # Write VCF header
            fh_out.write(str(header))
            n_records = 0
            for rec in vcf_in.fetch(chrom, start - 1, end):  # pysam is 0-based
                fh_out.write(str(rec))
                n_records += 1

        vcf_in.close()
        size_kb = out_path.stat().st_size // 1024
        print(f"  [{symbol}] {n_records} variants, {size_kb} KB → {out_path.name}")
        return out_path

    except Exception as exc:
        print(f"  [{symbol}] Error fetching {region}: {exc}")
        if out_path.exists():
            out_path.unlink()
        return None


def fetch_all_vcfs(hg19_table: pd.DataFrame, vcf_dir: Path) -> pd.DataFrame:
    vcf_dir.mkdir(parents=True, exist_ok=True)
    records = []
    autosomes = {str(i) for i in range(1, 23)}

    for row in hg19_table.itertuples():
        if not row.grch37_chr:
            records.append({"symbol": row.symbol, "vcf_path": None,
                            "n_variants": 0, "vcf_status": "no_hg19_coords"})
            continue
        chrom = str(row.grch37_chr)
        if chrom not in autosomes:
            records.append({"symbol": row.symbol, "vcf_path": None,
                            "n_variants": 0,
                            "vcf_status": f"skipped_chrom_{chrom}"})
            continue
        vcf_path = fetch_gene_vcf_pysam(
            row.symbol, chrom, int(row.fetch_start), int(row.fetch_end), vcf_dir
        )
        records.append({
            "symbol": row.symbol,
            "vcf_path": str(vcf_path) if vcf_path else None,
            "n_variants": None,
            "vcf_status": "ok" if vcf_path else "fetch_failed",
        })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gene-table", default="data/processed/nglyco_gene_table.tsv")
    parser.add_argument("--hg19-out", default="data/processed/nglyco_gene_table_hg19.tsv")
    parser.add_argument("--vcf-dir", default="data/raw/popgen/vcf_slices")
    parser.add_argument("--panel-dir", default="data/raw/popgen")
    parser.add_argument("--flank", type=int, default=10000)
    parser.add_argument("--skip-liftover", action="store_true")
    parser.add_argument("--skip-vcf", action="store_true")
    args = parser.parse_args()

    gene_table = pd.read_csv(args.gene_table, sep="\t")
    print(f"Loaded {len(gene_table)} genes")

    # Step 1: Liftover
    hg19_path = Path(args.hg19_out)
    if args.skip_liftover and hg19_path.exists():
        print(f"Loading existing hg19 table: {hg19_path}")
        hg19_table = pd.read_csv(hg19_path, sep="\t")
    else:
        print(f"\n--- Liftover hg38 → hg19 (flank={args.flank} bp) ---")
        hg19_table = liftover_all(gene_table, args.flank)
        hg19_path.parent.mkdir(parents=True, exist_ok=True)
        hg19_table.to_csv(hg19_path, sep="\t", index=False)
        n_ok = int(hg19_table["grch37_chr"].notna().sum())
        print(f"Liftover: {n_ok}/{len(hg19_table)} mapped → {hg19_path}")

    # Step 2: Panel
    panel_dir = Path(args.panel_dir)
    panel_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n--- 1000G population panel ---")
    fetch_panel(panel_dir)

    # Step 3: VCF slices
    if not args.skip_vcf:
        print(f"\n--- Fetching per-gene VCF slices via pysam (flank={args.flank} bp) ---")
        vcf_manifest = fetch_all_vcfs(hg19_table, Path(args.vcf_dir))
        manifest_path = Path(args.vcf_dir) / "vcf_manifest.tsv"
        vcf_manifest.to_csv(manifest_path, sep="\t", index=False)
        n_ok = int((vcf_manifest["vcf_status"] == "ok").sum())
        print(f"\nVCF slices: {n_ok}/{len(vcf_manifest)} fetched")
        print(f"Manifest: {manifest_path}")
    else:
        print("\nSkipping VCF fetch (--skip-vcf).")


if __name__ == "__main__":
    main()
