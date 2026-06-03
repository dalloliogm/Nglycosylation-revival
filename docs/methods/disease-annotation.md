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

## Next Implementation Step

Create a first curated CDG/Mendelian seed table from GeneReviews and the current pathway gene list. Keep it deliberately conservative: record only high-confidence CDG or overlapping multiple-pathway genes with source notes. Add ClinVar and GWAS layers only after the curated Mendelian seed table is stable.
