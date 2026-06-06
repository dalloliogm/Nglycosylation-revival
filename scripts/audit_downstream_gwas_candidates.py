#!/usr/bin/env python3
"""Audit downstream N-glycosylation GWAS candidates before gene-level storytelling."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


AUDIT_VERSION = "downstream_gwas_candidate_audit_v0.1_2026-06-06"

DOWNSTREAM_REGIONS = {
    "golgi_core_processing",
    "golgi_branching",
    "terminal_modification",
}

DIRECT_GLYCOME_TERMS = (
    "glycan",
    "glycome",
    "glycosylation",
    "n-glycan",
    "n glycan",
    "igg",
    "fucosylation",
    "fucosyltransferase",
    "galactosylation",
    "galactosyltransferase",
    "sialylation",
    "sialyltransferase",
    "mannosyl",
    "mannosidase",
    "acetylglucosaminyltransferase",
)

INTERFACE_TERMS = (
    "immune",
    "immunoglobulin",
    "antibody",
    "inflammation",
    "inflammatory",
    "infection",
    "virus",
    "viral",
    "cancer",
    "carcinoma",
    "tumor",
    "tumour",
    "neoplasm",
    "mucosal",
    "epithelial",
    "blood protein",
    "protein level",
)


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def trait_examples(rows: pd.DataFrame, limit: int = 5) -> str:
    examples: list[str] = []
    for row in rows.itertuples(index=False):
        disease_trait = str(row.disease_trait) if pd.notna(row.disease_trait) else ""
        mapped_trait = str(row.mapped_trait) if pd.notna(row.mapped_trait) else ""
        if mapped_trait and mapped_trait.lower() not in {"protein measurement", "blood protein amount"}:
            example = mapped_trait
        else:
            example = disease_trait or mapped_trait
        if example and example not in examples:
            examples.append(example)
        if len(examples) >= limit:
            break
    return "; ".join(examples)


def evidence_tier(row: pd.Series) -> str:
    if row["direct_glycome_association_count"] >= 3 and row["reported_direct_glycome_count"] >= 1:
        return "strong_candidate"
    if row["direct_glycome_association_count"] >= 1 and row["study_count"] >= 3:
        return "moderate_candidate"
    if row["interface_association_count"] >= 5 and row["reported_gene_association_count"] >= 1:
        return "interface_candidate"
    return "weak_or_broad_mapping"


def evidence_score(row: pd.Series) -> float:
    return round(
        row["direct_glycome_association_count"] * 4
        + row["reported_direct_glycome_count"] * 3
        + row["reported_gene_association_count"] * 1.5
        + row["interface_association_count"] * 0.5
        + min(row["pubmed_count"], 10) * 0.5
        + min(row["study_count"], 10) * 0.25,
        3,
    )


def build_audit(
    annotations: pd.DataFrame,
    counts: pd.DataFrame,
    matches: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    downstream = annotations[
        annotations["include_primary"].eq("yes")
        & annotations["primary_region"].isin(DOWNSTREAM_REGIONS)
    ][
        [
            "symbol",
            "primary_region",
            "analysis_group",
            "cdg_curated_status",
            "clinvar_evidence_status",
            "glycome_trait_flag",
            "immune_inflammation_trait_flag",
            "infection_trait_flag",
            "cancer_trait_flag",
            "tissue_identity_trait_flag",
        ]
    ].copy()

    downstream_symbols = set(downstream["symbol"])
    candidate_matches = matches[matches["symbol"].isin(downstream_symbols)].copy()
    candidate_matches["text_for_audit"] = (
        candidate_matches["disease_trait"].fillna("")
        + " "
        + candidate_matches["mapped_trait"].fillna("")
        + " "
        + candidate_matches["study_accession"].fillna("")
    )
    candidate_matches["direct_glycome_match"] = candidate_matches["text_for_audit"].map(
        lambda value: "yes" if contains_any(value, DIRECT_GLYCOME_TERMS) else "no"
    )
    candidate_matches["interface_match"] = candidate_matches["text_for_audit"].map(
        lambda value: "yes" if contains_any(value, INTERFACE_TERMS) else "no"
    )
    candidate_matches["reported_gene_match"] = candidate_matches["match_basis"].fillna("").str.contains(
        "reported_gene"
    ).map(lambda value: "yes" if value else "no")
    candidate_matches["mapped_gene_match"] = candidate_matches["match_basis"].fillna("").str.contains(
        "mapped_gene"
    ).map(lambda value: "yes" if value else "no")
    candidate_matches["p_value_numeric"] = pd.to_numeric(
        candidate_matches["p_value"], errors="coerce"
    )

    rows: list[dict[str, object]] = []
    for _, gene in downstream.iterrows():
        symbol = gene["symbol"]
        gene_matches = candidate_matches[candidate_matches["symbol"].eq(symbol)]
        direct = gene_matches[gene_matches["direct_glycome_match"].eq("yes")]
        interface = gene_matches[gene_matches["interface_match"].eq("yes")]
        reported = gene_matches[gene_matches["reported_gene_match"].eq("yes")]
        reported_direct = direct[direct["reported_gene_match"].eq("yes")]
        top_direct = direct.sort_values("p_value_numeric", na_position="last").head(5)
        top_any = gene_matches.sort_values("p_value_numeric", na_position="last").head(5)

        count_row = counts[counts["symbol"].eq(symbol)]
        gwas_association_count = int(count_row["gwas_association_count"].iloc[0]) if not count_row.empty else 0
        gwas_trait_categories = count_row["gwas_trait_categories"].iloc[0] if not count_row.empty else ""

        audit_row = {
            "audit_version": AUDIT_VERSION,
            "symbol": symbol,
            "primary_region": gene["primary_region"],
            "analysis_group": gene["analysis_group"],
            "cdg_curated_status": gene["cdg_curated_status"],
            "clinvar_evidence_status": gene["clinvar_evidence_status"],
            "gwas_association_count": gwas_association_count,
            "gwas_trait_categories": gwas_trait_categories,
            "direct_glycome_association_count": int(len(direct)),
            "reported_direct_glycome_count": int(len(reported_direct)),
            "interface_association_count": int(len(interface)),
            "reported_gene_association_count": int(len(reported)),
            "study_count": int(gene_matches["study_accession"].replace("NR", pd.NA).dropna().nunique()),
            "pubmed_count": int(gene_matches["pubmed_id"].replace("NR", pd.NA).dropna().nunique()),
            "min_p_value": gene_matches["p_value_numeric"].min(),
            "top_direct_glycome_traits": "; ".join(
                [trait_examples(top_direct)]
            ),
            "top_direct_glycome_studies": "; ".join(
                top_direct["study_accession"].dropna().astype(str).drop_duplicates().head(5)
            ),
            "top_any_traits": "; ".join(
                [trait_examples(top_any)]
            ),
            "audit_note": (
                "Prioritize reported-gene and direct glycome matches; mapped-gene-only associations require locus audit."
            ),
        }
        rows.append(audit_row)

    audit = pd.DataFrame(rows)
    audit["candidate_score"] = audit.apply(evidence_score, axis=1)
    audit["candidate_evidence_tier"] = audit.apply(evidence_tier, axis=1)
    audit = audit.sort_values(
        [
            "candidate_score",
            "direct_glycome_association_count",
            "reported_gene_association_count",
        ],
        ascending=[False, False, False],
    )

    prioritized_associations = candidate_matches[
        candidate_matches["direct_glycome_match"].eq("yes")
        | candidate_matches["interface_match"].eq("yes")
        | candidate_matches["reported_gene_match"].eq("yes")
    ].copy()
    prioritized_associations = prioritized_associations.sort_values(
        ["symbol", "direct_glycome_match", "reported_gene_match", "p_value_numeric"],
        ascending=[True, False, False, True],
        na_position="last",
    )
    output_columns = [
        "symbol",
        "match_basis",
        "direct_glycome_match",
        "interface_match",
        "reported_gene_match",
        "mapped_gene_match",
        "study_accession",
        "pubmed_id",
        "first_author",
        "publication_date",
        "disease_trait",
        "mapped_trait",
        "trait_categories",
        "reported_genes",
        "mapped_genes",
        "p_value",
    ]
    return audit, prioritized_associations[output_columns]


def write_report(audit: pd.DataFrame, output_report: str) -> None:
    tier_counts = audit["candidate_evidence_tier"].value_counts().to_dict()
    top = audit.head(10)
    lines = [
        "# Downstream GWAS Candidate Audit",
        "",
        "Date generated: 2026-06-06",
        "",
        "This audit ranks primary downstream N-glycosylation genes using the matched GWAS Catalog association table. It is designed to select examples for manuscript text, not to prove causal locus-to-gene assignments.",
        "",
        "## Evidence Rules",
        "",
        "- Stronger evidence: direct glycome/glycosylation trait text and a reported-gene match.",
        "- Moderate evidence: repeated direct glycome matches across multiple studies.",
        "- Weaker evidence: broad interface categories or mapped-gene-only assignments.",
        "- All candidates still require locus-level review before causal language.",
        "",
        "## Tier Counts",
        "",
    ]
    for tier in ["strong_candidate", "moderate_candidate", "interface_candidate", "weak_or_broad_mapping"]:
        lines.append(f"- {tier}: {tier_counts.get(tier, 0)}")

    lines.extend(["", "## Top Candidates", ""])
    for row in top.itertuples(index=False):
        lines.append(
            f"- `{row.symbol}` ({row.primary_region}): {row.candidate_evidence_tier}, "
            f"score {row.candidate_score}; direct glycome associations {row.direct_glycome_association_count}; "
            f"reported direct glycome {row.reported_direct_glycome_count}; examples: {row.top_direct_glycome_traits or 'none'}."
        )

    lines.extend(
        [
            "",
            "## Claim Limit",
            "",
            "Use this table to choose gene examples for closer inspection. Do not claim that a GWAS Catalog mapped gene is causal without fine-mapping, colocalization, coding, eQTL, or functional evidence.",
        ]
    )
    Path(output_report).parent.mkdir(parents=True, exist_ok=True)
    Path(output_report).write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit downstream GWAS/glycome candidates for manuscript examples."
    )
    parser.add_argument(
        "--annotations",
        default="data/processed/nglyco_disease_annotations.tsv",
        help="Disease annotation TSV.",
    )
    parser.add_argument(
        "--gwas-counts",
        default="results/tables/gwas_catalog_gene_trait_counts.tsv",
        help="Per-gene GWAS count TSV.",
    )
    parser.add_argument(
        "--gwas-matches",
        default="results/tables/gwas_catalog_nglyco_matched_associations.tsv",
        help="Matched GWAS association TSV.",
    )
    parser.add_argument(
        "--audit-out",
        default="results/tables/downstream_gwas_candidate_audit.tsv",
        help="Output downstream candidate audit TSV.",
    )
    parser.add_argument(
        "--associations-out",
        default="results/tables/downstream_gwas_candidate_associations.tsv",
        help="Output prioritized downstream candidate associations TSV.",
    )
    parser.add_argument(
        "--report-out",
        default="results/reports/downstream-gwas-candidate-audit.md",
        help="Output audit report.",
    )
    args = parser.parse_args()

    annotations = pd.read_csv(args.annotations, sep="\t")
    counts = pd.read_csv(args.gwas_counts, sep="\t")
    matches = pd.read_csv(args.gwas_matches, sep="\t")
    audit, associations = build_audit(annotations, counts, matches)

    Path(args.audit_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.associations_out).parent.mkdir(parents=True, exist_ok=True)
    audit.to_csv(args.audit_out, sep="\t", index=False)
    associations.to_csv(args.associations_out, sep="\t", index=False)
    write_report(audit, args.report_out)

    print(f"Wrote {len(audit)} rows to {args.audit_out}")
    print(f"Wrote {len(associations)} rows to {args.associations_out}")
    print(f"Wrote {args.report_out}")


if __name__ == "__main__":
    main()
