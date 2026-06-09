# Population-Genetics Gradient — Interpretation Note

Generated: 2026-06-09

## Claim limits

- FST outliers reflect population differentiation, which can arise from
  drift, bottleneck, founder effect, migration, or local selection.
  Do not describe elevated FST as evidence of selection without additional
  support from iHS, PBS replication, or functional annotations.
- iHS from PopHuman is pre-computed at 10 kb window resolution. Window-level
  signals cannot be attributed to a specific gene without LD inspection.
- PBS is more branch-specific than one-vs-rest FST but still requires
  demographic correction before pathway-level enrichment claims.
- Sample sizes (~25 upstream-core, ~27 downstream genes) limit power.
- All comparisons are exploratory and uncorrected for multiple testing.

## Group-level FST (AFR–EUR) summary

**upstream_core** (n=26): median=0.0808, max=0.1633
**checkpoint_layer** (n=13): median=0.0979, max=0.2854
**downstream_diversification** (n=28): median=0.0848, max=0.1698

## Pairwise comparisons

**upstream_core_vs_downstream** | metric: fst_mean_AFR_EUR
  upstream_core (n=22, med=0.08077) vs downstream_diversification (n=28, med=0.08482)
  Δ = -0.00405 [-0.02778, +0.02632]  r=0.013  p=0.9377

**upstream_plus_checkpoint_vs_downstream** | metric: fst_mean_AFR_EUR
  upstream_core+checkpoint (n=35, med=0.0878) vs downstream_diversification (n=28, med=0.08482)
  Δ = +0.00298 [-0.01957, +0.03115]  r=0.075  p=0.6088

**checkpoint_vs_downstream** | metric: fst_mean_AFR_EUR
  checkpoint_layer (n=13, med=0.09794) vs downstream_diversification (n=28, med=0.08482)
  Δ = +0.01312 [-0.02126, +0.05106]  r=0.225  p=0.2507

**upstream_core_vs_downstream** | metric: fst_mean_AFR_EAS
  upstream_core (n=22, med=0.09134) vs downstream_diversification (n=28, med=0.10215)
  Δ = -0.01081 [-0.04197, +0.02801]  r=0.062  p=0.7104

**upstream_plus_checkpoint_vs_downstream** | metric: fst_mean_AFR_EAS
  upstream_core+checkpoint (n=35, med=0.09285) vs downstream_diversification (n=28, med=0.10215)
  Δ = -0.00930 [-0.03083, +0.01720]  r=0.090  p=0.5428

**checkpoint_vs_downstream** | metric: fst_mean_AFR_EAS
  checkpoint_layer (n=13, med=0.09285) vs downstream_diversification (n=28, med=0.10215)
  Δ = -0.00930 [-0.02776, +0.01692]  r=0.137  p=0.4837

**upstream_core_vs_downstream** | metric: pbs_AFR_vs_EUR_EAS
  upstream_core (n=22, med=0.05724) vs downstream_diversification (n=28, med=0.04915)
  Δ = +0.00809 [-0.01334, +0.04306]  r=0.120  p=0.4696

**upstream_plus_checkpoint_vs_downstream** | metric: pbs_AFR_vs_EUR_EAS
  upstream_core+checkpoint (n=35, med=0.06677) vs downstream_diversification (n=28, med=0.04915)
  Δ = +0.01761 [-0.00732, +0.03526]  r=0.204  p=0.1666

**checkpoint_vs_downstream** | metric: pbs_AFR_vs_EUR_EAS
  checkpoint_layer (n=13, med=0.06782) vs downstream_diversification (n=28, med=0.04915)
  Δ = +0.01867 [-0.00515, +0.03937]  r=0.346  p=0.0776

**upstream_core_vs_downstream** | metric: pbs_EUR_vs_AFR_EAS
  upstream_core (n=22, med=0.02089) vs downstream_diversification (n=28, med=0.02669)
  Δ = -0.00580 [-0.01538, +0.00433]  r=0.243  p=0.1427

