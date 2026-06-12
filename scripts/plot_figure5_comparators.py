#!/usr/bin/env python3
"""
Figure 5 — Comparator pathway disease-gradient panel.
Grouped bar chart: Mendelian disease % in core vs downstream for
N-glycosylation, HS biosynthesis, ceramide/GSL, purine de novo, GPI anchor.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('results/figures', exist_ok=True)

# ── Data from pathway_null_model_summary.txt ─────────────────────────────────
# (pathway_label, topology, core_pct, dn_pct, fisher_p, core_n, dn_n)
pathways = [
    ('N-glycosylation\n(reference)',    'layered',  73,   4,  '<0.001', 26, 27),
    ('Heparan sulfate\nbiosynthesis',   'layered', 100,   0,  '<0.0001', 8, 16),
    ('Ceramide / GSL\nbiosynthesis',    'layered',  57,  25,   '0.20',  14,  8),
    ('Purine\nde novo synthesis',       'linear',   33,  50,   '1.0',    6,  4),
    ('GPI-anchor\nbiosynthesis',        'linear',   95, None,   'n/a',  21,  0),
]

labels   = [p[0] for p in pathways]
topos    = [p[1] for p in pathways]
core_pct = [p[2] for p in pathways]
dn_pct   = [p[3] for p in pathways]   # None = no downstream genes
fisher_p = [p[4] for p in pathways]

# colours
CORE_COLOR    = '#2c3e50'
DN_COLOR      = '#3498db'
CORE_HATCHED  = '#2c3e50'

x = np.arange(len(pathways))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 4.5))

bars_core = ax.bar(x - width/2, core_pct, width,
                   color=CORE_COLOR, alpha=0.85, label='Upstream core')

dn_vals = [v if v is not None else 0 for v in dn_pct]
bars_dn  = ax.bar(x + width/2, dn_vals, width,
                  color=DN_COLOR, alpha=0.85, label='Downstream layer')

# hatch GPI downstream bar to indicate no genes
ax.bar(x[-1] + width/2, 0.5, width,
       color='none', edgecolor='#bdc3c7', hatch='///', linewidth=0.8,
       label='No downstream genes')

# Fisher p-value annotations above each pair
for i, p in enumerate(fisher_p):
    ymax = max(core_pct[i], dn_vals[i]) + 3
    color = '#c0392b' if p not in ('n/a', '1.0', '0.20') else '#7f8c8d'
    ax.text(x[i], ymax + 2, p, ha='center', va='bottom',
            fontsize=8, color=color,
            fontweight='bold' if color == '#c0392b' else 'normal')

# topology labels below x-axis
for i, topo in enumerate(topos):
    color = '#8e44ad' if topo == 'layered' else '#e67e22'
    ax.text(x[i], -14, topo.capitalize(),
            ha='center', va='top', fontsize=7.5, color=color,
            style='italic')

ax.set_ylabel('Genes with Mendelian disease evidence (%)', fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylim(-18, 115)
ax.set_xlim(-0.6, len(pathways) - 0.4)
ax.axhline(0, color='#bdc3c7', linewidth=0.8)

# topology legend
layered_patch = mpatches.Patch(color='#8e44ad', alpha=0.7,
                                label='Layered topology')
linear_patch  = mpatches.Patch(color='#e67e22', alpha=0.7,
                                label='Linear topology')

h1 = mpatches.Patch(color=CORE_COLOR, alpha=0.85, label='Upstream core')
h2 = mpatches.Patch(color=DN_COLOR, alpha=0.85, label='Downstream layer')

ax.legend(handles=[h1, h2, layered_patch, linear_patch],
          fontsize=8, loc='upper right', framealpha=0.9, ncol=2)

# annotation key
ax.text(0.01, 0.97, 'p values: Fisher exact (core vs downstream disease burden)',
        transform=ax.transAxes, fontsize=7, va='top', color='#7f8c8d')

ax.set_title('Disease-burden gradient is topology-dependent', fontsize=10, pad=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
for ext in ('png', 'svg'):
    plt.savefig(f'results/figures/figure5_comparator_pathways.{ext}',
                dpi=150, bbox_inches='tight')
print('Saved results/figures/figure5_comparator_pathways.{png,svg}')
