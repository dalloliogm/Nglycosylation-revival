#!/usr/bin/env python3
"""
Task B2: IgG glycome GWAS locus contribution — upstream vs downstream N-glyco genes.

Question: Do downstream N-glyco gene variants account for more IgG glycan
phenotype associations (independent loci, summed effect size) than upstream genes?

Data: GWAS Catalog v1.0.2, filtered to IgG glycosylation and N-glycan measurement.
Method:
  1. Extract IgG/N-glycan GWS associations (p < 5e-8)
  2. Assign each association to pathway layer via MAPPED_GENE
  3. Collapse nearby SNPs on same chromosome into independent loci (500 kb windows)
  4. Compare locus count, mean |beta|, and summed effect proxy per layer
  5. Fisher's exact test: does downstream layer capture more independent IgG-glycan loci?
"""

import zipfile
import pandas as pd
import numpy as np
from scipy import stats
import re
import os

UPSTREAM_CORE = {
    'HK1','MPI','PMM1','PMM2','GMPPA','GMPPB','DPM1','DPM2','DPM3','DOLK',
    'DOLPP1','DHDDS','NUS1','SRD5A3','MPDU1','PGM3','UAP1','GFPT1','GFPT2',
    'GNPNAT1','NAGK','GNE','NANS','NANP','CMAS','SLC35A1','GMDS','FPGT',
    'FCSK','SLC35C1','DPAGT1','ALG13','ALG14','ALG1','ALG2','ALG11','RFT1',
    'ALG3','ALG9','ALG12','ALG6','ALG8','ALG10','ALG10B','ALG5','STT3A',
    'STT3B','DDOST','DAD1','RPN1','RPN2','OST4','OSTC','TMEM258','MAGT1','TUSC3'
}

DOWNSTREAM_DIVERS = {
    'MOGS','GANAB','PRKCSH','UGGT1','UGGT2','CANX','CALR','PDIA3','MAN1B1',
    'EDEM1','EDEM2','EDEM3','MLEC','NGLY1','ENGASE','OS9','SEL1L',
    'MAN1A1','MAN1A2','MAN1C1','MGAT1','MAN2A1','MAN2A2','MGAT2','MGAT3',
    'MGAT4A','MGAT4B','MGAT4C','MGAT5','FUT8','FUT3','B4GALT1','B4GALT2',
    'B4GALT3','B4GALT4','B4GALT5','B4GALT6','ST3GAL4','ST6GAL1','ST8SIA2',
    'ST8SIA3','ST8SIA6','CHST8','CHST10','B4GALNT2'
}

ALL_NGLYCO = UPSTREAM_CORE | DOWNSTREAM_DIVERS
LD_WINDOW_BP = 500_000   # independent-locus clumping window


def load_glycan_gwas(zip_path):
    print(f"Loading GWAS catalog...")
    dfs = []
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            with z.open(name) as f:
                df = pd.read_csv(f, sep='\t', low_memory=False,
                                 usecols=['MAPPED_GENE','DISEASE/TRAIT',
                                          'MAPPED_TRAIT','SNPS','OR or BETA',
                                          '95% CI (TEXT)','PVALUE_MLOG',
                                          'PUBMEDID','CHR_ID','CHR_POS'])
                dfs.append(df)
    gwas = pd.concat(dfs, ignore_index=True)
    gwas_sig = gwas[gwas['PVALUE_MLOG'] >= 7.3].copy()

    # IgG glycan traits only (exclude unrelated proteoglycan terms)
    mask = gwas_sig['MAPPED_TRAIT'].fillna('').str.lower().str.contains(
        r'igg glyco|n-glycan measurement|transferrin glyco'
    )
    iglycan = gwas_sig[mask].copy()

    # Parse beta / effect size
    iglycan['beta'] = pd.to_numeric(iglycan['OR or BETA'], errors='coerce')
    iglycan['abs_beta'] = iglycan['beta'].abs()

    # Parse effect direction from CI text
    iglycan['direction'] = iglycan['95% CI (TEXT)'].fillna('').apply(
        lambda x: -1 if 'decrease' in x.lower() else (1 if 'increase' in x.lower() else 0)
    )
    iglycan['signed_beta'] = iglycan['beta'] * iglycan['direction']

    # Numeric chromosome and position
    iglycan['chrom'] = pd.to_numeric(iglycan['CHR_ID'], errors='coerce')
    iglycan['pos'] = pd.to_numeric(iglycan['CHR_POS'], errors='coerce')

    print(f"  Total IgG/N-glycan GWS associations: {len(iglycan)}")
    return iglycan


