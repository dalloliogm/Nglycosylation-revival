#!/usr/bin/env python3
"""
Figure 1 — Conceptual architecture model of N-glycosylation robustness and evolvability.
Vertical pathway schematic: upstream core (grey/blue) → downstream diversification (teal/green).
Two annotation columns: disease burden (left) and trait/evolvability signal (right).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
import os

os.makedirs('results/figures', exist_ok=True)

fig, ax = plt.subplots(figsize=(7.5, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# ── Colour palette ────────────────────────────────────────────────────────────
C_UPSTREAM  = '#2c3e50'   # dark slate  — upstream core
C_CHECKPOINT= '#34495e'   # mid slate   — ER QC
C_GOLGI     = '#1a6a8a'   # teal-blue   — Golgi core
C_BRANCH    = '#27ae60'   # green       — branching
C_TERMINAL  = '#2ecc71'   # light green — terminal modification
C_ANNOT_L   = '#c0392b'   # red         — disease
C_ANNOT_R   = '#8e44ad'   # purple      — evolvability

def block(ax, x, y, w, h, color, label, sublabel='', alpha=0.9):
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle='round,pad=0.06',
        facecolor=color, edgecolor='white', linewidth=1.5, alpha=alpha
    )
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + (0.13 if sublabel else 0),
            label, ha='center', va='center',
            color='white', fontsize=9, fontweight='bold')
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.18, sublabel,
                ha='center', va='center', color='white', fontsize=7.5,
                alpha=0.85)

def arrow_down(ax, x, y, color='#95a5a6'):
    ax.annotate('', xy=(x, y - 0.22), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=1.6, mutation_scale=12))

# ── Central pathway blocks (x=3.0..7.0, width=4) ────────────────────────────
bx, bw = 3.0, 4.0

# Block y positions (bottom to top displayed top to bottom)
blocks = [
    (10.1, 1.0, C_UPSTREAM,   'LLO Assembly',        '(ER membrane, 15 genes)'),
    (8.85, 0.9, C_UPSTREAM,   'OST Transfer',         '(OST complex, 11 genes)'),
    (7.65, 0.9, C_CHECKPOINT, 'ER Quality Control',   '(CNX/CRT cycle, 13 genes)'),
    (6.35, 1.0, C_GOLGI,      'Golgi Core Processing','(Man trimming, 7 genes)'),
    (5.05, 1.0, C_BRANCH,     'Golgi Branching',      '(MGAT family, 5 genes)'),
    (3.60, 1.1, C_TERMINAL,   'Terminal Modification', '(B4GALT, ST, FUT, 16 genes)'),
    (2.30, 0.9, C_TERMINAL,   'Glycoprotein Surface',  '(cell surface / secreted)'),
]

for (y, h, c, lbl, sub) in blocks:
    block(ax, bx, y, bw, h, c, lbl, sub)

# Connecting arrows between blocks
arrow_xs = [bx + bw/2] * 6
arrow_ys = [b[0] for b in blocks[1:]]
for ax_y, (y, h, *_) in zip(arrow_ys, blocks[:-1]):
    arrow_down(ax, bx + bw/2, y)

# ── LEFT annotations — disease / robustness ───────────────────────────────────
def left_annot(ax, y, text, strong=True):
    lx = 2.8
    ax.annotate(text, xy=(bx, y), xytext=(lx, y),
                ha='right', va='center', fontsize=7.8,
                color=C_ANNOT_L if strong else '#7f8c8d',
                arrowprops=dict(arrowstyle='->', color=C_ANNOT_L if strong else '#bdc3c7',
                                lw=1.0, connectionstyle='arc3,rad=0.0'))

left_annot(ax, 10.6, '73% CDG genes\n(DOLK, DPAGT1,\nALG1–ALG14…)', strong=True)
left_annot(ax, 9.3,  '45% CDG genes\n(STT3A, STT3B,\nRPN1, DDOST…)', strong=True)
left_annot(ax, 8.1,  'ClinVar P/LP:\n14/15 genes', strong=True)
left_annot(ax, 6.85, 'ClinVar P/LP:\n2/7 genes', strong=False)
left_annot(ax, 5.55, '0% CDG\n0 ClinVar P/LP', strong=False)
left_annot(ax, 4.15, '1/16 CDG (B4GALT1)\n3/16 ClinVar P/LP', strong=False)

# ── RIGHT annotations — trait / evolvability ─────────────────────────────────
def right_annot(ax, y, text, strong=True):
    rx = 7.2
    ax.annotate(text, xy=(bx + bw, y), xytext=(rx, y),
                ha='left', va='center', fontsize=7.8,
                color=C_ANNOT_R if strong else '#7f8c8d',
                arrowprops=dict(arrowstyle='->', color=C_ANNOT_R if strong else '#bdc3c7',
                                lw=1.0, connectionstyle='arc3,rad=0.0'))

right_annot(ax, 10.6, 'No glycome\nGWAS loci', strong=False)
right_annot(ax, 9.3,  'No glycome\nGWAS loci', strong=False)
right_annot(ax, 8.1,  'Paralogs: 1 median\n(low diversification)', strong=False)
right_annot(ax, 6.85, 'Paralogs: 3 median', strong=False)
right_annot(ax, 5.55, '4/5 genes glycome\nGWAS evidence\n(MGAT family)', strong=True)
right_annot(ax, 4.15, '7 IgG glycan loci\n(FUT8, ST6GAL1,\nB4GALT1, MGAT3…)\nOR=∞, p=0.003', strong=True)

# ── Bracket labels ───────────────────────────────────────────────────────────
def bracket(ax, y1, y2, x, label, color):
    mid = (y1 + y2) / 2
    ax.plot([x, x+0.12, x+0.12, x], [y1, y1, y2, y2],
            color=color, lw=1.8, solid_capstyle='round')
    ax.text(x + 0.22, mid, label, va='center', ha='left',
            fontsize=9, fontweight='bold', color=color)

bracket(ax, 7.65, 11.1, 0.3, 'ROBUST\nCORE', C_UPSTREAM)
bracket(ax, 3.60,  7.35, 0.3, 'EVOLVABLE\nOUTPUT', C_BRANCH)

# ── Title & model label ───────────────────────────────────────────────────────
ax.text(5, 11.75, 'N-glycosylation architecture model',
        ha='center', va='bottom', fontsize=12, fontweight='bold', color='#2c3e50')
ax.text(5, 11.45, '(tested model, not a result)',
        ha='center', va='bottom', fontsize=8, color='#7f8c8d', style='italic')

# Column headers
ax.text(1.4, 11.75, '← Disease / robustness', ha='center', fontsize=8.5,
        color=C_ANNOT_L, fontweight='bold')
ax.text(8.6, 11.75, 'Trait / evolvability →', ha='center', fontsize=8.5,
        color=C_ANNOT_R, fontweight='bold')

plt.tight_layout()
for ext in ('png', 'svg'):
    plt.savefig(f'results/figures/figure1_architecture_model.{ext}',
                dpi=150, bbox_inches='tight')
print('Saved results/figures/figure1_architecture_model.{png,svg}')
