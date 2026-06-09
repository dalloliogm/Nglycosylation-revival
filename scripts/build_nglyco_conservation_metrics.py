#!/usr/bin/env python3
"""Fetch cross-species conservation metrics for N-glycosylation pathway genes.

Tier 1 data sources
-------------------
- Ortholog identity, GOC score, and WGA coverage (human-mouse and human-chimp):
  Ensembl BioMart. dN/dS was removed from Ensembl BioMart ~v110.
- PhyloP100 (100-way vertebrate conservation, mean/median/min/p5 over gene body):
  UCSC Genome Browser REST API.

BioMart note: attributes from different "attribute pages" cannot be mixed in a
single query. Homolog attributes for each species must be fetched in a separate
query, and hgnc_symbol cannot be included in the same query as homolog attributes.

Outputs
-------
- data/processed/nglyco_conservation_metrics.tsv
- results/tables/conservation_join_audit.tsv
- results/tables/conservation_summary.tsv

Usage
-----
    python scripts/build_nglyco_conservation_metrics.py [--skip-phylop]

Run from the repository root. Requires network access to www.ensembl.org and
api.genome.ucsc.edu. Expect ~5 min for BioMart (two queries) and ~10 min for
PhyloP (one request per gene, rate-limited to 1/s).
"""

from __future__ import annotations

import argparse
import io
import json
import time
import urllib.parse
from datetime import date
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd


CONSERVATION_VERSION = f"conservation_metrics_v0.2_{date.today().isoformat()}"

BIOMART_URL = "https://www.ensembl.org/biomart/martservice"
ENSEMBL_BASE = "https://rest.ensembl.org"
UCSC_BASE = "https://api.genome.ucsc.edu"

BIOMART_BATCH_SIZE = 200
BIOMART_RETRY_WAIT = 10.0
BIOMART_MAX_RETRIES = 3

UCSC_REQUESTS_PER_SECOND = 1
UCSC_TIMEOUT = 60
UCSC_MAX_RETRIES = 3

# Real BioMart column names (confirmed 2026-06-09)
MOUSE_COLS = {
    "gene_id": "Gene stable ID",
    "homolog_gene": "Mouse gene stable ID",
    "homology_type": "Mouse homology type",
    "perc_id": "%id. target Mouse gene identical to query gene",
    "perc_id_r1": "%id. query gene identical to target Mouse gene",
    "goc_score": "Mouse Gene-order conservation score",
    "wga_coverage": "Mouse Whole-genome alignment coverage",
}

CHIMP_COLS = {
    "gene_id": "Gene stable ID",
    "homolog_gene": "Chimpanzee gene stable ID",
    "homology_type": "Chimpanzee homology type",
    "perc_id": "%id. target Chimpanzee gene identical to query gene",
    "perc_id_r1": "%id. query gene identical to target Chimpanzee gene",
    "goc_score": "Chimpanzee Gene-order conservation score",
    "wga_coverage": "Chimpanzee Whole-genome alignment coverage",
}


# ---------------------------------------------------------------------------
# Generic HTTP helpers
# ---------------------------------------------------------------------------

def _get_json(url: str, timeout: int = 30, retries: int = 3, retry_wait: float = 5.0) -> Any:
    for attempt in range(retries):
        try:
            req = Request(url, headers={"Content-Type": "application/json"})
            with urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except HTTPError as exc:
            if exc.code == 429:
                wait = retry_wait * (attempt + 1)
                print(f"  Rate-limited (429). Waiting {wait:.0f}s before retry.")
                time.sleep(wait)
            elif exc.code in {500, 502, 503, 504} and attempt < retries - 1:
                print(f"  Server error {exc.code}. Retrying.")
                time.sleep(retry_wait)
            else:
                raise
        except URLError as exc:
            if attempt < retries - 1:
                print(f"  URL error: {exc.reason}. Retrying.")
                time.sleep(retry_wait)
            else:
                raise
    raise RuntimeError(f"Failed after {retries} retries: {url}")


def _safe_float(val: Any) -> float | None:
    try:
        f = float(val)
        return None if np.isnan(f) else f
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Ensembl BioMart ortholog metrics
# ---------------------------------------------------------------------------