def assign_layer(gene_str):
    """Return layer for a MAPPED_GENE string (may be comma-sep)."""
    if pd.isna(gene_str):
        return 'none'
    genes = {g.strip() for g in re.split(r',\s*', str(gene_str).replace(' - ', ','))}
    has_dn = bool(genes & DOWNSTREAM_DIVERS)
    has_up = bool(genes & UPSTREAM_CORE)
    if has_dn and not has_up:
        return 'downstream'
    if has_up and not has_dn:
        return 'upstream'
    if has_dn and has_up:
        return 'both'
    return 'other'


def clump_loci(df, window_bp=LD_WINDOW_BP):
    """
    Within each chromosome, greedily assign independent loci:
    sort by -log10(p), then any SNP within window_bp of an assigned locus
    is considered the same locus.
    Returns df with added 'locus_id' column.
    """
    df = df.copy()
    df['locus_id'] = -1
    df_sorted = df.dropna(subset=['chrom','pos']).sort_values('PVALUE_MLOG', ascending=False)

    locus_id = 0
    assigned = {}   # locus_id -> (chrom, pos)
    for idx, row in df_sorted.iterrows():
        ch, p = row['chrom'], row['pos']
        # Check if within window of any existing locus on same chromosome
        merged = False
        for lid, (lch, lpos) in assigned.items():
            if lch == ch and abs(p - lpos) <= window_bp:
                df.at[idx, 'locus_id'] = lid
                merged = True
                break
        if not merged:
            df.at[idx, 'locus_id'] = locus_id
            assigned[locus_id] = (ch, p)
            locus_id += 1

    return df, locus_id


def per_gene_summary(iglycan):
    """For each N-glyco gene, count IgG-glycan loci and effect proxy."""
    rows = []
    for gene in sorted(ALL_NGLYCO):
        layer = 'downstream' if gene in DOWNSTREAM_DIVERS else 'upstream'
        # rows where this gene appears in MAPPED_GENE
        mask = iglycan['MAPPED_GENE'].fillna('').str.contains(
            r'(?<![A-Z0-9])' + re.escape(gene) + r'(?![A-Z0-9])', regex=True
        )
        hits = iglycan[mask]
        if len(hits) == 0:
            rows.append({'gene': gene, 'layer': layer,
                         'n_raw_hits': 0, 'n_indep_loci': 0,
                         'sum_abs_beta': 0, 'max_abs_beta': 0,
                         'mean_abs_beta': np.nan})
            continue
        # Count independent loci via clumping
        hits_loc, _ = clump_loci(hits)
        n_loci = hits_loc['locus_id'].nunique()
        ab = hits['abs_beta'].dropna()
        rows.append({
            'gene': gene, 'layer': layer,
            'n_raw_hits': len(hits),
            'n_indep_loci': n_loci,
            'sum_abs_beta': ab.sum(),
            'max_abs_beta': ab.max() if len(ab) > 0 else 0,
            'mean_abs_beta': ab.mean() if len(ab) > 0 else np.nan,
        })
    return pd.DataFrame(rows)


