#!/usr/bin/env python3
"""Plot disease and trait evidence layers across N-glycosylation regions."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


REGION_ORDER = [
    "substrate_biosynthesis",
    "llo_assembly",
    "ost_transfer",
    "er_quality_control",
    "golgi_core_processing",
    "golgi_branching",
    "terminal_modification",
]

REGION_LABELS = {
    "substrate_biosynthesis": "Substrate\nbiosynthesis",
    "llo_assembly": "LLO\nassembly",
    "ost_transfer": "OST\ntransfer",
    "er_quality_control": "ER quality\ncontrol",
    "golgi_core_processing": "Golgi core\nprocessing",
    "golgi_branching": "Golgi\nbranching",
    "terminal_modification": "Terminal\nmodification",
}

REGION_COLORS = {
    "substrate_biosynthesis": "#8C6D31",
    "llo_assembly": "#4C78A8",
    "ost_transfer": "#6A9BD1",
    "er_quality_control": "#6B8F71",
    "golgi_core_processing": "#C5793A",
    "golgi_branching": "#D9822B",
    "terminal_modification": "#B85C38",
}

DISEASE_LAYERS = [
    ("cdg_seed_fraction", "Curated CDG"),
    ("clinvar_plp_gene_fraction", "ClinVar P/LP"),
]

TRAIT_COUNT_COLUMNS = [
    ("glycome_trait_gene_count", "Glycome"),
    ("immune_inflammation_trait_gene_count", "Immune/\ninflammation"),
    ("infection_trait_gene_count", "Infection"),
    ("cancer_trait_gene_count", "Cancer"),
    ("tissue_identity_trait_gene_count", "Tissue\nidentity"),
]


def ordered_summary(summary: pd.DataFrame) -> pd.DataFrame:
    data = summary.copy()
    data["primary_region"] = pd.Categorical(
        data["primary_region"], categories=REGION_ORDER, ordered=True
    )
    return data.sort_values("primary_region")


def plot_grouped_bar(ax: plt.Axes, data: pd.DataFrame) -> None:
    x = list(range(len(data)))
    bar_width = 0.34
    offsets = [-bar_width / 2, bar_width / 2]

    for index, (column, label) in enumerate(DISEASE_LAYERS):
        values = data[column].astype(float)
        ax.bar(
            [position + offsets[index] for position in x],
            values,
            width=bar_width,
            label=label,
            color="#4C78A8" if index == 0 else "#6B8F71",
            edgecolor="#2F3542",
            linewidth=0.6,
        )

    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Fraction of genes")
    ax.set_xticks(x)
    ax.set_xticklabels([REGION_LABELS[region] for region in data["primary_region"]])
    ax.set_title("A. Severe Mendelian/CDG evidence is concentrated early")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", color="#D9DEE7", linewidth=0.7)
    ax.set_axisbelow(True)


def plot_trait_heatmap(ax: plt.Axes, data: pd.DataFrame) -> None:
    fractions = []
    for count_column, _label in TRAIT_COUNT_COLUMNS:
        fractions.append((data[count_column] / data["gene_count"]).astype(float).tolist())
    heatmap = pd.DataFrame(
        fractions,
        index=[label for _column, label in TRAIT_COUNT_COLUMNS],
        columns=[REGION_LABELS[region] for region in data["primary_region"]],
    )

    image = ax.imshow(heatmap, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_title("B. GWAS Catalog trait categories are broad and downstream-rich")
    ax.set_xticks(range(len(heatmap.columns)))
    ax.set_xticklabels(heatmap.columns)
    ax.set_yticks(range(len(heatmap.index)))
    ax.set_yticklabels(heatmap.index)

    for y_index, row_label in enumerate(heatmap.index):
        for x_index, column_label in enumerate(heatmap.columns):
            value = heatmap.loc[row_label, column_label]
            text_color = "white" if value >= 0.65 else "#1F2933"
            ax.text(
                x_index,
                y_index,
                f"{value:.2f}",
                ha="center",
                va="center",
                color=text_color,
                fontsize=8,
            )

    colorbar = plt.colorbar(image, ax=ax, fraction=0.03, pad=0.02)
    colorbar.set_label("Fraction of genes")


def make_plot(summary: pd.DataFrame, output_png: str, output_svg: str) -> None:
    data = ordered_summary(summary)
    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )

    figure, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(11.5, 8.4),
        constrained_layout=True,
        gridspec_kw={"height_ratios": [1.0, 1.05]},
    )
    plot_grouped_bar(axes[0], data)
    plot_trait_heatmap(axes[1], data)
    figure.suptitle(
        "N-glycosylation disease and complex-trait architecture",
        fontsize=13,
        fontweight="bold",
    )
    figure.text(
        0.01,
        0.01,
        "GWAS mapped/reported gene evidence is hypothesis-generating; fractions summarize category flags, not causal burden.",
        fontsize=8,
        color="#4B5563",
    )

    Path(output_png).parent.mkdir(parents=True, exist_ok=True)
    Path(output_svg).parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_png, dpi=220)
    figure.savefig(output_svg)
    plt.close(figure)


def write_interpretation(summary: pd.DataFrame, output_report: str) -> None:
    data = ordered_summary(summary)
    upstream = data[data["primary_region"].isin(["llo_assembly", "ost_transfer"])]
    downstream = data[
        data["primary_region"].isin(
            ["golgi_core_processing", "golgi_branching", "terminal_modification"]
        )
    ]

    lines = [
        "# Disease Architecture Figure Interpretation",
        "",
        "Date generated: 2026-06-04",
        "",
        "This report accompanies `results/figures/disease_architecture.png` and `.svg`.",
        "",
        "## Readout",
        "",
        "- Curated CDG and ClinVar P/LP evidence are interpreted as severe Mendelian or pathogenic-variant layers.",
        "- GWAS Catalog evidence is interpreted as a broad complex-trait and glycome/interface layer.",
        "- GWAS mapped or reported genes are not treated as causal assignments.",
        "",
        "## Main Pattern",
        "",
        (
            f"Early core regions have high curated CDG fractions: "
            f"LLO assembly {data.loc[data['primary_region'].eq('llo_assembly'), 'cdg_seed_fraction'].iloc[0]:.2f}; "
            f"OST transfer {data.loc[data['primary_region'].eq('ost_transfer'), 'cdg_seed_fraction'].iloc[0]:.2f}."
        ),
        (
            f"ClinVar P/LP gene fractions are also high in LLO assembly "
            f"({data.loc[data['primary_region'].eq('llo_assembly'), 'clinvar_plp_gene_fraction'].iloc[0]:.2f}) "
            f"and substrate biosynthesis "
            f"({data.loc[data['primary_region'].eq('substrate_biosynthesis'), 'clinvar_plp_gene_fraction'].iloc[0]:.2f})."
        ),
        (
            f"Downstream regions show weaker severe Mendelian/CDG burden but broad GWAS trait-category coverage: "
            f"{int(downstream['glycome_trait_gene_count'].sum())} downstream genes have glycome-category GWAS evidence, "
            f"and {int(downstream['immune_inflammation_trait_gene_count'].sum())} have immune/inflammation-category evidence."
        ),
        "",
        "## Claim Limit",
        "",
        "The figure supports a layered disease/trait architecture hypothesis. It does not prove that GWAS mapped genes are causal, nor does it prove adaptive evolution. Candidate downstream loci require matched-association inspection and functional or fine-mapping support before gene-level storytelling.",
    ]

    _ = upstream  # Keeps the named intermediate visible for future extensions.
    Path(output_report).parent.mkdir(parents=True, exist_ok=True)
    Path(output_report).write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot disease and complex-trait evidence layers by pathway region."
    )
    parser.add_argument(
        "--summary",
        default="results/tables/disease_architecture_summary.tsv",
        help="Disease architecture summary TSV.",
    )
    parser.add_argument(
        "--output-png",
        default="results/figures/disease_architecture.png",
        help="Output PNG path.",
    )
    parser.add_argument(
        "--output-svg",
        default="results/figures/disease_architecture.svg",
        help="Output SVG path.",
    )
    parser.add_argument(
        "--report-out",
        default="results/reports/disease-architecture-interpretation.md",
        help="Output interpretation report.",
    )
    args = parser.parse_args()

    summary = pd.read_csv(args.summary, sep="\t")
    make_plot(summary, args.output_png, args.output_svg)
    write_interpretation(summary, args.report_out)
    print(f"Wrote {args.output_png}")
    print(f"Wrote {args.output_svg}")
    print(f"Wrote {args.report_out}")


if __name__ == "__main__":
    main()
