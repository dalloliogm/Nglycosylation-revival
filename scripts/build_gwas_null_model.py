#!/usr/bin/env python3
"""
Task 4: GWAS genome-wide null model for N-glyco downstream gene enrichment.

Question: Are downstream N-glyco genes enriched for immune/glycan GWAS traits
beyond what is expected given their gene length and GWAS hit density?

Approach:
1. Load all GWAS catalog associations (p < 5e-8)
2. Classify traits into: glycan_direct, immune_nonglycan, cardiometabolic, other
3. For each gene in the genome: count total hits and category-specific hits
4. Match downstream N-glyco genes to background by total GWAS hit count (±2-fold)
5. Fisher's exact test: downstream vs. background for glycan+immune hit fraction
"""

import zipfile
import pandas as pd
import numpy as np
from scipy import stats
import re
import os

# ── Trait classification ──────────────────────────────────────────────────────
# EFO trait categories
GLYCAN_DIRECT_TERMS = [
    'glycosylation', 'glycan', 'sialyl', 'fucosyl', 'galactosyl',
    'n-glycan', 'o-glycan', 'iga glyco', 'igg glyco', 'transferrin glyco',
    'immunoglobulin glyco'
]

IMMUNE_NONGLYCAN_TERMS = [
    'autoimmune', 'rheumatoid', 'lupus', 'sjogren', 'inflammatory bowel',
    'crohn', 'ulcerative colitis', 'multiple sclerosis', 'type 1 diabetes',
    'celiac', 'psoriasis', 'ankylosing spondylitis', 'asthma',
    'allergic', 'atopy', 'eczema', 'dermatitis', 'hay fever',
    'leukocyte', 'lymphocyte', 'monocyte', 'neutrophil', 'eosinophil',
    'basophil', 'nk cell', 'natural killer', 'cd4', 'cd8', 't cell',
    'b cell', 'immunoglobulin', 'antibody level', 'igg level', 'iga level',
    'igm level', 'immune response', 'vaccination', 'vaccine response',
    'white blood cell', 'platelet', 'granulocyte', 'hematocrit', 'lymphoma',
    'leukemia', 'sepsis', 'infection susceptibility', 'covid', 'hiv',
    'primary biliary', 'primary sclerosing', 'giant cell arteritis',
    'takayasu', 'vasculitis', 'uveitis', 'iritis', 'erythrocyte sedimentation',
    'c-reactive protein', 'interleukin', 'tumor necrosis factor', 'interferon'
]


def classify_trait(trait_str):
    """Classify MAPPED_TRAIT string into a category."""
    if pd.isna(trait_str):
        return 'other'
    t = str(trait_str).lower()

    for term in GLYCAN_DIRECT_TERMS:
        if term in t:
            return 'glycan_direct'

    for term in IMMUNE_NONGLYCAN_TERMS:
        if term in t:
            return 'immune_nonglycan'

    return 'other'


# ── Gene lists ────────────────────────────────────────────────────────────────
UPSTREAM_CORE = [
    'HK1','MPI','PMM1','PMM2','GMPPA','GMPPB','DPM1','DPM2','DPM3','DOLK',
    'DOLPP1','DHDDS','NUS1','SRD5A3','MPDU1','PGM3','UAP1','GFPT1','GFPT2',
    'GNPNAT1','NAGK','GNE','NANS','NANP','CMAS','SLC35A1','GMDS','FPGT',
    'FCSK','SLC35C1','DPAGT1','ALG13','ALG14','ALG1','ALG2','ALG11','RFT1',
    'ALG3','ALG9','ALG12','ALG6','ALG8','ALG10','ALG10B','ALG5','STT3A',
    'STT3B','DDOST','DAD1','RPN1','RPN2','OST4','OSTC','TMEM258','MAGT1','TUSC3'
]

DOWNSTREAM_DIVERS = [
    'MOGS','GANAB','PRKCSH','UGGT1','UGGT2','CANX','CALR','PDIA3','MAN1B1',
    'EDEM1','EDEM2','EDEM3','MLEC','NGLY1','ENGASE','OS9','SEL1L',
    'MAN1A1','MAN1A2','MAN1C1','MGAT1','MAN2A1','MAN2A2','MGAT2','MGAT3',
    'MGAT4A','MGAT4B','MGAT4C','MGAT5','FUT8','FUT3','B4GALT1','B4GALT2',
    'B4GALT3','B4GALT4','B4GALT5','B4GALT6','ST3GAL4','ST6GAL1','ST8SIA2',
    'ST8SIA3','ST8SIA6','CHST8','CHST10','B4GALNT2'
]

