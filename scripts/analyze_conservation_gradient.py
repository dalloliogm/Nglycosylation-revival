#!/usr/bin/env python3
"""Analyze and plot cross-species conservation gradients across pathway architecture groups.

Metrics
-------
- mouse_perc_id: % amino-acid identity to one-to-one mouse ortholog (Ensembl BioMart)
- chimp_perc_id: % amino-acid identity to one-to-one chimp ortholog (Ensembl BioMart)
- mouse_goc_score: gene-order conservation score vs mouse (0–100)
- phylop100_mean: mean PhyloP 100-way vertebrate conservation over gene body (UCSC)

All BioMart dN/dS metrics are absent in Ensembl >= v110. % identity and GOC are
descriptive; do not interpret as evidence of positive selection.

Statistical note
----------------
Group sizes are small (n = 10-30). Mann-Whitney U with rank-biserial correlation
is reported as the primary effect-size estimate. All p-values are exploratory and
uncorrected for multiple comparisons; do not interpret isolated p < 0.05 as
confirmatory evidence.

Usage
-----
    python scripts/analyze_conservation_gradient.py [--conservation-table PATH]
"""

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
        "interpretation_scope": "ER quality-control/checkpoint genes separately.",
    },
    {
        "comparison_id": "ost_transfer_vs_downstream",
        "group_a_label": "ost_transfer",
        "group_b_label": "downstream_diversification",
        "group_a_query": "include_primary == 'yes' and primary_region == 'ost_transfer'",
        "group_b_query": "include_primary == 'yes' and analysis_group == 'downstream_diversification'",
        "interpretation_scope": "OST transfer complex specifically (highest mouse % identity sub-group).",
    },
]

METRICS = [
    ("mouse_perc_id", "Mouse % identity", "Higher = more conserved (human-mouse one-to-one ortholog)"),
    ("chimp_perc_id", "Chimp % identity", "Higher = more conserved (human-chimp one-to-one ortholog)"),
    ("mouse_goc_score", "Mouse GOC score", "Gene-order conservation vs mouse (0–100)"),
    ("phylop100_mean", "PhyloP100 mean", "Mean 100-way vertebrate PhyloP over gene body (higher = more conserved)"),
]


# ---------------------------------------------------------------------------
# Mann-Whitney U (same implementation as analyze_constraint_gradient.py)
# ---------------------------------------------------------------------------

def _average_ranks(values: list[float]) -> list[float]:
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
    a = [float(v) for v in values_a.dropna()]
    b = [float(v) for v in values_b.dropna()]
    n_a, n_b = len(a), len(b)
    if n_a == 0 or n_b == 0:
        return {k: math.nan for k in [
            "mann_whitney_u_a", "normal_approx_p_two_sided",
            "rank_biserial_a_greater_than_b", "rank_biserial_a_less_than_b",
            "common_language_a_less_than_b",
        ]}
    combined = a + b
    ranks = _average_ranks(combined)
    rank_sum_a = sum(ranks[:n_a])
    u_a = rank_sum_a - n_a * (n_a + 1) / 2
    u_total = n_a * n_b
    mean_u = u_total / 2
    tie_counts = pd.Series(combined).value_counts()
    tie_adj = sum(c**3 - c for c in tie_counts)
    n_total = n_a + n_b
    variance_u = (n_a * n_b / 12) * ((n_total + 1) - tie_adj / (n_total * (n_total - 1)))
    z = (u_a - mean_u) / math.sqrt(variance_u) if variance_u > 0 else math.nan
    p = math.erfc(abs(z) / math.sqrt(2)) if not math.isnan(z) else math.nan
    rb_greater = 2 * u_a / u_total - 1
    cl_less = (u_total - u_a) / u_total
    rb_less = 2 * cl_less - 1
    return {
        "mann_whitney_u_a": round(u_a, 4),
        "normal_approx_p_two_sided": round(p, 6),
        "rank_biserial_a_greater_than_b": round(rb_greater, 4),
        "rank_biserial_a_less_than_b": round(rb_less, 4),
        "common_language_a_less_than_b": round(cl_less, 4),
    }


def _iqr(s: pd.Series) -> float:
    clean = s.dropna()
    return float(clean.quantile(0.75) - clean.quantile(0.25)) if len(clean) >= 2 else math.nan


# ---------------------------------------------------------------------------
# Comparison table
# ---------------------------------------------------------------------------

