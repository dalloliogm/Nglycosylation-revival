# Project Plan: Evolutionary Architecture of N-glycosylation

## Aim

Develop a new paper from the base idea of the 2012 N-glycosylation population-genetics study, without centering the project on a close reproduction of the original analysis.

The target contribution is a systems/evolutionary biology paper arguing that biological pathways can organize robustness and evolvability into different regions. N-glycosylation is the primary case study because its upstream machinery is tightly linked to protein-folding quality control, while its downstream machinery creates glycan diversity at the organism-environment interface.

## Candidate Paper Thesis

Biological pathways may localize evolvability away from catastrophic failure points. In N-glycosylation, upstream core machinery is expected to behave like a robustness layer, while downstream branching and terminal modification machinery behaves more like an evolvable interface layer.

This thesis must be positioned as a formalization and modern empirical test of an existing conceptual thread, not as a claim that the glycosylation/evolvability connection is entirely new. Prior work on N-glycosylation evolution across primates found strong protein-coding conservation and no clear positive-selection signal, while also showing that network structure relates to evolutionary constraint. Prior work on epigenetic and genetic regulation of protein glycosylation argued that glycan diversity can arise from regulated glyco-gene networks and environmental responsiveness rather than from direct genetic templates for glycan structures.

Revised novelty claim:

The paper should test whether conserved core machinery and variable interface-facing glycan outputs occupy different pathway regions and evidence layers. The expected evolvability signal may be regulatory, phenotypic, tissue-specific, or trait-associated rather than simple acceleration of coding-sequence evolution.

The paper should test this as an architectural hypothesis using multiple evidence streams:

- pathway position and topology
- evolutionary constraint
- human standing variation
- disease architecture
- glycome and IgG N-glycome genetic architecture
- regulatory and epigenetic evidence
- tissue specificity
- trait associations
- population differentiation or selection signals, if useful

Population genetics is a supporting layer, not the center of the paper.

## Failure Modes To Design Against

The original paper is valuable because it exposed the base idea, but its weaknesses should become design requirements for the new paper.

### F1: Interesting biology mistaken for demonstrated evolutionary mechanism

Risk:

The paper could tell a compelling story about upstream robustness and downstream interface biology without actually testing the mechanism.

Defense:

- State each claim as a measurable prediction before running analyses.
- Separate conceptual argument, empirical observation, and mechanistic inference.
- Use multiple evidence streams before making architecture-level claims.
- Use cautious language when evidence is indirect.

### F2: Outlier statistics treated as selection events

Risk:

Population-genetic or association outliers could be described as true adaptive events when they may reflect demography, drift, LD, ascertainment, local genomic context, or nearby genes.

Defense:

- Treat population genetics as optional supporting evidence.
- Use terms such as "candidate signal", "outlier", or "consistent with" unless there is strong causal evidence.
- Require replication across methods or datasets before highlighting a candidate locus.
- Do not build the main paper around individual selection-scan hits.

### F2b: Coding-sequence evolvability expected in the wrong layer

Risk:

The paper could predict downstream coding-sequence acceleration even though prior primate work found strong conservation across the pathway and no clear protein-coding positive-selection signal.

Defense:

- Treat prior dN/dS conservation as a constraint benchmark.
- Reframe evolvability as potentially regulatory, glycan-output, tissue-specific, disease-architecture, or trait-association variation.
- Use coding-sequence evolution as historical context, not as the primary test of downstream evolvability.
- State explicitly that downstream/interface evolvability does not require most downstream enzyme coding sequences to evolve rapidly.

### F3: Crude population categories and demographic confounding

Risk:

Broad population labels or one-vs-rest comparisons could create a false impression of local adaptation.

Defense:

- Avoid population genetics unless it contributes a clear, controlled test.
- If included, use modern datasets, explicit sample definitions, pairwise or branch-aware comparisons, and demographic caveats.
- Prefer pathway architecture, constraint, disease, and tissue evidence as the primary pillars.

### F4: Weak assignment of regional genomic signals to pathway genes

Risk:

Signals near a gene could be incorrectly attributed to that gene or to N-glycosylation biology.

Defense:

- Keep SNP-level, region-level, and gene-level claims distinct.
- Inspect nearby genes, LD, recombination, regulatory annotations, and variant consequences for candidate loci.
- Avoid causal gene language unless supported by functional, fine-mapping, eQTL, or disease evidence.

### F5: Fragile small-count upstream/downstream tests

Risk:

The key contrast could depend on arbitrary labels, window sizes, or a small number of genes.

Defense:

- Use sensitivity analyses across pathway-region definitions.
- Report effect sizes and uncertainty, not only p-values.
- Use matched null sets or covariate-adjusted models where possible.
- Test whether architecture features add information beyond a simple upstream/downstream binary.

### F6: Decorative network analysis

Risk:

Network centrality could become an underpowered add-on that sounds sophisticated but does not support the argument.

Defense:

- Define graph construction rules before computing metrics.
- Prioritize interpretable architecture features: depth, branch point status, redundancy, checkpoint proximity, terminal modification, and tissue specificity.
- Treat centrality metrics as exploratory unless robust across graph encodings and null models.

### F7: No functional grounding

Risk:

The paper could discuss glycan biology while analyzing only abstract gene lists.

Defense:

- Add disease, expression, tissue, trait, and functional annotation layers.
- Distinguish core biochemical function from downstream cell-surface/interface roles.
- Where possible, connect genes to known glycan phenotypes, CDG evidence, immune biology, cancer biology, or host-pathogen interactions.

### F8: Disease architecture missed or underused

Risk:

The strongest testable prediction may be missed: severe core defects upstream versus subtler/context-dependent phenotypes downstream.

Defense:

- Make disease architecture a core work package.
- Separate high-confidence Mendelian disease from broad association evidence.
- Test severe Mendelian burden, ClinVar pathogenicity, CDG membership, GWAS associations, and trait category profiles by pathway region.

### F9: Gene-hit narrative overwhelms architecture

Risk:

The manuscript could drift into a list of interesting genes rather than testing a general architecture hypothesis.

Defense:

- Organize results by predictions and pathway regions.
- Use individual genes as examples only after pathway-level patterns are shown.
- Include an evidence matrix distinguishing robust architecture-level findings from hypothesis-generating candidates.

### F10: Overconfident conclusions

Risk:

The final paper could make claims stronger than the data justify.

Defense:

- Include a dedicated limitations section.
- Maintain a claims register: what the paper shows, suggests, and does not show.
- Explicitly state whether the work demonstrates mechanism, supports a model, or proposes a testable framework.

## Main Hypotheses

### H1: Robustness/evolvability partition

Upstream N-glycosylation genes are enriched for robustness signatures, while downstream genes are enriched for evolvability/interface signatures.

Expected evidence:

- higher constraint upstream
- higher essentiality upstream
- higher severe Mendelian disease burden upstream
- lower tolerated damaging variation upstream
- greater phenotypic or regulatory diversity downstream
- more immune, infection, cancer, inflammation, microbiome, or tissue-specific links downstream

### H2: Disease architecture gradient

Core pathway disruption should produce rare severe disease, while downstream variation should more often contribute to quantitative or context-dependent phenotypes.

Expected evidence:

- upstream enrichment for Congenital Disorders of Glycosylation and severe OMIM/ClinVar annotations
- downstream enrichment for GWAS, regulatory, immune, inflammatory, cancer, infection, or tissue-specific associations
- distinct variant effect profiles across pathway regions

### H3: Network safety principle

Pathway regions with catastrophic failure potential should be depleted for tolerated functional variation, while redundant, branching, terminal, or tissue-specific regions should tolerate more variation.

Expected evidence:

- constraint correlates with pathway depth, checkpoint proximity, low redundancy, or essentiality
- tolerated variation correlates with branching, alternative routes, terminal modification, or tissue-specific deployment
- simple pathway-region labels outperform or complement generic gene-level covariates

### H4: N-glycosylation is a case study of a broader architectural principle

The robustness/evolvability pattern should not be unique to N-glycosylation.

Expected evidence:

- similar core/interface gradients in other pathways
- contrast with pathways that lack obvious environmental-interface layers
- stronger manuscript if at least one comparator pathway is included