ALL_NGLYCO = set(UPSTREAM_CORE + DOWNSTREAM_DIVERS)


def load_gwas(zip_path, pvalue_mlog_cutoff=7.3):
    """Load and filter GWAS catalog associations."""
    print(f"Loading GWAS catalog from {os.path.basename(zip_path)}...")
    dfs = []
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            with z.open(name) as f:
                df = pd.read_csv(f, sep='\t', low_memory=False,
                                 usecols=['MAPPED_GENE', 'DISEASE/TRAIT',
                                          'MAPPED_TRAIT', 'PVALUE_MLOG'])
                dfs.append(df)
    gwas = pd.concat(dfs, ignore_index=True)
    gwas_sig = gwas[gwas['PVALUE_MLOG'] >= pvalue_mlog_cutoff].copy()
    print(f"  Total rows: {len(gwas):,}")
    print(f"  GWS associations (p<5e-8): {len(gwas_sig):,}")
    return gwas_sig


def explode_to_gene_trait(gwas_sig):
    """Explode MAPPED_GENE (comma/pipe-separated) into one row per gene."""
    print("Exploding to gene-trait pairs...")
    rows = []
    for _, row in gwas_sig.iterrows():
        mg = row['MAPPED_GENE']
        if pd.isna(mg):
            continue
        # Handle both " - " (intergenic) and ", " (mapped gene list)
        genes = re.split(r',\s*', str(mg).replace(' - ', ','))
        for g in genes:
            g = g.strip()
            if g and g != 'NR':
                rows.append({
                    'gene': g,
                    'mapped_trait': row['MAPPED_TRAIT'],
                    'pvalue_mlog': row['PVALUE_MLOG'],
                    'category': classify_trait(row['MAPPED_TRAIT'])
                })
    gene_trait = pd.DataFrame(rows)
    print(f"  Gene-trait pairs: {len(gene_trait):,}")
    print(f"  Unique genes: {gene_trait['gene'].nunique():,}")
    return gene_trait


def build_gene_profile(gene_trait):
    """For each gene: total hits, glycan hits, immune hits."""
    profile = gene_trait.groupby('gene').agg(
        total_hits=('category', 'count'),
        glycan_hits=('category', lambda x: (x == 'glycan_direct').sum()),
        immune_hits=('category', lambda x: (x == 'immune_nonglycan').sum()),
        other_hits=('category', lambda x: (x == 'other').sum())
    ).reset_index()
    profile['glycan_or_immune_hits'] = profile['glycan_hits'] + profile['immune_hits']
    return profile


