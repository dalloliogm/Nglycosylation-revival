#!/usr/bin/env python3
"""Analyze population-genetics gradients across N-glycosylation pathway regions.

Compares FST, PBS, and iHS distributions across upstream-core, checkpoint-layer,
downstream-diversification, and substrate-support analysis groups.

Uses the same Mann-Whitney + rank-biserial + bootstrap CI framework as the
constraint and conservation gradient analyses.

Outputs
-------
- results/tables/popgen_group_comparisons.tsv
- results/tables/popgen_candidate_loci.tsv
- results/figures/popgen_fst_gradient.{png,svg}
- results/figures/popgen_pbs_gradient.{png,svg}
- results/reports/popgen-interpretation.md

Usage
-----
    python scripts/analyze_popgen_gradient.py [options]

Run from repository root after compute_fst_pbs.py and extract_pophuman_ihs.py.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


GROUP_ORDER = ["substrate_support", "upstream_core",
               "checkpoint_layer", "downstream_diversification"]
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
        "comparison_id": "upstream_core_vs_downstream",
        "group_a_query": "include_primary == 'yes' and analysis_group == 'upstream_core'",
        "group_b_query": "include_primary == 'yes' and analysis_group == 'downstream_diversification'",
        "group_a_label": "upstream_core",
        "group_b_label": "downstream_diversification",
        "scope": "Primary contrast.",
    },
    {
        "comparison_id": "upstream_plus_checkpoint_vs_downstream",
        "group_a_query": "include_primary == 'yes' and analysis_group in ['upstream_core','checkpoint_layer']",
        "group_b_query": "include_primary == 'yes' and analysis_group == 'downstream_diversification'",
        "group_a_label": "upstream_core+checkpoint",
        "group_b_label": "downstream_diversification",
        "scope": "Sensitivity: checkpoint merged with upstream.",
    },
    {
        "comparison_id": "checkpoint_vs_downstream",
        "group_a_query": "include_primary == 'yes' and analysis_group == 'checkpoint_layer'",
        "group_b_query": "include_primary == 'yes' and analysis_group == 'downstream_diversification'",
        "group_a_label": "checkpoint_layer",
        "group_b_label": "downstream_diversification",
        "scope": "Checkpoint layer tested separately.",
    },
]

# Pop-gen metric definitions
METRICS = [
    {"col": "fst_mean_AFR_EUR", "label": "Mean FST (AFR–EUR)", "short": "fst_afr_eur"},
    {"col": "fst_mean_AFR_EAS", "label": "Mean FST (AFR–EAS)", "short": "fst_afr_eas"},
    {"col": "fst_mean_EUR_EAS", "label": "Mean FST (EUR–EAS)", "short": "fst_eur_eas"},
    {"col": "pbs_AFR_vs_EUR_EAS", "label": "PBS AFR", "short": "pbs_afr"},
    {"col": "pbs_EUR_vs_AFR_EAS", "label": "PBS EUR", "short": "pbs_eur"},
    {"col": "pbs_EAS_vs_AFR_EUR", "label": "PBS EAS", "short": "pbs_eas"},
    {"col": "ihs_max_AFR",        "label": "Max |iHS| AFR", "short": "ihs_afr"},
    {"col": "ihs_max_EUR",        "label": "Max |iHS| EUR", "short": "ihs_eur"},
    {"col": "ihs_max_EAS",        "label": "Max |iHS| EAS", "short": "ihs_eas"},
]

FST_HIGH_THRESHOLD = 0.30    # mean FST > this → candidate locus flag


# ---------------------------------------------------------------------------
# Statistics (same helpers as other gradient scripts)
# ---------------------------------------------------------------------------

def _mann_whitney_u(a, b):
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return float("nan"), float("nan")
    combined = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    ranks, i = [], 0
    while i < len(combined):
        j = i + 1
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for _ in range(j - i):
            ranks.append(avg)
        i = j
    rank_a = sum(ranks[k] for k in range(len(combined)) if combined[k][1] == 0)
    u_a = rank_a - na * (na + 1) / 2.0
    u_b = na * nb - u_a
    u_stat = min(u_a, u_b)
    mu = na * nb / 2.0
    tie_sum = 0.0
    i = 0
    while i < len(combined):
        j = i + 1
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        t = j - i
        tie_sum += t * (t * t - 1)
        i = j
    n_total = na + nb
    sigma2 = (na * nb / 12.0) * (n_total + 1 - tie_sum / (n_total * (n_total - 1)))
    if sigma2 <= 0:
        return u_stat, 1.0
    z = (u_stat - mu) / math.sqrt(sigma2)
    p = 2.0 * (1.0 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return u_stat, p


def _rbc(a, b, u):
    na, nb = len(a), len(b)
    return 1.0 - 2.0 * u / (na * nb) if na and nb else float("nan")


def _bootstrap_ci(a, b, n_boot=2000, seed=42):
    rng = random.Random(seed)
    diffs = sorted(
        float(np.median([rng.choice(a) for _ in range(len(a))])) -
        float(np.median([rng.choice(b) for _ in range(len(b))]))
        for _ in range(n_boot)
    )
    return diffs[int(0.025 * n_boot)], diffs[int(0.975 * n_boot)]


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def run_comparisons(df: pd.DataFrame, metric_col: str) -> list[dict]:
    rows = []
    sub = df[df[metric_col].notna()]
    for comp in COMPARISONS:
        ga = sub.query(comp["group_a_query"])[metric_col].dropna().tolist()
        gb = sub.query(comp["group_b_query"])[metric_col].dropna().tolist()
        if len(ga) < 3 or len(gb) < 3:
            continue
        u, p = _mann_whitney_u(ga, gb)
        r = _rbc(ga, gb, u)
        ci_lo, ci_hi = _bootstrap_ci(ga, gb)
        rows.append({
            "metric": metric_col,
            "comparison_id": comp["comparison_id"],
            "group_a": comp["group_a_label"],
            "group_b": comp["group_b_label"],
            "n_a": len(ga), "n_b": len(gb),
            "median_a": round(float(np.median(ga)), 5),
            "median_b": round(float(np.median(gb)), 5),
            "median_diff": round(float(np.median(ga)) - float(np.median(gb)), 5),
            "ci95_lo": round(ci_lo, 5), "ci95_hi": round(ci_hi, 5),
            "mann_whitney_u": round(u, 2), "p_value": round(p, 5),
            "rank_biserial_r": round(r, 4),
            "scope": comp["scope"],
        })
    return rows


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_gradient(df: pd.DataFrame, col: str, label: str, out_prefix: Path) -> None:
    groups = [g for g in GROUP_ORDER if g in df["analysis_group"].unique()]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for pos, grp in enumerate(groups):
        vals = df[df["analysis_group"] == grp][col].dropna().tolist()
        if not vals:
            continue
        color = GROUP_COLORS[grp]
        jitter = np.random.default_rng(pos).uniform(-0.15, 0.15, len(vals))
        ax.scatter([pos + j for j in jitter], vals, color=color,
                   alpha=0.7, s=30, zorder=3, edgecolors="none")
        ax.boxplot(vals, positions=[pos], widths=0.35, patch_artist=True,
                   showfliers=False,
                   medianprops=dict(color="black", linewidth=2),
                   boxprops=dict(facecolor=color, alpha=0.35),
                   whiskerprops=dict(color="grey"), capprops=dict(color="grey"))
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([GROUP_LABELS[g] for g in groups], fontsize=9)
    ax.set_ylabel(label, fontsize=10)
    ax.set_title(f"Pop-gen gradient: {label}", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(f"{out_prefix}.{ext}", dpi=150)
    plt.close(fig)
    print(f"  Saved {out_prefix}.png/.svg")


# ---------------------------------------------------------------------------
# Candidate loci
# ---------------------------------------------------------------------------

def flag_candidates(fst_df: pd.DataFrame, pbs_df: pd.DataFrame) -> pd.DataFrame:
    """Flag genes with mean FST > threshold in any pairwise contrast."""
    fst_mean_cols = [c for c in fst_df.columns if c.startswith("fst_mean_")]
    candidates = []
    for _, row in fst_df.iterrows():
        flags = {}
        for col in fst_mean_cols:
            val = row.get(col)
            if pd.notna(val) and float(val) > FST_HIGH_THRESHOLD:
                flags[col] = round(float(val), 4)
        if flags:
            candidates.append({
                "symbol": row["symbol"],
                "analysis_group": row.get("analysis_group"),
                "primary_region": row.get("primary_region"),
                "high_fst_contrasts": "; ".join(
                    f"{k}={v}" for k, v in sorted(flags.items())
                ),
                "n_snps_used": row.get("n_snps_used"),
            })
    return pd.DataFrame(candidates)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def write_report(comparisons_df: pd.DataFrame, fst_df: pd.DataFrame,
                 candidates_df: pd.DataFrame, out_path: Path) -> None:
    lines = [
        "# Population-Genetics Gradient — Interpretation Note",
        "",
        f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d')}",
        "",
        "## Claim limits",
        "",
        "- FST outliers reflect population differentiation, which can arise from",
        "  drift, bottleneck, founder effect, migration, or local selection.",
        "  Do not describe elevated FST as evidence of selection without additional",
        "  support from iHS, PBS replication, or functional annotations.",
        "- iHS from PopHuman is pre-computed at 10 kb window resolution. Window-level",
        "  signals cannot be attributed to a specific gene without LD inspection.",
        "- PBS is more branch-specific than one-vs-rest FST but still requires",
        "  demographic correction before pathway-level enrichment claims.",
        "- Sample sizes (~25 upstream-core, ~27 downstream genes) limit power.",
        "- All comparisons are exploratory and uncorrected for multiple testing.",
        "",
        "## Group-level FST (AFR–EUR) summary",
        "",
    ]

    primary = fst_df[fst_df["include_primary"] == "yes"]
    for grp in GROUP_ORDER:
        sub = primary[primary["analysis_group"] == grp]
        if sub.empty:
            continue
        col = "fst_mean_AFR_EUR"
        if col in sub.columns:
            med = sub[col].median()
            mx = sub[col].max()
            lines.append(f"**{grp}** (n={len(sub)}): median={med:.4f}, max={mx:.4f}")
    lines.append("")

    lines.append("## Pairwise comparisons")
    lines.append("")
    for _, row in comparisons_df.iterrows():
        lines.append(f"**{row['comparison_id']}** | metric: {row['metric']}")
        lines.append(
            f"  {row['group_a']} (n={row['n_a']}, med={row['median_a']}) vs "
            f"{row['group_b']} (n={row['n_b']}, med={row['median_b']})"
        )
        lines.append(
            f"  Δ = {row['median_diff']:+.5f} [{row['ci95_lo']:+.5f}, {row['ci95_hi']:+.5f}]"
            f"  r={row['rank_biserial_r']:.3f}  p={row['p_value']:.4f}"
        )
        lines.append("")

    if not candidates_df.empty:
        lines += ["## High-FST candidate genes", ""]
        for _, row in candidates_df.iterrows():
            lines.append(f"- **{row['symbol']}** ({row['primary_region']}): {row['high_fst_contrasts']}")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print(f"  Saved {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fst-in",   default="data/processed/nglyco_fst_per_gene.tsv")
    parser.add_argument("--pbs-in",   default="data/processed/nglyco_pbs_per_gene.tsv")
    parser.add_argument("--ihs-in",   default="data/processed/nglyco_ihs_per_gene.tsv")
    parser.add_argument("--comparisons-out", default="results/tables/popgen_group_comparisons.tsv")
    parser.add_argument("--candidates-out",  default="results/tables/popgen_candidate_loci.tsv")
    parser.add_argument("--figures-dir",     default="results/figures")
    parser.add_argument("--report-out",      default="results/reports/popgen-interpretation.md")
    args = parser.parse_args()

    fst_df = pd.read_csv(args.fst_in, sep="\t")
    pbs_df = pd.read_csv(args.pbs_in, sep="\t")
    # iHS is optional (may not be ready yet)
    if Path(args.ihs_in).exists():
        ihs_df = pd.read_csv(args.ihs_in, sep="\t")
        combined = fst_df.merge(
            pbs_df.drop(columns=["ensembl_gene_id","primary_region","analysis_group",
                                  "include_primary","include_sensitivity"], errors="ignore"),
            on="symbol", how="left",
        ).merge(
            ihs_df.drop(columns=["ensembl_gene_id","primary_region","analysis_group",
                                   "include_primary","include_sensitivity"], errors="ignore"),
            on="symbol", how="left",
        )
    else:
        print("iHS data not found — running FST/PBS only.")
        combined = fst_df.merge(
            pbs_df.drop(columns=["ensembl_gene_id","primary_region","analysis_group",
                                  "include_primary","include_sensitivity"], errors="ignore"),
            on="symbol", how="left",
        )

    print(f"Loaded {len(combined)} genes")

    all_comparisons: list[dict] = []
    figs_dir = Path(args.figures_dir)
    figs_dir.mkdir(parents=True, exist_ok=True)

    for m in METRICS:
        col = m["col"]
        if col not in combined.columns:
            continue
        n = int(combined[col].notna().sum())
        if n < 5:
            continue
        print(f"\n--- {m['label']} (n={n}) ---")
        rows = run_comparisons(combined, col)
        all_comparisons.extend(rows)
        for r in rows:
            if r["comparison_id"] == "upstream_core_vs_downstream":
                print(f"  primary: Δ={r['median_diff']:+.5f} [{r['ci95_lo']:+.5f},{r['ci95_hi']:+.5f}]"
                      f"  r={r['rank_biserial_r']:.3f}  p={r['p_value']:.4f}")
        plot_gradient(
            combined[combined["include_primary"] == "yes"],
            col, m["label"],
            figs_dir / f"popgen_gradient_{m['short']}"
        )

    comparisons_df = pd.DataFrame(all_comparisons)
    comparisons_df.to_csv(args.comparisons_out, sep="\t", index=False)
    print(f"\nWrote {args.comparisons_out}")

    candidates_df = flag_candidates(fst_df, pbs_df)
    candidates_df.to_csv(args.candidates_out, sep="\t", index=False)
    print(f"Wrote {args.candidates_out}  ({len(candidates_df)} candidates)")

    write_report(comparisons_df, fst_df, candidates_df, Path(args.report_out))


if __name__ == "__main__":
    main()