def layer_locus_test(iglycan):
    """
    Global test: for independent loci in IgG/glycan GWAS,
    does downstream layer capture more loci than upstream?
    Assign each locus to a layer; test with Fisher's exact.
    """
    iglycan = iglycan.copy()
    iglycan['layer'] = iglycan['MAPPED_GENE'].apply(assign_layer)

    # Clump globally
    iglycan_loc, total_loci = clump_loci(iglycan)
    print(f"  Total independent IgG/glycan loci (500 kb windows): {total_loci}")

    # For each locus, take the most significant row, then assign layer
    best_per_locus = (iglycan_loc[iglycan_loc['locus_id'] >= 0]
                      .sort_values('PVALUE_MLOG', ascending=False)
                      .groupby('locus_id').first().reset_index())
    best_per_locus['layer'] = best_per_locus['MAPPED_GENE'].apply(assign_layer)

    layer_counts = best_per_locus['layer'].value_counts()
    print(f"\n  Loci by layer assignment:")
    print(layer_counts.to_string())

    dn_loci = layer_counts.get('downstream', 0)
    up_loci = layer_counts.get('upstream', 0)
    other_loci = layer_counts.get('other', 0) + layer_counts.get('both', 0) + layer_counts.get('none', 0)

    # Fisher: downstream vs upstream (ignore other/both)
    # 2x2: [downstream_nglyco, upstream_nglyco] vs [other_genes]
    total = len(best_per_locus)
    table = [[dn_loci, total - dn_loci],
             [up_loci, total - up_loci]]
    or_dn, p_dn = stats.fisher_exact([[dn_loci, other_loci + up_loci],
                                       [len(DOWNSTREAM_DIVERS), len(UPSTREAM_CORE) + 10000]],
                                      alternative='greater')

    # Direct comparison downstream vs upstream loci
    if up_loci > 0:
        print(f"\n  Downstream: {dn_loci} loci  Upstream: {up_loci} loci")
        print(f"  Ratio downstream/upstream: {dn_loci/up_loci:.1f}x")

    return best_per_locus, layer_counts


