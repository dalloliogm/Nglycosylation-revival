# Interface Essentiality Interpretation

Date: 2026-06-16

## Question

Does the DepMap CRISPR essentiality difference between upstream-core and downstream-diversification N-glycosylation genes survive basic covariate control?

## Inputs

- Expression and essentiality table: `data/processed/nglyco_expression_essentiality.tsv`
- Covariate table: `data/processed/nglyco_loeuf_covariates.tsv`
- Primary contrast: upstream core versus downstream diversification, checkpoint genes held separate.

## Main Result

The DepMap signal remains strong after covariate control. In the raw primary contrast, upstream-core genes had much higher DepMap fitness cost than downstream-diversification genes. In the original DepMap sign convention, median mean gene effect was -0.496 upstream versus -0.014 downstream (Mann-Whitney p = 2.16e-07).

Using fitness cost as `-1 * depmap_mean_gene_effect`, the group-only model estimated a downstream coefficient of -0.632 (HC3 p = 3.72e-08). The full model including expression breadth, tissue-specificity tau, log gene length, and log paralog count estimated a downstream coefficient of -0.514 (HC3 p = 0.0015).

## Interpretation

The downstream coefficient remains negative and statistically strong in the full model, meaning downstream-diversification genes remain less fitness-costly than upstream-core genes after accounting for broad expression, tissue specificity, gene length, and paralog count. This supports using DepMap essentiality as a major evidence layer for the catastrophic-core component of the architecture model.

The strongest univariate covariate correlations with DepMap fitness cost were:

- `log_paralog_count`: Spearman rho = -0.550, p = 1.67e-05
- `expression_tau`: Spearman rho = -0.508, p = 8.91e-05
- `log_gene_length`: Spearman rho = -0.396, p = 0.0030

## Claim Limits

DepMap CRISPR gene-effect scores measure cancer-cell-line fitness effects. They should not be described as organismal lethality, developmental essentiality, or direct evolutionary fitness. The manuscript should phrase this result as cell-viability evidence that supports the catastrophic-core model.

## Manuscript Implication

The current manuscript wording can remain strong but specific: upstream-core N-glycosylation genes show much stronger pan-cell-line fitness costs than downstream-diversification genes, and this separation is not explained by the first-pass expression, tissue-specificity, gene-length, or paralog covariates tested here.