def _build_biomart_xml(gene_ids: list[str], species: str) -> str:
    """Build a BioMart XML query for one species (mouse or chimp).

    Each species must be queried separately because mixing homolog attributes
    from two species triggers a BioMart multi-page error. hgnc_symbol is also
    omitted for the same reason.
    """
    if species == "mouse":
        attrs = """
    <Attribute name="ensembl_gene_id"/>
    <Attribute name="mmusculus_homolog_ensembl_gene"/>
    <Attribute name="mmusculus_homolog_orthology_type"/>
    <Attribute name="mmusculus_homolog_perc_id"/>
    <Attribute name="mmusculus_homolog_perc_id_r1"/>
    <Attribute name="mmusculus_homolog_goc_score"/>
    <Attribute name="mmusculus_homolog_wga_coverage"/>"""
    elif species == "chimp":
        attrs = """
    <Attribute name="ensembl_gene_id"/>
    <Attribute name="ptroglodytes_homolog_ensembl_gene"/>
    <Attribute name="ptroglodytes_homolog_orthology_type"/>
    <Attribute name="ptroglodytes_homolog_perc_id"/>
    <Attribute name="ptroglodytes_homolog_perc_id_r1"/>
    <Attribute name="ptroglodytes_homolog_goc_score"/>
    <Attribute name="ptroglodytes_homolog_wga_coverage"/>"""
    else:
        raise ValueError(f"Unknown species: {species}")

    ids_str = ",".join(gene_ids)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query virtualSchemaName="default" formatter="TSV" header="1" uniqueRows="1" datasetConfigVersion="0.6">
  <Dataset name="hsapiens_gene_ensembl" interface="default">
    <Filter name="ensembl_gene_id" value="{ids_str}"/>{attrs}
  </Dataset>
