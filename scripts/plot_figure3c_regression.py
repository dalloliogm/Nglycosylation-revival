#!/usr/bin/env python3
"""
Figure 3C — LOEUF regression coefficient forest plot.
Shows how the downstream group coefficient changes across five OLS models
(null, +gene_length, +paralog_count, +n_tissues, full).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('results/figures', exist_ok=True)

# ── Data from loeuf_regression_results.txt ───────────────────────────────────
# (coef, ci_low, ci_high, p, label)
models = [
    ('Group only',                -0.1994, -0.404,  0.005,  0.0558),
    ('+ log gene length',         -0.1252, -0.329,  0.079,  0.2225),
    ('+ log paralog count',       -0.2349, -0.519,  0.050,  0.1034),
    ('+ n tissues expressed',     -0.2352, -0.438, -0.033,  0.0239),
    ('Full model\n(all covariates)', -0.2289, -0.496,  0.038,  0.0907),
]

labels   = [m[0] for m in models]
coefs    = np.array([m[1] for m in models])
ci_low   = np.array([m[2] for m in models])
ci_high  = np.array([m[3] for m in models])
pvals    = np.array([m[4] for m in models])

# error bar half-widths
err_lo = coefs - ci_low
err_hi = ci_high - coefs

fig, ax = plt.subplots(figsize=(6.5, 3.8))

y = np.arange(len(models))[::-1]   # top-to-bottom

for i, (yi, coef, elo, ehi, p) in enumerate(zip(y, coefs, err_lo, err_hi, pvals)):
    color = '#c0392b' if p < 0.05 else '#2c3e50'
    ax.errorbar(coef, yi, xerr=[[elo], [ehi]],
                fmt='o', color=color, ecolor=color,
                markersize=7, linewidth=1.5, capsize=4, capthick=1.5)

# null reference line
ax.axvline(0, color='#7f8c8d', linewidth=1, linestyle='--', zorder=0)

# significance shading
ax.axvspan(-0.55, 0, alpha=0.04, color='#c0392b', zorder=0)

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel('Downstream coefficient (ΔLOEUF vs upstream)', fontsize=9)
ax.set_xlim(-0.60, 0.15)
ax.set_ylim(-0.6, len(models) - 0.4)

# p-value annotations
for i, (yi, p) in enumerate(zip(y, pvals)):
    sig = '**' if p < 0.01 else ('*' if p < 0.05 else f'p={p:.2f}')
    ax.text(0.12, yi, sig, va='center', ha='left', fontsize=8,
            color='#c0392b' if p < 0.05 else '#7f8c8d')

# legend
sig_patch   = mpatches.Patch(color='#c0392b', label='p < 0.05')
nonsig_patch = mpatches.Patch(color='#2c3e50', label='p ≥ 0.05')
ax.legend(handles=[sig_patch, nonsig_patch], fontsize=8,
          loc='lower left', framealpha=0.8)

ax.set_title('LOEUF downstream coefficient across covariate models',
             fontsize=10, pad=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
for ext in ('png', 'svg'):
    plt.savefig(f'results/figures/figure3c_loeuf_regression.{ext}',
                dpi=150, bbox_inches='tight')
print('Saved results/figures/figure3c_loeuf_regression.{png,svg}')
