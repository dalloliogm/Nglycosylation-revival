# Claims Register

Date drafted: 2026-05-31

Agentic work unit: `draft_claims_register`

Agent roles: `hypothesis_agent`; `critic_agent`

## Purpose

This file controls claim strength for the N-glycosylation evolutionary architecture paper. It should be updated whenever new analyses, literature extraction, or reviewer-risk checks change what the paper can responsibly say.

Claim levels:

- **Demonstrated**: directly shown by this project's analysis with documented data, controls, and sensitivity checks.
- **Supported**: backed by multiple evidence streams, but still not a mechanistic proof.
- **Consistent with**: compatible with evidence, but alternative explanations remain plausible.
- **Hypothesis-generating**: useful for framing or follow-up, not a conclusion.
- **Not shown**: explicitly outside the paper's evidence.

## Core Thesis Claims

| Claim | Current level | Evidence needed to strengthen | Allowed language | Avoid |
| --- | --- | --- | --- | --- |
| N-glycosylation is a useful case study for testing whether pathway architecture separates robustness and evolvability. | Supported | Curated pathway regions, architecture features, constraint, disease, glycome/regulatory, and trait evidence. | "N-glycosylation provides a tractable case study"; "we test an architecture model." | "N-glycosylation proves a universal design principle." |
| Upstream core, OST, ER processing, and quality-control-linked machinery behave as a robustness layer. | Hypothesis-generating | Stronger constraint, higher severe Mendelian/CDG burden, lower tolerated damaging variation, checkpoint proximity, sensitivity analyses. | "We predict"; "is expected to"; "is consistent with a robustness layer." | "Upstream genes are invariant"; "the pathway evolved this layer for robustness." |
| Downstream Golgi branching, terminal modification, and interface-facing machinery behave as an evolvability layer. | Hypothesis-generating | Glycan-output GWAS links, regulatory/tissue specificity, richer immune/infection/inflammation/cancer traits, tolerated variation, sensitivity to gene labels. | "May expose evolvability through glycan-output and regulatory layers." | "Downstream genes are adaptive"; "downstream enzymes are under positive selection." |
| Evolvability may be regulatory, glycan-output, tissue-specific, or trait-associated rather than coding-sequence acceleration. | Supported | Prior primate coding conservation plus glycome/IgG GWAS, eQTL or methylation evidence, tissue specificity, disease/trait links. | "Coding conservation is compatible with regulatory or phenotypic evolvability." | "No coding acceleration means no evolvability"; "regulatory variation proves adaptation." |

## Prior-Art And Novelty Claims

| Claim | Current level | Evidence needed to strengthen | Allowed language | Avoid |
| --- | --- | --- | --- | --- |
| Prior work already linked N-glycosylation to molecular evolution and network topology. | Demonstrated | Montanucci et al. and related pathway/network literature. | "Direct predecessor"; "prior work found strong coding conservation and network-associated constraint." | "This is the first evolutionary analysis of N-glycosylation." |
| Prior work already framed glycosylation as a gene-environment and regulatory interface. | Demonstrated | Zoldos/Lauc reviews and glyco-gene regulation literature. | "Builds on"; "formalizes and tests an existing conceptual thread." | "The glycosylation/evolvability connection is entirely new." |
| The new contribution is a formal, multi-evidence architecture test across pathway regions and evidence layers. | Hypothesis-generating | Completed architecture, constraint, disease, glycome/regulatory, tissue, and trait analyses. | "We formalize"; "we test"; "we integrate modern evidence streams." | "We prove the mechanism"; "we settle the origin of glycan evolvability." |

## Constraint And Disease Claims

| Claim | Current level | Evidence needed to strengthen | Allowed language | Avoid |
| --- | --- | --- | --- | --- |
| Upstream/core genes should show stronger gene-level constraint than downstream/interface genes. | Hypothesis-generating | gnomAD-style LOEUF/missense constraint with covariates and pathway-label sensitivity. | "Stronger constraint upstream would support"; "effect sizes and uncertainty show." | "Constraint equals selected robustness." |
| Upstream/core disruption should be enriched for severe Mendelian disease or CDG-like phenotypes. | Hypothesis-generating | Curated CDG, OMIM-style, and ClinVar pathogenic/likely pathogenic annotations by region. | "Severe disease burden is enriched"; "consistent with catastrophic-core sensitivity." | "All upstream variants cause severe disease." |
| Downstream/interface genes should show more complex, context-dependent, immune, inflammatory, cancer, infection, or tissue-related associations. | Hypothesis-generating | GWAS Catalog and curated trait categories with clear locus-to-gene confidence. | "Enriched for trait associations"; "more often linked to context-dependent phenotypes." | "GWAS loci prove causal pathway genes"; "trait association proves adaptation." |

