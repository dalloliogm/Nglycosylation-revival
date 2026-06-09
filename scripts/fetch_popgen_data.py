#!/usr/bin/env python3
"""Fetch population-genetics data for N-glycosylation pathway genes.

Step 1: Liftover gene coordinates from GRCh38 to GRCh37 (hg19) using the
        Ensembl REST API liftover endpoint.
Step 2: Fetch targeted VCF slices from the 1000 Genomes Phase 3 FTP using
        tabix (requires tabix to be installed).
Step 3: Download the 1000G population panel file.

This script prepares the data needed for FST/PBS computation
(scripts/compute_fst_pbs.py) and iHS extraction (scripts/extract_pophuman_ihs.py).

Usage
-----
    python scripts/fetch_popgen_data.py [--flank 10000] [--skip-vcf]

Requirements
------------
- tabix (htslib) in PATH for VCF fetching
- Network access to rest.ensembl.org and ftp.1000genomes.ebi.ac.uk
- ~2–5 GB disk space for per-gene VCF slices (compressed)

Run from the repository root.
"""

from __future__ import annotations

import argparse
import json
import subprocess
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
KG_PANEL_URL = (
    f"{KG_FTP_BASE}/integrated_call_samples_v3.20130502.ALL.panel"
)

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
    """Download a URL to dest using urllib."""
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
    """Liftover one region from GRCh38 to GRCh37. Returns dict or None."""
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
        # Take first mapping (should be one-to-one for most genes)
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
    """Liftover all genes from hg38 to hg19 with flanks applied."""
    records = []
    n = len(gene_table)
    for i, row in enumerate(gene_table.itertuples(), start=1):
        print(f"  Liftover [{i}/{n}] {row.symbol}  chr{row.grch38_chr}:{row.grch38_start}-{row.grch38_end}")
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
                "symbol": row.symbol,
                "ensembl_gene_id": row.ensembl_gene_id,
                "grch38_chr": str(row.grch38_chr),
                "grch38_start": int(row.grch38_start),
                "grch38_end": int(row.grch38_end),
                "grch37_chr": None,
                "grch37_start": None,
                "grch37_end": None,
                "grch37_strand": None,
                "flank_bp": flank,
                "fetch_start": None,
                "fetch_end": None,
            }
        records.append(result)
        time.sleep(0.1)   # be gentle on the REST API

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Step 2: Download 1000G panel file
# ---------------------------------------------------------------------------

def fetch_panel(out_dir: Path) -> Path:
    """Download the 1000G Phase 3 population panel file."""
    dest = out_dir / "1000g_phase3_panel.tsv"
    if dest.exists():
        print(f"  Panel already exists: {dest}")
        return dest
    print(f"  Downloading 1000G panel to {dest}")
    _download(KG_PANEL_URL, dest)
    print(f"  Done ({dest.stat().st_size // 1024} KB)")
    return dest


# ---------------------------------------------------------------------------
# Step 3: Tabix-fetch per-gene VCF slices
# ---------------------------------------------------------------------------

