# Paper Outline

ARS workflow: `academic-paper` Phase 2, Structure Architect output.

## Structure Pattern

Hybrid theoretical analysis plus computational case study.

This is not a standard IMRaD paper yet because several empirical work packages are still planned. The recommended manuscript shape is a hypothesis-driven architecture paper: theory and predictions first, N-glycosylation as the worked case, then multi-evidence tests across pathway curation, constraint, disease, tissue/trait association, and optional population genetics.

## Overview

The paper should move from a general systems-biology problem to a specific testable architecture. It opens with robustness/evolvability theory, argues that pathway architecture can spatially separate catastrophic core functions from evolvable interface functions, introduces N-glycosylation as a concrete biological system with an upstream-to-downstream functional gradient, and tests whether modern evidence supports the predicted gradient in constraint, disease architecture, standing variation, tissue/trait association, and pathway topology.

## Detailed Outline

### 1. Introduction: Pathways as Evolutionary Architectures (~800 words)

**Purpose**: Establish the problem and the paper's contribution.

**Content**:

- Biological systems must preserve core viability while retaining capacity for environmental response and innovation.
- Robustness/evolvability theory often treats this as a general property, but pathway-level localization is less often tested directly.
- N-glycosylation is introduced as a tractable case because its upstream machinery is tied to protein folding and conserved biosynthesis, while downstream glycan diversification mediates cell-surface and environmental interactions.

**Sources**: Kitano; Felix and Wagner; Payne and Wagner; Edelman and Gally; Varki; Stanley et al.; Helenius and Aebi.

**Transition to next**: Move from general theory to explicit competing hypotheses and measurable predictions.

### 2. Conceptual Model and Predictions (~900 words)

**Purpose**: Turn the central idea into falsifiable claims.

**Content**:

- Define pathway regions: conserved core, OST/checkpoint layer, ER quality-control processing, substrate-support genes, Golgi diversification, terminal modification, environmental interface.
- State competing explanations: real architecture gradient, annotation artifact, disease-study ascertainment, local genomic covariates, or N-glycosylation-specific idiosyncrasy.
- Present primary predictions: stronger constraint and severe Mendelian burden upstream; greater tolerated variation and immune/environmental trait links downstream; catastrophic network positions depleted for tolerated functional variation; redundant/branching/tissue-specific nodes enriched for innovation-zone signals.

**Sources**: Concept memo; project plan; robustness/evolvability literature; network biology literature.

**Transition to next**: Explain how the pathway and evidence layers are curated to test these predictions.

### 3. Case Definition: Modern N-glycosylation Pathway Curation (~900 words)

**Purpose**: Define the object of study reproducibly.

**Content**:

- Describe gene-table construction, stable identifiers, pathway-region labels, and evidence sources.
- Separate substrate biosynthesis and low-specificity terminal-modification genes from primary pathway-core genes where needed.
- Define graph/edge abstraction rules and show the first pathway architecture visualization.
- State planned sensitivity analyses for ambiguous genes and alternative region labels.

**Sources**: `docs/methods/pathway-curation.md`; `docs/methods/pathway-edge-curation.md`; `data/processed/nglyco_gene_table.tsv`; Reactome; GlyGen; UniProt; GO; Essentials of Glycobiology.

**Transition to next**: Once the pathway is defined, test whether architecture predicts molecular intolerance and clinical severity.

### 4. Evidence Stream 1: Constraint, Essentiality, and Standing Variation (~1,100 words)

**Purpose**: Test whether upstream/core regions are less tolerant of damaging perturbation.

**Content**:

- Compare gene-level constraint and intolerance across pathway regions.
- Add standing variation and rare damaging burden if available.
- Use matched nulls or covariate adjustment for gene length, mutability, expression breadth, SNP density, recombination, background selection, and mappability where possible.
- Report effect sizes and uncertainty, not only p-values.

**Sources**: gnomAD/ExAC constraint literature; modern constraint datasets; analysis plan.

**Transition to next**: Molecular intolerance should have a clinical counterpart if the robustness-layer hypothesis is correct.

### 5. Evidence Stream 2: Disease Architecture (~1,100 words)

**Purpose**: Test whether severe Mendelian disease concentrates in the upstream/core and checkpoint layers while downstream/interface genes show more context-dependent trait links.

**Content**:

- Curate CDG, OMIM/GeneReviews, ClinVar pathogenic evidence, and high-confidence Mendelian annotations.
- Separately curate GWAS Catalog and complex trait evidence for immune, infection, inflammation, cancer, microbiome, and tissue identity categories.
- Avoid conflating severe causal disease genes with broad association evidence.
- Present disease architecture as a gradient rather than a binary claim.

**Sources**: GeneReviews/CDG sources; ClinVar; OMIM-style sources; GWAS Catalog; disease/constraint literature.

