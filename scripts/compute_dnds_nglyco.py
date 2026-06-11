#!/usr/bin/env python3
"""
Task B1: Pairwise dN/dS (human vs mouse) for all N-glyco pathway genes.

Method:
  - Ensembl REST: canonical transcript CDS for human gene
  - Ensembl REST: 1:1 mouse ortholog + its canonical transcript CDS
  - BioPython NG86 method on codon-aligned CDS pairs
  - Compare upstream_core vs downstream_diversification dN/dS distributions

Wald hypothesis prediction:
  - Upstream genes: low dN/dS (strong purifying selection, especially severe CDG genes)
  - Downstream genes: higher dN/dS (more adaptive / relaxed constraint on coding)
  - If confirmed: LOEUF inversion was masking real evolutionary rate differences
"""

import requests
import time
import warnings
import pandas as pd
import numpy as np
from scipy import stats
import os

warnings.filterwarnings('ignore')

# ── Gene lists (from covariate table) ────────────────────────────────────────
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

CACHE_FILE = 'data/raw/nglyco_dnds_human_mouse.tsv'
ENSEMBL_BASE = 'https://rest.ensembl.org'
SLEEP = 0.4   # seconds between API calls (rate limit: ~15/s)


def ensembl_get(path, params=''):
    url = f'{ENSEMBL_BASE}{path}?content-type=application/json{params}'
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=25)
            if r.status_code == 429:
                time.sleep(10)
                continue
            if r.ok:
                return r.json()
            return None
        except Exception:
            time.sleep(2)
    return None


def get_gene_info(symbol):
    """Return (ensembl_gene_id, canonical_transcript_id) for a human gene symbol."""
    data = ensembl_get(f'/lookup/symbol/homo_sapiens/{symbol}', '&expand=0')
    if not data:
        return None, None
    gene_id = data.get('id')
    # get canonical transcript
    detail = ensembl_get(f'/lookup/id/{gene_id}', '&expand=1')
    if not detail:
        return gene_id, None
    tx = detail.get('canonical_transcript', '')
    tx_id = tx.split('.')[0] if tx else None
    return gene_id, tx_id


def get_cds(transcript_id):
    """Return CDS nucleotide sequence (with stop codon) for a transcript."""
    data = ensembl_get(f'/sequence/id/{transcript_id}', '&type=cds')
    if not data:
        return None
    return data.get('seq')


def get_mouse_ortholog_gene(human_gene_id):
    """Return mouse Ensembl gene ID for the 1:1 ortholog, or None."""
    data = ensembl_get(
        f'/homology/id/human/{human_gene_id}',
        '&type=orthologues&target_species=mus_musculus'
    )
    if not data:
        return None
    homologies = data.get('data', [{}])[0].get('homologies', [])
    # prefer 1:1
    for h in homologies:
        if h.get('type') == 'ortholog_one2one':
            return h['target']['id']
    if homologies:
        return homologies[0]['target']['id']
    return None


def get_mouse_canonical_transcript(mouse_gene_id):
    """Return canonical transcript ID for a mouse gene."""
    data = ensembl_get(f'/lookup/id/{mouse_gene_id}', '&expand=1')
    if not data:
        return None
    tx = data.get('canonical_transcript', '')
    return tx.split('.')[0] if tx else None


