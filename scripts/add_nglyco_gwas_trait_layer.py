#!/usr/bin/env python3
"""Add GWAS Catalog trait-category evidence to disease annotations."""

from __future__ import annotations

import argparse
import re
import zipfile
from collections import defaultdict
from pathlib import Path

import pandas as pd


GWAS_LAYER_VERSION = "cdg_clinvar_plus_gwas_catalog_v0.1_2026-06-03"
GWAS_SOURCE_URL = "https://www.ebi.ac.uk/gwas/api/search/downloads/associations/v1.0.2"
GWAS_RELEASE = "gwas_catalog_v1.0.2-associations_e115_r2026-06-01"
GWAS_ACCESS_DATE = "2026-06-03"

USE_COLUMNS = [
    "PUBMEDID",
    "FIRST AUTHOR",
    "DATE",
    "STUDY",
    "DISEASE/TRAIT",
    "REPORTED GENE(S)",
    "MAPPED_GENE",
    "P-VALUE",
    "MAPPED_TRAIT",
    "MAPPED_TRAIT_URI",
    "STUDY ACCESSION",
]

GWAS_NOTE_PATTERN = re.compile(
    r"( GWAS Catalog layer: \d+ association\(s\), \d+ mapped trait\(s\), "
    r"categories [^.;]+, accessed \d{4}-\d{2}-\d{2}\.)+"
)

CATEGORY_KEYWORDS = {
    "glycome": (
        "glycan",
        "glycation",
        "glyco",
        "glycosylation",
        "n-glycome",
        "n glycome",
        "igg n-glycosylation",
        "igg glycosylation",
        "plasma n-glycome",
    ),
    "immune_inflammation": (
        "immune",
        "immunoglobulin",
        "igg",
        "antibody",
        "autoimmune",
        "inflammation",
        "inflammatory",
        "cytokine",
        "leukocyte",
        "lymphocyte",
        "monocyte",
        "neutrophil",
        "eosinophil",
        "asthma",
        "allergy",
        "arthritis",
        "lupus",
        "crohn",
        "colitis",
        "psoriasis",
    ),
    "infection": (
        "infection",
        "infectious",
        "virus",
        "viral",
        "bacterial",
        "pathogen",
        "hiv",
        "hepatitis",
        "covid",
        "tuberculosis",
        "malaria",
    ),
    "cancer": (
        "cancer",
        "carcinoma",
        "tumor",
        "tumour",
        "neoplasm",
        "melanoma",
        "leukemia",
        "lymphoma",
        "glioma",
        "sarcoma",
    ),
    "tissue_identity": (
        "epithelial",
        "mucosal",
        "skin",
        "liver",
        "kidney",
        "lung",
        "intest",
        "colon",
        "brain",
        "muscle",
        "retina",
        "plasma protein",
        "serum protein",
    ),
    "metabolism": (
        "metabolite",
        "metabolic",
        "lipid",
        "glucose",
        "insulin",
        "cholesterol",
        "triglyceride",
        "protein level",
        "protein measurement",
        "enzyme",
    ),
}


def split_gene_field(value: object) -> set[str]:
    if not isinstance(value, str) or not value.strip() or value.strip() == "NR":
        return set()
    text = value.upper()
    text = re.sub(r"\bINTERGENIC\b", " ", text)
    tokens = re.split(r"[^A-Z0-9]+", text)
    return {token for token in tokens if token}


