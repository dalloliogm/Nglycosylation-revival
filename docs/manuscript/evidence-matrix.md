# Evidence Matrix

Date drafted: 2026-06-06

Agentic work unit: `draft_evidence_matrix`

Purpose: connect manuscript claims to current evidence artifacts, allowed wording, and claim limits. This file should be used before drafting Results, Discussion, and figure legends.

## Claim Level Key

- **Supported**: backed by current project evidence, with limitations.
- **Consistent with**: compatible with current evidence, but not a direct test or not yet controlled enough.
- **Hypothesis-generating**: useful for framing or follow-up only.
- **Not supported**: current evidence argues against this wording.

## Core Architecture Claims

| Claim | Current level | Main evidence | Safe manuscript wording | Do not say |
| --- | --- | --- | --- | --- |
| N-glycosylation is a tractable case study for pathway-level robustness/evolvability architecture. | Supported | `docs/methods/pathway-curation.md`; `data/processed/nglyco_gene_table.tsv`; `data/processed/nglyco_architecture_features.tsv`; `results/figures/nglyco_pathway_network.*` | "N-glycosylation provides a structured case study for testing whether biological pathways partition catastrophic core functions and interface-facing variation." | "N-glycosylation proves a universal design principle." |
| A simple pathway-depth model is insufficient. | Supported | `results/reports/constraint-gradient-interpretation.md`; `results/tables/constraint_group_comparisons.tsv` | "Constraint results refine the model: pathway depth alone does not explain intolerance." | "The robustness/evolvability model is falsified by constraint." |
| Severe Mendelian/CDG disease burden is concentrated in early shared machinery. | Supported | `data/processed/nglyco_disease_annotations.tsv`; `results/tables/disease_architecture_summary.tsv`; `results/figures/disease_architecture.*` | "Curated CDG and ClinVar P/LP evidence concentrate in substrate-support, LLO assembly, and OST-related machinery." | "All upstream genes are severe disease genes." |
| Downstream regions show richer glycome and interface trait evidence than severe Mendelian disease evidence. | Supported, with GWAS caveat | `results/figures/disease_architecture.*`; `results/tables/gwas_catalog_gene_trait_counts.tsv`; `results/tables/downstream_gwas_candidate_audit.tsv`; `results/tables/downstream_gwas_locus_review_summary.tsv` | "Downstream branching and terminal-modification genes show broad glycome and immune/interface trait-category evidence, especially in GWAS Catalog annotations." | "GWAS mapped genes are causal"; "downstream variation proves adaptation." |
| The current evidence supports a layered disease/trait architecture more strongly than a pure coding-constraint gradient. | Supported | Disease, DepMap essentiality, expression, constraint, and GWAS layers above | "The strongest current support is a layered architecture: severe disease and cell-viability evidence are concentrated in core/shared machinery, while glycome and interface trait evidence is richer downstream." | "Downstream genes are generally unconstrained"; "upstream genes are the only constrained genes." |

## Constraint Evidence

| Finding | Interpretation | Supporting artifact | Claim limit |
| --- | --- | --- | --- |
| Primary upstream-core genes have higher median LOEUF than downstream genes in the provisional gnomAD run. | This goes against the naive expectation that upstream always means more LoF-constrained. | `results/tables/constraint_group_comparisons.tsv`; `results/reports/constraint-gradient-interpretation.md` | Do not use LOEUF alone as the architecture proof. |
| Downstream genes have higher median missense Z than upstream-core genes in the primary contrast. | Some downstream enzymes may be coding-constrained despite being part of the glycan-output/interface layer. | `results/tables/constraint_group_comparisons.tsv`; `results/figures/constraint_gradient.*` | Do not equate downstream diversification with coding tolerance. |
| Strong constraint examples span OST, ER quality control, and downstream glycan-output genes. | Catastrophic potential may localize to dependency/checkpoint/output nodes rather than just early pathway position. | `results/figures/nglyco_pathway_constraint_loeuf.*`; `results/figures/nglyco_pathway_constraint_mis_z.*` | Requires matched nulls, covariates, and expression/essentiality layers before strong generalization. |

## Expression And Essentiality Evidence

| Finding | Interpretation | Supporting artifact | Claim limit |
| --- | --- | --- | --- |
| Upstream-core genes have much stronger DepMap CRISPR fitness costs than downstream-diversification genes. | This is one of the strongest current supports for the catastrophic-core component of the model. | `data/processed/nglyco_expression_essentiality.tsv`; `results/tables/interface_essentiality_summary.tsv`; `results/tables/interface_essentiality_primary_contrasts.tsv` | DepMap cancer-cell fitness is not the same as organism-level developmental essentiality, and should be treated as cell-viability evidence. |
| Median DepMap mean gene effect is -0.496 upstream versus -0.014 downstream. | Upstream/core disruption is broadly costly across cell lines, while downstream terminal/branching genes are much less pan-essential. | `results/tables/interface_essentiality_primary_contrasts.tsv` | Do not claim every upstream gene is essential or every downstream gene is dispensable. |
| Downstream-diversification genes have higher HPA/GTEx tissue-specificity tau than upstream-core genes. | This supports more context-specific deployment downstream. | `results/tables/interface_expression_summary.tsv`; `results/tables/interface_expression_primary_contrasts.tsv`; `results/figures/interface_expression_profile.*` | Bulk tissue expression does not resolve cell-type-specific immune or epithelial expression. |
| Barrier and immune bulk-tissue proxy expression ratios are not clearly downstream-enriched. | This weakens any simple claim that downstream genes are globally higher in barrier or immune tissues. | `results/tables/interface_expression_primary_contrasts.tsv` | Do not use the first-pass HPA tissue proxy as strong evidence for immune or mucosal deployment. |

