# Constraint Analysis

Date drafted: 2026-06-02

Agentic work unit: `scope_constraint_dataset`

Agent role: `data_provenance_agent`

## Purpose

This note defines the constraint and standing-variation evidence stream before any quantitative analysis is run. The goal is to test whether N-glycosylation pathway architecture predicts intolerance to damaging variation, without treating constraint as proof of evolved robustness.

Primary future outputs:

- `results/tables/constraint_summary.tsv`
- `results/figures/constraint_gradient.*`

Primary inputs:

- `data/processed/nglyco_gene_table.tsv`
- `data/processed/nglyco_architecture_features.tsv` once created
- `docs/methods/architecture-metrics.md`
- `docs/concept/claims-register.md`

## Primary Dataset

Use gnomAD v4.1.1 gene constraint metrics as the primary source.

Source:

- gnomAD browser release note: https://gnomad.broadinstitute.org/news/2026-03-gnomad-v4-1-1/
- gnomAD constraint help page: https://gnomad.broadinstitute.org/help/constraint
- Access date: 2026-06-02

Rationale:

gnomAD v4.1.1 is the current gnomAD release as of 2026-06-02. The release note states that v4.1.1 includes updated gene constraint metrics, LOFTEE flag updates, sex-chromosome constraint metrics, gene/transcript quality flags, and updated LOEUF interpretation guidance. The v4 series is aligned to GRCh38, matching the coordinate system planned for this repository.

Use gnomAD v2.1.1 only as a legacy sensitivity comparison if needed, especially when interpreting results against older literature. Do not mix v2.1.1 and v4.1.1 metrics in the same primary model because their reference builds, sample sizes, and LOEUF distributions differ.

Implementation note, 2026-06-03:

The importer in `scripts/build_nglyco_constraint_summary.py` intentionally requires an explicit local constraint metrics file path. The gnomAD v4.1.1 release note states that updated gene constraint metrics are available for download, and the older public TSV path for `gnomad.v4.1.constraint_metrics.tsv` is reachable. However, guessed v4.1.1-specific TSV paths were not reachable during this implementation pass. Do not silently treat the v4.1 public TSV as v4.1.1. When the exact v4.1.1 metrics file or API export is identified, run the importer with `CONSTRAINT_DATASET_VERSION=gnomAD_v4.1.1` and record the exact URL, file name, access date, and checksum.

Provisional implementation, 2026-06-03:

The first constraint tables were generated from `data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv`, downloaded from `https://storage.googleapis.com/gcp-public-data--gnomad/release/4.1/constraint/gnomad.v4.1.constraint_metrics.tsv`, and labeled `gnomAD_v4.1`. The importer matched 95 of 101 N-glycosylation genes by Ensembl gene ID. Six genes lacked matched metrics in this file: `GNPNAT1`, `ALG13`, `RPN2`, `MAGT1`, `CANX`, and `MGAT4B`. The results should be treated as provisional until the exact v4.1.1 constraint export is identified or the v4.1 choice is formally accepted.

## Metrics To Extract

Extract gene-level metrics where available:

| Metric | Use | Direction |
| --- | --- | --- |
| `loeuf` | Primary loss-of-function intolerance metric. | Lower means stronger LoF constraint. |
| `oe_lof` | Observed/expected LoF ratio. | Lower means fewer LoF variants than expected. |
| `oe_lof_lower` and `oe_lof_upper` | Uncertainty around LoF observed/expected. | Use to avoid overinterpreting small differences. |
| `pLI` | Legacy categorical LoF-intolerance support. | Higher suggests LoF intolerance, but use cautiously. |
| `mis_z` | Missense constraint signal. | Higher suggests stronger missense constraint. |
| `oe_mis` | Observed/expected missense ratio. | Lower suggests missense depletion. |
| `oe_mis_lower` and `oe_mis_upper` | Uncertainty around missense observed/expected. | Use to report uncertainty. |
| `syn_z` and `oe_syn` | Technical/context control. | Not a biological outcome; useful for data-quality review. |
| low-coverage or low-mappability flags | Quality filter or sensitivity flag. | Flag genes where constraint may be unreliable. |

LOEUF should be analyzed as a continuous metric by default. If a binary constrained-gene label is needed for a secondary table, use the current gnomAD v4.1.1 guidance rather than older v2 thresholds. Record the exact threshold used in the table metadata.

## Join Rules

Primary join key:

- `ensembl_gene_id` from `data/processed/nglyco_gene_table.tsv`

Secondary cross-check:

- `symbol`

Before final analysis, cross-check provisional Ensembl IDs in the gene table against HGNC/Ensembl because the current gene table was initially populated from MyGene.info. Any unmatched, retired, duplicate, or symbol-only genes should be recorded in a join-audit table.

Required join-audit fields:

```text
symbol
ensembl_gene_id_repo
ensembl_gene_id_gnomad
constraint_metric_available
join_status
join_notes
```

Allowed `join_status` values:

- `matched_ensembl`
- `matched_symbol_only`
- `missing_constraint`
- `ambiguous_identifier`
- `retired_or_merged_gene`