def main():
    os.makedirs('results/tables', exist_ok=True)
    zip_path = 'data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip'

    iglycan = load_glycan_gwas(zip_path)

    print("\n" + "="*65)
    print("GLYCOME GWAS VARIANCE PARTITIONING — N-glyco pathway layers")
    print("="*65)

    # --- Per-gene analysis ---
    gene_df = per_gene_summary(iglycan)

    up = gene_df[gene_df['layer'] == 'upstream']
    dn = gene_df[gene_df['layer'] == 'downstream']

    print(f"\n--- PER-GENE IgG/N-GLYCAN LOCUS COUNTS ---")
    print(f"Upstream   ({len(up)} genes): "
          f"median loci={up.n_indep_loci.median():.1f}  "
          f"total loci={up.n_indep_loci.sum()}")
    print(f"Downstream ({len(dn)} genes): "
          f"median loci={dn.n_indep_loci.median():.1f}  "
          f"total loci={dn.n_indep_loci.sum()}")

    # Genes with any loci
    up_any = (up.n_indep_loci > 0).sum()
    dn_any = (dn.n_indep_loci > 0).sum()
    print(f"\nGenes with ≥1 IgG-glycan locus: upstream {up_any}/{len(up)}, downstream {dn_any}/{len(dn)}")

    or_any, p_any = stats.fisher_exact(
        [[dn_any, len(dn) - dn_any], [up_any, len(up) - up_any]],
        alternative='greater'
    )
    print(f"Fisher (downstream enriched for genes with hits): OR={or_any:.2f}, p={p_any:.4f}")

    # Mann-Whitney on locus counts
    mw_u, mw_p = stats.mannwhitneyu(dn.n_indep_loci, up.n_indep_loci, alternative='greater')
    mw_r = 1 - 2*mw_u / (len(dn)*len(up))
    print(f"Mann-Whitney (downstream > upstream loci/gene): p={mw_p:.4f}, r={mw_r:.3f}")

    # --- Effect size comparison ---
    up_beta = up[up.mean_abs_beta.notna()]['mean_abs_beta']
    dn_beta = dn[dn.mean_abs_beta.notna()]['mean_abs_beta']
    print(f"\n--- EFFECT SIZE (|beta|, genes with any hit) ---")
    if len(up_beta) > 0 and len(dn_beta) > 0:
        print(f"Upstream   (n={len(up_beta)}): median |beta|={up_beta.median():.3f}")
        print(f"Downstream (n={len(dn_beta)}): median |beta|={dn_beta.median():.3f}")
        u2, p2 = stats.mannwhitneyu(dn_beta, up_beta, alternative='two-sided')
        print(f"Mann-Whitney (two-sided): p={p2:.4f}")

    # --- Global locus test ---
    print(f"\n--- GLOBAL INDEPENDENT LOCI BY LAYER ---")
    best_loci, layer_counts = layer_locus_test(iglycan)

    # --- Top downstream genes ---
    print(f"\n--- TOP DOWNSTREAM GENES BY IgG-GLYCAN LOCI ---")
    print(dn.nlargest(10, 'n_indep_loci')[
        ['gene','n_raw_hits','n_indep_loci','mean_abs_beta']
    ].to_string(index=False))

    print(f"\n--- TOP UPSTREAM GENES BY IgG-GLYCAN LOCI ---")
    print(up.nlargest(5, 'n_indep_loci')[
        ['gene','n_raw_hits','n_indep_loci','mean_abs_beta']
    ].to_string(index=False))

    # --- Summary ---
    print(f"\n{'='*65}")
    print("SUMMARY")
    print(f"{'='*65}")
    dn_total = int(dn.n_indep_loci.sum())
    up_total = int(up.n_indep_loci.sum())
    print(f"Total independent IgG/N-glycan loci:")
    print(f"  Downstream N-glyco genes: {dn_total}")
    print(f"  Upstream N-glyco genes:   {up_total}")
    print(f"  Ratio: {dn_total/max(up_total,1):.1f}x more in downstream layer")
    print(f"Genes with ≥1 hit: {dn_any}/{len(dn)} downstream vs {up_any}/{len(up)} upstream")
    print(f"  Fisher OR={or_any:.2f}, p={p_any:.4f}")
    print(f"Per-gene locus count MW: p={mw_p:.4f}, r={mw_r:.3f}")

    # Save
    gene_df.to_csv('results/tables/glycome_gwas_per_gene.tsv', sep='\t', index=False)
    print("\nSaved: results/tables/glycome_gwas_per_gene.tsv")

    summary_lines = [
        "GLYCOME GWAS VARIANCE PARTITIONING",
        "="*65,
        "Data: GWAS Catalog v1.0.2 IgG glycosylation + N-glycan measurement",
        f"GWS associations analysed: {len(iglycan)}",
        f"Independent loci (500 kb clumping): reported per gene",
        "",
        f"DOWNSTREAM layer ({len(dn)} genes):",
        f"  Genes with ≥1 IgG-glycan locus: {dn_any}",
        f"  Total independent loci: {dn_total}",
        f"  Median loci/gene: {dn.n_indep_loci.median():.1f}",
        "",
        f"UPSTREAM layer ({len(up)} genes):",
        f"  Genes with ≥1 IgG-glycan locus: {up_any}",
        f"  Total independent loci: {up_total}",
        f"  Median loci/gene: {up.n_indep_loci.median():.1f}",
        "",
        f"Fisher test (≥1 hit): OR={or_any:.2f}, p={p_any:.4f}",
        f"Mann-Whitney (loci/gene): p={mw_p:.4f}, r={mw_r:.3f}",
        f"Loci ratio downstream/upstream: {dn_total/max(up_total,1):.1f}x",
        "",
        "Note: locus counts reflect GWAS catalog gene mapping (not causal).",
        "Variance explained requires summary stats + MAF (not in catalog).",
    ]
    with open('results/tables/glycome_gwas_summary.txt', 'w') as f:
        f.write('\n'.join(summary_lines))
    print("Saved: results/tables/glycome_gwas_summary.txt")


if __name__ == '__main__':
    main()
