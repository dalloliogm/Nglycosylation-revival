# Paper Thesis

Date drafted: 2026-05-30

Agentic work unit: `draft_paper_thesis`

Agent role: `hypothesis_agent`

## Thesis as a Testable Model

This paper should test N-glycosylation as a case study for a broader evolutionary-architecture model: biological pathways may localize robustness near catastrophic failure points and localize evolvability in branching, redundant, tissue-specific, or organism-environment interface layers.

For N-glycosylation, the working model is:

- Upstream conserved core, oligosaccharyltransferase, ER processing, and quality-control-linked machinery should behave as a robustness layer.
- Downstream Golgi branching, diversification, and terminal modification machinery should behave more like an evolvable interface layer.
- Substrate biosynthesis and broad donor-supply genes should be analyzed separately unless a specific test justifies assigning them to either layer.

This is a hypothesis to be evaluated, not a conclusion. The paper should ask whether pathway position and architecture predict evolutionary constraint, tolerated variation, disease architecture, tissue or trait associations, and optional population-genetic signals after accounting for obvious confounders.

## Central Claim Levels

### Claim 1: Conceptual Claim

Pathway architecture can create different evolutionary regimes within the same biological system.

Current status: supported by robustness/evolvability theory and network-biology framing, but not demonstrated specifically for N-glycosylation until the planned analyses are run.

Allowed manuscript language: "we test", "we propose", "the model predicts".

Avoid: "the pathway evolved to", "designed to", or "proves a robustness/evolvability partition".

### Claim 2: N-glycosylation Case-Study Claim

N-glycosylation is a plausible case study because its early steps are coupled to conserved protein maturation and ER quality control, while later glycan elaboration contributes to cell-surface diversity, immune recognition, pathogen interaction, tissue identity, inflammation, and other interface-facing phenotypes.

Current status: supported as biological motivation by the literature review. It remains a hypothesis at the gene-set and pathway-region level until tested with curated gene labels and quantitative evidence.

Allowed manuscript language: "provides a tractable case study", "motivates the prediction", "is consistent with".

Avoid: "all downstream genes are adaptive", "downstream genes are under positive selection", or "upstream genes are invariant".

### Claim 3: Empirical Architecture Claim

Upstream and downstream pathway regions should differ in constraint, disease burden, standing variation, and trait-association profiles.

Current status: primary empirical hypothesis.

Allowed manuscript language before analysis: "we predict", "we evaluate".

Allowed manuscript language after analysis depends on results: "shows", "supports", "is consistent with", or "does not support" only as justified by effect sizes, uncertainty, sensitivity analyses, and controls.

### Claim 4: Population-Genetic Claim

Population differentiation or selection-scan outliers, if included, can only provide supporting or hypothesis-generating evidence.

Current status: optional evidence layer.

Allowed manuscript language: "candidate signal", "outlier", "consistent with local differentiation", "requires locus-level follow-up".

Avoid: "selection event", "adaptive mutation", "population-specific adaptation", or causal gene assignment without fine-mapping, functional, or strong regulatory evidence.

## Competing Hypotheses

1. Architecture model: the upstream/downstream contrast reflects biological architecture, with catastrophic core machinery more constrained and branching interface machinery more permissive of variation.
2. Generic constraint model: any apparent contrast is explained by gene length, expression breadth, essentiality, mutation rate, recombination, background selection, or other generic genomic covariates rather than N-glycosylation architecture.
3. Annotation and ascertainment model: the contrast reflects database coverage, disease-study bias, pathway-label choices, SNP density, or literature attention rather than biology.
4. Population-structure artifact model: any differentiation or selection signal reflects demography, drift, LD, phasing, array or variant ascertainment, local recombination, or broad continental grouping rather than pathway-specific adaptation.
5. Local-context model: signals assigned to N-glycosylation genes may actually arise from nearby genes, regulatory elements, LD blocks, or regional genomic features.
6. General-interface model: N-glycosylation is not special; similar core/interface gradients should appear in many pathways with conserved cores and environmentally exposed outputs.
7. Null model: pathway region does not predict constraint, disease, variation, or trait evidence once measurement noise and covariates are considered.

## Predictions and Evidence Streams

