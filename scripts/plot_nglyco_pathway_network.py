#!/usr/bin/env python3
"""Plot the curated N-glycosylation pathway architecture network."""

from __future__ import annotations

import argparse
import textwrap
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.lines import Line2D


REGION_LABELS = {
    "substrate_biosynthesis": "Substrate\nbiosynthesis",
    "llo_assembly": "LLO\nassembly",
    "ost_transfer": "OST\ntransfer",
    "er_quality_control": "ER quality\ncontrol",
    "golgi_core_processing": "Golgi core\nprocessing",
    "golgi_branching": "Golgi\nbranching",
    "terminal_modification": "Terminal\nmodification",
}

REGION_POSITIONS = {
    "substrate_biosynthesis": (0.6, 1.0),
    "llo_assembly": (0.8, 0.22),
    "ost_transfer": (2.25, 0.22),
    "er_quality_control": (3.75, 0.22),
    "golgi_core_processing": (5.25, 0.22),
    "golgi_branching": (6.75, 0.22),
    "terminal_modification": (8.35, 0.22),
}

GROUP_COLORS = {
    "substrate_support": "#D7C9A5",
    "upstream_core": "#4C78A8",
    "checkpoint_layer": "#6B8F71",
    "downstream_diversification": "#D9822B",
}

REGION_COLORS = {
    "substrate_biosynthesis": GROUP_COLORS["substrate_support"],
    "llo_assembly": GROUP_COLORS["upstream_core"],
    "ost_transfer": GROUP_COLORS["upstream_core"],
    "er_quality_control": GROUP_COLORS["checkpoint_layer"],
    "golgi_core_processing": GROUP_COLORS["downstream_diversification"],
    "golgi_branching": GROUP_COLORS["downstream_diversification"],
    "terminal_modification": "#C44E52",
}

EDGE_STYLES = {
    "biosynthetic_order": {"edge_color": "#263238", "style": "solid", "width": 2.0},
    "substrate_support": {"edge_color": "#8A6F2A", "style": "dashed", "width": 1.6},
}

GROUP_BANDS = [
    ("Upstream robustness core", 0.2, 2.85, "#EAF1F8", -0.68),
    ("Checkpoint layer", 3.15, 4.35, "#EEF5EE", -0.68),
    ("Downstream diversification/interface", 4.7, 9.1, "#FBEFE4", -0.68),
]

COMPONENT_SUMMARIES = {
    "substrate_biosynthesis": "Mannose, dolichol,\nUDP-GlcNAc, GDP-Fuc,\nand sialic acid supply",
    "llo_assembly": "ALG family, DPAGT1,\nRFT1, ALG5",
    "ost_transfer": "STT3A/STT3B OST\ncomplex subunits",
    "er_quality_control": "Glucosidases,\nUGGT1/2, CANX/CALR,\nMAN1B1/EDEMs",
    "golgi_core_processing": "MAN1/MAN2 trimming,\nMGAT1, MGAT2",
    "golgi_branching": "MGAT3, MGAT4A-C,\nMGAT5",
    "terminal_modification": "B4GALT family, FUTs,\nST3/ST6/ST8 sialylation,\nCHST/B4GALNT2",
}


def read_display_genes(gene_table: Path) -> dict[str, list[str]]:
    table = pd.read_csv(gene_table, sep="\t")
    display = table[(table["include_primary"] == "yes") | (table["primary_region"] == "substrate_biosynthesis")]
    genes_by_region: dict[str, list[str]] = defaultdict(list)
    for row in display.itertuples(index=False):
        genes_by_region[row.primary_region].append(row.symbol)
    return {region: sorted(genes) for region, genes in genes_by_region.items()}


def build_graph(edge_table: Path) -> nx.DiGraph:
    edges = pd.read_csv(edge_table, sep="\t")
    graph = nx.from_pandas_edgelist(
        edges,
        source="source",
        target="target",
        edge_attr=True,
        create_using=nx.DiGraph,
    )
    for node in graph.nodes:
        graph.nodes[node]["label"] = REGION_LABELS[node]
        graph.nodes[node]["color"] = REGION_COLORS[node]
        graph.nodes[node]["pos"] = REGION_POSITIONS[node]
    return graph


def draw_band(ax, label: str, x0: float, x1: float, color: str, label_y: float) -> None:
    band = FancyBboxPatch(
        (x0, -0.82),
        x1 - x0,
        1.28,
        boxstyle="round,pad=0.025,rounding_size=0.05",
        linewidth=0,
        facecolor=color,
        alpha=0.9,
        zorder=0,
    )
    ax.add_patch(band)
    ax.text(
        (x0 + x1) / 2,
        label_y,
        label,
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="#29323A",
    )