def categories_for_text(*values: object) -> set[str]:
    text = " ".join(str(value).lower() for value in values if isinstance(value, str))
    categories: set[str] = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            categories.add(category)
    return categories


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def summarize_gwas_catalog(
    gwas_zip_path: str,
    target_symbols: set[str],
    chunksize: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    association_ids: dict[str, set[str]] = defaultdict(set)
    study_ids: dict[str, set[str]] = defaultdict(set)
    pubmed_ids: dict[str, set[str]] = defaultdict(set)
    mapped_traits: dict[str, set[str]] = defaultdict(set)
    categories: dict[str, set[str]] = defaultdict(set)
    pvalue_min: dict[str, float] = defaultdict(lambda: float("inf"))
    matched_rows: list[dict[str, object]] = []

    with zipfile.ZipFile(gwas_zip_path) as archive:
        for member in sorted(archive.namelist()):
            with archive.open(member) as handle:
                for chunk in pd.read_csv(
                    handle,
                    sep="\t",
                    usecols=USE_COLUMNS,
                    dtype=str,
                    chunksize=chunksize,
                    low_memory=False,
                ):
                    for row in chunk.itertuples(index=False, name=None):
                        (
                            pubmed_id,
                            first_author,
                            publication_date,
                            study,
                            disease_trait,
                            reported_genes,
                            mapped_genes,
                            p_value_raw,
                            mapped_trait,
                            _mapped_trait_uri,
                            study_accession,
                        ) = row
                        reported = split_gene_field(reported_genes)
                        mapped = split_gene_field(mapped_genes)
                        matched_reported = reported & target_symbols
                        matched_mapped = mapped & target_symbols
                        matched = matched_reported | matched_mapped
                        if not matched:
                            continue

                        row_categories = categories_for_text(
                            disease_trait,
                            mapped_trait,
                            study,
                        )
                        try:
                            pvalue = float(p_value_raw)
                        except (TypeError, ValueError):
                            pvalue = float("nan")

                        for symbol in matched:
                            association_key = f"{study_accession}|{mapped_trait}|{p_value_raw}|{disease_trait}"
                            association_ids[symbol].add(association_key)
                            if study_accession and study_accession != "NR":
                                study_ids[symbol].add(study_accession)
                            if pubmed_id and pubmed_id != "NR":
                                pubmed_ids[symbol].add(pubmed_id)
                            if mapped_trait and mapped_trait != "NR":
                                mapped_traits[symbol].update(
                                    trait.strip()
                                    for trait in mapped_trait.split(",")
                                    if trait.strip()
                                )
                            categories[symbol].update(row_categories)
                            if pd.notna(pvalue):
                                pvalue_min[symbol] = min(pvalue_min[symbol], pvalue)
                            matched_rows.append(
                                {
                                    "symbol": symbol,
                                    "match_basis": ";".join(
                                        basis
                                        for basis, condition in [
                                            ("reported_gene", symbol in matched_reported),
                                            ("mapped_gene", symbol in matched_mapped),
                                        ]
                                        if condition
                                    ),
                                    "study_accession": study_accession,
                                    "pubmed_id": pubmed_id,
                                    "first_author": first_author,
                                    "publication_date": publication_date,
                                    "disease_trait": disease_trait,
                                    "mapped_trait": mapped_trait,
                                    "trait_categories": ";".join(sorted(row_categories)),
                                    "reported_genes": reported_genes,
                                    "mapped_genes": mapped_genes,
                                    "p_value": p_value_raw,
                                }
                            )

    count_rows = []
    for symbol in sorted(target_symbols):
        min_pvalue = pvalue_min[symbol]
        count_rows.append(
            {
                "symbol": symbol,
                "gwas_association_count": len(association_ids[symbol]),
                "gwas_study_count": len(study_ids[symbol]),
                "gwas_pubmed_count": len(pubmed_ids[symbol]),
                "gwas_trait_category_count": len(categories[symbol]),
                "gwas_mapped_trait_count": len(mapped_traits[symbol]),
                "gwas_min_p_value": "" if min_pvalue == float("inf") else min_pvalue,
                "gwas_trait_categories": ";".join(sorted(categories[symbol])),
                "gwas_mapped_trait_examples": "; ".join(sorted(mapped_traits[symbol])[:8]),
                "gwas_catalog_release": GWAS_RELEASE,
                "gwas_catalog_source_url": GWAS_SOURCE_URL,
                "gwas_catalog_access_date": GWAS_ACCESS_DATE,
            }
        )

    counts = pd.DataFrame(count_rows)
    matched = pd.DataFrame(matched_rows)
    if not matched.empty:
        matched = matched.sort_values(["symbol", "study_accession", "disease_trait"])
    return counts, matched


def disease_class(row: pd.Series) -> str:
    has_cdg = row["cdg_curated_status"] != "not_cdg_gene"
    has_clinvar = row["clinvar_plp_variant_count"] > 0
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


def add_gwas_layer(annotations: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    drop_columns = [
        "gwas_association_count",
        "gwas_trait_category_count",
        "immune_inflammation_trait_flag",
        "infection_trait_flag",
        "cancer_trait_flag",
        "tissue_identity_trait_flag",
        "complex_trait_evidence_status",
    ]
    if "glycome_trait_flag" in annotations.columns:
        drop_columns.append("glycome_trait_flag")

    merged = annotations.drop(columns=drop_columns, errors="ignore").merge(
        counts, on="symbol", how="left"
    )
    count_columns = [
        "gwas_association_count",
        "gwas_study_count",
        "gwas_pubmed_count",
        "gwas_trait_category_count",
        "gwas_mapped_trait_count",
    ]
    for column in count_columns:
        merged[column] = merged[column].fillna(0).astype(int)

    merged["complex_trait_evidence_status"] = merged["gwas_association_count"].map(
        lambda count: "gwas_trait_evidence_present"
        if count > 0
        else "no_gwas_trait_evidence_found"
    )
    merged["glycome_trait_flag"] = merged["gwas_trait_categories"].fillna("").str.contains(
        "glycome"
    ).map(yes_no)
    merged["immune_inflammation_trait_flag"] = (
        merged["gwas_trait_categories"].fillna("").str.contains("immune_inflammation").map(yes_no)
    )
    merged["infection_trait_flag"] = merged["gwas_trait_categories"].fillna("").str.contains(
        "infection"
    ).map(yes_no)
    merged["cancer_trait_flag"] = merged["gwas_trait_categories"].fillna("").str.contains(
        "cancer"
    ).map(yes_no)
    merged["tissue_identity_trait_flag"] = (
        merged["gwas_trait_categories"].fillna("").str.contains("tissue_identity").map(yes_no)
    )
    merged["disease_architecture_class"] = merged.apply(disease_class, axis=1)
    merged["disease_annotation_version"] = GWAS_LAYER_VERSION
    merged["disease_annotation_notes"] = merged.apply(
        lambda row: (
            f"{GWAS_NOTE_PATTERN.sub('', row['disease_annotation_notes'])} "
            f"GWAS Catalog layer: {row['gwas_association_count']} association(s), "
            f"{row['gwas_mapped_trait_count']} mapped trait(s), "
            f"categories {row['gwas_trait_categories'] or 'none'}, "
            f"accessed {GWAS_ACCESS_DATE}."
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
        "glycome_trait_flag",
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
            gwas_gene_count=(
                "complex_trait_evidence_status",
                lambda values: int((values == "gwas_trait_evidence_present").sum()),
            ),
            gwas_association_count=("gwas_association_count", "sum"),
            glycome_trait_gene_count=("glycome_trait_flag", lambda values: int((values == "yes").sum())),
            immune_inflammation_trait_gene_count=(
                "immune_inflammation_trait_flag",
                lambda values: int((values == "yes").sum()),
            ),
            infection_trait_gene_count=("infection_trait_flag", lambda values: int((values == "yes").sum())),
            cancer_trait_gene_count=("cancer_trait_flag", lambda values: int((values == "yes").sum())),
            tissue_identity_trait_gene_count=(
                "tissue_identity_trait_flag",
                lambda values: int((values == "yes").sum()),
            ),
        )
        .reset_index()
    )
    summary["cdg_seed_fraction"] = (
        summary["cdg_seed_gene_count"] / summary["gene_count"]
    ).round(4)
    summary["clinvar_plp_gene_fraction"] = (
        summary["clinvar_plp_gene_count"] / summary["gene_count"]
    ).round(4)
    summary["gwas_gene_fraction"] = (summary["gwas_gene_count"] / summary["gene_count"]).round(4)
    summary["median_clinvar_plp_variant_count"] = (
        summary["median_clinvar_plp_variant_count"].round(4)
    )
    summary.insert(0, "disease_annotation_version", GWAS_LAYER_VERSION)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add GWAS Catalog mapped/reported gene trait evidence."
    )
    parser.add_argument(
        "--annotations",
        default="data/processed/nglyco_disease_annotations.tsv",
        help="Input disease annotation TSV.",
    )
    parser.add_argument(
        "--gwas-catalog-zip",
        default="data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip",
        help="GWAS Catalog v1.0.2 associations zip.",
    )
    parser.add_argument(
        "--annotations-out",
        default="data/processed/nglyco_disease_annotations.tsv",
        help="Updated disease annotation TSV.",
    )
    parser.add_argument(
        "--gwas-counts-out",
        default="results/tables/gwas_catalog_gene_trait_counts.tsv",
        help="Compact per-gene GWAS Catalog count table.",
    )
    parser.add_argument(
        "--gwas-matches-out",
        default="results/tables/gwas_catalog_nglyco_matched_associations.tsv",
        help="Matched GWAS Catalog association table.",
    )
    parser.add_argument(
        "--summary-out",
        default="results/tables/disease_architecture_summary.tsv",
        help="Updated disease summary TSV.",
    )
    parser.add_argument("--chunksize", type=int, default=100_000)
    args = parser.parse_args()

    annotations = pd.read_csv(args.annotations, sep="\t")
    target_symbols = {symbol.upper() for symbol in annotations["symbol"]}
    counts, matched = summarize_gwas_catalog(args.gwas_catalog_zip, target_symbols, args.chunksize)
    updated = add_gwas_layer(annotations, counts)
    summary = build_summary(updated)

    Path(args.annotations_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.gwas_counts_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.gwas_matches_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary_out).parent.mkdir(parents=True, exist_ok=True)
    updated.to_csv(args.annotations_out, sep="\t", index=False)
    counts.to_csv(args.gwas_counts_out, sep="\t", index=False)
    matched.to_csv(args.gwas_matches_out, sep="\t", index=False)
    summary.to_csv(args.summary_out, sep="\t", index=False)

    print(f"Wrote {len(updated)} rows to {args.annotations_out}")
    print(f"Wrote {len(counts)} rows to {args.gwas_counts_out}")
    print(f"Wrote {len(matched)} rows to {args.gwas_matches_out}")
    print(f"Wrote {len(summary)} rows to {args.summary_out}")


if __name__ == "__main__":
    main()
