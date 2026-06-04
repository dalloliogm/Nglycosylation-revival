# Disease Annotation Plan

Date drafted: 2026-06-03

Agentic work unit: `scope_disease_annotation`

Agent role: `data_provenance_agent`

## Purpose

This note defines the disease-architecture evidence stream before annotation tables are built. The goal is to test whether severe Mendelian disease burden is concentrated in catastrophic-core or checkpoint regions, while downstream/interface regions show more complex, context-dependent, immune, inflammatory, cancer, infection, or tissue-related associations.

This is a testable hypothesis, not a conclusion. Disease annotations must not be used to retroactively define the architecture features.

Primary future outputs:

- `data/processed/nglyco_disease_annotations.tsv`
- `results/tables/disease_architecture_summary.tsv`
- `results/figures/disease_architecture.*`

Primary inputs:

- `data/processed/nglyco_architecture_features.tsv`
- `data/processed/nglyco_constraint_metrics.tsv`
- `docs/concept/claims-register.md`
- `docs/methods/pathway-curation.md`

## Evidence Sources

Use three evidence tiers.

### Tier 1: Curated CDG And Mendelian Disease

Primary source:

- GeneReviews, "Congenital Disorders of N-Linked Glycosylation and Multiple Pathway Overview"
- URL: `https://www.ncbi.nlm.nih.gov/books/NBK1332/`
- Access date: 2026-06-03

Use this source for high-confidence CDG membership, mode of inheritance, CDG subtype, and clinical severity notes. GeneReviews states that CDG-N-linked includes disorders of the N-linked glycan synthetic pathway and overlapping multiple-pathway disorders. It includes a table of CDG types, genes, proteins, and modes of inheritance.

Secondary curated sources can be added later:

- individual GeneReviews entries such as PMM2-CDG;
- recent clinical reviews of CDG involving N-linked glycosylation;
- ClinGen disease validity where available;
- OMIM entries if access and terms permit local use.

### Tier 2: ClinVar Pathogenic Or Likely Pathogenic Evidence

Primary source:

- ClinVar variant summary TSV
- URL: `https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz`
- Access date verified: 2026-06-03

Use ClinVar as variant-level clinical evidence, not as a direct gene-disease causality source. Filter to germline variants with `ClinicalSignificance` containing `Pathogenic` or `Likely pathogenic`; exclude variants that are only VUS, conflicting, benign, or somatic-only unless a separate cancer analysis is explicitly planned.

Count ClinVar evidence separately from curated CDG/Mendelian membership because ClinVar variant volume can reflect study intensity, assay availability, submission practices, and gene length.

### Tier 3: GWAS Catalog Complex-Trait Associations

Primary source:

- NHGRI-EBI GWAS Catalog file downloads
- URL: `https://www.ebi.ac.uk/gwas/docs/file-downloads`
- Access date: 2026-06-03

Use GWAS Catalog as broad complex-trait evidence. The catalog provides downloadable association files with reported and mapped genes, traits, mapped EFO traits, study accessions, and genotyping technology. It is curated from GWAS publications and released on a regular cycle.

GWAS evidence must be treated cautiously:

- mapped genes are not necessarily causal genes;
- reported genes can reflect author annotation rather than fine mapping;
- nearby-gene assignment is weak without eQTL, colocalization, coding, or functional evidence;
- trait categories should be broad and conservative.

## Output Schema

Minimum first version of `data/processed/nglyco_disease_annotations.tsv`:

```text
symbol
ensembl_gene_id
primary_region
analysis_group
include_primary
include_sensitivity
cdg_curated_status
cdg_subtype
mendelian_disease_status
mode_of_inheritance
severe_mendelian_burden
clinvar_plp_variant_count
clinvar_plp_condition_count
clinvar_evidence_status
gwas_association_count
gwas_trait_category_count
immune_inflammation_trait_flag
infection_trait_flag
cancer_trait_flag
tissue_identity_trait_flag
complex_trait_evidence_status
disease_architecture_class
evidence_confidence
disease_annotation_version
disease_annotation_notes
```

## Classification Rules

### `cdg_curated_status`

Allowed values:

- `known_cdg_gene`
- `overlapping_or_multiple_pathway_cdg_gene`
- `not_cdg_gene`
- `uncertain`

Use GeneReviews CDG overview as the first-pass source. Do not infer CDG status from ClinVar counts alone.

### `severe_mendelian_burden`

Allowed values:

- `high`: known CDG or well-established severe Mendelian disorder with multisystem, developmental, neurologic, congenital, immune, or metabolic phenotype.
- `moderate`: curated Mendelian disease evidence but phenotype is narrower, later-onset, treatable, or not clearly catastrophic.
- `low`: weak or no curated Mendelian disease evidence.
- `unknown`: insufficient curation.