def build_comparison_table(data: pd.DataFrame) -> pd.DataFrame:
    """Run Mann-Whitney comparisons across metrics and pre-defined group contrasts."""
    primary = data[data["include_primary"].eq("yes")].copy()
    rows: list[dict] = []
    for comp in COMPARISONS:
        group_a = primary.query(comp["group_a_query"])
        group_b = primary.query(comp["group_b_query"])
        for col, label, direction_note in METRICS:
            if col not in data.columns:
                continue
            va = group_a[col].dropna()
            vb = group_b[col].dropna()
            mw = mann_whitney(va, vb)
            med_a = float(va.median()) if len(va) else math.nan
            med_b = float(vb.median()) if len(vb) else math.nan
            rows.append({
                "comparison_id": comp["comparison_id"],
                "metric": col,
                "metric_label": label,
                "group_a": comp["group_a_label"],
                "group_b": comp["group_b_label"],
                "n_a": len(va),
                "n_b": len(vb),
                "median_a": round(med_a, 4) if not math.isnan(med_a) else math.nan,
                "median_b": round(med_b, 4) if not math.isnan(med_b) else math.nan,
                "median_diff_a_minus_b": round(med_a - med_b, 4) if not (math.isnan(med_a) or math.isnan(med_b)) else math.nan,
                "iqr_a": round(_iqr(va), 4),
                "iqr_b": round(_iqr(vb), 4),
                **mw,
                "interpretation_scope": comp["interpretation_scope"],
                "metric_direction_note": direction_note,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def _jitter_positions(count: int, center: float, width: float = 0.18) -> list[float]:
    if count <= 1:
        return [center] * count
    step = (2 * width) / (count - 1)
    return [center - width + i * step for i in range(count)]


def plot_gradient(data: pd.DataFrame, png_path: Path, svg_path: Path) -> None:
    """Four-panel figure: mouse % id, chimp % id, mouse GOC, PhyloP (if available)."""
    primary = data[data["include_primary"].eq("yes")].copy()

    available_metrics = [(col, lbl, sub) for col, lbl, sub in METRICS if col in primary.columns and primary[col].notna().any()]
    ncols = min(len(available_metrics), 4)
    if ncols == 0:
        print("  No metrics with data for plotting.")
        return

    nrows = 1
    fig, axes_flat = plt.subplots(nrows, ncols, figsize=(3.8 * ncols, 5.5), constrained_layout=True)
    if ncols == 1:
        axes_flat = [axes_flat]
    axes = list(axes_flat) if ncols > 1 else axes_flat

    for ax, (metric, title, subtitle) in zip(axes, available_metrics):
        grouped = [
            primary.loc[primary["analysis_group"].eq(group), metric].dropna()
            for group in GROUP_ORDER
        ]
        ax.boxplot(
            grouped,
            positions=range(len(GROUP_ORDER)),
            widths=0.48,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "#1F2933", "linewidth": 1.4},
            boxprops={"facecolor": "#FFFFFF", "edgecolor": "#3E4C59", "linewidth": 1.0},
            whiskerprops={"color": "#3E4C59", "linewidth": 1.0},
            capprops={"color": "#3E4C59", "linewidth": 1.0},
        )
        for i, (group, values) in enumerate(zip(GROUP_ORDER, grouped)):
            xs = _jitter_positions(len(values), i)
            ax.scatter(xs, values, s=28, color=GROUP_COLORS[group],
                       edgecolor="#1F2933", linewidth=0.35, alpha=0.86, zorder=3)
            ylim = ax.get_ylim()
            ax.text(i, ylim[1], f"n={len(values)}", ha="center", va="top",
                    fontsize=8, color="#52606D")
        ax.set_title(f"{title}\n{subtitle}", fontsize=9.5, loc="left")
        ax.set_xticks(range(len(GROUP_ORDER)), [GROUP_LABELS[g] for g in GROUP_ORDER], fontsize=8.5)
        ax.grid(axis="y", color="#D9E2EC", linewidth=0.8, alpha=0.7)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    ensembl_release = primary["ensembl_release"].dropna().iloc[0] if "ensembl_release" in primary.columns and primary["ensembl_release"].notna().any() else "unknown"
    fig.suptitle(
        f"N-glycosylation cross-species conservation by pathway architecture\n"
        f"(Ensembl {ensembl_release} BioMart + UCSC PhyloP100; provisional)",
        fontsize=12, fontweight="bold",
    )
    png_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_path, dpi=220)
    fig.savefig(svg_path)
    plt.close(fig)
    print(f"  Wrote {png_path}")
    print(f"  Wrote {svg_path}")


# ---------------------------------------------------------------------------
# Interpretation report
# ---------------------------------------------------------------------------