**upstream_plus_checkpoint_vs_downstream** | metric: pbs_EUR_vs_AFR_EAS
  upstream_core+checkpoint (n=35, med=0.02062) vs downstream_diversification (n=28, med=0.02669)
  Δ = -0.00607 [-0.01511, +0.00463]  r=0.198  p=0.1797

**checkpoint_vs_downstream** | metric: pbs_EUR_vs_AFR_EAS
  checkpoint_layer (n=13, med=0.02062) vs downstream_diversification (n=28, med=0.02669)
  Δ = -0.00607 [-0.02232, +0.02085]  r=0.121  p=0.5376

**upstream_core_vs_downstream** | metric: pbs_EAS_vs_AFR_EUR
  upstream_core (n=22, med=0.02742) vs downstream_diversification (n=28, med=0.03739)
  Δ = -0.00996 [-0.04213, +0.02019]  r=0.146  p=0.3791

**upstream_plus_checkpoint_vs_downstream** | metric: pbs_EAS_vs_AFR_EUR
  upstream_core+checkpoint (n=35, med=0.02502) vs downstream_diversification (n=28, med=0.03739)
  Δ = -0.01237 [-0.04306, +0.01063]  r=0.208  p=0.1583

**checkpoint_vs_downstream** | metric: pbs_EAS_vs_AFR_EUR
  checkpoint_layer (n=13, med=0.02293) vs downstream_diversification (n=28, med=0.03739)
  Δ = -0.01446 [-0.04700, +0.00677]  r=0.313  p=0.1103

**upstream_core_vs_downstream** | metric: ihs_max_AFR
  upstream_core (n=24, med=1.38045) vs downstream_diversification (n=27, med=1.2476)
  Δ = +0.13285 [-0.28025, +0.57990]  r=0.136  p=0.4063

**upstream_plus_checkpoint_vs_downstream** | metric: ihs_max_AFR
  upstream_core+checkpoint (n=36, med=1.3466) vs downstream_diversification (n=27, med=1.2476)
  Δ = +0.09900 [-0.33875, +0.44645]  r=0.093  p=0.5320

**checkpoint_vs_downstream** | metric: ihs_max_AFR
  checkpoint_layer (n=12, med=1.2491) vs downstream_diversification (n=27, med=1.2476)
  Δ = +0.00150 [-0.39655, +0.37900]  r=0.006  p=0.9757

**upstream_core_vs_downstream** | metric: ihs_max_EUR
  upstream_core (n=24, med=1.2218) vs downstream_diversification (n=27, med=1.2715)
  Δ = -0.04970 [-0.45710, +0.46740]  r=0.105  p=0.5211

**upstream_plus_checkpoint_vs_downstream** | metric: ihs_max_EUR
  upstream_core+checkpoint (n=36, med=1.2218) vs downstream_diversification (n=27, med=1.2715)
  Δ = -0.04970 [-0.40580, +0.27690]  r=0.111  p=0.4532

**checkpoint_vs_downstream** | metric: ihs_max_EUR
  checkpoint_layer (n=12, med=1.19905) vs downstream_diversification (n=27, med=1.2715)
  Δ = -0.07245 [-0.43860, +0.33090]  r=0.123  p=0.5428

**upstream_core_vs_downstream** | metric: ihs_max_EAS
  upstream_core (n=24, med=1.38675) vs downstream_diversification (n=27, med=1.443)
  Δ = -0.05625 [-0.42290, +0.41495]  r=0.034  p=0.8356

**upstream_plus_checkpoint_vs_downstream** | metric: ihs_max_EAS
  upstream_core+checkpoint (n=36, med=1.38675) vs downstream_diversification (n=27, med=1.443)
  Δ = -0.05625 [-0.38075, +0.35560]  r=0.031  p=0.8350

**checkpoint_vs_downstream** | metric: ihs_max_EAS
  checkpoint_layer (n=12, med=1.35445) vs downstream_diversification (n=27, med=1.443)
  Δ = -0.08855 [-0.52130, +0.44455]  r=0.025  p=0.9031

