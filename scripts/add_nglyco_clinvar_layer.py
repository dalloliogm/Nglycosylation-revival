#!/usr/bin/env python3
"""Add ClinVar pathogenic/likely pathogenic counts to disease annotations."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd


CLINVAR_LAYER_VERSION = "cdg_seed_plus_clinvar_plp_v0.1_2026-06-03"
CLINVAR_SOURCE_URL = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
CLINVAR_ACCESS_DATE = "2026-06-03"
CLINVAR_ASSEMBLY = "GRCh38"
CLINVAR_NOTE_PATTERN = re.compile(
    r"( ClinVar P/LP layer: \d+ unique GRCh38 germline P/LP VariationID\(s\), "
    r"accessed \d{4}-\d{2}-\d{2}\.)+"
)

USE_COLUMNS = [
    "#AlleleID",
    "GeneSymbol",
    "ClinicalSignificance",
    "ClinSigSimple",
    "RCVaccession",
    "PhenotypeList",
    "OriginSimple",
    "Assembly",
    "ReviewStatus",
    "VariationID",
]

EXCLUDED_CLINSIG_TERMS = (
    "benign",
    "uncertain",
    "conflicting",
    "not provided",
    "association",
    "risk factor",
    "protective",
    "affects",
    "drug response",
)


def split_symbols(value: object) -> set[str]:
    if not isinstance(value, str) or not value or value == "-":
        return set()
    normalized = value.replace("|", ";").replace(",", ";")
    return {symbol.strip() for symbol in normalized.split(";") if symbol.strip()}


def is_plp_clinsig(value: object) -> bool:
    text = str(value).lower()
    if "pathogenic" not in text:
        return False
    return not any(term in text for term in EXCLUDED_CLINSIG_TERMS)


def split_conditions(value: object) -> set[str]:
    if not isinstance(value, str) or not value or value == "-":
        return set()
    conditions: set[str] = set()
    for condition in value.split("|"):
        condition = condition.strip()
        if condition and condition.lower() != "not provided":
            conditions.add(condition)
    return conditions


def summarize_clinvar(
    clinvar_path: str,
    target_symbols: set[str],
    chunksize: int,
) -> pd.DataFrame:
    variant_ids: dict[str, set[str]] = defaultdict(set)
    allele_ids: dict[str, set[str]] = defaultdict(set)
    conditions: dict[str, set[str]] = defaultdict(set)
    review_statuses: dict[str, set[str]] = defaultdict(set)
    rcv_accessions: dict[str, set[str]] = defaultdict(set)

    for chunk in pd.read_csv(
        clinvar_path,
        sep="\t",
        compression="gzip",
        usecols=USE_COLUMNS,
        dtype=str,
        chunksize=chunksize,
        low_memory=False,
    ):
        chunk = chunk[
            chunk["Assembly"].eq(CLINVAR_ASSEMBLY)
            & chunk["OriginSimple"].fillna("").str.lower().eq("germline")
            & chunk["ClinicalSignificance"].map(is_plp_clinsig)
        ].copy()
        if chunk.empty:
            continue

        chunk["matched_symbols"] = chunk["GeneSymbol"].map(
            lambda value: split_symbols(value) & target_symbols
        )
        chunk = chunk[chunk["matched_symbols"].map(bool)]
        if chunk.empty:
            continue

        for row in chunk.itertuples(index=False):
            for symbol in row.matched_symbols:
                variant_id = str(row.VariationID)
                allele_id = str(getattr(row, "_0"))
                if variant_id and variant_id != "-":
                    variant_ids[symbol].add(variant_id)
                if allele_id and allele_id != "-":
                    allele_ids[symbol].add(allele_id)
                conditions[symbol].update(split_conditions(row.PhenotypeList))
                if row.ReviewStatus and row.ReviewStatus != "-":
                    review_statuses[symbol].add(row.ReviewStatus)
                if row.RCVaccession and row.RCVaccession != "-":
                    rcv_accessions[symbol].update(row.RCVaccession.split("|"))

    rows = []
    for symbol in sorted(target_symbols):
        rows.append(
            {
                "symbol": symbol,
                "clinvar_plp_variant_count": len(variant_ids[symbol]),
                "clinvar_plp_allele_count": len(allele_ids[symbol]),
                "clinvar_plp_condition_count": len(conditions[symbol]),
                "clinvar_plp_rcv_count": len(rcv_accessions[symbol]),
                "clinvar_review_statuses": "; ".join(sorted(review_statuses[symbol])),
                "clinvar_plp_condition_examples": "; ".join(sorted(conditions[symbol])[:5]),
                "clinvar_assembly": CLINVAR_ASSEMBLY,
                "clinvar_source_url": CLINVAR_SOURCE_URL,
                "clinvar_access_date": CLINVAR_ACCESS_DATE,
            }
        )
    return pd.DataFrame(rows)


def disease_class(row: pd.Series) -> str:
    has_clinvar = row["clinvar_plp_variant_count"] > 0
    has_cdg = row["cdg_curated_status"] != "not_cdg_gene"
    has_complex = row["complex_trait_evidence_status"] == "gwas_trait_evidence_present"

    if has_cdg and has_complex:
        return "mixed_mendelian_and_complex"
    if (has_cdg or has_clinvar) and row["primary_region"] == "er_quality_control":
        return "checkpoint_or_quality_control_disease"
    if has_cdg or has_clinvar:
        return "severe_mendelian_core"
    if has_complex:
        return "complex_or_context_dependent_trait"
    return "no_current_disease_signal"


def add_clinvar_layer(annotations: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    merged = annotations.drop(
        columns=[
            "clinvar_plp_variant_count",
            "clinvar_plp_condition_count",
            "clinvar_evidence_status",
        ],
        errors="ignore",
    ).merge(counts, on="symbol", how="left")

    count_columns = [
        "clinvar_plp_variant_count",
        "clinvar_plp_allele_count",
        "clinvar_plp_condition_count",
        "clinvar_plp_rcv_count",
    ]
    for column in count_columns:
        merged[column] = merged[column].fillna(0).astype(int)

    merged["clinvar_evidence_status"] = merged["clinvar_plp_variant_count"].map(
        lambda count: "plp_variants_present" if count > 0 else "no_plp_variants_found"
    )
    merged["disease_architecture_class"] = merged.apply(disease_class, axis=1)
    merged["disease_annotation_version"] = CLINVAR_LAYER_VERSION
    merged["disease_annotation_notes"] = merged.apply(
        lambda row: (
            f"{CLINVAR_NOTE_PATTERN.sub('', row['disease_annotation_notes'])} ClinVar P/LP layer: "
            f"{row['clinvar_plp_variant_count']} unique GRCh38 germline P/LP "
            f"VariationID(s), accessed {CLINVAR_ACCESS_DATE}."
        ),
        axis=1,
    )

    output_columns = [
        "symbol",
        "ensembl_gene_id",
        "primary_region",
        "analysis_group",
        "include_primary",
        "include_sensitivity",
        "cdg_curated_status",
        "cdg_subtype",
        "mendelian_disease_status",
        "mode_of_inheritance",
        "severe_mendelian_burden",
        "clinvar_plp_variant_count",
        "clinvar_plp_condition_count",
        "clinvar_evidence_status",
        "gwas_association_count",
        "gwas_trait_category_count",
        "immune_inflammation_trait_flag",
        "infection_trait_flag",
        "cancer_trait_flag",
        "tissue_identity_trait_flag",
        "complex_trait_evidence_status",
        "disease_architecture_class",
        "evidence_confidence",
        "disease_annotation_version",
        "disease_annotation_source",
        "disease_annotation_source_url",
        "disease_annotation_access_date",
        "disease_annotation_notes",
    ]
    return merged[output_columns]


def build_summary(annotations: pd.DataFrame) -> pd.DataFrame:
    cdg_statuses = {"known_cdg_gene", "overlapping_or_multiple_pathway_cdg_gene"}
    summary = (
        annotations.groupby(["analysis_group", "primary_region"], dropna=False)
        .agg(
            gene_count=("symbol", "count"),
            primary_gene_count=("include_primary", lambda values: int((values == "yes").sum())),
            cdg_seed_gene_count=(
                "cdg_curated_status",
                lambda values: int(values.isin(cdg_statuses).sum()),
            ),
            known_cdg_gene_count=(
                "cdg_curated_status",
                lambda values: int((values == "known_cdg_gene").sum()),
            ),
            multiple_pathway_cdg_gene_count=(
                "cdg_curated_status",
                lambda values: int((values == "overlapping_or_multiple_pathway_cdg_gene").sum()),
            ),
            high_severe_mendelian_burden_count=(
                "severe_mendelian_burden",
                lambda values: int((values == "high").sum()),
            ),
            moderate_or_high_severe_mendelian_burden_count=(
                "severe_mendelian_burden",
                lambda values: int(values.isin(["moderate", "high"]).sum()),
            ),
            clinvar_plp_gene_count=(
                "clinvar_evidence_status",
                lambda values: int((values == "plp_variants_present").sum()),
            ),
            clinvar_plp_variant_count=("clinvar_plp_variant_count", "sum"),
            median_clinvar_plp_variant_count=("clinvar_plp_variant_count", "median"),
        )
        .reset_index()
    )
    summary["cdg_seed_fraction"] = (
        summary["cdg_seed_gene_count"] / summary["gene_count"]
    ).round(4)
    summary["clinvar_plp_gene_fraction"] = (
        summary["clinvar_plp_gene_count"] / summary["gene_count"]
    ).round(4)
    summary["median_clinvar_plp_variant_count"] = (
        summary["median_clinvar_plp_variant_count"].round(4)
    )
    summary.insert(0, "disease_annotation_version", CLINVAR_LAYER_VERSION)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add ClinVar germline P/LP counts to N-glycosylation disease annotations."
    )
    parser.add_argument(
        "--annotations",
        default="data/processed/nglyco_disease_annotations.tsv",
        help="Input disease annotation TSV.",
    )
    parser.add_argument(
        "--clinvar-variant-summary",
        default="data/external/clinvar/variant_summary.txt.gz",
        help="ClinVar variant_summary.txt.gz.",
    )
    parser.add_argument(
        "--annotations-out",
        default="data/processed/nglyco_disease_annotations.tsv",
        help="Updated disease annotation TSV.",
    )
    parser.add_argument(
        "--clinvar-counts-out",
        default="results/tables/clinvar_plp_gene_counts.tsv",
        help="Compact per-gene ClinVar P/LP count table.",
    )
    parser.add_argument(
        "--summary-out",
        default="results/tables/disease_architecture_summary.tsv",
        help="Updated disease summary TSV.",
    )
    parser.add_argument("--chunksize", type=int, default=200_000)
    args = parser.parse_args()

    annotations = pd.read_csv(args.annotations, sep="\t")
    target_symbols = set(annotations["symbol"])
    counts = summarize_clinvar(args.clinvar_variant_summary, target_symbols, args.chunksize)
    updated = add_clinvar_layer(annotations, counts)
    summary = build_summary(updated)

    Path(args.annotations_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.clinvar_counts_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary_out).parent.mkdir(parents=True, exist_ok=True)
    updated.to_csv(args.annotations_out, sep="\t", index=False)
    counts.to_csv(args.clinvar_counts_out, sep="\t", index=False)
    summary.to_csv(args.summary_out, sep="\t", index=False)

    print(f"Wrote {len(updated)} rows to {args.annotations_out}")
    print(f"Wrote {len(counts)} rows to {args.clinvar_counts_out}")
    print(f"Wrote {len(summary)} rows to {args.summary_out}")


if __name__ == "__main__":
    main()