| Prediction | Primary evidence streams | Required controls or caveats | Claim level if supported |
| --- | --- | --- | --- |
| Upstream core, OST, ER processing, and quality-control genes show stronger intolerance to damaging variation. | gnomAD-style constraint, missense and loss-of-function intolerance, standing variation summaries. | Gene length, mutation rate proxy, expression breadth, essentiality, mappability, background selection, and pathway-label sensitivity. | Supported architecture pattern, not proof of evolved design. |
| Upstream genes are enriched for severe Mendelian disease and CDG-like phenotypes. | GeneReviews/CDG curation, OMIM-style annotations, ClinVar pathogenic/likely pathogenic evidence. | Separate causal disease genes from broad association evidence; control for ascertainment and clinical-study intensity. | Supported disease-architecture gradient if effect is robust. |
| Downstream branching and terminal-modification genes show more tolerated standing variation or weaker constraint. | Population allele-frequency summaries, constraint metrics, rare-variant burden summaries where available. | Do not equate tolerance with positive selection; test sensitivity to low-specificity terminal-modification genes. | Consistent with evolvability/interface model. |
| Downstream/interface genes have richer links to immune, infection, inflammatory, cancer, microbiome, and tissue-identity phenotypes. | GWAS Catalog categories, ClinVar context, expression and tissue-specificity resources, glycoimmunology literature. | Gene assignment in GWAS is uncertain; distinguish nearby-locus evidence from causal-gene evidence. | Hypothesis-supporting trait profile, unless causal evidence is strong. |
| Catastrophic network positions are depleted for tolerated functional variation. | Curated pathway graph, depth, checkpoint proximity, branch-point status, redundancy/paralogy, essentiality, constraint. | Centrality alone is exploratory; graph construction and alternative encodings must be documented. | Supported network-safety pattern if robust across encodings. |
| Redundant, branching, terminal, or tissue-specific regions are enriched for innovation-zone signals. | Architecture features, tissue specificity, constraint, trait categories, optional population-genetic outliers. | Define "innovation-zone signal" operationally; avoid adaptive language unless independently supported. | Consistent with model; mechanism remains hypothetical. |
| Population differentiation, if analyzed, is more interpretable as a supporting layer than as the main result. | Pairwise FST, PBS or branch-aware statistics, optional iHS/nSL/XP-EHH/XP-CLR with modern data. | Explicit population definitions; regional inspection; LD, nearby genes, recombination, and replication checks. | Candidate or hypothesis-generating only. |

## Minimum Evidence Needed for the Paper

The paper should not require a successful selection scan. The minimum viable empirical story is:

1. A defensible pathway-region and architecture-feature table.
2. A constraint or tolerated-variation gradient across regions.
3. A disease-architecture comparison separating severe Mendelian evidence from broader trait associations.
4. A trait or tissue profile testing whether downstream genes are more interface-facing.
5. A limitations and claims framework that prevents outlier or gene-example storytelling from replacing the architecture-level test.

Population genetics can be included only if it clarifies or challenges the architecture model with modern controls. If the signals are weak or hard to assign to genes, they should be moved to supplemental or omitted.

## Reviewer-Risk Checklist

- Do not describe population-genetic outliers as proven adaptation.
- Do not assign a regional SNP or GWAS signal to a pathway gene without local-context review.
- Do not treat fixed gene windows as causal evidence.
- Do not use Fisher-combined SNP p-values or one-vs-rest continental comparisons as a central pillar.
- Do not let individual candidate genes dominate the paper unless the pathway-level pattern is already established.
- Do not treat network centrality as explanatory unless graph construction, null models, and sensitivity analyses support it.
- Do not merge substrate biosynthesis, core N-glycosylation, and broad terminal-modification genes without sensitivity analyses.
- Do not claim mechanism where the evidence supports only association, consistency, or hypothesis generation.

## Draft Manuscript Framing

The introduction should frame N-glycosylation as a concrete test bed for a broader model of pathway architecture. The results should be organized by predictions rather than by data source or favorite genes. The discussion should state that a supported gradient would argue for an architecture-level pattern, while still leaving open whether the pattern arises from direct selection for evolvability, biochemical constraint, historical contingency, or generic network properties.

The strongest possible conclusion is not that N-glycosylation proves adaptive modular design. The strongest disciplined conclusion is that N-glycosylation can reveal whether robustness-linked and interface-linked regions of a pathway carry measurably different evolutionary and disease signatures.