def check_tabix() -> bool:
    try:
        subprocess.run(["tabix", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def fetch_gene_vcf(symbol: str, chrom: str, start: int, end: int,
                   out_dir: Path) -> Path | None:
    """Fetch a VCF slice for one gene from the 1000G FTP using tabix."""
    out_path = out_dir / f"{symbol}.chr{chrom}_{start}_{end}.vcf.gz"
    if out_path.exists() and out_path.stat().st_size > 1000:
        print(f"  [{symbol}] VCF slice already exists, skipping")
        return out_path

    remote_vcf = KG_VCF_PATTERN.format(base=KG_FTP_BASE, chrom=chrom)
    region = f"{chrom}:{start}-{end}"

    cmd = ["tabix", "-h", remote_vcf, region]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True)
        # Compress output
        bgzip_cmd = ["bgzip", "-c"]
        gz_result = subprocess.run(
            bgzip_cmd, input=result.stdout, capture_output=True
        )
        out_path.write_bytes(gz_result.stdout)
        # Index
        subprocess.run(["tabix", "-p", "vcf", str(out_path)], check=True)
        n_bytes = out_path.stat().st_size
        print(f"  [{symbol}] Fetched {n_bytes // 1024} KB → {out_path.name}")
        return out_path
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode() if exc.stderr else ""
        print(f"  [{symbol}] tabix error: {stderr[:200]}")
        return None
    except Exception as exc:
        print(f"  [{symbol}] Error: {exc}")
        return None


def fetch_all_vcfs(hg19_table: pd.DataFrame, vcf_dir: Path) -> pd.DataFrame:
    """Fetch per-gene VCF slices for all genes with valid hg19 coordinates."""
    vcf_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for row in hg19_table.itertuples():
        if not row.grch37_chr:
            records.append({"symbol": row.symbol, "vcf_path": None,
                            "vcf_status": "no_hg19_coords"})
            continue
        # Skip non-autosomal / X/Y for now (1000G VCF naming differs)
        chrom = str(row.grch37_chr)
        if chrom not in [str(i) for i in range(1, 23)] + ["X"]:
            records.append({"symbol": row.symbol, "vcf_path": None,
                            "vcf_status": f"unsupported_chrom_{chrom}"})
            continue
        vcf_path = fetch_gene_vcf(
            row.symbol, chrom, int(row.fetch_start), int(row.fetch_end), vcf_dir
        )
        records.append({
            "symbol": row.symbol,
            "vcf_path": str(vcf_path) if vcf_path else None,
            "vcf_status": "ok" if vcf_path else "fetch_failed",
        })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch population-genetics data for N-glycosylation genes."
    )
    parser.add_argument("--gene-table", default="data/processed/nglyco_gene_table.tsv")
    parser.add_argument("--hg19-out", default="data/processed/nglyco_gene_table_hg19.tsv")
    parser.add_argument("--vcf-dir", default="data/raw/popgen/vcf_slices")
    parser.add_argument("--panel-dir", default="data/raw/popgen")
    parser.add_argument("--flank", type=int, default=10000,
                        help="Flanking bp to add on each side (default: 10000)")
    parser.add_argument("--skip-liftover", action="store_true",
                        help="Skip liftover if hg19 table already exists.")
    parser.add_argument("--skip-vcf", action="store_true",
                        help="Skip VCF fetching (liftover only).")
    args = parser.parse_args()

    gene_table = pd.read_csv(args.gene_table, sep="\t")
    print(f"Loaded {len(gene_table)} genes from {args.gene_table}")

    # Step 1: Liftover
    hg19_path = Path(args.hg19_out)
    if args.skip_liftover and hg19_path.exists():
        print(f"\nLoading existing hg19 table from {hg19_path}")
        hg19_table = pd.read_csv(hg19_path, sep="\t")
    else:
        print(f"\n--- Liftoving hg38 → hg19 (flank={args.flank} bp) ---")
        hg19_table = liftover_all(gene_table, args.flank)
        hg19_path.parent.mkdir(parents=True, exist_ok=True)
        hg19_table.to_csv(hg19_path, sep="\t", index=False)
        n_ok = int(hg19_table["grch37_chr"].notna().sum())
        print(f"\nLiftover complete: {n_ok}/{len(hg19_table)} genes mapped")
        print(f"Wrote {hg19_path}")

    # Step 2: Panel file
    panel_dir = Path(args.panel_dir)
    panel_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n--- Downloading 1000G population panel ---")
    fetch_panel(panel_dir)

    # Step 3: VCF slices
    if not args.skip_vcf:
        if not check_tabix():
            print(
                "\nWARNING: tabix not found in PATH. Install htslib and re-run"
                " without --skip-vcf to fetch VCF slices."
            )
        else:
            print(f"\n--- Fetching per-gene VCF slices (flank={args.flank} bp) ---")
            vcf_manifest = fetch_all_vcfs(hg19_table, Path(args.vcf_dir))
            manifest_path = Path(args.vcf_dir) / "vcf_manifest.tsv"
            vcf_manifest.to_csv(manifest_path, sep="\t", index=False)
            n_ok = int((vcf_manifest["vcf_status"] == "ok").sum())
            print(f"\nVCF slices: {n_ok}/{len(vcf_manifest)} fetched successfully")
            print(f"Manifest: {manifest_path}")
    else:
        print("\nSkipping VCF fetch (--skip-vcf).")


if __name__ == "__main__":
    main()
