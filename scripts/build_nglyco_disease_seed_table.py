#!/usr/bin/env python3
"""Build a first-pass CDG disease seed table for N-glycosylation genes."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DISEASE_ANNOTATION_VERSION = "cdg_seed_genereviews_v0.1_2026-06-03"
SOURCE_NAME = "GeneReviews CDG N-linked and multiple-pathway overview"
SOURCE_URL = "https://www.ncbi.nlm.nih.gov/books/NBK1332/"
SOURCE_ACCESS_DATE = "2026-06-03"


CURATED_CDG: dict[str, dict[str, str]] = {
    "PMM2": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "PMM2-CDG (CDG-Ia)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "MPI": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "MPI-CDG (CDG-Ib)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "moderate",
    },
    "ALG6": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG6-CDG (CDG-Ic)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "ALG3": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG3-CDG (CDG-Id)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "DPM1": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "DPM1-CDG (CDG-Ie)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "MPDU1": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "MPDU1-CDG (CDG-If)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "ALG12": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG12-CDG (CDG-Ig)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "ALG8": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG8-CDG (CDG-Ih)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "ALG2": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG2-CDG (CDG-Ii)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "DPAGT1": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "DPAGT1-CDG (CDG-Ij)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "ALG1": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG1-CDG (CDG-Ik)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "ALG9": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG9-CDG (CDG-IL)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "DOLK": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "DOLK-CDG (CDG-Im)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "RFT1": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "RFT1-CDG (CDG-In)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "DPM3": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "DPM3-CDG (CDG-Io)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "moderate",
    },
    "ALG11": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG11-CDG (CDG-Ip)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "SRD5A3": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "SRD5A3-CDG (CDG-Iq)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "DDOST": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "DDOST-CDG (CDG-Ir)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "MAGT1": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "MAGT1-CDG",
        "mode_of_inheritance": "XL",
        "severe_mendelian_burden": "moderate",
    },
    "TUSC3": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "TUSC3-CDG",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "moderate",
    },
    "ALG13": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "ALG13-CDG",
        "mode_of_inheritance": "XL",
        "severe_mendelian_burden": "high",
    },
    "STT3A": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "STT3A-CDG",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "STT3B": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "STT3B-CDG",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "MGAT2": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "MGAT2-CDG (CDG-IIa)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "MOGS": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "MOGS-CDG (CDG-IIb)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "SLC35C1": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "SLC35C1-CDG (CDG-IIc)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "B4GALT1": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "B4GALT1-CDG (CDG-IId)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "moderate",
    },
    "GMPPA": {
        "cdg_curated_status": "known_cdg_gene",
        "cdg_subtype": "GMPPA-CDG",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "moderate",
    },
    "SLC35A1": {
        "cdg_curated_status": "overlapping_or_multiple_pathway_cdg_gene",
        "cdg_subtype": "SLC35A1-CDG (CDG-IIf)",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "DPM2": {
        "cdg_curated_status": "overlapping_or_multiple_pathway_cdg_gene",
        "cdg_subtype": "DPM2-CDG",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "DHDDS": {
        "cdg_curated_status": "overlapping_or_multiple_pathway_cdg_gene",
        "cdg_subtype": "DHDDS-CDG",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
    "MAN1B1": {
        "cdg_curated_status": "overlapping_or_multiple_pathway_cdg_gene",
        "cdg_subtype": "MAN1B1-CDG",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "moderate",
    },
    "PGM3": {
        "cdg_curated_status": "overlapping_or_multiple_pathway_cdg_gene",
        "cdg_subtype": "PGM3-CDG",
        "mode_of_inheritance": "AR",
        "severe_mendelian_burden": "high",
    },
}


def disease_class(row: pd.Series) -> str:
    if row["cdg_curated_status"] == "not_cdg_gene":
        return "no_current_disease_signal"
    if row["primary_region"] == "er_quality_control":
        return "checkpoint_or_quality_control_disease"
    if row["severe_mendelian_burden"] in {"high", "moderate"}:
        return "severe_mendelian_core"
    return "uncertain"


def annotation_notes(row: pd.Series) -> str:
    if row["cdg_curated_status"] == "not_cdg_gene":
        return (
            "Not listed in first-pass GeneReviews CDG seed curation; "
            "ClinVar and GWAS evidence not assessed in this version."
        )

    status = row["cdg_curated_status"].replace("_", " ")
    return (
        f"{status}; subtype {row['cdg_subtype']}; mode {row['mode_of_inheritance']}; "
        f"source {SOURCE_NAME}, accessed {SOURCE_ACCESS_DATE}; "
        "ClinVar and GWAS evidence not assessed in this version."
    )


def build_annotations(features: pd.DataFrame) -> pd.DataFrame:
    annotations = features[
        [
            "symbol",
            "ensembl_gene_id",
            "primary_region",
            "analysis_group",
            "include_primary",
            "include_sensitivity",
        ]
    ].copy()

    annotations["cdg_curated_status"] = "not_cdg_gene"
    annotations["cdg_subtype"] = ""
    annotations["mendelian_disease_status"] = "no_curated_cdg_mendelian_seed_evidence"
    annotations["mode_of_inheritance"] = ""
    annotations["severe_mendelian_burden"] = "low"

    for symbol, fields in CURATED_CDG.items():
        mask = annotations["symbol"].eq(symbol)
        for column, value in fields.items():
            annotations.loc[mask, column] = value
        annotations.loc[mask, "mendelian_disease_status"] = "curated_cdg_mendelian_evidence"

    annotations["clinvar_plp_variant_count"] = 0
    annotations["clinvar_plp_condition_count"] = 0
    annotations["clinvar_evidence_status"] = "not_assessed"
    annotations["gwas_association_count"] = 0
    annotations["gwas_trait_category_count"] = 0
    annotations["immune_inflammation_trait_flag"] = "not_assessed"
    annotations["infection_trait_flag"] = "not_assessed"
    annotations["cancer_trait_flag"] = "not_assessed"
    annotations["tissue_identity_trait_flag"] = "not_assessed"
    annotations["complex_trait_evidence_status"] = "not_assessed"
    annotations["disease_architecture_class"] = annotations.apply(disease_class, axis=1)
    annotations["evidence_confidence"] = annotations["cdg_curated_status"].map(
        {
            "known_cdg_gene": "high",
            "overlapping_or_multiple_pathway_cdg_gene": "high",
            "not_cdg_gene": "first_pass_genereviews_only",
        }
    )
    annotations["disease_annotation_version"] = DISEASE_ANNOTATION_VERSION
    annotations["disease_annotation_source"] = SOURCE_NAME
    annotations["disease_annotation_source_url"] = SOURCE_URL
    annotations["disease_annotation_access_date"] = SOURCE_ACCESS_DATE
    annotations["disease_annotation_notes"] = annotations.apply(annotation_notes, axis=1)

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
    return annotations[output_columns]


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
        )
        .reset_index()
    )
    summary["cdg_seed_fraction"] = (
        summary["cdg_seed_gene_count"] / summary["gene_count"]
    ).round(4)
    summary.insert(0, "disease_annotation_version", DISEASE_ANNOTATION_VERSION)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build first-pass CDG seed annotations from GeneReviews."
    )
    parser.add_argument(
        "--architecture-features",
        default="data/processed/nglyco_architecture_features.tsv",
        help="Input architecture feature table TSV.",
    )
    parser.add_argument(
        "--annotations-out",
        default="data/processed/nglyco_disease_annotations.tsv",
        help="Output disease annotation TSV.",
    )
    parser.add_argument(
        "--summary-out",
        default="results/tables/disease_architecture_summary.tsv",
        help="Output disease summary TSV.",
    )
    args = parser.parse_args()

    features = pd.read_csv(args.architecture_features, sep="\t")
    annotations = build_annotations(features)
    summary = build_summary(annotations)

    Path(args.annotations_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary_out).parent.mkdir(parents=True, exist_ok=True)
    annotations.to_csv(args.annotations_out, sep="\t", index=False)
    summary.to_csv(args.summary_out, sep="\t", index=False)

    print(f"Wrote {len(annotations)} rows to {args.annotations_out}")
    print(f"Wrote {len(summary)} rows to {args.summary_out}")


if __name__ == "__main__":
    main()