</Query>"""


def _fetch_biomart_df(gene_ids: list[str], species: str) -> pd.DataFrame:
    """Fetch BioMart homolog data for all genes (batched), one species."""
    all_frames: list[pd.DataFrame] = []
    batches = [gene_ids[i:i + BIOMART_BATCH_SIZE] for i in range(0, len(gene_ids), BIOMART_BATCH_SIZE)]
    for batch_num, batch in enumerate(batches, start=1):
        print(f"  BioMart {species} batch {batch_num}/{len(batches)} ({len(batch)} genes)")
        xml = _build_biomart_xml(batch, species)
        url = BIOMART_URL + "?query=" + urllib.parse.quote(xml)
        raw = None
        for attempt in range(BIOMART_MAX_RETRIES):
            try:
                req = Request(url, headers={"Accept": "text/plain"})
                with urlopen(req, timeout=120) as resp:
                    raw = resp.read().decode("utf-8")
                break
            except Exception as exc:
                if attempt < BIOMART_MAX_RETRIES - 1:
                    print(f"    Error: {exc}, retrying ({attempt + 1}/{BIOMART_MAX_RETRIES})")
                    time.sleep(BIOMART_RETRY_WAIT)
                else:
                    raise
        if raw and raw.startswith("Query ERROR"):
            raise RuntimeError(f"BioMart query error: {raw[:300]}")
        if raw:
            all_frames.append(pd.read_csv(io.StringIO(raw), sep="\t"))
    return pd.concat(all_frames, ignore_index=True) if all_frames else pd.DataFrame()


def _best_one2one(subset: pd.DataFrame, col_map: dict) -> dict:
    """Pick the best one2one row for one gene from a multi-row BioMart result."""
    empty = {
        "ortholog_type": None, "perc_id": None, "perc_id_r1": None,
        "goc_score": None, "wga_coverage": None,
    }
    if subset.empty:
        return empty
    type_col = col_map["homology_type"]
    if type_col not in subset.columns:
        return empty
    one2one = subset[subset[type_col].astype(str).str.contains("one2one", na=False)]
    row = one2one.iloc[0] if not one2one.empty else subset.iloc[0]
    return {
        "ortholog_type": str(row.get(type_col, "")) or None,
        "perc_id": _safe_float(row.get(col_map["perc_id"])),
        "perc_id_r1": _safe_float(row.get(col_map["perc_id_r1"])),
        "goc_score": _safe_float(row.get(col_map["goc_score"])),
        "wga_coverage": _safe_float(row.get(col_map["wga_coverage"])),
    }


def fetch_all_ortholog_metrics(gene_table: pd.DataFrame) -> pd.DataFrame:
    """Fetch ortholog % identity, GOC, and WGA for mouse and chimp from BioMart."""
    try:
        ensembl_release = str(
            _get_json(f"{ENSEMBL_BASE}/info/software?content-type=application/json", timeout=15)
            .get("release", "unknown")
        )
    except Exception:
        ensembl_release = "unknown"
    print(f"Ensembl release: {ensembl_release}")

    gene_ids = gene_table["ensembl_gene_id"].tolist()

    mouse_df = _fetch_biomart_df(gene_ids, "mouse")
    chimp_df = _fetch_biomart_df(gene_ids, "chimp")

    # Normalise the gene ID column (BioMart returns "Gene stable ID").
    for df in (mouse_df, chimp_df):
        if not df.empty:
            id_col = MOUSE_COLS["gene_id"]  # same header in both queries
            if id_col in df.columns:
                df.rename(columns={id_col: "ensembl_gene_id"}, inplace=True)
            df["ensembl_gene_id"] = df["ensembl_gene_id"].astype(str).str.split(".").str[0]

    records = []
    for _, gene_row in gene_table.iterrows():
        eid = gene_row["ensembl_gene_id"]
        symbol = gene_row["symbol"]

        mouse_subset = mouse_df[mouse_df["ensembl_gene_id"] == eid] if not mouse_df.empty else pd.DataFrame()
        chimp_subset = chimp_df[chimp_df["ensembl_gene_id"] == eid] if not chimp_df.empty else pd.DataFrame()

        mouse = _best_one2one(mouse_subset, MOUSE_COLS)
        chimp = _best_one2one(chimp_subset, CHIMP_COLS)

        records.append({
            "symbol": symbol,
            "ensembl_gene_id": eid,
            "mouse_ortholog_type": mouse["ortholog_type"],
            "mouse_perc_id": mouse["perc_id"],
            "mouse_perc_id_r1": mouse["perc_id_r1"],
            "mouse_goc_score": mouse["goc_score"],
            "mouse_wga_coverage": mouse["wga_coverage"],
            "chimp_ortholog_type": chimp["ortholog_type"],
            "chimp_perc_id": chimp["perc_id"],
            "chimp_perc_id_r1": chimp["perc_id_r1"],
            "chimp_goc_score": chimp["goc_score"],
            "chimp_wga_coverage": chimp["wga_coverage"],
            "ortholog_missing_reason": (
                None if (mouse["perc_id"] is not None or chimp["perc_id"] is not None)
                else "not_in_biomart"
            ),
            "ensembl_release": ensembl_release,
        })

    result = pd.DataFrame(records)
    n_mouse = int(result["mouse_perc_id"].notna().sum())
    n_chimp = int(result["chimp_perc_id"].notna().sum())
    print(f"  Mouse % identity: {n_mouse}/{len(result)} genes with values")
    print(f"  Chimp % identity: {n_chimp}/{len(result)} genes with values")
    return result


# ---------------------------------------------------------------------------
# UCSC PhyloP100
# ---------------------------------------------------------------------------

def fetch_phylop(chrom: str, start: int, end: int) -> dict[str, Any]:
    """Return PhyloP100way summary statistics for a genomic region (GRCh38)."""
    result: dict[str, Any] = {
        "phylop100_mean": None, "phylop100_median": None,
        "phylop100_min": None, "phylop100_p5": None,
        "phylop100_positions_total": None, "phylop100_positions_missing": None,
        "phylop_query_status": "not_attempted",
        "ucsc_access_date": date.today().isoformat(),
    }

    chrom_str = str(chrom) if str(chrom).startswith("chr") else "chr" + str(chrom)
    url = (
        f"{UCSC_BASE}/getData/track"
        f"?genome=hg38&track=phyloP100way"
        f"&chrom={chrom_str}&start={start}&end={end}"
    )

    try:
        data = _get_json(url, timeout=UCSC_TIMEOUT, retries=UCSC_MAX_RETRIES, retry_wait=5.0)
    except HTTPError as exc:
        result["phylop_query_status"] = f"api_error_http_{exc.code}"
        return result
    except TimeoutError:
        result["phylop_query_status"] = "timeout"
        return result
    except Exception as exc:
        result["phylop_query_status"] = f"api_error: {exc}"
        return result

    raw = data.get("phyloP100way", data.get("data", []))
    if not raw:
        result["phylop_query_status"] = "empty"
        return result

    if isinstance(raw, list) and raw and isinstance(raw[0], dict):
        values = [entry["value"] for entry in raw if "value" in entry]
    elif isinstance(raw, list):
        values = [v for v in raw if v is not None]
    else:
        result["phylop_query_status"] = "parse_error"
        return result

    total_positions = end - start
    missing_positions = total_positions - len(values)

    if not values:
        result["phylop_query_status"] = "empty_after_parse"
        result["phylop100_positions_total"] = total_positions
        result["phylop100_positions_missing"] = missing_positions
        return result

    arr = np.array(values, dtype=float)
    result["phylop100_mean"] = float(np.nanmean(arr))
    result["phylop100_median"] = float(np.nanmedian(arr))
    result["phylop100_min"] = float(np.nanmin(arr))
    result["phylop100_p5"] = float(np.nanpercentile(arr, 5))
    result["phylop100_positions_total"] = total_positions
    result["phylop100_positions_missing"] = missing_positions
    result["phylop_query_status"] = "ok"
    return result


def fetch_all_phylop(gene_table: pd.DataFrame) -> pd.DataFrame:
    """Fetch PhyloP100 for all genes using their GRCh38 coordinates."""
    records = []
    n = len(gene_table)
    interval = 1.0 / UCSC_REQUESTS_PER_SECOND
    for i, row in enumerate(gene_table.itertuples(), start=1):
        print(f"  PhyloP [{i}/{n}] {row.symbol}  chr{row.grch38_chr}:{row.grch38_start}-{row.grch38_end}")
        r = fetch_phylop(row.grch38_chr, int(row.grch38_start), int(row.grch38_end))
        r["symbol"] = row.symbol
        r["ensembl_gene_id"] = row.ensembl_gene_id
        records.append(r)
        time.sleep(interval)
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Merge and summarise
# ---------------------------------------------------------------------------

def merge_conservation(
    gene_table: pd.DataFrame,
    ortholog_df: pd.DataFrame,
    phylop_df: pd.DataFrame | None,
) -> pd.DataFrame:
    base_cols = [
        "symbol", "ensembl_gene_id", "primary_region", "analysis_group",
        "include_primary", "include_sensitivity",
    ]
    out = gene_table[base_cols].copy()
    out["conservation_version"] = CONSERVATION_VERSION

    out = out.merge(ortholog_df.drop(columns=["symbol"], errors="ignore"), on="ensembl_gene_id", how="left")

    if phylop_df is not None:
        out = out.merge(phylop_df.drop(columns=["symbol"], errors="ignore"), on="ensembl_gene_id", how="left")
    else:
        for col in ["phylop100_mean", "phylop100_median", "phylop100_min", "phylop100_p5",
                    "phylop100_positions_total", "phylop100_positions_missing",
                    "phylop_query_status", "ucsc_access_date"]:
            out[col] = pd.NA

    has_ortholog = out["mouse_perc_id"].notna() | out["chimp_perc_id"].notna()
    has_phylop = out["phylop100_mean"].notna() if "phylop100_mean" in out.columns else pd.Series(False, index=out.index)

    conditions = [has_ortholog & has_phylop, has_ortholog & ~has_phylop, ~has_ortholog & has_phylop]
    choices = ["ortholog_and_phylop", "ortholog_only", "phylop_only"]
    out["conservation_join_status"] = np.select(conditions, choices, default="missing_both")
    return out


def summarise_conservation(merged: pd.DataFrame) -> pd.DataFrame:
    available = merged[merged["conservation_join_status"].isin(["ortholog_and_phylop", "ortholog_only"])]
    if available.empty:
        return pd.DataFrame()
    grp = available.groupby(["analysis_group", "primary_region"])

    def iqr(s: pd.Series) -> float:
        return float(s.quantile(0.75) - s.quantile(0.25))

    return grp.agg(
        gene_count=("symbol", "count"),
        median_mouse_perc_id=("mouse_perc_id", "median"),
        iqr_mouse_perc_id=("mouse_perc_id", iqr),
        n_mouse_perc_id=("mouse_perc_id", "count"),
        median_chimp_perc_id=("chimp_perc_id", "median"),
        iqr_chimp_perc_id=("chimp_perc_id", iqr),
        n_chimp_perc_id=("chimp_perc_id", "count"),
        median_mouse_goc=("mouse_goc_score", "median"),
        median_phylop100_mean=("phylop100_mean", "median"),
        iqr_phylop100_mean=("phylop100_mean", iqr),
        n_phylop=("phylop100_mean", "count"),
    ).round(4).reset_index()


def write_join_audit(merged: pd.DataFrame, path: Path) -> None:
    audit_cols = [
        "symbol", "ensembl_gene_id", "analysis_group", "primary_region",
        "conservation_join_status", "ortholog_missing_reason",
        "mouse_ortholog_type", "mouse_perc_id", "mouse_goc_score", "mouse_wga_coverage",
        "chimp_ortholog_type", "chimp_perc_id", "chimp_goc_score",
        "phylop100_mean", "phylop_query_status",
    ]
    cols = [c for c in audit_cols if c in merged.columns]
    merged[cols].to_csv(path, sep="\t", index=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch ortholog identity, GOC, WGA, and PhyloP100 for N-glycosylation genes."
    )
    parser.add_argument("--gene-table", default="data/processed/nglyco_gene_table.tsv")
    parser.add_argument("--conservation-out", default="data/processed/nglyco_conservation_metrics.tsv")
    parser.add_argument("--join-audit-out", default="results/tables/conservation_join_audit.tsv")
    parser.add_argument("--summary-out", default="results/tables/conservation_summary.tsv")
    parser.add_argument("--skip-phylop", action="store_true", help="Skip PhyloP (faster).")
    args = parser.parse_args()

    gene_table = pd.read_csv(args.gene_table, sep="\t")
    print(f"Loaded {len(gene_table)} genes from {args.gene_table}")

    print("\n--- Fetching ortholog metrics from Ensembl BioMart ---")
    ortholog_df = fetch_all_ortholog_metrics(gene_table)

    phylop_df: pd.DataFrame | None = None
    if not args.skip_phylop:
        print("\n--- Fetching PhyloP100 from UCSC ---")
        phylop_df = fetch_all_phylop(gene_table)
    else:
        print("\nSkipping PhyloP (--skip-phylop).")

    print("\n--- Merging and writing outputs ---")
    merged = merge_conservation(gene_table, ortholog_df, phylop_df)
    summary = summarise_conservation(merged)

    for path in [args.conservation_out, args.join_audit_out, args.summary_out]:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    merged.to_csv(args.conservation_out, sep="\t", index=False)
    write_join_audit(merged, Path(args.join_audit_out))
    summary.to_csv(args.summary_out, sep="\t", index=False)

    n_mouse = int(merged["mouse_perc_id"].notna().sum())
    n_chimp = int(merged["chimp_perc_id"].notna().sum())
    n_phylop = int(merged["phylop100_mean"].notna().sum()) if "phylop100_mean" in merged.columns else 0
    print(f"\nInput genes:               {len(merged)}")
    print(f"Mouse % identity:          {n_mouse}")
    print(f"Chimp % identity:          {n_chimp}")
    print(f"PhyloP available:          {n_phylop}")
    print(f"\nWrote {args.conservation_out}")
    print(f"Wrote {args.join_audit_out}")
    print(f"Wrote {args.summary_out}")


if __name__ == "__main__":
    main()