This is a curated label and must include notes.

### `clinvar_evidence_status`

Allowed values:

- `plp_variants_present`
- `no_plp_variants_found`
- `not_assessed`
- `ambiguous`

Record variant and condition counts, but do not treat counts alone as severity.

### `complex_trait_evidence_status`

Allowed values:

- `gwas_trait_evidence_present`
- `no_gwas_trait_evidence_found`
- `not_assessed`
- `ambiguous`

Use broad categories such as immune/inflammation, infection, cancer, glycan/glycome, metabolism, neurological, developmental, and tissue identity. Keep exact traits in a longer table if needed.

### `disease_architecture_class`

Allowed values:

- `severe_mendelian_core`
- `checkpoint_or_quality_control_disease`
- `complex_or_context_dependent_trait`
- `mixed_mendelian_and_complex`
- `no_current_disease_signal`
- `uncertain`

This class should be assigned after collecting Tier 1-3 evidence. It is an analysis output, not an input feature.

## Planned Analyses

Start with descriptive summaries:

1. Count known CDG genes by `analysis_group` and `primary_region`.
2. Count high severe-Mendelian-burden genes by `analysis_group`.
3. Count ClinVar P/LP variant-bearing genes by region.
4. Count genes with immune/inflammation, infection, cancer, tissue-identity, or glycan/glycome GWAS traits by region.
5. Compare the pattern to LOEUF/missense constraint, especially checkpoint-layer genes and downstream genes with strong constraint.

Then run sensitivity analyses:

1. Primary genes only versus primary plus sensitivity genes.
2. Excluding substrate-support genes.
3. Excluding low-specificity terminal-modification genes.
4. Treating checkpoint layer separately versus merged with upstream core.
5. High-confidence CDG/Mendelian evidence only versus CDG plus ClinVar P/LP evidence.
6. GWAS mapped genes only versus reported genes plus mapped genes.

## Claim Limits

Allowed language if supported:

- "Known CDG or severe Mendelian disease burden is enriched in specific pathway regions."
- "Disease evidence is consistent with a catastrophic-core or checkpoint-layer interpretation."
- "Downstream genes show more complex/context-dependent trait links."

Forbidden or downgraded language:

- "ClinVar variant counts prove disease burden."
- "GWAS mapped genes are causal."
- "Disease architecture proves the pathway evolved robustness."
- "A gene without current annotations has no disease relevance."

## Reproducibility Record To Fill During Implementation

When disease files are downloaded or curated, record:

```text
dataset_name
dataset_version_or_release_date
source_url
download_or_access_date
file_name_or_api_endpoint
genome_build
filters_applied
join_key
number_of_genes_input
number_of_genes_with_cdg_evidence
number_of_genes_with_clinvar_plp_evidence
number_of_genes_with_gwas_trait_evidence
missingness_notes
manual_curation_rule
```

## Current Implementation Record

Date implemented: 2026-06-03

Agentic work unit: `curate_cdg_seed_table`

Script:

- `scripts/build_nglyco_disease_seed_table.py`

Outputs:

- `data/processed/nglyco_disease_annotations.tsv`
- `results/tables/disease_architecture_summary.tsv`

Dataset record:

```text
dataset_name: GeneReviews CDG N-linked and multiple-pathway overview
dataset_version_or_release_date: last updated 2017-01-12 on source page
source_url: https://www.ncbi.nlm.nih.gov/books/NBK1332/
download_or_access_date: 2026-06-03
file_name_or_api_endpoint: NCBI Bookshelf HTML page, Table 1 and surrounding clinical overview text
genome_build: not applicable for curated disease table
filters_applied: retained only GeneReviews CDG genes present in data/processed/nglyco_architecture_features.tsv
join_key: HGNC gene symbol
number_of_genes_input: 101
number_of_genes_with_cdg_evidence: 33
number_of_genes_with_clinvar_plp_evidence: not assessed in this version
number_of_genes_with_gwas_trait_evidence: not assessed in this version
missingness_notes: genes not listed in this GeneReviews seed curation are labeled not_cdg_gene only for this first-pass source; this does not mean absence of disease relevance
manual_curation_rule: encode only CDG-N-linked and multiple-pathway rows from GeneReviews Table 1 that match the current pathway gene symbols
```

This implementation is intentionally conservative. It captures curated CDG-N-linked and multiple-pathway disorders from GeneReviews, but it does not yet add ClinVar pathogenic/likely pathogenic counts, OMIM-style disease breadth, or GWAS trait categories. The summary table should therefore be interpreted as a high-confidence Mendelian/CDG seed layer, not as the final disease architecture analysis.

## ClinVar P/LP Layer Implementation Record

Date implemented: 2026-06-03

Agentic work unit: `add_clinvar_plp_layer`

Script:

- `scripts/add_nglyco_clinvar_layer.py`

Local input:

- `data/external/clinvar/variant_summary.txt.gz`

Tracked outputs:

- `results/tables/clinvar_plp_gene_counts.tsv`
- `data/processed/nglyco_disease_annotations.tsv`
- `results/tables/disease_architecture_summary.tsv`

Dataset record:

```text
dataset_name: ClinVar variant summary
dataset_version_or_release_date: current NCBI FTP file downloaded 2026-06-03
source_url: https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz
download_or_access_date: 2026-06-03
file_name_or_api_endpoint: variant_summary.txt.gz
genome_build: GRCh38 rows only
filters_applied: Assembly == GRCh38; OriginSimple == germline; ClinicalSignificance contains pathogenic and excludes benign, uncertain, conflicting, not provided, association, risk factor, protective, affects, and drug response labels
join_key: ClinVar GeneSymbol matched to pathway HGNC gene symbol
number_of_genes_input: 101
number_of_genes_with_cdg_evidence: 33
number_of_genes_with_clinvar_plp_evidence: 55
number_of_genes_with_gwas_trait_evidence: not assessed in this version
missingness_notes: ClinVar variant counts reflect submission density, gene length, disease ascertainment, and curation history; counts are evidence features, not direct severity scores
manual_curation_rule: count unique GRCh38 germline P/LP VariationID values per pathway gene and unique non-empty phenotype labels
```

The ClinVar layer broadens the disease evidence beyond the curated CDG seed set. It should be used to identify genes with pathogenic-variant evidence that were not part of the conservative GeneReviews seed table, especially substrate-support genes and ER quality-control genes. It should not be used alone to declare a gene a CDG gene.

## GWAS Catalog Trait Layer Implementation Record

Date implemented: 2026-06-03

Agentic work unit: `add_gwas_trait_layer`

Script:

- `scripts/add_nglyco_gwas_trait_layer.py`

Local input:

- `data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip`

Tracked outputs:

- `results/tables/gwas_catalog_gene_trait_counts.tsv`
- `results/tables/gwas_catalog_nglyco_matched_associations.tsv`
- `data/processed/nglyco_disease_annotations.tsv`
- `results/tables/disease_architecture_summary.tsv`

Dataset record:

```text
dataset_name: NHGRI-EBI GWAS Catalog associations
dataset_version_or_release_date: v1.0.2 associations e115 r2026-06-01 split archive
source_url: https://www.ebi.ac.uk/gwas/api/search/downloads/associations/v1.0.2
download_or_access_date: 2026-06-03
file_name_or_api_endpoint: gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip
genome_build: mixed study-specific GWAS Catalog associations; no coordinate filtering in this gene-symbol layer
filters_applied: retained associations where REPORTED GENE(S) or MAPPED_GENE contains one of the 101 pathway HGNC symbols
join_key: GWAS Catalog reported or mapped gene symbol matched to pathway HGNC gene symbol
number_of_genes_input: 101
number_of_genes_with_cdg_evidence: 33
number_of_genes_with_clinvar_plp_evidence: 55
number_of_genes_with_gwas_trait_evidence: 99
missingness_notes: GWAS mapped/reported genes are association annotations, not causal gene assignments; association counts are dense and should be interpreted by trait category and curated examples rather than as direct burden scores
manual_curation_rule: classify disease/trait, mapped trait, and study text into broad glycome, immune/inflammation, infection, cancer, tissue-identity, and metabolism categories using explicit keyword rules
```

The GWAS layer is intentionally broad and hypothesis-generating. It is useful for identifying trait-category profiles, especially glycome and interface-related traits, but it should not be treated as evidence that a mapped gene is causal without fine mapping, colocalization, coding, eQTL, or functional support. The matched-association table is retained so candidate genes can be audited before being used in manuscript examples.

## Disease Architecture Figure Implementation Record

Date implemented: 2026-06-04

Agentic work unit: `plot_disease_architecture`

Script:

- `scripts/plot_disease_architecture.py`

Inputs:

- `results/tables/disease_architecture_summary.tsv`

Outputs:

- `results/figures/disease_architecture.png`
- `results/figures/disease_architecture.svg`
- `results/reports/disease-architecture-interpretation.md`

The figure has two layers. The upper panel plots curated CDG and ClinVar P/LP gene fractions by pathway region, emphasizing severe Mendelian/pathogenic-variant burden. The lower panel plots GWAS Catalog trait-category fractions, emphasizing broad complex-trait, glycome, and interface-related evidence. The figure intentionally avoids raw GWAS association counts because GWAS Catalog density and mapped-gene practices make raw counts poor burden scores.

## Next Implementation Step

Audit the strongest downstream glycome/interface GWAS examples against the matched-association table before using individual genes in manuscript text.
