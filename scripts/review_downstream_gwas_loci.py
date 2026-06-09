#!/usr/bin/env python3
"""Create locus-level review packets for strong downstream GWAS candidates."""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path

import pandas as pd


REVIEW_VERSION = "downstream_gwas_locus_review_v0.1_2026-06-06"

USE_COLUMNS = [
    "PUBMEDID",
    "FIRST AUTHOR",
    "DATE",
    "STUDY",
    "DISEASE/TRAIT",
    "REGION",
    "CHR_ID",
    "CHR_POS",
    "REPORTED GENE(S)",
    "MAPPED_GENE",
    "UPSTREAM_GENE_ID",
    "DOWNSTREAM_GENE_ID",
    "SNP_GENE_IDS",
    "UPSTREAM_GENE_DISTANCE",
    "DOWNSTREAM_GENE_DISTANCE",
    "STRONGEST SNP-RISK ALLELE",
    "SNPS",
    "CONTEXT",
    "INTERGENIC",
    "P-VALUE",
    "MAPPED_TRAIT",
    "STUDY ACCESSION",
]

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


def split_gene_field(value: object) -> set[str]:
    if not isinstance(value, str) or not value.strip() or value.strip() == "NR":
        return set()
    text = value.upper()
    text = re.sub(r"\bINTERGENIC\b", " ", text)
    tokens = re.split(r"[^A-Z0-9]+", text)
    return {token for token in tokens if token}


def contains_direct_glycome(*values: object) -> bool:
    text = " ".join(str(value).lower() for value in values if isinstance(value, str))
    return any(term in text for term in DIRECT_GLYCOME_TERMS)


def locus_risk(
    symbol: str,
    reported_genes: object,
    mapped_genes: object,
    intergenic: object,
) -> str:
    reported = split_gene_field(reported_genes)
    mapped = split_gene_field(mapped_genes)
    is_intergenic = str(intergenic).strip() == "1"

    if symbol in reported and not is_intergenic:
        return "lower_reported_gene_match"
    if symbol in reported:
        return "moderate_reported_but_intergenic"
    if symbol in mapped and len(mapped) <= 2 and not is_intergenic:
        return "moderate_mapped_gene_match"
    if symbol in mapped:
        return "higher_mapped_multi_gene_or_intergenic"
    return "higher_unclear_gene_assignment"


def match_basis(symbol: str, reported_genes: object, mapped_genes: object) -> str:
    basis: list[str] = []
    if symbol in split_gene_field(reported_genes):
        basis.append("reported_gene")
    if symbol in split_gene_field(mapped_genes):
        basis.append("mapped_gene")
    return ";".join(basis)


def review_loci(
    gwas_zip_path: str,
    candidate_symbols: set[str],
    chunksize: int,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
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
                            region,
                            chr_id,
                            chr_pos,
                            reported_genes,
                            mapped_genes,
                            upstream_gene_id,
                            downstream_gene_id,
                            snp_gene_ids,
                            upstream_gene_distance,
                            downstream_gene_distance,
                            strongest_snp_risk_allele,
                            snps,
                            context,
                            intergenic,
                            p_value,
                            mapped_trait,
                            study_accession,
                        ) = row
                        if not contains_direct_glycome(disease_trait, mapped_trait, study):
                            continue
                        reported = split_gene_field(reported_genes)
                        mapped = split_gene_field(mapped_genes)
                        matched = (reported | mapped) & candidate_symbols
                        if not matched:
                            continue

                        for symbol in matched:
                            rows.append(
                                {
                                    "review_version": REVIEW_VERSION,
                                    "symbol": symbol,
                                    "match_basis": match_basis(symbol, reported_genes, mapped_genes),
                                    "locus_assignment_risk": locus_risk(
                                        symbol, reported_genes, mapped_genes, intergenic
                                    ),
                                    "study_accession": study_accession,
                                    "pubmed_id": pubmed_id,
                                    "first_author": first_author,
                                    "publication_date": publication_date,
                                    "disease_trait": disease_trait,
                                    "mapped_trait": mapped_trait,
                                    "region": region,
                                    "chr_id": chr_id,
                                    "chr_pos": chr_pos,
                                    "snps": snps,
                                    "strongest_snp_risk_allele": strongest_snp_risk_allele,
                                    "context": context,
                                    "intergenic": intergenic,
                                    "reported_genes": reported_genes,
                                    "mapped_genes": mapped_genes,
                                    "snp_gene_ids": snp_gene_ids,
                                    "upstream_gene_id": upstream_gene_id,
                                    "upstream_gene_distance": upstream_gene_distance,
                                    "downstream_gene_id": downstream_gene_id,
                                    "downstream_gene_distance": downstream_gene_distance,
                                    "p_value": p_value,
                                }
                            )

    review = pd.DataFrame(rows)
    if review.empty:
        return review

    review["p_value_numeric"] = pd.to_numeric(review["p_value"], errors="coerce")
    return review.sort_values(
        ["symbol", "locus_assignment_risk", "p_value_numeric"],
        ascending=[True, True, True],
        na_position="last",
    )