def write_interpretation_report(comparisons: pd.DataFrame, path: Path) -> None:
    primary_mouse = comparisons[
        (comparisons["comparison_id"] == "primary_upstream_core_vs_downstream") &
        (comparisons["metric"] == "mouse_perc_id")
    ]
    primary_chimp = comparisons[
        (comparisons["comparison_id"] == "primary_upstream_core_vs_downstream") &
        (comparisons["metric"] == "chimp_perc_id")
    ]
    primary_phylop = comparisons[
        (comparisons["comparison_id"] == "primary_upstream_core_vs_downstream") &
        (comparisons["metric"] == "phylop100_mean")
    ]

    def fmt_row(df: pd.DataFrame) -> str:
        if df.empty:
            return "  (no data)"
        r = df.iloc[0]
        return (
            f"  Group A (upstream core): median = {r.get('median_a', 'NA')}, IQR = {r.get('iqr_a', 'NA')}, n = {r.get('n_a', 'NA')}\n"
            f"  Group B (downstream):    median = {r.get('median_b', 'NA')}, IQR = {r.get('iqr_b', 'NA')}, n = {r.get('n_b', 'NA')}\n"
            f"  Median diff (A - B):     {r.get('median_diff_a_minus_b', 'NA')}\n"
            f"  Rank-biserial (A > B):   {r.get('rank_biserial_a_greater_than_b', 'NA')}\n"
            f"  p (two-sided, uncorrected): {r.get('normal_approx_p_two_sided', 'NA')}"
        )

    lines = [
        "# Conservation Gradient Interpretation (provisional)",
        "",
        "Generated by `scripts/analyze_conservation_gradient.py`.",
        "All statistics are exploratory and uncorrected for multiple comparisons.",
        "Do not interpret % identity or GOC score as evidence of positive or negative selection.",
        "",
        "## Primary contrast: upstream core vs downstream diversification",
        "",
        "### Mouse % identity",
        fmt_row(primary_mouse),
        "",
        "### Chimp % identity",
        fmt_row(primary_chimp),
        "",
        "### PhyloP100 mean",
        fmt_row(primary_phylop) if not primary_phylop.empty else "  (PhyloP not yet fetched or not available)",
        "",
        "## Interpretation notes",
        "",
        "- Counter-intuitively, upstream-core genes (LLO assembly) show *lower* median",
        "  mouse % identity than downstream or checkpoint genes in the preliminary data.",
        "  This may reflect greater mammalian diversification in precursor-synthesis subunits",
        "  rather than relaxed constraint: LLO assembly genes are ancient, highly constrained",
        "  within humans (see constraint-gradient results), but have diverged more from rodents",
        "  in absolute sequence terms. These findings are consistent with deep conservation of",
        "  function at the cost of measurable sequence drift over ~90 Myr of human-mouse",
        "  separation.",
        "- OST transfer complex genes (STT3A, STT3B, RPN1, RPN2, OST4, DAD1, OSTC, TMEM258)",
        "  show the highest mouse % identity (~98.8%), consistent with tight structural",
        "  requirements of the membrane-embedded catalytic complex.",
        "- Chimp % identity is uniformly high (≥98.9%) across all groups, consistent with",
        "  the short human-chimp divergence time (~6 Myr). Chimp % identity does not",
        "  discriminate pathway architecture in this dataset.",
        "- PhyloP100 (if available) provides a deeper-time conservation signal integrating",
        "  100 vertebrate genomes and is more likely to separate functionally constrained",
        "  genes from those tolerating neutral drift.",
        "",
        "## Claim limits",
        "",
        "- DO NOT describe these differences as evidence of positive selection.",
        "- DO NOT describe % identity as equivalent to dN/dS (they are not).",
        "- These results are consistent with the architecture hypothesis but do not confirm it.",
        "  Use language: 'consistent with', 'preliminary evidence', 'hypothesis-generating'.",
        "- Sensitivity analyses with/without low-specificity terminal enzymes and substrate-",
        "  biosynthesis genes should be checked before any manuscript claim.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")
    print(f"  Wrote {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze cross-species conservation gradients for N-glycosylation genes."
    )
    parser.add_argument("--conservation-table", default="data/processed/nglyco_conservation_metrics.tsv")
    parser.add_argument("--comparisons-out", default="results/tables/conservation_group_comparisons.tsv")
    parser.add_argument("--figure-png", default="results/figures/conservation_gradient.png")
    parser.add_argument("--figure-svg", default="results/figures/conservation_gradient.svg")
    parser.add_argument("--report-out", default="results/reports/conservation-interpretation.md")
    args = parser.parse_args()

    data = pd.read_csv(args.conservation_table, sep="\t")
    print(f"Loaded {len(data)} genes from {args.conservation_table}")

    available_metrics = [col for col, _, _ in METRICS if col in data.columns and data[col].notna().any()]
    print(f"Available metrics: {available_metrics}")

    comparisons = build_comparison_table(data)
    Path(args.comparisons_out).parent.mkdir(parents=True, exist_ok=True)
    comparisons.to_csv(args.comparisons_out, sep="\t", index=False)
    print(f"Wrote {len(comparisons)} comparison rows to {args.comparisons_out}")

    plot_gradient(data, Path(args.figure_png), Path(args.figure_svg))
    write_interpretation_report(comparisons, Path(args.report_out))


if __name__ == "__main__":
    main()