def matched_null_test(profile, focal_genes, background_exclude, n_bins=10):
    """
    For focal_genes: test enrichment for glycan/immune traits.
    Background: all genes NOT in background_exclude, matched by total_hits decile.

    Returns:
        summary dict with Fisher test results and binomial test
    """
    profile['group'] = 'background'
    profile.loc[profile['gene'].isin(focal_genes), 'group'] = 'focal'
    profile.loc[profile['gene'].isin(background_exclude - set(focal_genes)), 'group'] = 'exclude'

    focal = profile[profile['group'] == 'focal'].copy()
    bg = profile[profile['group'] == 'background'].copy()

    print(f"\nFocal genes: {len(focal)} with GWAS data")
    print(f"Background genes: {len(bg):,}")

    # --- Simple (unmatched) Fisher test ---
    focal_with = (focal['glycan_or_immune_hits'] > 0).sum()
    focal_without = len(focal) - focal_with
    bg_with = (bg['glycan_or_immune_hits'] > 0).sum()
    bg_without = len(bg) - bg_with

    table_unmatched = [[focal_with, focal_without], [bg_with, bg_without]]
    or_unmatched, p_unmatched = stats.fisher_exact(table_unmatched, alternative='greater')
    print(f"\nUnmatched Fisher test (glycan/immune hit ≥1):")
    print(f"  Focal: {focal_with}/{len(focal)} = {focal_with/len(focal):.1%}")
    print(f"  Background: {bg_with}/{len(bg)} = {bg_with/len(bg):.1%}")
    print(f"  OR={or_unmatched:.2f}, p={p_unmatched:.2e}")

    # --- Hit-count–matched background ---
    # Bin all genes by log10(total_hits+1) decile
    all_with_hits = profile[profile['total_hits'] > 0].copy()
    all_with_hits['hit_bin'] = pd.qcut(
        np.log10(all_with_hits['total_hits'] + 1),
        q=n_bins, labels=False, duplicates='drop'
    )

    # For each focal gene, sample background genes in same bin (5:1 ratio)
    np.random.seed(42)
    matched_bg_rows = []
    focal_with_hits = all_with_hits[all_with_hits['group'] == 'focal']
    bg_pool = all_with_hits[all_with_hits['group'] == 'background']

    for _, frow in focal_with_hits.iterrows():
        bin_bg = bg_pool[bg_pool['hit_bin'] == frow['hit_bin']]
        n_sample = min(5, len(bin_bg))
        if n_sample > 0:
            sampled = bin_bg.sample(n=n_sample, replace=False)
            matched_bg_rows.append(sampled)

    if matched_bg_rows:
        matched_bg = pd.concat(matched_bg_rows).drop_duplicates('gene')
    else:
        matched_bg = pd.DataFrame()

    if len(matched_bg) > 0:
        mb_with = (matched_bg['glycan_or_immune_hits'] > 0).sum()
        mb_without = len(matched_bg) - mb_with
        table_matched = [[focal_with, focal_without], [mb_with, mb_without]]
        or_matched, p_matched = stats.fisher_exact(table_matched, alternative='greater')
        print(f"\nMatched Fisher test (hit-count matched, 5:1 ratio):")
        print(f"  Focal: {focal_with}/{len(focal)} = {focal_with/len(focal):.1%}")
        print(f"  Matched background: {mb_with}/{len(matched_bg)} = {mb_with/len(matched_bg):.1%}")
        print(f"  OR={or_matched:.2f}, p={p_matched:.2e}")
    else:
        or_matched, p_matched = None, None
        matched_bg = pd.DataFrame()

    # --- Trait-count comparison ---
    print(f"\nMedian glycan/immune hits:")
    print(f"  Focal: {focal['glycan_or_immune_hits'].median():.1f}")
    if len(matched_bg) > 0:
        print(f"  Matched background: {matched_bg['glycan_or_immune_hits'].median():.1f}")
    mw_stat, mw_p = stats.mannwhitneyu(
        focal['glycan_or_immune_hits'],
        bg['glycan_or_immune_hits'],
        alternative='greater'
    )
    print(f"  Mann-Whitney U (focal > bg): p={mw_p:.2e}")

    return {
        'focal': focal,
        'background': bg,
        'matched_bg': matched_bg,
        'unmatched_OR': or_unmatched,
        'unmatched_p': p_unmatched,
        'matched_OR': or_matched,
        'matched_p': p_matched,
        'mw_p': mw_p,
    }


def summarize_top_traits(gene_trait, gene_list, label, top_n=15):
    """Show top traits for a group of genes."""
    df = gene_trait[gene_trait['gene'].isin(gene_list)]
    print(f"\nTop {top_n} traits in {label} ({len(df)} hits, {df['gene'].nunique()} genes):")
    print(df['mapped_trait'].value_counts().head(top_n).to_string())