## Work Packages

### WP1: Concept and Scope

Deliverables:

- `docs/concept/concept-memo.md` refined into a paper-facing concept note
- one-page thesis statement
- list of claims the paper will and will not make
- prior-art positioning note covering primate N-glycosylation evolution and glyco-gene regulatory/epigenetic work
- target journal category: conceptual systems biology, evolutionary genomics, or computational biology

Key decisions:

- Is this primarily a single-pathway case study or a broader cross-pathway framework?
- Are population-genetic scans necessary, or can the first paper stand on constraint, disease, topology, and trait architecture?
- What is the minimum analysis set needed for a publishable story?

### WP2: Pathway Curation

Deliverables:

- machine-readable N-glycosylation gene table
- stable gene identifiers, symbols, coordinates, and aliases
- region labels: upstream core, OST/checkpoint, ER quality control, substrate biosynthesis, Golgi branching, terminal modification, environmental interface, ambiguous
- evidence source for every classification
- curated pathway graph or edge table

Candidate sources:

- Reactome
- GlyGen
- UniProt
- Ensembl/GENCODE
- Gene Ontology
- literature curation where databases disagree

Output files:

- `data/processed/nglyco_gene_table.tsv`
- `data/processed/nglyco_pathway_edges.tsv`
- `docs/methods/pathway-curation.md`

### WP3: Architecture Metrics

Deliverables:

- per-gene architecture feature table
- topology metrics and pathway-region descriptors
- documented graph construction rules

Features to consider:

- pathway region
- pathway depth
- branch point status
- terminal modification status
- checkpoint proximity
- substrate biosynthesis involvement
- redundancy or paralog family membership
- degree, betweenness, closeness, and other graph metrics
- tissue specificity
- expression breadth
- essentiality

Output files:

- `data/processed/nglyco_architecture_features.tsv`
- `docs/methods/architecture-metrics.md`

### WP4: Constraint and Human Variation

Deliverables:

- upstream/downstream comparison of constraint metrics
- matched-null analysis controlling for basic genomic covariates
- visualization of variation tolerance across pathway architecture

Candidate evidence:

- gene-level constraint metrics
- loss-of-function intolerance
- missense constraint
- rare damaging variant burden
- standing variation from modern population datasets

Important controls:

- gene length
- coding sequence length
- expression breadth
- local mutation rate proxies
- mappability
- recombination/background selection where available

Output files:

- `results/tables/constraint_summary.tsv`
- `results/figures/constraint_gradient.*`
- `docs/methods/constraint-analysis.md`

### WP5: Disease Architecture

Deliverables:

- curated disease annotations for N-glycosylation genes
- tests of severe Mendelian burden vs complex/context-dependent trait burden
- disease architecture figure

Candidate evidence:

- OMIM-style Mendelian disease annotation
- ClinVar pathogenic/likely pathogenic burden
- known Congenital Disorders of Glycosylation genes
- GWAS Catalog associations
- cancer relevance where directly connected to glycosylation biology
- immune, inflammatory, infection, autoimmune, and microbiome-related annotations

Interpretation rule:

Do not count every vague gene-disease association equally. Separate high-confidence causal disease genes from broad association signals.

Output files:

- `data/processed/nglyco_disease_annotations.tsv`
- `results/tables/disease_architecture_summary.tsv`
- `results/figures/disease_architecture.*`
- `docs/methods/disease-annotation.md`

### WP6: Trait and Tissue Interface Layer

Deliverables:

- test whether downstream genes are enriched for tissue-specific or environment-interface biology
- trait-category profile by pathway region

Candidate evidence:

- tissue specificity and expression breadth
- immune-cell expression
- epithelial/barrier-tissue expression
- GTEx-style tissue expression
- GWAS category mapping
- glycome and IgG N-glycome GWAS evidence
- eQTL, TWAS, methylation, or other regulatory evidence where available
- microbiome, infection, inflammation, autoimmunity, cancer, and cell-surface biology annotations

Key tests:

- whether downstream/interface genes are enriched for relevant trait categories
- whether tissue-specific deployment is stronger downstream
- whether glycan-output variation and regulatory loci map preferentially to downstream/interface or trans-regulatory control layers
- whether upstream genes mostly map to severe Mendelian disease rather than broad complex-trait associations