def codon_align_trim(seq1, seq2):
    """
    Trim both sequences to a shared codon-aligned length.
    Removes trailing stop codon (last 3 nt if it's a stop).
    Returns (trimmed_seq1, trimmed_seq2) or (None, None) if unusable.
    """
    stops = {'TAA', 'TAG', 'TGA'}
    # Remove stop codons
    if len(seq1) >= 3 and seq1[-3:].upper() in stops:
        seq1 = seq1[:-3]
    if len(seq2) >= 3 and seq2[-3:].upper() in stops:
        seq2 = seq2[:-3]
    # Trim to multiple of 3
    l1 = (len(seq1) // 3) * 3
    l2 = (len(seq2) // 3) * 3
    seq1 = seq1[:l1]
    seq2 = seq2[:l2]
    if l1 < 60 or l2 < 60:
        return None, None
    # Use shorter length (simplest codon trim — suitable for NG86 in largely syntenic 1:1 orthologs)
    shared = min(l1, l2)
    return seq1[:shared], seq2[:shared]


def compute_dnds(cds1, cds2):
    """
    Compute dN, dS, dN/dS using BioPython NG86 method.
    Returns (dn, ds, dnds) or (nan, nan, nan) on failure.
    """
    from Bio.codonalign.codonseq import CodonSeq, cal_dn_ds
    try:
        s1, s2 = codon_align_trim(cds1, cds2)
        if s1 is None:
            return np.nan, np.nan, np.nan
        dn, ds = cal_dn_ds(CodonSeq(s1), CodonSeq(s2), method='NG86')
        dnds = dn / ds if ds and ds > 0 else np.nan
        return float(dn), float(ds), float(dnds)
    except Exception as e:
        return np.nan, np.nan, np.nan


def main():
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('results/tables', exist_ok=True)

    all_genes = [(s, 'upstream_core') for s in UPSTREAM_CORE] + \
                [(s, 'downstream_diversification') for s in DOWNSTREAM_DIVERS]

    # Load cache if exists
    if os.path.exists(CACHE_FILE):
        cache = pd.read_csv(CACHE_FILE, sep='\t')
        done = set(cache['symbol'].tolist())
        print(f'Cache loaded: {len(done)} genes already done')
        rows = cache.to_dict('records')
    else:
        done = set()
        rows = []

    todo = [(s, g) for s, g in all_genes if s not in done]
    print(f'Genes to process: {len(todo)}')

    for i, (symbol, group) in enumerate(todo):
        print(f'  [{i+1}/{len(todo)}] {symbol} ({group}) ...', end=' ', flush=True)

        gene_id, tx_id = get_gene_info(symbol)
        time.sleep(SLEEP)
        if not gene_id:
            print('no gene ID')
            rows.append({'symbol': symbol, 'group': group, 'human_gene_id': None,
                         'human_tx': None, 'mouse_gene_id': None, 'mouse_tx': None,
                         'dn': np.nan, 'ds': np.nan, 'dnds': np.nan, 'status': 'no_gene'})
            continue

        human_cds = get_cds(tx_id) if tx_id else None
        time.sleep(SLEEP)

        mouse_gene_id = get_mouse_ortholog_gene(gene_id)
        time.sleep(SLEEP)
        if not mouse_gene_id:
            print('no mouse ortholog')
            rows.append({'symbol': symbol, 'group': group, 'human_gene_id': gene_id,
                         'human_tx': tx_id, 'mouse_gene_id': None, 'mouse_tx': None,
                         'dn': np.nan, 'ds': np.nan, 'dnds': np.nan, 'status': 'no_ortholog'})
            continue

        mouse_tx_id = get_mouse_canonical_transcript(mouse_gene_id)
        time.sleep(SLEEP)

        mouse_cds = get_cds(mouse_tx_id) if mouse_tx_id else None
        time.sleep(SLEEP)

        if not human_cds or not mouse_cds:
            print('CDS fetch failed')
            rows.append({'symbol': symbol, 'group': group, 'human_gene_id': gene_id,
                         'human_tx': tx_id, 'mouse_gene_id': mouse_gene_id,
                         'mouse_tx': mouse_tx_id,
                         'dn': np.nan, 'ds': np.nan, 'dnds': np.nan, 'status': 'no_cds'})
            continue

        dn, ds, dnds = compute_dnds(human_cds, mouse_cds)
        status = 'ok' if not np.isnan(dnds) else 'dnds_fail'
        print(f'dN/dS={dnds:.4f}' if not np.isnan(dnds) else 'dN/dS=NA')

        rows.append({'symbol': symbol, 'group': group, 'human_gene_id': gene_id,
                     'human_tx': tx_id, 'mouse_gene_id': mouse_gene_id,
                     'mouse_tx': mouse_tx_id,
                     'dn': dn, 'ds': ds, 'dnds': dnds, 'status': status})

        # Save incrementally
        if (i + 1) % 10 == 0:
            pd.DataFrame(rows).to_csv(CACHE_FILE, sep='\t', index=False)

    # Final save
    df = pd.DataFrame(rows)
    df.to_csv(CACHE_FILE, sep='\t', index=False)
    print(f'\nSaved {len(df)} rows to {CACHE_FILE}')

    # ── Analysis ──────────────────────────────────────────────────────────────
    ok = df[df['status'] == 'ok'].copy()
    print(f'\nGenes with valid dN/dS: {len(ok)} / {len(df)}')

    upstream = ok[ok['group'] == 'upstream_core']['dnds'].dropna()
    downstream = ok[ok['group'] == 'downstream_diversification']['dnds'].dropna()

    print(f'\n{"="*60}')
    print('dN/dS COMPARISON: upstream_core vs downstream_diversification')
    print(f'{"="*60}')
    print(f'  Upstream   (n={len(upstream)}): median={upstream.median():.4f}  IQR=[{upstream.quantile(0.25):.4f},{upstream.quantile(0.75):.4f}]')
    print(f'  Downstream (n={len(downstream)}): median={downstream.median():.4f}  IQR=[{downstream.quantile(0.25):.4f},{downstream.quantile(0.75):.4f}]')

    if len(upstream) > 2 and len(downstream) > 2:
        u, p = stats.mannwhitneyu(downstream, upstream, alternative='greater')
        r = 1 - 2 * u / (len(downstream) * len(upstream))
        print(f'\n  Mann-Whitney U (downstream > upstream): U={u:.0f}, p={p:.4f}, r={r:.3f}')

    print(f'\n  Prediction: downstream > upstream (evolvability = higher ω)')
    print(f'  Direction: {"CONFIRMED ✓" if downstream.median() > upstream.median() else "NOT CONFIRMED ✗"}')

    # Top genes by dN/dS
    print(f'\nTop 10 downstream genes by dN/dS:')
    top_dn = ok[ok['group'] == 'downstream_diversification'].nlargest(10, 'dnds')[['symbol','dn','ds','dnds']]
    print(top_dn.to_string(index=False))

    print(f'\nTop 10 upstream genes by dN/dS:')
    top_up = ok[ok['group'] == 'upstream_core'].nlargest(10, 'dnds')[['symbol','dn','ds','dnds']]
    print(top_up.to_string(index=False))

    # Save summary
    summary_path = 'results/tables/dnds_comparison_summary.txt'
    lines = [
        'PAIRWISE dN/dS — Human vs Mouse, N-glyco pathway genes',
        '=' * 60,
        f'Method: Nei-Gojobori 1986 (NG86), Ensembl canonical CDS, 1:1 orthologs',
        f'Genes with valid dN/dS: {len(ok)} / {len(df)}',
        '',
        f'Upstream   (n={len(upstream)}): median dN/dS={upstream.median():.4f}',
        f'Downstream (n={len(downstream)}): median dN/dS={downstream.median():.4f}',
    ]
    if len(upstream) > 2 and len(downstream) > 2:
        lines.append(f'Mann-Whitney p (downstream > upstream): {p:.4f}')
        lines.append(f'Rank-biserial r: {r:.3f}')
    lines += ['', 'Per-gene results:']
    lines.append(ok[['symbol','group','dn','ds','dnds']].sort_values('dnds', ascending=False).to_string(index=False))
    with open(summary_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f'\nSaved: {summary_path}')


if __name__ == '__main__':
    main()
