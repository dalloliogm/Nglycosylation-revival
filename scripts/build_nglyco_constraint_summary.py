#!/usr/bin/env python3
"""Join gene-level constraint metrics to N-glycosylation architecture features."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


LOEUF_CONSTRAINED_THRESHOLD = 0.45


def first_existing_column(columns: set[str], candidates: tuple[str, ...]) -> str | None:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None


def normalize_constraint_metrics(metrics: pd.DataFrame) -> pd.DataFrame:
    columns = set(metrics.columns)
    mapping = {
        "constraint_symbol": first_existing_column(columns, ("gene", "symbol", "gene_symbol")),
        "constraint_ensembl_gene_id": first_existing_column(
            columns, ("gene_id", "ensg", "ensembl_gene_id")
        ),
        "constraint_transcript": first_existing_column(columns, ("transcript", "transcript_id")),
        "constraint_flags": first_existing_column(columns, ("constraint_flags", "flags")),
        "gene_flags": first_existing_column(columns, ("gene_flags",)),
        "cds_length": first_existing_column(columns, ("cds_length", "cds_len")),
        "num_coding_exons": first_existing_column(columns, ("num_coding_exons",)),
        "loeuf": first_existing_column(
            columns, ("lof.oe_ci.upper", "lof_hc_lc.oe_ci.upper", "oe_lof_upper", "loeuf")
        ),
        "oe_lof": first_existing_column(columns, ("lof.oe", "lof_hc_lc.oe", "oe_lof")),
        "oe_lof_lower": first_existing_column(
            columns, ("lof.oe_ci.lower", "lof_hc_lc.oe_ci.lower", "oe_lof_lower")
        ),
        "oe_lof_upper": first_existing_column(
            columns, ("lof.oe_ci.upper", "lof_hc_lc.oe_ci.upper", "oe_lof_upper", "loeuf")
        ),
        "pLI": first_existing_column(columns, ("lof.pLI", "lof_hc_lc.pLI", "pLI", "pli")),
        "mis_z": first_existing_column(columns, ("mis.z_score", "mis_z", "mis.z")),
        "oe_mis": first_existing_column(columns, ("mis.oe", "oe_mis")),
        "oe_mis_lower": first_existing_column(columns, ("mis.oe_ci.lower", "oe_mis_lower")),
        "oe_mis_upper": first_existing_column(columns, ("mis.oe_ci.upper", "oe_mis_upper")),
        "syn_z": first_existing_column(columns, ("syn.z_score", "syn_z", "syn.z")),
        "oe_syn": first_existing_column(columns, ("syn.oe", "oe_syn")),
    }
    required = ["constraint_symbol", "constraint_ensembl_gene_id", "loeuf"]
    missing_required = [name for name in required if mapping[name] is None]
    if missing_required:
        raise ValueError(
            "Constraint metrics file is missing required columns or aliases: "
            + ", ".join(missing_required)
        )

    normalized = pd.DataFrame()
    for output_column, input_column in mapping.items():
        normalized[output_column] = metrics[input_column] if input_column else pd.NA

    normalized["constraint_ensembl_gene_id"] = (
        normalized["constraint_ensembl_gene_id"].astype(str).str.split(".").str[0]
    )
    for column in [
        "cds_length",
        "num_coding_exons",
        "loeuf",
        "oe_lof",
        "oe_lof_lower",
        "oe_lof_upper",
        "pLI",
        "mis_z",
        "oe_mis",
        "oe_mis_lower",
        "oe_mis_upper",
        "syn_z",
        "oe_syn",
    ]:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce")

    normalized = normalized.sort_values(
        ["constraint_ensembl_gene_id", "constraint_transcript"], na_position="last"
    )
    return normalized.drop_duplicates("constraint_ensembl_gene_id", keep="first")


def join_constraint(features: pd.DataFrame, metrics: pd.DataFrame, dataset_version: str) -> pd.DataFrame:
    joined = features.merge(
        metrics,
        left_on="ensembl_gene_id",
        right_on="constraint_ensembl_gene_id",
        how="left",
    )
    symbol_match = joined["symbol"].eq(joined["constraint_symbol"])
    has_constraint = joined["loeuf"].notna()
    joined["constraint_dataset_version"] = dataset_version
    joined["constraint_metric_available"] = has_constraint.map(lambda value: "yes" if value else "no")
    joined["loeuf_constrained_threshold"] = LOEUF_CONSTRAINED_THRESHOLD
    joined["is_loeuf_constrained"] = (
        (joined["loeuf"] <= LOEUF_CONSTRAINED_THRESHOLD)
        .where(has_constraint, pd.NA)
        .map(lambda value: "yes" if value is True else ("no" if value is False else "missing"))
    )
    joined["join_status"] = "missing_constraint"
    joined.loc[has_constraint & symbol_match, "join_status"] = "matched_ensembl_symbol"
    joined.loc[has_constraint & ~symbol_match, "join_status"] = "matched_ensembl_symbol_mismatch"
    joined["join_notes"] = ""
    joined.loc[
        joined["join_status"].eq("matched_ensembl_symbol_mismatch"),
        "join_notes",
    ] = (
        "Ensembl ID matched but repository symbol differs from constraint file symbol: "
        + joined["symbol"].astype(str)
        + " vs "
        + joined["constraint_symbol"].astype(str)
    )
    joined.loc[
        joined["join_status"].eq("missing_constraint"),
        "join_notes",
    ] = "No constraint metrics matched by Ensembl gene ID."
    return joined


def write_join_audit(joined: pd.DataFrame, output_path: Path) -> None:
    audit = joined[
        [
            "symbol",
            "ensembl_gene_id",
            "constraint_ensembl_gene_id",
            "constraint_symbol",
            "constraint_metric_available",
            "join_status",
            "join_notes",
        ]
    ].rename(columns={"ensembl_gene_id": "ensembl_gene_id_repo"})
    audit.to_csv(output_path, sep="\t", index=False)


def write_constraint_table(joined: pd.DataFrame, output_path: Path) -> None:
    columns = [
        "symbol",
        "ensembl_gene_id",
        "primary_region",
        "analysis_group",
        "include_primary",
        "include_sensitivity",
        "curation_confidence",
        "pathway_depth_rank",
        "checkpoint_proximity",
        "catastrophic_potential_prior",
        "branching_role",
        "terminal_modification_role",
        "interface_layer_prior",
        "glycan_output_layer",
        "low_specificity_terminal_enzyme",
        "constraint_dataset_version",
        "constraint_metric_available",
        "constraint_symbol",
        "constraint_transcript",
        "constraint_flags",
        "gene_flags",
        "cds_length",
        "num_coding_exons",
        "loeuf",
        "oe_lof",
        "oe_lof_lower",
        "oe_lof_upper",
        "pLI",
        "mis_z",
        "oe_mis",
        "oe_mis_lower",
        "oe_mis_upper",
        "syn_z",
        "oe_syn",
        "loeuf_constrained_threshold",
        "is_loeuf_constrained",
        "join_status",
        "join_notes",
    ]
    joined[columns].to_csv(output_path, sep="\t", index=False)


def summarize(joined: pd.DataFrame) -> pd.DataFrame:
    available = joined[joined["constraint_metric_available"].eq("yes")].copy()
    if available.empty:
        return pd.DataFrame(
            columns=[
                "constraint_dataset_version",
                "analysis_group",
                "primary_region",
                "gene_count",
                "constraint_metric_available_count",
                "median_loeuf",
                "iqr_loeuf",
                "median_mis_z",
                "loeuf_constrained_count",
                "loeuf_constrained_fraction",
            ]
        )

    summary = (
        available.groupby(["constraint_dataset_version", "analysis_group", "primary_region"])
        .agg(
            gene_count=("symbol", "count"),
            constraint_metric_available_count=("constraint_metric_available", "count"),
            median_loeuf=("loeuf", "median"),
            q1_loeuf=("loeuf", lambda values: values.quantile(0.25)),
            q3_loeuf=("loeuf", lambda values: values.quantile(0.75)),
            median_mis_z=("mis_z", "median"),
            loeuf_constrained_count=(
                "is_loeuf_constrained",
                lambda values: int((values == "yes").sum()),
            ),
        )
        .reset_index()
    )
    summary["iqr_loeuf"] = (summary["q3_loeuf"] - summary["q1_loeuf"]).round(4)
    summary["loeuf_constrained_fraction"] = (
        summary["loeuf_constrained_count"]
        / summary["constraint_metric_available_count"]
    ).round(4)
    for column in ["median_loeuf", "q1_loeuf", "q3_loeuf", "median_mis_z"]:
        summary[column] = summary[column].round(4)
    return summary.drop(columns=["q1_loeuf", "q3_loeuf"])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build N-glycosylation constraint tables from a local gnomAD metrics TSV."
    )
    parser.add_argument(
        "--architecture-features",
        default="data/processed/nglyco_architecture_features.tsv",
        help="Input architecture feature TSV.",
    )
    parser.add_argument(
        "--constraint-metrics",
        required=True,
        help="Local gnomAD-like gene constraint metrics TSV.",
    )
    parser.add_argument(
        "--dataset-version",
        required=True,
        help="Dataset version label to record in outputs, e.g. gnomAD_v4.1.1.",
    )
    parser.add_argument(
        "--constraint-table-out",
        default="data/processed/nglyco_constraint_metrics.tsv",
        help="Output joined per-gene constraint TSV.",
    )
    parser.add_argument(
        "--join-audit-out",
        default="results/tables/constraint_join_audit.tsv",
        help="Output join audit TSV.",
    )
    parser.add_argument(
        "--summary-out",
        default="results/tables/constraint_summary.tsv",
        help="Output group summary TSV.",
    )
    args = parser.parse_args()

    features = pd.read_csv(args.architecture_features, sep="\t")
    raw_metrics = pd.read_csv(args.constraint_metrics, sep="\t", low_memory=False)
    normalized_metrics = normalize_constraint_metrics(raw_metrics)
    joined = join_constraint(features, normalized_metrics, args.dataset_version)

    for output in [
        args.constraint_table_out,
        args.join_audit_out,
        args.summary_out,
    ]:
        Path(output).parent.mkdir(parents=True, exist_ok=True)

    write_constraint_table(joined, Path(args.constraint_table_out))
    write_join_audit(joined, Path(args.join_audit_out))
    summarize(joined).to_csv(args.summary_out, sep="\t", index=False)

    matched = int(joined["constraint_metric_available"].eq("yes").sum())
    print(f"Input genes: {len(joined)}")
    print(f"Matched constraint metrics: {matched}")
    print(f"Wrote {args.constraint_table_out}")
    print(f"Wrote {args.join_audit_out}")
    print(f"Wrote {args.summary_out}")


if __name__ == "__main__":
    main()