def draw_nodes(ax, graph: nx.DiGraph, genes_by_region: dict[str, list[str]]) -> None:
    for node, attrs in graph.nodes(data=True):
        x, y = attrs["pos"]
        width = 1.08 if node not in {"terminal_modification", "substrate_biosynthesis"} else 1.38
        height = 0.47 if node != "substrate_biosynthesis" else 0.64
        text_color = "white" if node != "substrate_biosynthesis" else "#263238"
        rect = FancyBboxPatch(
            (x - width / 2, y - height / 2),
            width,
            height,
            boxstyle="round,pad=0.03,rounding_size=0.055",
            linewidth=1.35,
            edgecolor="#263238",
            facecolor=attrs["color"],
            zorder=3,
        )
        ax.add_patch(rect)
        ax.text(
            x,
            y + 0.055,
            attrs["label"],
            ha="center",
            va="center",
            fontsize=9.1,
            fontweight="bold",
            color=text_color,
            linespacing=0.9,
            zorder=4,
        )
        genes = genes_by_region.get(node, [])
        count_label = "support genes" if node == "substrate_biosynthesis" else "primary genes"
        if node == "substrate_biosynthesis":
            ax.text(
                x,
                y - 0.19,
                f"{len(genes)} {count_label}",
                ha="center",
                va="center",
                fontsize=7.7,
                color="#263238",
                zorder=4,
            )
            ax.text(
                x,
                y - 0.28,
                "mannose/dolichol\nand donor sugars",
                ha="center",
                va="center",
                fontsize=6.6,
                color="#263238",
                linespacing=1.05,
                zorder=4,
            )
            continue
        ax.text(
            x,
            y - height / 2 - 0.08,
            f"{len(genes)} {count_label}",
            ha="center",
            va="top",
            fontsize=7.5,
            color="#263238",
            zorder=4,
        )
        ax.text(
            x,
            y - height / 2 - 0.22,
            COMPONENT_SUMMARIES[node],
            ha="center",
            va="top",
            fontsize=6.9,
            color="#263238",
            linespacing=1.18,
            zorder=4,
        )


def draw_edges(ax, graph: nx.DiGraph) -> None:
    pos = nx.get_node_attributes(graph, "pos")
    for edge_type, style in EDGE_STYLES.items():
        selected = [(u, v) for u, v, attrs in graph.edges(data=True) if attrs["edge_type"] == edge_type]
        if not selected:
            continue
        connectionstyle = "arc3,rad=0.0" if edge_type == "biosynthetic_order" else "arc3,rad=0.18"
        nx.draw_networkx_edges(
            graph,
            pos,
            ax=ax,
            edgelist=selected,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=17,
            min_source_margin=18,
            min_target_margin=18,
            connectionstyle=connectionstyle,
            **style,
        )


def plot_network(gene_table: Path, edge_table: Path, output_png: Path, output_svg: Path) -> None:
    genes_by_region = read_display_genes(gene_table)
    graph = build_graph(edge_table)

    fig, ax = plt.subplots(figsize=(15, 6.8))
    ax.set_xlim(-0.05, 9.25)
    ax.set_ylim(-1.1, 1.55)
    ax.axis("off")

    for band in GROUP_BANDS:
        draw_band(ax, *band)

    draw_edges(ax, graph)
    draw_nodes(ax, graph, genes_by_region)

    ax.text(
        4.6,
        1.42,
        "Curated N-glycosylation pathway architecture",
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold",
        color="#1F2933",
    )
    ax.text(
        4.6,
        1.25,
        "Primary genes only; substrate-support genes are shown as a separate feeder module",
        ha="center",
        va="center",
        fontsize=10,
        color="#4B5563",
    )

    legend_handles = [
        Patch(facecolor=GROUP_COLORS["upstream_core"], edgecolor="#263238", label="Upstream core"),
        Patch(facecolor=GROUP_COLORS["checkpoint_layer"], edgecolor="#263238", label="ER checkpoint"),
        Patch(facecolor=GROUP_COLORS["downstream_diversification"], edgecolor="#263238", label="Downstream diversification"),
        Patch(facecolor=GROUP_COLORS["substrate_support"], edgecolor="#263238", label="Substrate support"),
        Line2D([0], [0], color="#263238", linewidth=2, label="Biosynthetic order"),
        Line2D([0], [0], color="#8A6F2A", linewidth=2, linestyle="--", label="Substrate support edge"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.0),
        ncol=6,
        frameon=False,
        fontsize=7.8,
    )

    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=300, bbox_inches="tight")
    fig.savefig(output_svg, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gene-table", type=Path, default=Path("data/processed/nglyco_gene_table.tsv"))
    parser.add_argument("--edge-table", type=Path, default=Path("data/processed/nglyco_pathway_edges.tsv"))
    parser.add_argument("--output-png", type=Path, default=Path("results/figures/nglyco_pathway_network.png"))
    parser.add_argument("--output-svg", type=Path, default=Path("results/figures/nglyco_pathway_network.svg"))
    args = parser.parse_args()
    plot_network(args.gene_table, args.edge_table, args.output_png, args.output_svg)


if __name__ == "__main__":
    main()