def main():
    zip_path = "data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip"
    os.makedirs("results/tables", exist_ok=True)

    gwas_sig = load_gwas(zip_path)
    gene_trait = explode_to_gene_trait(gwas_sig)
    profile = build_gene_profile(gene_trait)

    print("\n" + "="*70)
    print("GWAS NULL MODEL — Downstream N-glyco gene trait enrichment")
    print("="*70)

    # --- Downstream vs. genome-wide background ---
    print("\n\n--- TEST A: DOWNSTREAM vs GENOME-WIDE BACKGROUND ---")
    res_dn = matched_null_test(
        profile.copy(),
        focal_genes=set(DOWNSTREAM_DIVERS),
        background_exclude=ALL_NGLYCO
    )

    # --- Upstream vs. genome-wide background (control) ---
    print("\n\n--- TEST B: UPSTREAM (CONTROL) vs GENOME-WIDE BACKGROUND ---")
    res_up = matched_null_test(
        profile.copy(),
        focal_genes=set(UPSTREAM_CORE),
        background_exclude=ALL_NGLYCO
    )

    # --- Downstream vs. upstream direct comparison ---
    print("\n\n--- TEST C: DOWNSTREAM vs UPSTREAM (DIRECT) ---")
    dn_profile = profile[profile['gene'].isin(DOWNSTREAM_DIVERS)].copy()
    up_profile = profile[profile['gene'].isin(UPSTREAM_CORE)].copy()

    dn_glycan_immune = dn_profile['glycan_or_immune_hits'].sum()
    dn_other = dn_profile['other_hits'].sum()
    up_glycan_immune = up_profile['glycan_or_immune_hits'].sum()
    up_other = up_profile['other_hits'].sum()

    table_vs = [[dn_glycan_immune, dn_other], [up_glycan_immune, up_other]]
    or_vs, p_vs = stats.fisher_exact(table_vs, alternative='greater')
    print(f"  Downstream: {dn_glycan_immune} glycan/immune, {dn_other} other")
    print(f"  Upstream:   {up_glycan_immune} glycan/immune, {up_other} other")
    print(f"  OR={or_vs:.2f}, p={p_vs:.2e}")

    # --- Top traits ---
    summarize_top_traits(gene_trait, DOWNSTREAM_DIVERS, "Downstream N-glyco")
    summarize_top_traits(gene_trait, UPSTREAM_CORE, "Upstream N-glyco")

    # --- Per-gene breakdown for downstream ---
    print("\n\nPer-gene GWAS hit profile (downstream genes with most hits):")
    dn_profile_sorted = dn_profile.sort_values('glycan_or_immune_hits', ascending=False)
    print(dn_profile_sorted[['gene','total_hits','glycan_hits','immune_hits','other_hits']].head(20).to_string(index=False))

    # --- Summary table ---
    print("\n\n" + "="*70)
    print("SUMMARY TABLE")
    print("="*70)
    print(f"{'Test':<50}  {'OR':>6}  {'p-value':>10}  {'Sig':>5}")
    print("-"*75)

    def sigcode(p):
        if p is None: return 'n/a'
        if p < 0.001: return '***'
        if p < 0.01: return '**'
        if p < 0.05: return '*'
        return 'n.s.'

    rows = [
        ("Downstream vs genome (unmatched)", res_dn['unmatched_OR'], res_dn['unmatched_p']),
        ("Downstream vs genome (hit-matched)", res_dn['matched_OR'], res_dn['matched_p']),
        ("Upstream vs genome (unmatched)", res_up['unmatched_OR'], res_up['unmatched_p']),
        ("Upstream vs genome (hit-matched)", res_up['matched_OR'], res_up['matched_p']),
        ("Downstream vs upstream (direct)", or_vs, p_vs),
    ]
    for label, OR, p in rows:
        or_str = f"{OR:.2f}" if OR is not None else 'n/a'
        p_str = f"{p:.2e}" if p is not None else 'n/a'
        print(f"  {label:<50}  {or_str:>6}  {p_str:>10}  {sigcode(p):>5}")

    # --- Write outputs ---
    # Save per-gene profile
    gene_trait_grouped = gene_trait.groupby(['gene','category'])['mapped_trait'].count().unstack(fill_value=0).reset_index()
    dn_table = dn_profile_sorted.copy()
    dn_table['group'] = 'downstream'
    up_table = up_profile.copy()
    up_table['group'] = 'upstream'
    out_profile = pd.concat([dn_table, up_table], ignore_index=True)
    out_profile.to_csv("results/tables/gwas_null_model_gene_profile.tsv", sep='\t', index=False)
    print("\nSaved: results/tables/gwas_null_model_gene_profile.tsv")

    # Save summary
    summary_lines = [
        "GWAS GENOME-WIDE NULL MODEL — N-glyco downstream gene enrichment",
        "="*70,
        "",
        "Question: Is the immune/glycan GWAS enrichment in downstream N-glyco genes",
        "explained by gene length (more LD capture) or is it pathway-specific?",
        "",
        "Trait classification:",
        "  glycan_direct: IgG glycosylation, N-glycan, transferrin glycosylation",
        "  immune_nonglycan: autoimmune, blood cell traits, immune biomarkers",
        "  other: cardiometabolic, anthropometric, neurological, etc.",
        "",
        f"Downstream N-glyco genes: {len(res_dn['focal'])} with GWAS hits",
        f"Upstream N-glyco genes: {len(res_up['focal'])} with GWAS hits",
        f"Background (non-N-glyco): {len(res_dn['background']):,} genes",
        "",
        "RESULTS:",
    ]
    for label, OR, p in rows:
        or_str = f"{OR:.2f}" if OR is not None else 'n/a'
        p_str = f"{p:.2e}" if p is not None else 'n/a'
        summary_lines.append(f"  {label}: OR={or_str}, p={p_str} {sigcode(p)}")

    summary_lines += [
        "",
        "INTERPRETATION:",
        "  If downstream OR > upstream OR: enrichment is LAYER-SPECIFIC, not gene-density artifact",
        "  If matched p remains significant: enrichment SURVIVES length control",
        "",
        "Outputs: results/tables/gwas_null_model_gene_profile.tsv",
    ]
    with open("results/tables/gwas_null_model_summary.txt", 'w') as f:
        f.write('\n'.join(summary_lines))
    print("Saved: results/tables/gwas_null_model_summary.txt")

    print("\nDone.")


if __name__ == '__main__':
    main()
