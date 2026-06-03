#!/usr/bin/env python3
"""Analyze and plot provisional constraint gradients across pathway regions."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


GROUP_ORDER = [
    "substrate_support",
    "upstream_core",
    "checkpoint_layer",
    "downstream_diversification",
]

GROUP_LABELS = {
    "substrate_support": "Substrate\nsupport",
    "upstream_core": "Upstream\ncore",
    "checkpoint_layer": "Checkpoint\nlayer",
    "downstream_diversification": "Downstream\ndiversification",
}

GROUP_COLORS = {
    "substrate_support": "#D7C9A5",
    "upstream_core": "#4C78A8",
    "checkpoint_layer": "#6B8F71",
    "downstream_diversification": "#D9822B",
}

COMPARISONS = [
    {
        "comparison_id": "primary_upstream_core_vs_downstream",
        "group_a_label": "upstream_core",
        "group_b_label": "downstream_diversification",
        "group_a_query": "include_primary == 'yes' and analysis_group == 'upstream_core'",
        "group_b_query": "include_primary == 'yes' and analysis_group == 'downstream_diversification'",
        "interpretation_scope": "Primary upstream/downstream contrast; checkpoint layer held separate.",
    },
    {
        "comparison_id": "upstream_plus_checkpoint_vs_downstream",
        "group_a_label": "upstream_core_plus_checkpoint_layer",
        "group_b_label": "downstream_diversification",
        "group_a_query": "include_primary == 'yes' and analysis_group in ['upstream_core', 'checkpoint_layer']",
        "group_b_query": "include_primary == 'yes' and analysis_group == 'downstream_diversification'",
        "interpretation_scope": "Sensitivity merging checkpoint layer with upstream/core genes.",
    },
    {
        "comparison_id": "checkpoint_layer_vs_downstream",
        "group_a_label": "checkpoint_layer",
        "group_b_label": "downstream_diversification",
        "group_a_query": "include_primary == 'yes' and analysis_group == 'checkpoint_layer'",
        "group_b_query": "include_primary == 'yes' and analysis_group == 'downstream_diversification'",
        "interpretation_scope": "Tests ER quality-control/checkpoint genes separately.",
    },
    {
        "comparison_id": "upstream_vs_downstream_excluding_low_specificity_terminal",
        "group_a_label": "upstream_core",
        "group_b_label": "downstream_diversification_without_low_specificity_terminal",
        "group_a_query": "include_primary == 'yes' and analysis_group == 'upstream_core'",
        "group_b_query": "include_primary == 'yes' and analysis_group == 'downstream_diversification' and low_specificity_terminal_enzyme != 'yes'",
        "interpretation_scope": "Sensitivity excluding broad low-specificity terminal-modification enzymes.",
    },
]


def average_ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    position = 0
    while position < len(indexed):
        end = position + 1
        while end < len(indexed) and indexed[end][1] == indexed[position][1]:
            end += 1
        average_rank = (position + 1 + end) / 2
        for index, _ in indexed[position:end]:
            ranks[index] = average_rank
        position = end
    return ranks


def mann_whitney(values_a: pd.Series, values_b: pd.Series) -> dict[str, float]:
    a = [float(value) for value in values_a.dropna()]
    b = [float(value) for value in values_b.dropna()]
    n_a = len(a)
    n_b = len(b)
    if n_a == 0 or n_b == 0:
        return {
            "mann_whitney_u_a": math.nan,
            "normal_approx_p_two_sided": math.nan,
            "rank_biserial_a_greater_than_b": math.nan,
            "rank_biserial_a_less_than_b": math.nan,
            "common_language_a_less_than_b": math.nan,
        }

    combined = a + b
    ranks = average_ranks(combined)
    rank_sum_a = sum(ranks[:n_a])
    u_a = rank_sum_a - n_a * (n_a + 1) / 2
    u_total = n_a * n_b
    mean_u = u_total / 2

    tie_counts = pd.Series(combined).value_counts()
    tie_adjustment = sum(count**3 - count for count in tie_counts)
    n_total = n_a + n_b
    variance_u = (n_a * n_b / 12) * (
        (n_total + 1) - tie_adjustment / (n_total * (n_total - 1))
    )
    z_score = (u_a - mean_u) / math.sqrt(variance_u) if variance_u > 0 else math.nan
    p_value = math.erfc(abs(z_score) / math.sqrt(2)) if not math.isnan(z_score) else math.nan

    rank_biserial_greater = 2 * u_a / u_total - 1
    common_language_less = (u_total - u_a) / u_total
    rank_biserial_less = 2 * common_language_less - 1
    return {
        "mann_whitney_u_a": round(u_a, 4),
        "normal_approx_p_two_sided": round(p_value, 6),
        "rank_biserial_a_greater_than_b": round(rank_biserial_greater, 4),
        "rank_biserial_a_less_than_b": round(rank_biserial_less, 4),
        "common_language_a_less_than_b": round(common_language_less, 4),
    }


def iqr(values: pd.Series) -> float:
    clean = values.dropna()
    if clean.empty:
        return math.nan
    return float(clean.quantile(0.75) - clean.quantile(0.25))


def comparison_rows(data: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    available = data[data["constraint_metric_available"].eq("yes")].copy()
    for comparison in COMPARISONS:
        group_a = available.query(comparison["group_a_query"])
        group_b = available.query(comparison["group_b_query"])
        for metric in ["loeuf", "mis_z"]:
            values_a = group_a[metric].dropna()
            values_b = group_b[metric].dropna()
            mw = mann_whitney(values_a, values_b)
            median_a = values_a.median()
            median_b = values_b.median()
            if metric == "loeuf":
                direction_note = (
                    "Lower LOEUF indicates stronger LoF constraint; negative median difference means group A is more constrained."
                )
            else:
                direction_note = (
                    "Higher missense Z indicates stronger missense constraint; positive median difference means group A is more constrained."
                )
            rows.append(
                {
                    "comparison_id": comparison["comparison_id"],
                    "metric": metric,
                    "group_a": comparison["group_a_label"],
                    "group_b": comparison["group_b_label"],
                    "n_a": len(values_a),
                    "n_b": len(values_b),
                    "median_a": round(float(median_a), 4) if not math.isnan(median_a) else math.nan,
                    "median_b": round(float(median_b), 4) if not math.isnan(median_b) else math.nan,
                    "median_diff_a_minus_b": round(float(median_a - median_b), 4)
                    if not math.isnan(median_a) and not math.isnan(median_b)
                    else math.nan,
                    "iqr_a": round(iqr(values_a), 4),
                    "iqr_b": round(iqr(values_b), 4),
                    **mw,
                    "interpretation_scope": comparison["interpretation_scope"],
                    "metric_direction_note": direction_note,
                }
            )
    return pd.DataFrame(rows)


def jitter_positions(count: int, center: float, width: float = 0.18) -> list[float]:
    if count <= 1:
        return [center] * count
    step = (2 * width) / (count - 1)
    return [center - width + index * step for index in range(count)]


def plot_gradient(data: pd.DataFrame, png_path: Path, svg_path: Path) -> None:
    available = data[data["constraint_metric_available"].eq("yes")].copy()
    dataset_versions = sorted(available["constraint_dataset_version"].dropna().unique())
    dataset_label = ", ".join(dataset_versions) if dataset_versions else "unknown dataset"

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), constrained_layout=True)
    plot_specs = [
        ("loeuf", "LOEUF", "Lower values indicate stronger LoF constraint"),
        ("mis_z", "Missense Z", "Higher values indicate stronger missense constraint"),
    ]

    for axis, (metric, title, subtitle) in zip(axes, plot_specs):
        grouped_values = [
            available.loc[available["analysis_group"].eq(group), metric].dropna()
            for group in GROUP_ORDER
        ]
        axis.boxplot(
            grouped_values,
            positions=range(len(GROUP_ORDER)),
            widths=0.48,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "#1F2933", "linewidth": 1.4},
            boxprops={"facecolor": "#FFFFFF", "edgecolor": "#3E4C59", "linewidth": 1.0},
            whiskerprops={"color": "#3E4C59", "linewidth": 1.0},
            capprops={"color": "#3E4C59", "linewidth": 1.0},
        )
        for index, (group, values) in enumerate(zip(GROUP_ORDER, grouped_values)):
            xs = jitter_positions(len(values), index)
            axis.scatter(
                xs,
                values,
                s=28,
                color=GROUP_COLORS[group],
                edgecolor="#1F2933",
                linewidth=0.35,
                alpha=0.86,
                zorder=3,
            )
            axis.text(
                index,
                axis.get_ylim()[1],
                f"n={len(values)}",
                ha="center",
                va="top",
                fontsize=8,
                color="#52606D",
            )
        axis.set_title(f"{title}\n{subtitle}", fontsize=11, loc="left")
        axis.set_xticks(range(len(GROUP_ORDER)), [GROUP_LABELS[group] for group in GROUP_ORDER])
        axis.grid(axis="y", color="#D9E2EC", linewidth=0.8, alpha=0.7)
        axis.set_axisbelow(True)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    fig.suptitle(
        f"N-glycosylation constraint by pathway architecture ({dataset_label}; provisional)",
        fontsize=14,
        fontweight="bold",
    )
    png_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_path, dpi=220)
    fig.savefig(svg_path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze provisional constraint gradients across N-glycosylation architecture groups."
    )
    parser.add_argument(
        "--constraint-table",
        default="data/processed/nglyco_constraint_metrics.tsv",
        help="Input per-gene constraint metrics table.",
    )
    parser.add_argument(
        "--comparisons-out",
        default="results/tables/constraint_group_comparisons.tsv",
        help="Output comparison table.",
    )
    parser.add_argument(
        "--figure-png",
        default="results/figures/constraint_gradient.png",
        help="Output PNG figure.",
    )
    parser.add_argument(
        "--figure-svg",
        default="results/figures/constraint_gradient.svg",
        help="Output SVG figure.",
    )
    args = parser.parse_args()

    data = pd.read_csv(args.constraint_table, sep="\t")
    comparisons = comparison_rows(data)
    Path(args.comparisons_out).parent.mkdir(parents=True, exist_ok=True)
    comparisons.to_csv(args.comparisons_out, sep="\t", index=False)
    plot_gradient(data, Path(args.figure_png), Path(args.figure_svg))

    print(f"Wrote {len(comparisons)} comparison rows to {args.comparisons_out}")
    print(f"Wrote {args.figure_png}")
    print(f"Wrote {args.figure_svg}")


if __name__ == "__main__":
    main()
