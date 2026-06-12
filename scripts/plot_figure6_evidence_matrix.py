#!/usr/bin/env python3
"""
Figure 6 — Evidence matrix.
Rows = predictions; columns = evidence streams.
Cell values: Supported / Partial / Not confirmed / Not tested.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('results/figures', exist_ok=True)

# ── Matrix definition ─────────────────────────────────────────────────────────
# Predictions (rows)
predictions = [
    'Severe disease\nconcentrates upstream',
    'Disease gradient is\ntopology-dependent',
    'Downstream enriched\nfor glycan-output traits',
    'Heritable glycan-output\nvariation is downstream',
    'Coding constraint does\nnot show simple gradient',
]

# Evidence streams (columns) — abbreviated
streams = [
    'CDG\ncuration',
    'ClinVar\nP/LP',
    'Comparator\npathways',
    'GWAS null\nmodel',
    'IgG glycan\nloci',
    'LOEUF\nregression',
    'dN/dS\nhuman-mouse',
    'Cross-species\n% identity',
]

# Cell outcomes: S=Supported, P=Partial, N=Not confirmed, X=Not tested
# (rows × cols)
matrix = [
    #CDG   ClinVar  Comp  GWAS   IgG   LOEUF  dNdS   %ID
    ['S',   'S',    'S',  'X',   'X',  'X',   'X',   'X'],   # disease upstream
    ['X',   'X',    'S',  'X',   'X',  'X',   'X',   'X'],   # topology-dep
    ['X',   'X',    'X',  'P',   'X',  'X',   'X',   'X'],   # glycan-trait enrich
    ['X',   'X',    'X',  'X',   'S',  'X',   'X',   'X'],   # heritable output
    ['X',   'X',    'X',  'X',   'X',  'S',   'S',   'S'],   # no coding gradient
]

# Annotation text (short note per cell that isn't X)
notes = {
    (0, 0): '73% LLO\nCDG',
    (0, 1): '14/15 LLO\nP/LP',
    (0, 2): 'HS 100%\nvs 0%',
    (1, 2): 'p<0.0001\n(HS); p=1.0\n(purine)',
    (2, 3): 'OR=4.24\nvs upstream',
    (3, 4): 'OR=∞\np=0.003',
    (4, 5): 'β: −0.20→\n−0.13 after\ngene-length',
    (4, 6): 'p=0.49\n(null)',
    (4, 7): 'No gradient\n(null)',
}

COLORS = {
    'S': '#27ae60',   # green — supported
    'P': '#f39c12',   # amber — partial
    'N': '#c0392b',   # red   — not confirmed
    'X': '#ecf0f1',   # light grey — not tested
}
LABELS = {
    'S': 'Supported',
    'P': 'Partial / caveated',
    'N': 'Not confirmed',
    'X': 'Not tested',
}

nrows = len(predictions)
ncols = len(streams)

fig, ax = plt.subplots(figsize=(11, 4.8))
ax.set_xlim(0, ncols)
ax.set_ylim(0, nrows)
ax.axis('off')

for r, row_cells in enumerate(matrix):
    for c, val in enumerate(row_cells):
        y_cell = nrows - 1 - r
        rect = mpatches.FancyBboxPatch(
            (c + 0.04, y_cell + 0.04), 0.92, 0.92,
            boxstyle='round,pad=0.02',
            facecolor=COLORS[val], edgecolor='white', linewidth=1.5,
            transform=ax.transData, clip_on=False
        )
        ax.add_patch(rect)
        note = notes.get((r, c), '')
        if note:
            ax.text(c + 0.5, y_cell + 0.5, note,
                    ha='center', va='center', fontsize=6.5,
                    color='white' if val in ('S', 'N') else '#2c3e50',
                    multialignment='center', linespacing=1.3)

# Column headers
for c, s in enumerate(streams):
    ax.text(c + 0.5, nrows + 0.05, s,
            ha='center', va='bottom', fontsize=8, fontweight='bold',
            multialignment='center', color='#2c3e50')

# Row headers
for r, p in enumerate(predictions):
    y_cell = nrows - 1 - r
    ax.text(-0.08, y_cell + 0.5, p,
            ha='right', va='center', fontsize=8.5,
            multialignment='right', color='#2c3e50')

# Legend
legend_patches = [mpatches.Patch(facecolor=v, edgecolor='#bdc3c7',
                                  label=LABELS[k])
                  for k, v in COLORS.items()]
ax.legend(handles=legend_patches, loc='lower right',
          bbox_to_anchor=(1.0, -0.12), ncol=4, fontsize=8,
          framealpha=0.9, edgecolor='#bdc3c7')

fig.suptitle('Evidence matrix: architecture model predictions vs evidence streams',
             fontsize=10, y=1.03, x=0.52)

plt.tight_layout()
for ext in ('png', 'svg'):
    plt.savefig(f'results/figures/figure6_evidence_matrix.{ext}',
                dpi=150, bbox_inches='tight')
print('Saved results/figures/figure6_evidence_matrix.{png,svg}')