Output files:

- `results/tables/interface_trait_profile.tsv`
- `results/figures/interface_trait_profile.*`
- `docs/methods/interface-layer-analysis.md`

### WP7: Population Genetics as Supporting Evidence

Deliverables:

- decide whether population differentiation or selection scans add value to the paper
- if yes, run a restrained modern analysis with strong caveats

Possible analyses:

- pairwise FST
- PBS
- allele-frequency differentiation
- iHS/nSL/XP-EHH only if phased data and interpretation are solid

Interpretation rule:

These analyses should support or challenge the architecture hypothesis. They should not become the main story unless the signals are exceptionally clean and replicated.

Output files:

- `docs/methods/popgen-decision.md`
- `results/tables/popgen_supporting_signals.tsv`
- `results/figures/popgen_supporting_signals.*`

### WP8: Comparator Pathways

Deliverables:

- decide whether to include comparator pathways
- if included, curate a small set that tests generality

Candidate comparator classes:

- robustness-heavy core pathways: core ER protein folding, ribosome/translation, central metabolism
- evolvable interface pathways: immune receptors, MHC-related pathways, olfactory receptors, mucins/glycocalyx-related systems
- mixed architecture pathways: insulin/TOR, other glycosylation pathways, secretory pathway modules

Minimum useful comparison:

- one constrained core pathway
- one adaptive interface pathway
- N-glycosylation as the layered architecture example

Output files:

- `data/processed/comparator_pathway_gene_table.tsv`
- `results/figures/cross_pathway_architecture.*`
- `docs/methods/comparator-pathways.md`

### WP9: Manuscript Assembly

Deliverables:

- manuscript outline
- figure list
- results narrative
- discussion framing
- limitations section

Proposed manuscript structure:

1. Introduction: robustness, evolvability, and pathway architecture
2. Why N-glycosylation is an ideal case study
3. Curated pathway architecture
4. Constraint and disease gradients
5. Interface-layer trait/tissue evidence
6. Optional population-genetic support
7. General model and comparator pathways
8. Limitations and future work

Output files:

- `docs/manuscript/outline.md`
- `docs/manuscript/draft.md`
- `results/figures/`

## Analysis Order

1. Finalize the concept and claims.
2. Curate the N-glycosylation gene set and pathway-region labels.
3. Build architecture features.
4. Run constraint and disease analyses first.
5. Add tissue/trait interface analyses.
6. Decide whether population genetics adds enough value.
7. Decide whether comparator pathways are necessary for the target journal.
8. Assemble figures and manuscript.

## Early Go/No-Go Criteria

The project is strong if:

- upstream genes clearly show stronger constraint and severe disease burden
- downstream genes show credible enrichment for interface traits, tissue specificity, or context-dependent disease biology
- architecture features explain more than a simple upstream/downstream binary
- at least one comparator pathway supports the broader principle

The project is weaker if:

- upstream/downstream differences disappear after basic controls
- disease and trait annotations are too sparse or too biased
- the story depends mostly on old selection-scan outliers
- pathway-region labels are too subjective to defend

If the main N-glycosylation result is weak, pivot to a broader review/perspective or methods paper on how to test robustness/evolvability architecture across pathways.

## First Concrete Tasks

1. Create `docs/concept/paper-thesis.md` with a sharper title, abstract-level thesis, and explicit claims.
2. Create `docs/methods/pathway-curation.md` defining pathway-region labels and evidence rules.
3. Build `data/processed/nglyco_gene_table.tsv`.
4. Build a first static pathway figure from the curated labels.
5. Collect constraint and disease annotation sources.
6. Run a first upstream/downstream comparison for constraint and disease burden.

## Working Title Options

- Robustness and Evolvability in the Architecture of N-glycosylation
- Localizing Evolvability Away from Failure Points in Biological Pathways
- N-glycosylation as a Model for Evolutionary Architecture in Cellular Systems
- From Core Constraint to Interface Diversity: Evolutionary Architecture of N-glycosylation
- Catastrophic Cores and Evolvable Interfaces in Biological Pathways
