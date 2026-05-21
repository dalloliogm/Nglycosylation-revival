#!/usr/bin/env python3
"""Plot a gene-level N-glycosylation network with metabolite-like edges."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


GROUP_COLORS = {
    "substrate_support": "#D7C9A5",
    "upstream_core": "#4C78A8",
    "checkpoint_layer": "#6B8F71",
    "downstream_diversification": "#D9822B",
}

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
    "donor_substrate": {"width": 0.35, "alpha": 0.11, "arrowsize": 5, "rad": 0.05},
    "complex_or_binding_context": {"width": 0.45, "alpha": 0.22, "arrowsize": 6, "rad": 0.03},
    "metabolite_intermediate": {"width": 1.15, "alpha": 0.68, "arrowsize": 10, "rad": 0.02},
    "glycoprotein_intermediate": {"width": 1.05, "alpha": 0.60, "arrowsize": 9, "rad": 0.02},
    "quality_control_cycle": {"width": 1.0, "alpha": 0.60, "arrowsize": 9, "rad": 0.08},
}

EDGE_DRAW_ORDER = [
    "donor_substrate",
    "complex_or_binding_context",
    "quality_control_cycle",
    "glycoprotein_intermediate",
    "metabolite_intermediate",
]

SOURCE_METADATA = {
    "reactome_substrates": {
        "source_database": "Reactome",
        "source_pathway_id": "R-HSA-446219",
        "source_pathway_name": "Synthesis of substrates in N-glycan biosythesis",
        "source_url": "https://reactome.org/content/detail/R-HSA-446219",
        "evidence_basis": "curated pathway membership; gene-to-transferase edge is an abstracted donor-supply relationship",
        "curation_confidence": "supporting",
    },
    "reactome_llo": {
        "source_database": "Reactome",
        "source_pathway_id": "R-HSA-446193",
        "source_pathway_name": "Biosynthesis of the N-glycan precursor (LLO) and transfer to a nascent protein",
        "source_url": "https://reactome.org/content/detail/R-HSA-446193",
        "evidence_basis": "curated Reactome reaction order; represented here as adjacent gene-to-gene edges through shared LLO intermediates",
        "curation_confidence": "high",
    },
    "reactome_er_qc": {
        "source_database": "Reactome",
        "source_pathway_id": "R-HSA-532668",
        "source_pathway_name": "N-glycan trimming in the ER and Calnexin/Calreticulin cycle",
        "source_url": "https://reactome.org/content/detail/R-HSA-532668",
        "evidence_basis": "curated pathway events; chaperone and recycling edges are abstracted from glycoprotein-processing context",
        "curation_confidence": "high",
    },
    "reactome_golgi_cis": {
        "source_database": "Reactome",
        "source_pathway_id": "R-HSA-964739",
        "source_pathway_name": "N-glycan trimming and elongation in the cis-Golgi",
        "source_url": "https://reactome.org/content/detail/R-HSA-964739",
        "evidence_basis": "curated pathway events; represented as adjacent gene-to-gene edges through generic N-glycan intermediates",
        "curation_confidence": "high",
    },
    "reactome_golgi_antennae": {
        "source_database": "Reactome",
        "source_pathway_id": "R-HSA-975576",
        "source_pathway_name": "N-glycan antennae elongation in the medial/trans-Golgi",
        "source_url": "https://reactome.org/content/detail/R-HSA-975576",
        "evidence_basis": "Reactome generic reaction annotation; downstream network topology is intentionally abstracted because exact glycan topography is incomplete",
        "curation_confidence": "moderate",
    },
    "kegg_nglycan": {
        "source_database": "KEGG",
        "source_pathway_id": "hsa00510",
        "source_pathway_name": "N-Glycan biosynthesis - Homo sapiens",
        "source_url": "https://www.kegg.jp/pathway/hsa00510",
        "evidence_basis": "pathway-level support for donor substrate use and enzyme classes; not a direct source of this edge topology",
        "curation_confidence": "supporting",
    },
}


def add_edges(
    edges: list[dict[str, str]],
    sources: list[str],
    targets: list[str],
    metabolite: str,
    edge_class: str,
    source_key: str,
    curation_notes: str = "Generic edge label; exact glycan structure not curated in this pass.",
) -> None:
    for source in sources:
        for target in targets:
            edges.append(
                {
                    "source_gene": source,
                    "target_gene": target,
                    "edge_metabolite": metabolite,
                    "edge_class": edge_class,
                    **SOURCE_METADATA[source_key],
                    "curation_notes": curation_notes,
                }
            )


def curated_gene_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []

    add_edges(edges, ["DHDDS", "NUS1", "SRD5A3", "DOLK", "DOLPP1"], ["DPAGT1"], "dolichol phosphate pool", "donor_substrate", "reactome_substrates")
    add_edges(edges, ["GFPT1", "GFPT2", "GNPNAT1", "PGM3", "UAP1", "NAGK"], ["DPAGT1", "ALG13", "ALG14"], "UDP-GlcNAc donor", "donor_substrate", "reactome_substrates")
    add_edges(edges, ["HK1", "MPI", "PMM1", "PMM2", "GMPPA", "GMPPB"], ["ALG1", "ALG2", "ALG11"], "GDP-mannose donor", "donor_substrate", "reactome_substrates")
    add_edges(edges, ["DPM1", "DPM2", "DPM3", "MPDU1"], ["ALG3", "ALG9", "ALG12"], "Dol-P-mannose donor", "donor_substrate", "reactome_substrates")
    add_edges(edges, ["ALG5"], ["ALG6", "ALG8", "ALG10", "ALG10B"], "Dol-P-glucose donor", "donor_substrate", "reactome_substrates")

    add_edges(edges, ["DPAGT1"], ["ALG13", "ALG14"], "early LLO intermediate", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG13", "ALG14"], ["ALG1"], "GlcNAc2-PP-dolichol", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG1"], ["ALG2"], "mannosylated LLO intermediate", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG2"], ["ALG11"], "mannosylated LLO intermediate", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG11"], ["RFT1"], "Man5-GlcNAc2-PP-dolichol", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["RFT1"], ["ALG3"], "flipped LLO intermediate", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG3"], ["ALG9"], "luminal LLO intermediate", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG9"], ["ALG12"], "luminal LLO intermediate", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG12"], ["ALG6"], "Man9 LLO intermediate", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG6"], ["ALG8"], "glucosylated LLO intermediate", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, ["ALG8"], ["ALG10", "ALG10B"], "glucosylated LLO intermediate", "metabolite_intermediate", "reactome_llo")

    ost_subunits = ["DAD1", "DDOST", "MAGT1", "OST4", "OSTC", "RPN1", "RPN2", "STT3A", "STT3B", "TMEM258", "TUSC3"]
    add_edges(edges, ["ALG10", "ALG10B"], ["STT3A", "STT3B"], "mature LLO donor", "metabolite_intermediate", "reactome_llo")
    add_edges(edges, [g for g in ost_subunits if g not in {"STT3A", "STT3B"}], ["STT3A", "STT3B"], "OST complex context", "complex_or_binding_context", "reactome_llo")

    add_edges(edges, ["STT3A", "STT3B"], ["MOGS"], "nascent N-glycoprotein", "glycoprotein_intermediate", "reactome_er_qc")
    add_edges(edges, ["MOGS"], ["GANAB", "PRKCSH"], "monoglucosylated N-glycoprotein", "glycoprotein_intermediate", "reactome_er_qc")
    add_edges(edges, ["GANAB", "PRKCSH"], ["CANX", "CALR", "MLEC"], "folding-checkpoint glycoprotein", "complex_or_binding_context", "reactome_er_qc")
    add_edges(edges, ["CANX", "CALR"], ["PDIA3"], "chaperone-bound glycoprotein", "complex_or_binding_context", "reactome_er_qc")
    add_edges(edges, ["CANX", "CALR", "PDIA3"], ["UGGT1", "UGGT2"], "folding-assessed glycoprotein", "quality_control_cycle", "reactome_er_qc")
    add_edges(edges, ["UGGT1", "UGGT2"], ["MOGS"], "reglucosylated N-glycoprotein", "quality_control_cycle", "reactome_er_qc")
    add_edges(edges, ["GANAB", "PRKCSH"], ["MAN1B1"], "deglucosylated N-glycoprotein", "glycoprotein_intermediate", "reactome_er_qc")
    add_edges(edges, ["MAN1B1"], ["EDEM1", "EDEM2", "EDEM3"], "mannose-trimmed ER glycoprotein", "quality_control_cycle", "reactome_er_qc")
    add_edges(edges, ["MAN1B1"], ["MAN1A1", "MAN1A2", "MAN1C1"], "ER-exit N-glycoprotein", "glycoprotein_intermediate", "reactome_golgi_cis")

    add_edges(edges, ["MAN1A1", "MAN1A2", "MAN1C1"], ["MGAT1"], "Golgi-trimmed N-glycan", "glycoprotein_intermediate", "reactome_golgi_cis")
    add_edges(edges, ["MGAT1"], ["MAN2A1", "MAN2A2"], "hybrid/complex precursor N-glycan", "glycoprotein_intermediate", "reactome_golgi_cis")
    add_edges(edges, ["MAN2A1", "MAN2A2"], ["MGAT2"], "complex precursor N-glycan", "glycoprotein_intermediate", "reactome_golgi_cis")
    add_edges(edges, ["GFPT1", "GFPT2", "GNPNAT1", "PGM3", "UAP1", "NAGK"], ["MGAT1", "MGAT2", "MGAT3", "MGAT4A", "MGAT4B", "MGAT4C", "MGAT5"], "UDP-GlcNAc donor", "donor_substrate", "kegg_nglycan")
    add_edges(edges, ["MGAT2"], ["MGAT3", "MGAT4A", "MGAT4B", "MGAT4C", "MGAT5"], "complex N-glycan acceptor", "glycoprotein_intermediate", "reactome_golgi_antennae")

    add_edges(edges, ["MGAT3", "MGAT4A", "MGAT4B", "MGAT4C", "MGAT5"], ["B4GALT1", "B4GALT2", "B4GALT3", "B4GALT4", "B4GALT5", "B4GALT6"], "branched N-glycan acceptor", "glycoprotein_intermediate", "reactome_golgi_antennae")
    add_edges(edges, ["MGAT2", "MGAT3", "MGAT4A", "MGAT4B", "MGAT4C", "MGAT5"], ["FUT8"], "core-fucosylation acceptor", "glycoprotein_intermediate", "reactome_golgi_antennae")
    add_edges(edges, ["GMDS", "FPGT", "FCSK", "SLC35C1"], ["FUT8", "FUT3"], "GDP-fucose donor", "donor_substrate", "kegg_nglycan")
    add_edges(edges, ["B4GALT1", "B4GALT2", "B4GALT3", "B4GALT4", "B4GALT5", "B4GALT6"], ["ST3GAL4", "ST6GAL1", "ST8SIA2", "ST8SIA3", "ST8SIA6"], "galactosylated N-glycan acceptor", "glycoprotein_intermediate", "reactome_golgi_antennae")
    add_edges(edges, ["GNE", "NANS", "NANP", "CMAS", "SLC35A1"], ["ST3GAL4", "ST6GAL1", "ST8SIA2", "ST8SIA3", "ST8SIA6"], "CMP-sialic acid donor", "donor_substrate", "kegg_nglycan")
    add_edges(edges, ["B4GALT1", "B4GALT2", "B4GALT3", "B4GALT4", "B4GALT5", "B4GALT6"], ["FUT3", "CHST8", "CHST10", "B4GALNT2"], "terminal N-glycan acceptor", "glycoprotein_intermediate", "reactome_golgi_antennae")

    return edges


def write_edge_table(edges: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_gene",
                "target_gene",
                "edge_metabolite",
                "edge_class",
                "source_database",
                "source_pathway_id",
                "source_pathway_name",
                "source_url",
                "evidence_basis",
                "curation_confidence",
                "curation_notes",
            ],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(edges)


def build_graph(gene_table: Path, edge_table: Path) -> tuple[nx.DiGraph, pd.DataFrame]:
    genes = pd.read_csv(gene_table, sep="\t")
    visible = genes[(genes["include_primary"] == "yes") | (genes["primary_region"] == "substrate_biosynthesis")]
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
        graph.nodes[row.symbol].update(
            {
                "primary_region": row.primary_region,
                "analysis_group": row.analysis_group,
                "include_primary": row.include_primary,
                "color": GROUP_COLORS[row.analysis_group],
            }
        )
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
        ax.text((x0 + x1) / 2, -2.95, label, ha="center", va="center", fontsize=12, fontweight="bold", color="#263238")
    for region, label in REGION_STAGE.items():
        ax.text(STAGE_X[region], 1.75, label, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#263238")


def draw_network(ax: plt.Axes, graph: nx.DiGraph, positions: dict[str, tuple[float, float]]) -> None:
    for edge_class in EDGE_DRAW_ORDER:
        color = EDGE_COLORS[edge_class]
        style = EDGE_STYLES[edge_class]
        selected = [(u, v) for u, v, attrs in graph.edges(data=True) if attrs["edge_class"] == edge_class]
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
            edge_color=color,
            alpha=style["alpha"],
            connectionstyle=f"arc3,rad={style['rad']}",
        )

    node_colors = [graph.nodes[node].get("color", "#CCCCCC") for node in graph.nodes]
    node_sizes = [340 if graph.nodes[node].get("include_primary") == "yes" else 270 for node in graph.nodes]
    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=node_colors,
        node_size=node_sizes,
        edgecolors="#263238",
        linewidths=0.8,
        ax=ax,
    )
    nx.draw_networkx_labels(graph, positions, font_size=5.8, font_color="#1F2933", ax=ax)


def add_title_and_legend(ax: plt.Axes, visible: pd.DataFrame, edge_count: int) -> None:
    n_primary = int((visible["include_primary"] == "yes").sum())
    n_support = int((visible["analysis_group"] == "substrate_support").sum())
    ax.text(6.0, 3.22, "N-glycosylation gene-level metabolic network", ha="center", va="center", fontsize=18, fontweight="bold", color="#1F2933")
    ax.text(
        6.0,
        2.94,
        f"Nodes are genes; {edge_count} directed edges are glycan/metabolite intermediates, donor substrates, or complex contexts ({n_primary} primary, {n_support} support)",
        ha="center",
        va="center",
        fontsize=10.5,
        color="#4B5563",
    )
    legend = [
        Patch(facecolor=GROUP_COLORS["upstream_core"], edgecolor="#263238", label="Upstream core gene"),
        Patch(facecolor=GROUP_COLORS["checkpoint_layer"], edgecolor="#263238", label="Checkpoint gene"),
        Patch(facecolor=GROUP_COLORS["downstream_diversification"], edgecolor="#263238", label="Downstream gene"),
        Patch(facecolor=GROUP_COLORS["substrate_support"], edgecolor="#263238", label="Substrate-support gene"),
        Line2D([0], [0], color=EDGE_COLORS["metabolite_intermediate"], linewidth=1.5, label="LLO/metabolite intermediate"),
        Line2D([0], [0], color=EDGE_COLORS["glycoprotein_intermediate"], linewidth=1.5, label="N-glycoprotein intermediate"),
        Line2D([0], [0], color=EDGE_COLORS["donor_substrate"], linewidth=1.5, label="Donor substrate"),
        Line2D([0], [0], color=EDGE_COLORS["quality_control_cycle"], linewidth=1.5, label="Quality-control cycle"),
    ]
    ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False, fontsize=7.8)


def plot_network(gene_table: Path, edge_table: Path, output_png: Path, output_svg: Path) -> None:
    edges = curated_gene_edges()
    write_edge_table(edges, edge_table)
    graph, visible = build_graph(gene_table, edge_table)
    positions = compute_positions(visible)

    fig, ax = plt.subplots(figsize=(20, 11))
    ax.set_xlim(-1.0, 13.0)
    ax.set_ylim(-3.35, 3.45)
    ax.axis("off")

    draw_background(ax)
    draw_network(ax, graph, positions)
    add_title_and_legend(ax, visible, len(edges))

    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=300, bbox_inches="tight")
    fig.savefig(output_svg, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gene-table", type=Path, default=Path("data/processed/nglyco_gene_table.tsv"))
    parser.add_argument("--edge-table", type=Path, default=Path("data/processed/nglyco_gene_gene_edges.tsv"))
    parser.add_argument("--output-png", type=Path, default=Path("results/figures/nglyco_pathway_network.png"))
    parser.add_argument("--output-svg", type=Path, default=Path("results/figures/nglyco_pathway_network.svg"))
    args = parser.parse_args()
    plot_network(args.gene_table, args.edge_table, args.output_png, args.output_svg)


if __name__ == "__main__":
    main()
