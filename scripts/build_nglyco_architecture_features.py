#!/usr/bin/env python3
"""Build first-pass architecture features for the N-glycosylation gene table."""

from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx
import pandas as pd


ARCHITECTURE_VERSION = "architecture_features_v0.1_2026-06-03"

DEPTH_BY_REGION = {
    "substrate_biosynthesis": 1,
    "llo_assembly": 2,
    "ost_transfer": 3,
    "er_quality_control": 4,
    "golgi_core_processing": 5,
    "golgi_branching": 6,
    "terminal_modification": 7,
}

FAMILY_PREFIXES = (
    "ALG",
    "B3GNT",
    "B4GALT",
    "DPM",
    "EDEM",
    "FUT",
    "GFPT",
    "GMP",
    "MAN1",
    "MAN2",
    "MGAT",
    "OST",
    "PMM",
    "SLC35",
    "ST3GAL",
    "ST6GAL",
    "UGGT",
)

PRIMARY_REACTION_EDGE_CLASSES = {
    "metabolite_intermediate",
    "glycoprotein_intermediate",
    "quality_control_cycle",
    "complex_or_binding_context",
}


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def family_name(symbol: str) -> str:
    for prefix in sorted(FAMILY_PREFIXES, key=len, reverse=True):
        if symbol.startswith(prefix):
            return prefix
    return ""


def redundancy_prior(family: str, analysis_group: str, primary_region: str) -> str:
    if not family:
        return "low" if analysis_group in {"upstream_core", "checkpoint_layer"} else "unknown"
    if primary_region in {"terminal_modification", "golgi_branching"}:
        return "high"
    if analysis_group == "downstream_diversification":
        return "moderate"
    if family in {"ALG", "OST"}:
        return "low"
    return "moderate"


def checkpoint_proximity(primary_region: str, analysis_group: str) -> str:
    if primary_region == "er_quality_control":
        return "direct"
    if primary_region == "ost_transfer":
        return "adjacent"
    if analysis_group == "substrate_support":
        return "not_applicable"
    return "distant"


def catastrophic_prior(primary_region: str, analysis_group: str) -> str:
    if primary_region in {"llo_assembly", "ost_transfer", "er_quality_control"}:
        return "high"
    if primary_region == "golgi_core_processing":
        return "moderate"
    if primary_region in {"golgi_branching", "terminal_modification"}:
        return "low"
    if analysis_group == "substrate_support":
        return "unknown"
    return "unknown"


def branching_role(primary_region: str, analysis_group: str) -> str:
    if primary_region == "golgi_branching":
        return "branch_initiation"
    if primary_region == "terminal_modification":
        return "branch_extension"
    if analysis_group == "substrate_support":
        return "unknown"
    return "not_branching"


def interface_prior(primary_region: str, analysis_group: str) -> str:
    if primary_region == "terminal_modification":
        return "high"
    if primary_region in {"golgi_branching", "golgi_core_processing"}:
        return "moderate"
    if analysis_group in {"upstream_core", "checkpoint_layer"}:
        return "low"
    return "unknown"


def low_specificity_terminal(symbol: str, primary_region: str) -> str:
    low_specificity_prefixes = ("B4GALT", "B3GNT", "FUT", "ST3GAL", "ST6GAL")
    return yes_no(primary_region == "terminal_modification" and symbol.startswith(low_specificity_prefixes))