## Regulatory And Glycan-Output Claims

| Claim | Current level | Evidence needed to strengthen | Allowed language | Avoid |
| --- | --- | --- | --- | --- |
| Glycome and IgG N-glycome GWAS provide a modern evidence stream for glycan-output variation. | Supported | Structured extraction of plasma/IgG N-glycome loci and mapping to glyco-genes, regulators, and pathway regions. | "Glycan-output variation is genetically tractable"; "loci implicate direct enzymes and regulators." | "Every glycome GWAS locus is a direct N-glycosylation enzyme." |
| Regulatory loci and epigenetic control may be central to glycosylation evolvability. | Consistent with | eQTL/TWAS/methylation evidence, glyco-gene expression, and tissue-specific deployment. | "Consistent with regulatory evolvability"; "suggests a regulatory layer." | "Epigenetic regulation is the demonstrated evolutionary mechanism." |
| IgG glycosylation links downstream glycan variation to immune and inflammatory phenotypes. | Supported | IgG N-glycome GWAS, immune pleiotropy studies, glycoimmunology literature. | "Antibody glycan traits connect glycosylation to immune regulation." | "IgG results generalize automatically to all N-glycosylation." |

## Population-Genetic Claims

| Claim | Current level | Evidence needed to strengthen | Allowed language | Avoid |
| --- | --- | --- | --- | --- |
| Population differentiation or selection scans are optional supporting evidence, not the paper's center. | Supported | Decision note and any modern analyses with demographic/local-context caveats. | "Supporting layer"; "candidate signal"; "outlier"; "consistent with." | "Proven adaptation"; "selection event"; "adaptive mutation." |
| Any candidate population-genetic locus requires nearby-gene and local-context review. | Demonstrated as requirement | LD, recombination, regulatory annotations, variant consequences, nearby genes, replication across methods or datasets. | "Regional signal near"; "candidate locus requiring follow-up." | "This signal belongs to gene X" without locus-level support. |
| Prior primate coding conservation argues against a simple downstream coding-adaptation model. | Supported | Montanucci et al.; any updated comparative coding analysis if run. | "Constrains the model"; "motivates looking at regulatory and glycan-output layers." | "No coding positive selection disproves interface evolvability." |

## Comparator-Pathway Claims

| Claim | Current level | Evidence needed to strengthen | Allowed language | Avoid |
| --- | --- | --- | --- | --- |
| A 1-3 pathway comparator module can test specificity against conserved linear pathways. | Hypothesis-generating | Curated comparator gene sets and lightweight constraint/disease/trait comparisons. | "Specificity check"; "comparative context." | "These few pathways prove a universal principle." |
| Heme biosynthesis is a useful negative comparator for conserved linear metabolic constraint. | Hypothesis-generating | Curated heme gene set, ordered positions, constraint and disease annotations. | "Constrained-core contrast." | "Heme is directly analogous to N-glycosylation's interface layer." |
| GPI-anchor biosynthesis is a useful positive comparator with glycan/cell-surface interface features. | Hypothesis-generating | Curated GPI gene set and interface/disease evidence. | "Closest architectural cousin"; "positive comparator." | "GPI-anchor biology is equivalent to N-glycosylation." |

## Forbidden Or Downgraded Claims

- Do not claim that N-glycosylation proves adaptive modular design.
- Do not claim that downstream genes are generally under positive selection.
- Do not claim that population-genetic outliers are demonstrated adaptations.
- Do not claim that GWAS loci identify causal glycosylation genes without locus-to-gene evidence.
- Do not claim that network centrality explains evolution unless graph encodings and null models support it.
- Do not claim that 1-3 comparator pathways establish a general law across biology.
- Do not claim that regulatory or epigenetic glyco-gene variation is adaptive unless the evidence directly supports adaptation.

## Update Rules

When a new result is added, update this register before manuscript drafting:

1. Add or revise the relevant claim.
2. Assign the claim level.
3. Link the evidence source: table, figure, methods note, or literature row.
4. Add the strongest alternative explanation.
5. Downgrade language if sensitivity analyses, provenance, or local-context review are incomplete.