def summarize_review(review: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for symbol, group in review.groupby("symbol", sort=True):
        lower = group[group["locus_assignment_risk"].eq("lower_reported_gene_match")]
        moderate = group[group["locus_assignment_risk"].str.startswith("moderate")]
        higher = group[group["locus_assignment_risk"].str.startswith("higher")]
        top = group.sort_values("p_value_numeric", na_position="last").head(5)
        rows.append(
            {
                "review_version": REVIEW_VERSION,
                "symbol": symbol,
                "direct_glycome_locus_count": int(len(group)),
                "reported_gene_locus_count": int(group["match_basis"].str.contains("reported_gene").sum()),
                "distinct_study_count": int(group["study_accession"].replace("NR", pd.NA).dropna().nunique()),
                "distinct_pubmed_count": int(group["pubmed_id"].replace("NR", pd.NA).dropna().nunique()),
                "lower_risk_locus_count": int(len(lower)),
                "moderate_risk_locus_count": int(len(moderate)),
                "higher_risk_locus_count": int(len(higher)),
                "min_p_value": group["p_value_numeric"].min(),
                "top_locus_traits": "; ".join(
                    top["mapped_trait"].dropna().astype(str).drop_duplicates().head(5)
                ),
                "top_locus_snps": "; ".join(
                    top["snps"].dropna().astype(str).drop_duplicates().head(5)
                ),
                "locus_review_note": (
                    "Lower-risk rows have reported-gene support; higher-risk rows are mapped-gene or multi-gene/intergenic and need manual locus review."
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["lower_risk_locus_count", "direct_glycome_locus_count"], ascending=False
    )


def write_report(summary: pd.DataFrame, output_report: str) -> None:
    lines = [
        "# Downstream GWAS Locus Review",
        "",
        "Date generated: 2026-06-06",
        "",
        "This review extracts SNP, region, and nearby-gene context for strong downstream glycome GWAS candidates. It is a triage artifact for choosing manuscript examples, not a final causal assignment.",
        "",
        "## Candidate Summary",
        "",
    ]
    for row in summary.itertuples(index=False):
        lines.append(
            f"- `{row.symbol}`: {row.direct_glycome_locus_count} direct glycome locus rows; "
            f"{row.reported_gene_locus_count} reported-gene rows; "
            f"risk counts lower/moderate/higher = {row.lower_risk_locus_count}/"
            f"{row.moderate_risk_locus_count}/{row.higher_risk_locus_count}; "
            f"top traits: {row.top_locus_traits or 'none'}."
        )

    lines.extend(
        [
            "",
            "## Use In Manuscript",
            "",
            "Best near-term examples are genes with many direct glycome rows and substantial reported-gene support, especially `FUT8`, `ST6GAL1`, `MGAT3`, `B4GALT1`, `FUT3`, `MGAT5`, and `ST3GAL4`.",
            "",
            "## Claim Limit",
            "",
            "Even lower-risk rows are association evidence. Causal language still requires fine-mapping, colocalization, coding evidence, eQTL support, or functional validation.",
        ]
    )
    Path(output_report).parent.mkdir(parents=True, exist_ok=True)
    Path(output_report).write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Review loci for strong downstream GWAS/glycome candidates."
    )
    parser.add_argument(
        "--candidate-audit",
        default="results/tables/downstream_gwas_candidate_audit.tsv",
        help="Downstream candidate audit TSV.",
    )
    parser.add_argument(
        "--gwas-catalog-zip",
        default="data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip",
        help="GWAS Catalog v1.0.2 associations zip.",
    )
    parser.add_argument(
        "--loci-out",
        default="results/tables/downstream_gwas_locus_review.tsv",
        help="Output locus review TSV.",
    )
    parser.add_argument(
        "--summary-out",
        default="results/tables/downstream_gwas_locus_review_summary.tsv",
        help="Output per-candidate locus summary TSV.",
    )
    parser.add_argument(
        "--report-out",
        default="results/reports/downstream-gwas-locus-review.md",
        help="Output locus review report.",
    )
    parser.add_argument("--chunksize", type=int, default=100_000)
    args = parser.parse_args()

    audit = pd.read_csv(args.candidate_audit, sep="\t")
    candidate_symbols = set(
        audit.loc[audit["candidate_evidence_tier"].eq("strong_candidate"), "symbol"].str.upper()
    )
    review = review_loci(args.gwas_catalog_zip, candidate_symbols, args.chunksize)
    summary = summarize_review(review)

    Path(args.loci_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary_out).parent.mkdir(parents=True, exist_ok=True)
    review.to_csv(args.loci_out, sep="\t", index=False)
    summary.to_csv(args.summary_out, sep="\t", index=False)
    write_report(summary, args.report_out)

    print(f"Wrote {len(review)} rows to {args.loci_out}")
    print(f"Wrote {len(summary)} rows to {args.summary_out}")
    print(f"Wrote {args.report_out}")


if __name__ == "__main__":
    main()