def build_primary_reaction_graph(edges: pd.DataFrame, symbols: list[str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_nodes_from(symbols)
    primary_edges = edges[edges["edge_class"].isin(PRIMARY_REACTION_EDGE_CLASSES)]
    graph.add_edges_from(zip(primary_edges["source_gene"], primary_edges["target_gene"]))
    return graph


def graph_metrics(graph: nx.DiGraph) -> pd.DataFrame:
    in_degree = dict(graph.in_degree())
    out_degree = dict(graph.out_degree())
    total_degree = {node: in_degree[node] + out_degree[node] for node in graph.nodes}
    betweenness = nx.betweenness_centrality(graph)
    closeness = nx.closeness_centrality(graph)

    weak_components: dict[str, str] = {}
    for index, component in enumerate(nx.weakly_connected_components(graph), start=1):
        component_id = f"primary_reaction_component_{index}"
        for node in component:
            weak_components[node] = component_id

    return pd.DataFrame(
        {
            "symbol": list(graph.nodes),
            "graph_in_degree_primary_reaction": [in_degree[node] for node in graph.nodes],
            "graph_out_degree_primary_reaction": [out_degree[node] for node in graph.nodes],
            "graph_total_degree_primary_reaction": [total_degree[node] for node in graph.nodes],
            "graph_betweenness_primary_reaction": [betweenness[node] for node in graph.nodes],
            "graph_closeness_primary_reaction": [closeness[node] for node in graph.nodes],
            "graph_component_id_primary_reaction": [
                weak_components[node] for node in graph.nodes
            ],
        }
    )


def architecture_notes(row: pd.Series, family: str) -> str:
    notes: list[str] = []
    if row["analysis_group"] == "substrate_support":
        notes.append("substrate-support gene; keep separate from primary upstream/downstream contrast")
    if row["curation_confidence"] != "high":
        notes.append(f"{row['curation_confidence']}-confidence pathway label pending cross-check")
    if row["primary_region"] == "terminal_modification":
        notes.append("terminal-modification specificity should be tested in sensitivity analyses")
    if family and redundancy_prior(family, row["analysis_group"], row["primary_region"]) in {"high", "moderate"}:
        notes.append(f"assigned {family} paralog-family prior from symbol prefix")
    return "; ".join(notes)


def build_features(gene_table: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    features = gene_table.copy()
    features["architecture_version"] = ARCHITECTURE_VERSION

    features["pathway_depth_rank"] = features["primary_region"].map(DEPTH_BY_REGION)
    min_depth = min(DEPTH_BY_REGION.values())
    max_depth = max(DEPTH_BY_REGION.values())
    features["pathway_depth_scaled"] = (
        (features["pathway_depth_rank"] - min_depth) / (max_depth - min_depth)
    ).round(4)

    features["is_upstream_core"] = features["analysis_group"].eq("upstream_core").map(yes_no)
    features["is_checkpoint_layer"] = features["analysis_group"].eq("checkpoint_layer").map(yes_no)
    features["is_downstream_diversification"] = (
        features["analysis_group"].eq("downstream_diversification").map(yes_no)
    )
    features["is_substrate_support"] = features["analysis_group"].eq("substrate_support").map(yes_no)

    features["checkpoint_proximity"] = [
        checkpoint_proximity(region, group)
        for region, group in zip(features["primary_region"], features["analysis_group"])
    ]
    features["ost_or_lbo_core_member"] = (
        features["primary_region"].isin({"llo_assembly", "ost_transfer"}).map(yes_no)
    )
    features["er_quality_control_member"] = (
        features["primary_region"].eq("er_quality_control").map(yes_no)
    )
    features["catastrophic_potential_prior"] = [
        catastrophic_prior(region, group)
        for region, group in zip(features["primary_region"], features["analysis_group"])
    ]

    features["branching_role"] = [
        branching_role(region, group)
        for region, group in zip(features["primary_region"], features["analysis_group"])
    ]
    features["terminal_modification_role"] = (
        features["primary_region"].eq("terminal_modification").map(yes_no)
    )
    features["interface_layer_prior"] = [
        interface_prior(region, group)
        for region, group in zip(features["primary_region"], features["analysis_group"])
    ]
    features["glycan_output_layer"] = (
        features["analysis_group"].eq("downstream_diversification").map(yes_no)
    )
    features["regulatory_or_trans_layer_candidate"] = "no"

    features["paralog_family_name"] = features["symbol"].map(family_name)
    features["has_paralog_family"] = features["paralog_family_name"].ne("").map(yes_no)
    features["redundancy_prior"] = [
        redundancy_prior(family, group, region)
        for family, group, region in zip(
            features["paralog_family_name"],
            features["analysis_group"],
            features["primary_region"],
        )
    ]
    features["low_specificity_terminal_enzyme"] = [
        low_specificity_terminal(symbol, region)
        for symbol, region in zip(features["symbol"], features["primary_region"])
    ]

    graph = build_primary_reaction_graph(edges, features["symbol"].tolist())
    features = features.merge(graph_metrics(graph), on="symbol", how="left")

    features["architecture_notes"] = [
        architecture_notes(row, row["paralog_family_name"])
        for _, row in features.iterrows()
    ]

    output_columns = [
        "symbol",
        "ensembl_gene_id",
        "primary_region",
        "analysis_group",
        "include_primary",
        "include_sensitivity",
        "curation_confidence",
        "pathway_depth_rank",
        "pathway_depth_scaled",
        "is_upstream_core",
        "is_checkpoint_layer",
        "is_downstream_diversification",
        "is_substrate_support",
        "checkpoint_proximity",
        "ost_or_lbo_core_member",
        "er_quality_control_member",
        "catastrophic_potential_prior",
        "branching_role",
        "terminal_modification_role",
        "interface_layer_prior",
        "glycan_output_layer",
        "regulatory_or_trans_layer_candidate",
        "has_paralog_family",
        "paralog_family_name",
        "redundancy_prior",
        "low_specificity_terminal_enzyme",
        "graph_in_degree_primary_reaction",
        "graph_out_degree_primary_reaction",
        "graph_total_degree_primary_reaction",
        "graph_betweenness_primary_reaction",
        "graph_closeness_primary_reaction",
        "graph_component_id_primary_reaction",
        "architecture_version",
        "architecture_notes",
    ]
    return features[output_columns]


def build_summary(features: pd.DataFrame) -> pd.DataFrame:
    summary = (
        features.groupby(["analysis_group", "primary_region"], dropna=False)
        .agg(
            gene_count=("symbol", "count"),
            primary_gene_count=("include_primary", lambda values: int((values == "yes").sum())),
            mean_depth_scaled=("pathway_depth_scaled", "mean"),
            high_catastrophic_prior_count=(
                "catastrophic_potential_prior",
                lambda values: int((values == "high").sum()),
            ),
            high_or_moderate_interface_prior_count=(
                "interface_layer_prior",
                lambda values: int(values.isin(["high", "moderate"]).sum()),
            ),
            paralog_family_count=("has_paralog_family", lambda values: int((values == "yes").sum())),
            low_specificity_terminal_count=(
                "low_specificity_terminal_enzyme",
                lambda values: int((values == "yes").sum()),
            ),
        )
        .reset_index()
    )
    summary["mean_depth_scaled"] = summary["mean_depth_scaled"].round(4)
    summary.insert(0, "architecture_version", ARCHITECTURE_VERSION)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build first-pass N-glycosylation architecture features."
    )
    parser.add_argument(
        "--gene-table",
        default="data/processed/nglyco_gene_table.tsv",
        help="Input gene table TSV.",
    )
    parser.add_argument(
        "--edge-table",
        default="data/processed/nglyco_gene_gene_edges.tsv",
        help="Input gene-gene edge table TSV.",
    )
    parser.add_argument(
        "--features-out",
        default="data/processed/nglyco_architecture_features.tsv",
        help="Output architecture feature TSV.",
    )
    parser.add_argument(
        "--summary-out",
        default="results/tables/architecture_feature_summary.tsv",
        help="Output architecture summary TSV.",
    )
    args = parser.parse_args()

    gene_table = pd.read_csv(args.gene_table, sep="\t")
    edges = pd.read_csv(args.edge_table, sep="\t")
    features = build_features(gene_table, edges)
    summary = build_summary(features)

    Path(args.features_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary_out).parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(args.features_out, sep="\t", index=False)
    summary.to_csv(args.summary_out, sep="\t", index=False)

    print(f"Wrote {len(features)} rows to {args.features_out}")
    print(f"Wrote {len(summary)} rows to {args.summary_out}")


if __name__ == "__main__":
    main()