## Disease Evidence

| Finding | Interpretation | Supporting artifact | Claim limit |
| --- | --- | --- | --- |
| LLO assembly has high curated CDG fraction: 11 of 15 genes. | Early lipid-linked oligosaccharide assembly is a strong severe Mendelian/CDG layer. | `results/tables/disease_architecture_summary.tsv`; `data/processed/nglyco_disease_annotations.tsv` | GeneReviews seed curation is conservative and not exhaustive. |
| OST transfer has curated CDG evidence in 5 of 11 genes. | Transfer of the glycan precursor to protein is clinically sensitive. | `results/tables/disease_architecture_summary.tsv`; `results/figures/disease_architecture.*` | Some OST genes have sparse or complex annotation. |
| Substrate-support genes have high ClinVar P/LP burden. | Donor/substrate biology is clinically important but should be handled separately from the primary upstream/downstream contrast. | `results/tables/clinvar_plp_gene_counts.tsv`; `results/tables/disease_architecture_summary.tsv` | Substrate support is not the same pathway half as the LLO/OST core. |
| Downstream Golgi branching and terminal-modification regions have weaker curated CDG burden. | This supports the idea that severe Mendelian/CDG burden is not evenly distributed across the pathway. | `results/figures/disease_architecture.*` | Absence from the CDG seed table is not absence of disease relevance. |

## GWAS And Glycome Trait Evidence

| Finding | Interpretation | Supporting artifact | Claim limit |
| --- | --- | --- | --- |
| GWAS Catalog evidence is dense: nearly all genes have at least one reported/mapped association. | "Any GWAS hit" is not informative; category and locus-quality evidence matter. | `results/tables/gwas_catalog_gene_trait_counts.tsv`; `results/tables/gwas_catalog_nglyco_matched_associations.tsv` | Avoid raw GWAS association counts as burden scores. |
| Downstream genes show strong glycome/interface category coverage. | This is the best current support for the downstream interface/evolvability layer. | `results/figures/disease_architecture.*`; `results/tables/downstream_gwas_candidate_audit.tsv` | Trait-category enrichment remains descriptive, not causal. |
| Locus review identifies stronger downstream examples with reported-gene glycome support. | Some gene examples are plausible enough for cautious manuscript use. | `results/tables/downstream_gwas_locus_review.tsv`; `results/tables/downstream_gwas_locus_review_summary.tsv` | Still association evidence; causal language requires fine mapping or functional support. |

## Candidate Gene Examples

| Candidate | Manuscript use | Evidence summary | Wording |
| --- | --- | --- | --- |
| `ST6GAL1` | Strong example | 79 direct glycome locus rows; 39 reported-gene rows; no higher-risk locus rows in current review. | "A strong downstream example with repeated reported-gene glycome associations." |
| `MGAT3` | Strong but mention assignment risk | 91 direct glycome locus rows; 28 reported-gene rows; 40 higher-risk rows. | "A strong glycome-association example, with some loci requiring assignment caution." |
| `B4GALT1` | Strong, also connects severe disease and glycome traits | Known CDG gene; ClinVar P/LP present; 67 direct glycome locus rows; 11 reported-gene rows. | "Illustrates overlap between downstream enzymatic function, Mendelian annotation, and glycome traits." |
| `FUT8` | Useful but cautious | 203 direct glycome locus rows; 38 reported-gene rows; many moderate/higher-risk mapped/intergenic rows. | "A prominent fucosylation-associated locus/gene example, requiring careful locus assignment." |
| `MGAT5` | Useful supporting example | 16 direct glycome locus rows; 4 reported-gene rows. | "A branching enzyme with repeated glycome/transferrin glycosylation associations." |
| `ST3GAL4` | Cautious supporting example | 15 direct glycome locus rows; 1 reported-gene row. | "A terminal sialylation candidate with glycome associations, but weaker reported-gene support." |
| `FUT3` | Cautious supporting example | 44 direct glycome locus rows; 18 reported-gene rows; zero lower-risk rows under current intergenic/context rule. | "A fucosyltransferase-associated trait example requiring locus-context review." |

## Claims To Avoid

- Do not claim that downstream genes are generally weakly constrained.
- Do not claim that severe disease burden is absent downstream.
- Do not claim that GWAS Catalog mapped genes are causal.
- Do not claim adaptation, selection, or local evolutionary optimization from disease or GWAS layers.
- Do not use ClinVar P/LP variant counts as direct severity scores.
- Do not use individual gene examples as substitutes for pathway-region patterns.

## Manuscript-Ready Synthesis

The current results support a cautious architecture model. The simple prediction that upstream genes are always more constrained by LOEUF is not supported by the provisional gnomAD constraint analysis. Instead, the stronger pattern is layered: early shared machinery, especially LLO assembly and OST transfer, carries high severe Mendelian/CDG burden and strong DepMap cell-viability cost, while downstream branching and terminal-modification genes show richer glycome and interface trait evidence and more tissue-specific expression. This supports a model in which robustness and evolvability are not separated by coding constraint alone; the downstream layer may express evolvability through glycan-output traits, regulatory deployment, and context-dependent phenotypes.

## Remaining Gaps

- Build matched-null controls for gene length, constraint, and GWAS annotation density.
- Convert this matrix into Results and Discussion prose with strict claim levels.
