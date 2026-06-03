#!/usr/bin/env python3
"""Plot the N-glycosylation pathway network colored by constraint metrics."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


REGION_STAGE = {
    "substrate_biosynthesis": "Substrate supply",
    "llo_assembly": "LLO assembly",
    "ost_transfer": "OST transfer",
    "er_quality_control": "ER quality control",
    "golgi_core_processing": "Golgi core processing",
    "golgi_branching": "Golgi branching",
    "terminal_modification": "Terminal modification",
}

STAGE_X = {
    "substrate_biosynthesis": 0.0,
    "llo_assembly": 2.0,
    "ost_transfer": 4.0,
    "er_quality_control": 6.0,
    "golgi_core_processing": 8.0,
    "golgi_branching": 10.0,
    "terminal_modification": 12.0,
}

REGION_ORDER = list(STAGE_X)

BANDS = [
    ("Substrate support", -0.8, 0.8, "#F4EAD0"),
    ("Upstream core", 1.2, 4.8, "#EAF1F8"),
    ("Checkpoint layer", 5.2, 6.8, "#EEF5EE"),
    ("Downstream diversification/interface", 7.2, 12.8, "#FBEFE4"),
]

EDGE_COLORS = {
    "metabolite_intermediate": "#263238",
    "donor_substrate": "#8A6F2A",
    "glycoprotein_intermediate": "#5B6770",
    "quality_control_cycle": "#6B8F71",
    "complex_or_binding_context": "#9AA4AD",
}

EDGE_STYLES = {
    "donor_substrate": {"width": 0.30, "alpha": 0.08, "arrowsize": 4, "rad": 0.05},
    "complex_or_binding_context": {"width": 0.38, "alpha": 0.16, "arrowsize": 5, "rad": 0.03},
    "metabolite_intermediate": {"width": 0.92, "alpha": 0.42, "arrowsize": 8, "rad": 0.02},
    "glycoprotein_intermediate": {"width": 0.85, "alpha": 0.35, "arrowsize": 7, "rad": 0.02},
    "quality_control_cycle": {"width": 0.85, "alpha": 0.40, "arrowsize": 7, "rad": 0.08},
}

EDGE_DRAW_ORDER = [
    "donor_substrate",
    "complex_or_binding_context",
    "quality_control_cycle",
    "glycoprotein_intermediate",
    "metabolite_intermediate",
]

METRICS = {
    "loeuf": {
        "title": "LOEUF across the N-glycosylation pathway",
        "subtitle": "Lower values indicate stronger loss-of-function constraint",
        "cmap": "viridis_r",
        "legend_label": "LOEUF (lower = stronger LoF constraint)",
    },
    "mis_z": {
        "title": "Missense Z across the N-glycosylation pathway",
        "subtitle": "Higher values indicate stronger missense constraint",
        "cmap": "magma",
        "legend_label": "Missense Z (higher = stronger missense constraint)",
    },
}


def build_graph(constraint_table: Path, edge_table: Path) -> tuple[nx.DiGraph, pd.DataFrame]:
    genes = pd.read_csv(constraint_table, sep="\t")
    visible = genes[
        (genes["include_primary"] == "yes")
        | (genes["primary_region"] == "substrate_biosynthesis")
    ].copy()
    edges = pd.read_csv(edge_table, sep="\t")

    graph = nx.from_pandas_edgelist(
        edges,
        source="source_gene",
        target="target_gene",
        edge_attr=True,
        create_using=nx.DiGraph,
    )
    for row in visible.itertuples(index=False):
        if row.symbol not in graph:
            graph.add_node(row.symbol)
        graph.nodes[row.symbol].update(row._asdict())
    return graph, visible


def compute_positions(visible: pd.DataFrame) -> dict[str, tuple[float, float]]:
    positions: dict[str, tuple[float, float]] = {}
    for region in REGION_ORDER:
        subset = visible[visible["primary_region"] == region].sort_values("symbol")
        x = STAGE_X[region]
        n = len(subset)
        if n == 0:
            continue
        columns = 2 if n <= 18 else 3
        y_step = 0.34 if n <= 18 else 0.28
        x_step = 0.42
        for idx, row in enumerate(subset.itertuples(index=False)):
            col = idx % columns
            row_idx = idx // columns
            positions[row.symbol] = (
                x + (col - (columns - 1) / 2) * x_step,
                1.1 - row_idx * y_step,
            )
    return positions


def draw_background(ax: plt.Axes) -> None:
    for label, x0, x1, color in BANDS:
        ax.axvspan(x0, x1, ymin=0.08, ymax=0.83, color=color, zorder=0)
        ax.text(
            (x0 + x1) / 2,
            -2.95,
            label,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="#263238",
        )
    for region, label in REGION_STAGE.items():
        ax.text(
            STAGE_X[region],
            1.75,
            label,
            ha="center",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color="#263238",
        )


def draw_edges(ax: plt.Axes, graph: nx.DiGraph, positions: dict[str, tuple[float, float]]) -> None:
    for edge_class in EDGE_DRAW_ORDER:
        style = EDGE_STYLES[edge_class]
        selected = [
            (u, v)
            for u, v, attrs in graph.edges(data=True)
            if attrs["edge_class"] == edge_class and u in positions and v in positions
        ]
        if not selected:
            continue
        nx.draw_networkx_edges(
            graph,
            positions,
            edgelist=selected,
            ax=ax,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=style["arrowsize"],
            width=style["width"],
            edge_color=EDGE_COLORS[edge_class],
            alpha=style["alpha"],
            connectionstyle=f"arc3,rad={style['rad']}",
        )


def draw_metric_nodes(
    ax: plt.Axes,
    graph: nx.DiGraph,
    positions: dict[str, tuple[float, float]],
    metric: str,
    visible: pd.DataFrame,
) -> None:
    values = pd.to_numeric(visible[metric], errors="coerce")
    norm = Normalize(vmin=float(values.quantile(0.05)), vmax=float(values.quantile(0.95)))
    cmap = plt.get_cmap(METRICS[metric]["cmap"])

    available_nodes = []
    available_colors = []
    missing_nodes = []
    for node in positions:
        value = graph.nodes[node].get(metric)
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            numeric_value = float("nan")
        if pd.isna(numeric_value):
            missing_nodes.append(node)
        else:
            available_nodes.append(node)
            available_colors.append(cmap(norm(numeric_value)))

    sizes = [
        360 if graph.nodes[node].get("include_primary") == "yes" else 270
        for node in available_nodes
    ]
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=available_nodes,
        node_color=available_colors,
        node_size=sizes,
        edgecolors="#1F2933",
        linewidths=0.85,
        ax=ax,
    )
    if missing_nodes:
        nx.draw_networkx_nodes(
            graph,
            positions,
            nodelist=missing_nodes,
            node_color="#D9E2EC",
            node_size=[360 if graph.nodes[node].get("include_primary") == "yes" else 270 for node in missing_nodes],
            edgecolors="#52606D",
            linewidths=0.85,
            ax=ax,
        )
    nx.draw_networkx_labels(graph, positions, font_size=5.8, font_color="#111827", ax=ax)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    colorbar = plt.colorbar(sm, ax=ax, fraction=0.028, pad=0.012)
    colorbar.set_label(METRICS[metric]["legend_label"], fontsize=9)


def add_title_and_legend(ax: plt.Axes, visible: pd.DataFrame, metric: str) -> None:
    n_available = int(visible[metric].notna().sum())
    n_missing = int(visible[metric].isna().sum())
    dataset = ", ".join(sorted(visible["constraint_dataset_version"].dropna().unique()))
    ax.text(
        6.0,
        3.25,
        METRICS[metric]["title"],
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#1F2933",
    )
    ax.text(
        6.0,
        2.96,
        f"{METRICS[metric]['subtitle']} ({dataset}; provisional; {n_available} scored, {n_missing} missing)",
        ha="center",
        va="center",
        fontsize=10.5,
        color="#4B5563",
    )
    legend = [
        Patch(facecolor="#D9E2EC", edgecolor="#52606D", label="Missing constraint metric"),
        Line2D([0], [0], color=EDGE_COLORS["metabolite_intermediate"], linewidth=1.5, label="LLO/metabolite edge"),
        Line2D([0], [0], color=EDGE_COLORS["glycoprotein_intermediate"], linewidth=1.5, label="N-glycoprotein edge"),
        Line2D([0], [0], color=EDGE_COLORS["donor_substrate"], linewidth=1.5, label="Donor substrate edge"),
        Line2D([0], [0], color=EDGE_COLORS["quality_control_cycle"], linewidth=1.5, label="Quality-control cycle"),
    ]
    ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=5, frameon=False, fontsize=7.8)


def plot_metric(
    constraint_table: Path,
    edge_table: Path,
    metric: str,
    output_png: Path,
    output_svg: Path,
) -> None:
    graph, visible = build_graph(constraint_table, edge_table)
    positions = compute_positions(visible)

    fig, ax = plt.subplots(figsize=(20, 11))
    ax.set_xlim(-1.0, 13.65)
    ax.set_ylim(-3.35, 3.45)
    ax.axis("off")

    draw_background(ax)
    draw_edges(ax, graph, positions)
    draw_metric_nodes(ax, graph, positions, metric, visible)
    add_title_and_legend(ax, visible, metric)

    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=300, bbox_inches="tight")
    fig.savefig(output_svg, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--constraint-table",
        type=Path,
        default=Path("data/processed/nglyco_constraint_metrics.tsv"),
    )
    parser.add_argument(
        "--edge-table",
        type=Path,
        default=Path("data/processed/nglyco_gene_gene_edges.tsv"),
    )
    parser.add_argument(
        "--metric",
        choices=sorted(METRICS),
        required=True,
    )
    parser.add_argument("--output-png", type=Path, required=True)
    parser.add_argument("--output-svg", type=Path, required=True)
    args = parser.parse_args()
    plot_metric(args.constraint_table, args.edge_table, args.metric, args.output_png, args.output_svg)


if __name__ == "__main__":
    main()