**Transition to next**: Disease and trait architecture connects the biochemical pathway to organism-environment interface biology.

### 6. Evidence Stream 3: Interface Biology, Tissue Deployment, and Traits (~900 words)

**Purpose**: Test whether downstream N-glycosylation genes are richer in immune, barrier, infection, inflammation, cancer, microbiome, and tissue-context associations.

**Content**:

- Integrate expression breadth, tissue specificity, immune-cell expression, epithelial/barrier tissue expression, and trait-category profiles.
- Use glycoimmunology and host-pathogen glycan literature to interpret results cautiously.
- Avoid claims that every downstream enzyme is adaptive; frame downstream regions as plausibly more exposed to interface-mediated selection and tolerated phenotypic variation.

**Sources**: Marth and Grewal; Rabinovich et al.; Poole et al.; Reily et al.; Smith and Cummings; IgG glycosylation GWAS papers.

**Transition to next**: Evaluate whether population-genetic evidence adds independent support or should remain historical context.

### 7. Optional Evidence Stream: Population Differentiation and Selection Signals (~600 words)

**Purpose**: Decide whether modern population-genetic evidence supports the architecture model without becoming the central story.

**Content**:

- Treat the 2012 paper as historical context.
- If included, use modern data, pairwise or branch-aware statistics, local genomic covariates, and candidate-locus inspection.
- Keep SNP-level, region-level, and gene-level claims distinct.
- Use cautious language: candidate signal, outlier, consistent with, hypothesis-generating.

**Sources**: Dall'Olio et al. 2012; Nielsen et al.; Voight et al.; Sabeti et al.; Coop et al.; Berg and Coop; 1000 Genomes high-coverage release.

**Transition to next**: Synthesize evidence streams and explain what the case study does and does not establish.

### 8. Synthesis: A Robustness/Evolvability Architecture for N-glycosylation (~900 words)

**Purpose**: Integrate the evidence without overclaiming mechanism.

**Content**:

- Summarize whether evidence supports, weakens, or complicates each prediction.
- Distinguish robust architecture-level findings from individual gene examples and candidate signals.
- Explain how this case relates to modular engineering, fault-tolerant architecture, and layered protocols without letting analogies replace biological evidence.
- Discuss whether comparator pathways are needed for generalization.

**Sources**: All evidence streams; claims register; reviewer-risk checklist.

**Transition to next**: End with limitations and the general research program.

### 9. Limitations and Future Directions (~500 words)

**Purpose**: Pre-empt the strongest reviewer objections.

**Content**:

- Small gene-set size and label sensitivity.
- Database incompleteness and annotation bias.
- Disease ascertainment bias.
- Population structure and local genomic confounding if population genetics is included.
- Generalization beyond N-glycosylation requires comparator pathways.

**Sources**: Project-plan failure modes; methods notes.

**Transition to next**: Conclude with the precise claim the paper can support.

### 10. Conclusion (~300 words)

**Purpose**: State the contribution tightly.

**Content**:

- N-glycosylation provides a concrete test case for the idea that pathway architectures may separate robustness and evolvability.
- The paper contributes a framework, curated pathway representation, and multi-evidence tests.
- The appropriate claim is support for a testable architecture model, not proof of adaptation at specific loci.

## Evidence Map

| Section | Assigned Sources or Inputs | Evidence Type |
|---------|----------------------------|---------------|
| 1 | Robustness/evolvability theory; glycobiology reviews | Conceptual framing |
| 2 | Concept memo; project plan; network biology literature | Hypotheses and predictions |
| 3 | Pathway curation notes; gene/edge tables; Reactome/GlyGen/UniProt/GO | Reproducible case definition |
| 4 | gnomAD/ExAC; constraint metrics; standing variation data | Quantitative empirical test |
| 5 | GeneReviews/CDG; ClinVar; OMIM-style sources; GWAS Catalog | Disease architecture test |
| 6 | Glycoimmunology, host-pathogen, expression, trait sources | Interface-layer support |
| 7 | 2012 paper; modern population genetics methods and datasets | Optional supporting/historical evidence |
| 8 | Results across all streams | Synthesis and interpretation |
| 9 | Failure modes and sensitivity analyses | Reviewer-risk management |
| 10 | All sections | Contribution statement |

## Word Count Summary

| Section | Target Words |
|---------|--------------|
| Introduction | 800 |
| Conceptual Model and Predictions | 900 |
| Case Definition | 900 |
| Constraint and Standing Variation | 1,100 |
| Disease Architecture | 1,100 |
| Interface Biology and Traits | 900 |
| Optional Population Genetics | 600 |
| Synthesis | 900 |
| Limitations and Future Directions | 500 |
| Conclusion | 300 |
| **Total** | **8,000** |
