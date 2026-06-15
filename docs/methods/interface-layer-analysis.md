# Interface Layer, Expression, and Essentiality Analysis

Date drafted: 2026-06-15

## Purpose

This work package tests whether the downstream N-glycosylation layer is better described as a context-deployed interface layer rather than simply a weakly constrained or disease-free pathway tail.

The analysis separates two related questions:

1. **Expression deployment**: are downstream branching and terminal-modification genes expressed in different tissue contexts, especially barrier and immune-relevant tissues?
2. **Essentiality**: are upstream/core and checkpoint genes more broadly required for cell viability, while downstream/interface genes show weaker or more context-specific essentiality?

These are supporting tests for the architecture model. They should not be interpreted as proof of adaptation.

## Candidate Data Sources

### Expression

Primary first-pass source:

- Human Protein Atlas GTEx RNA tissue table.
- Local expected path: `data/raw/hpa_rna_tissue_gtex.tsv`.
- Expression unit: `nTPM`.
- First-pass expressed threshold: `nTPM >= 1`.

This file is already cached locally because it was used in the LOEUF covariate analysis.

### Essentiality

Primary planned source:

- DepMap CRISPR gene-effect matrix, preferably the current public release.
- Local expected path: `data/external/depmap/CRISPRGeneEffect.csv`.

The first implementation accepts a DepMap-style matrix but does not require it. If the file is absent, the script writes expression metrics and marks essentiality fields as missing. This avoids blocking the expression analysis on a large external dataset.

## Expression Metrics

For each gene, compute:

| Column | Definition |
| --- | --- |
| `expression_n_tissues_ntpm_ge_1` | Number of GTEx tissues with `nTPM >= 1`. |
| `expression_mean_ntpm` | Mean `nTPM` across GTEx tissues. |
| `expression_median_ntpm` | Median `nTPM` across GTEx tissues. |
| `expression_max_ntpm` | Maximum `nTPM` across GTEx tissues. |
| `expression_tau` | Tissue-specificity index; higher values indicate narrower expression. |
| `barrier_tissue_mean_ntpm` | Mean `nTPM` across predefined epithelial/barrier tissues. |
| `immune_tissue_mean_ntpm` | Mean `nTPM` across blood/spleen/lymphoid proxy tissues available in HPA GTEx. |
| `barrier_to_all_expression_ratio` | Barrier mean divided by all-tissue mean. |
| `immune_to_all_expression_ratio` | Immune mean divided by all-tissue mean. |

First-pass barrier tissue set:

- `skin`
- `colon`
- `small intestine`
- `stomach`
- `esophagus`
- `lung`
- `breast`
- `cervix`
- `vagina`
- `urinary bladder`

First-pass immune tissue proxy set:

- `blood`
- `spleen`

This is intentionally conservative because the HPA GTEx tissue table is not an immune-cell atlas.

## Essentiality Metrics

If a DepMap CRISPR gene-effect matrix is available, compute:

| Column | Definition |
| --- | --- |
| `depmap_n_cell_lines` | Number of cell lines with non-missing gene-effect values. |
| `depmap_mean_gene_effect` | Mean gene-effect score across cell lines. More negative means stronger fitness cost. |
| `depmap_median_gene_effect` | Median gene-effect score across cell lines. |
| `depmap_fraction_strongly_essential` | Fraction of cell lines with gene effect <= -0.5. |
| `depmap_fraction_common_essential` | Fraction of cell lines with gene effect <= -1.0. |

Thresholds are pragmatic first-pass summaries, not official essential-gene calls. Manuscript language should focus on relative architecture patterns unless DepMap release-specific essentiality calls are added later.

## Outputs

Primary output:

- `data/processed/nglyco_expression_essentiality.tsv`

Summary output:

- `results/tables/interface_expression_summary.tsv`
- `results/tables/interface_essentiality_summary.tsv` if DepMap input is available.

Optional figure output:

- `results/figures/interface_expression_profile.{png,svg}`

## Claim Limits

- Broad expression is not equivalent to essentiality.
- Tissue-specific expression is not equivalent to evolvability.
- GTEx bulk tissue expression can miss cell-type-specific immune and epithelial deployment.
- DepMap cancer-cell essentiality is not the same as organism-level developmental essentiality.
- These metrics are controls and supporting evidence, not the central disease-architecture result.

## Next Steps

1. Run the first expression-only pass from the cached HPA GTEx table.
2. Add a DepMap CRISPR gene-effect file under `data/external/depmap/` and re-run the same script.
3. Decide whether the expression/essentiality results strengthen the first manuscript or belong in a supplementary sensitivity section.