Do not silently drop missing genes. Missingness may be informative if it reflects low coverage, poor mappability, noncoding genes, pseudogenes, or annotation mismatches.

## Analysis Groups

Use the grouping definitions from `docs/methods/pathway-curation.md` and `docs/methods/architecture-metrics.md`.

Primary groups:

- `upstream_core`
- `checkpoint_layer`
- `downstream_diversification`
- `substrate_support`

Default primary contrast:

- `upstream_core` versus `downstream_diversification`

Do not merge `checkpoint_layer` or `substrate_support` into the main contrast unless the sensitivity analysis explicitly states the rationale.

## Planned Tests

Start with descriptive summaries before inferential models:

1. Per-gene table of constraint metrics and architecture labels.
2. Median, interquartile range, and range of LOEUF by `analysis_group`.
3. Median and distribution of `mis_z` by `analysis_group`.
4. Count and proportion of genes passing any predeclared LoF-constraint threshold by `analysis_group`.
5. Visual distribution of LOEUF and missense constraint by pathway region.

Then run lightweight models only if sample size and missingness justify them:

- rank-based group comparison for `upstream_core` versus `downstream_diversification`;
- regression or matched-null model with LOEUF as a continuous outcome;
- sensitivity models with `checkpoint_layer` handled separately and merged into upstream core;
- sensitivity models excluding substrate-support and low-specificity terminal-modification genes.

Report effect sizes and uncertainty, not only p-values.

## Covariates And Confounders

Constraint is not purely a pathway-architecture signal. Record and, where possible, control for:

- coding sequence length;
- exon count or transcript length;
- expression breadth;
- median or maximum expression level;
- mappability and low-coverage flags;
- mutation rate proxies;
- GC content or sequence context if available;
- background selection or local genomic context if available;
- essentiality when used as a comparator rather than an outcome;
- disease ascertainment and literature attention, handled mainly in disease analyses.

Do not overfit models if the pathway gene count is small. Prefer matched null sets or transparent descriptive summaries when covariate-rich regression is underpowered.

## Matched Null Strategy

The first matched-null design should compare each N-glycosylation gene to genome-wide genes matched on basic technical covariates:

- protein-coding status;
- coding sequence length or transcript length;
- expression breadth if available;
- mappability/coverage flags;
- broad functional category sensitivity if needed.

The matched null should answer:

1. Are N-glycosylation genes as a set unusually constrained?
2. Within N-glycosylation, does architecture group explain variation beyond generic gene properties?

If no matched null is available in the first pass, describe group summaries as exploratory.

## Sensitivity Analyses

Required before any architecture-level claim:

1. Primary genes only versus primary plus sensitivity genes.
2. Exclude `substrate_support`.
3. Exclude low-specificity terminal-modification genes.
4. Analyze `checkpoint_layer` separately.
5. Merge `checkpoint_layer` with `upstream_core`.
6. Compare coarse `analysis_group` to finer `primary_region`.
7. Repeat using LOEUF deciles rather than raw LOEUF.
8. Repeat using missense metrics rather than LoF metrics.
9. Flag or exclude genes with low coverage or poor mappability.
10. Check whether results are driven by one or two extreme genes.

## Standing Variation Extension

Standing variation should be treated as a related but separate output. If added, define per-gene summaries such as:

- count of high-confidence pLoF variants;
- count of rare missense variants;
- count of predicted damaging missense variants if a variant-level score is available;
- observed variant burden normalized by expected counts or coding length.

Do not compare raw variant counts across genes without normalizing for gene length, coverage, and mutation opportunity.

## Claim Limits

Allowed language if the analysis supports the model:

- "Upstream/core genes show stronger constraint than downstream/diversification genes."
- "The pattern is consistent with a catastrophic-core interpretation."
- "Constraint gradients support, but do not prove, the robustness/evolvability architecture model."

Forbidden or downgraded language:

- "Constraint proves that the pathway evolved robustness."
- "Low LOEUF demonstrates adaptive design."
- "Downstream genes are adaptive because they are less constrained."
- "gnomAD constraint establishes disease causality."

Interpretation must follow `docs/concept/claims-register.md`: constraint can support a robustness pattern, but it cannot by itself demonstrate mechanism, adaptation, or design.

## Reproducibility Record To Fill During Implementation

When the data are downloaded or queried, record:

```text
dataset_name
dataset_version
source_url
download_or_access_date
file_name_or_api_endpoint
genome_build
transcript_set
software_versions
filters_applied
join_key
number_of_genes_input
number_of_genes_matched
number_of_genes_missing
missingness_notes
```

## Next Implementation Step

After `data/processed/nglyco_architecture_features.tsv` exists, write a script that:

1. reads the N-glycosylation gene table and architecture features;
2. imports gnomAD v4.1.1 gene constraint metrics;
3. joins by Ensembl gene ID with symbol cross-checks;
4. writes a per-gene constraint table;
5. writes a join-audit table;
6. produces `results/tables/constraint_summary.tsv` with group-level summaries.
