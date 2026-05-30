# STUDY.md

This is the live progress tracker for the N-glycosylation evolutionary architecture project. Update it whenever a step is started, completed, blocked, or re-scoped.

Status key:

- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked or needs decision

## Current Project Goal

Develop a new paper arguing that biological pathways can localize robustness and evolvability into different regions, using N-glycosylation as the primary case study.

The project is not centered on reproducing the 2012 population-genetics analysis. The original paper is historical context and a source of the base idea.

## Phase 0: Repository and Project Setup

- `[x]` Create repository scaffold.
- `[x]` Create `AGENTS.md` with project guidance for future agents.
- `[x]` Create `README.md` describing the project direction.
- `[x]` Create initial concept memo.
- `[x]` Create initial analysis plan.
- `[x]` Create original-paper context and critique note.
- `[x]` Create full project plan.
- `[~]` Create and maintain this live `STUDY.md` tracker.

Key files:

- `AGENTS.md`
- `README.md`
- `docs/concept/concept-memo.md`
- `docs/concept/project-plan.md`
- `docs/methods/analysis-plan.md`
- `docs/original-paper/context-and-critique.md`

## Phase 1: Literature Search and Conceptual Foundation

- `[~]` Define literature-search clusters.
- `[x]` Seed the literature matrix with high-priority papers.
- `[~]` Expand robustness/evolvability theory references.
- `[~]` Expand glycan evolution and Golgi diversification references.
- `[~]` Expand glycoimmunology, mucosal, microbiome, and host-pathogen interface references.
- `[~]` Expand disease architecture and CDG references.
- `[~]` Expand pathway/network biology references.
- `[ ]` Expand comparator-pathway references.
- `[ ]` Extract structured notes from high-priority papers.
- `[ ]` Write `docs/concept/paper-thesis.md`.
- `[ ]` Create a claims register distinguishing what the paper shows, suggests, and does not show.
- `[ ]` Create a reviewer-risk checklist from the original paper criticisms.
- `[ ]` Decide the paper type: primary analysis, conceptual synthesis plus analysis, or perspective with computational case study.

Key files:

- `docs/concept/literature-search-plan.md`
- `docs/concept/literature-matrix.tsv`
- `docs/concept/literature-review.md`
- `docs/concept/paper-thesis.md`

Immediate next tasks:

1. Extract structured notes from the highest-priority pathway-core papers into `docs/concept/literature-matrix.tsv`.
2. Read and extract the new sialic-acid evolution, glycosyltransferase evolution, mucosal glycan interface, and comparator-anchor papers added on 2026-05-28.
3. Draft the core paper thesis in one page.

## Phase 2: Pathway Curation

- `[x]` Define pathway-region labels and classification rules.
- `[x]` Create `docs/methods/pathway-curation.md`.
- `[x]` Create `docs/methods/pathway-edge-curation.md`.
- `[~]` Collect N-glycosylation genes from Reactome.
- `[ ]` Cross-check genes against GlyGen.
- `[ ]` Cross-check genes against UniProt, Ensembl/GENCODE, and Gene Ontology.
- `[~]` Identify aliases, deprecated symbols, and stable gene IDs.
- `[~]` Assign each gene to a pathway region.
- `[ ]` Flag ambiguous or multi-role genes.
- `[ ]` Test sensitivity to alternative pathway-region labels.
- `[x]` Create machine-readable gene table.
- `[x]` Create component-level pathway edge table.
- `[x]` Create gene-level pathway edge table with metabolite/intermediate labels.
- `[x]` Create first gene-level pathway network visualization.

Expected outputs:

- `docs/methods/pathway-curation.md`
- `docs/methods/pathway-edge-curation.md`
- `data/processed/nglyco_gene_table.tsv`
- `data/processed/nglyco_pathway_edges.tsv`
- `data/processed/nglyco_gene_gene_edges.tsv`
- `results/figures/nglyco_pathway_network.*`

Immediate next tasks:

1. Cross-check provisional MyGene.info Ensembl IDs and coordinates against Ensembl/HGNC.
2. Cross-check first-pass labels against GlyGen, UniProt, HGNC, and GO.
3. Decide whether low-specificity terminal modification genes should remain in the primary downstream set or only in sensitivity analyses.
4. Review gene-level pathway network visualization for readability and decide whether to split substrate-support donor edges into a separate panel.

## Phase 3: Architecture Metrics

- `[ ]` Define architecture features.
- `[ ]` Create `docs/methods/architecture-metrics.md`.
- `[ ]` Compute or curate pathway depth.
- `[ ]` Annotate branch point status.
- `[ ]` Annotate terminal modification status.
- `[ ]` Annotate checkpoint proximity.
- `[ ]` Annotate substrate biosynthesis involvement.
- `[ ]` Annotate redundancy or paralog family membership.
- `[ ]` Compute graph metrics.
- `[ ]` Test whether centrality metrics are robust across graph encodings before using them in the manuscript.
- `[ ]` Add expression breadth and tissue specificity metrics.
- `[ ]` Add essentiality metrics.
- `[ ]` Create combined architecture feature table.

Expected outputs:

- `docs/methods/architecture-metrics.md`
- `data/processed/nglyco_architecture_features.tsv`

## Phase 4: Constraint and Human Variation

- `[ ]` Identify current best constraint datasets.
- `[ ]` Create `docs/methods/constraint-analysis.md`.
- `[ ]` Add gene-level constraint metrics.
- `[ ]` Add loss-of-function intolerance metrics.
- `[ ]` Add missense constraint metrics.
- `[ ]` Add standing variation metrics.
- `[ ]` Compare upstream/core vs downstream/interface regions.
- `[ ]` Build matched-null controls.
- `[ ]` Test sensitivity to gene-region labels.
- `[ ]` Test sensitivity to covariates such as gene length and expression breadth.
- `[ ]` Report effect sizes and uncertainty, not only p-values.
- `[ ]` Test whether architecture features add information beyond a simple upstream/downstream binary.
- `[ ]` Create constraint-gradient figure.

Expected outputs:

- `docs/methods/constraint-analysis.md`
- `results/tables/constraint_summary.tsv`
- `results/figures/constraint_gradient.*`

## Phase 5: Disease Architecture

- `[ ]` Identify disease annotation sources.
- `[ ]` Create `docs/methods/disease-annotation.md`.
- `[ ]` Curate known Congenital Disorders of Glycosylation genes.
- `[ ]` Add OMIM-style Mendelian annotations.
- `[ ]` Add ClinVar pathogenic/likely pathogenic evidence.
- `[ ]` Add GWAS Catalog associations.
- `[ ]` Classify disease evidence by severity and confidence.
- `[ ]` Separate high-confidence causal disease genes from broad or weak association evidence.
- `[ ]` Compare severe Mendelian burden across pathway regions.
- `[ ]` Compare complex/context-dependent trait burden across pathway regions.
- `[ ]` Create disease architecture figure.

Expected outputs:

- `docs/methods/disease-annotation.md`
- `data/processed/nglyco_disease_annotations.tsv`
- `results/tables/disease_architecture_summary.tsv`
- `results/figures/disease_architecture.*`

## Phase 6: Trait and Tissue Interface Layer

- `[ ]` Identify tissue expression datasets.
- `[ ]` Create `docs/methods/interface-layer-analysis.md`.
- `[ ]` Add expression breadth.
- `[ ]` Add tissue specificity.
- `[ ]` Add epithelial/barrier tissue signal.
- `[ ]` Add immune-cell expression signal.
- `[ ]` Map GWAS traits to broad categories.
- `[ ]` Test enrichment of immune, infection, inflammation, cancer, microbiome, and tissue-identity traits downstream.
- `[ ]` Create interface-layer trait profile figure.

Expected outputs:

- `docs/methods/interface-layer-analysis.md`
- `results/tables/interface_trait_profile.tsv`
- `results/figures/interface_trait_profile.*`

## Phase 7: Population Genetics Decision

- `[ ]` Decide whether population genetics adds enough value.
- `[ ]` Create `docs/methods/popgen-decision.md`.
- `[ ]` If useful, select modern data sources.
- `[ ]` If useful, define population labels and comparisons.
- `[ ]` If useful, run pairwise FST or PBS.
- `[ ]` If useful, consider iHS, nSL, XP-EHH, or XP-CLR with strict caveats.
- `[ ]` Keep SNP-level, region-level, and gene-level claims distinct.
- `[ ]` For candidate loci, inspect nearby genes, LD, recombination, regulatory annotations, and variant consequences.
- `[ ]` Require replication across methods or datasets before highlighting any candidate locus.
- `[ ]` Integrate only robust and interpretable signals into the manuscript.

Expected outputs:

- `docs/methods/popgen-decision.md`
- `results/tables/popgen_supporting_signals.tsv`
- `results/figures/popgen_supporting_signals.*`

Decision rule:

Population genetics should support or challenge the architecture hypothesis. It should not become the main story unless the evidence is unusually clean and replicated.

## Phase 8: Comparator Pathways

- `[~]` Decide whether comparator pathways are necessary for the target paper.
- `[x]` Record deferred cross-pathway expansion idea and candidate linear comparators.
- `[ ]` Create `docs/methods/comparator-pathways.md`.
- `[ ]` Select one constrained-core comparator pathway.
- `[ ]` Select one adaptive-interface comparator pathway.
- `[ ]` Curate comparator gene sets.
- `[ ]` Apply a lightweight version of architecture, constraint, and disease analyses.
- `[ ]` Create cross-pathway architecture figure.

Expected outputs:

- `docs/concept/linear-pathway-comparators.md`
- `docs/methods/comparator-pathways.md`
- `data/processed/comparator_pathway_gene_table.tsv`
- `results/figures/cross_pathway_architecture.*`

## Phase 9: Figures and Manuscript

- `[x]` Create ARS-style paper configuration record.
- `[x]` Create manuscript outline.
- `[x]` Create ARS-style argument blueprint.
- `[x]` Create figure plan.
- `[ ]` Create evidence matrix separating robust architecture-level findings from hypothesis-generating candidate signals.
- `[ ]` Draft introduction.
- `[ ]` Draft methods.
- `[ ]` Draft results.
- `[ ]` Draft discussion.
- `[ ]` Draft limitations.
- `[ ]` Check that individual gene examples do not dominate the architecture-level argument.
- `[ ]` Assemble first complete manuscript draft.
- `[ ]` Prepare supplementary tables.
- `[ ]` Prepare reproducibility statement.

Expected outputs:

- `docs/manuscript/outline.md`
- `docs/manuscript/paper-configuration.md`
- `docs/manuscript/argument-blueprint.md`
- `docs/manuscript/figure-plan.md`
- `docs/manuscript/draft.md`
- `results/figures/`
- `results/tables/`

## Phase 10: Quality Control and Submission Preparation

- `[ ]` Check all scripts and notebooks are reproducible.
- `[ ]` Verify all data sources are documented with versions and access dates.
- `[ ]` Verify all figures can be regenerated.
- `[ ]` Review statistical assumptions and sensitivity analyses.
- `[ ]` Review the manuscript against the original-paper failure modes in `docs/concept/project-plan.md`.
- `[ ]` Verify that all adaptive or mechanistic claims are supported by the appropriate evidence level.
- `[ ]` Review citation coverage.
- `[ ]` Select target journal.
- `[ ]` Format manuscript for target journal.
- `[ ]` Prepare cover letter.
- `[ ]` Archive reproducible release.

Expected outputs:

- final manuscript
- reproducible repository release
- submission package

## Phase 11: Agentic Paper Implementation

- `[x]` Define an agentic-system plan for implementing the paper as supervised research workflows.
- `[x]` Create a machine-readable agent and gate registry.
- `[x]` Create a lightweight registry inspection script.
- `[x]` Create Makefile targets for inspecting and checking the agentic workflow.
- `[ ]` Draft `docs/concept/paper-thesis.md` using the hypothesis agent role.
- `[ ]` Draft `docs/concept/claims-register.md` using the critic and hypothesis agent roles.
- `[ ]` Draft `docs/methods/architecture-metrics.md` using the architecture agent role.
- `[ ]` Use the registry to choose and commit small agentic work units.

Expected outputs:

- `docs/methods/agentic-system-plan.md`
- `workflow/agentic_paper_system.json`
- `scripts/inspect_agentic_system.py`
- `Makefile`

## Active Decisions

- `[!]` Decide whether the first paper should include comparator pathways or stay focused on N-glycosylation.
- `[!]` Decide how much population genetics to include.
- `[!]` Decide whether this is framed as a primary computational analysis paper or a conceptual paper with quantitative support.
- `[!]` Confirm the ARS paper configuration record before moving from planning to drafting.

## Change Log

- 2026-05-20: Created `STUDY.md` as the live project tracker.
- 2026-05-20: Added `docs/concept/literature-review.md` as the readable grouped literature summary; corrected the N-linked glycosylation network citation; expanded `docs/concept/literature-matrix.tsv` with high-priority references across N-glycosylation, population genetics, network biology, disease/constraint, glycoimmunology, and robustness/evolvability.
- 2026-05-21: Added original-paper criticisms as explicit robustness/reviewer-risk safeguards in `docs/concept/project-plan.md` and mirrored them as checklist items in this tracker.
- 2026-05-21: Deferred all-pathway expansion for later and added `docs/concept/linear-pathway-comparators.md` to preserve candidate linear or quasi-linear pathway comparators, including GPI-anchor biosynthesis, heme biosynthesis, cholesterol biosynthesis, CoQ biosynthesis, and related metabolic controls.
- 2026-05-21: Started N-glycosylation pathway curation. Added `docs/methods/pathway-curation.md` and first-pass `data/processed/nglyco_gene_table.tsv` with pathway-region labels, primary-analysis flags, sensitivity flags, provisional Ensembl IDs, and provisional coordinates. Reactome release 96 and MyGene.info were checked; direct Ensembl/HGNC validation and GlyGen/UniProt/GO cross-checks remain pending.
- 2026-05-21: Added uv project environment, `data/processed/nglyco_pathway_edges.tsv`, and `scripts/plot_nglyco_pathway_network.py`; generated first pathway architecture visualization at `results/figures/nglyco_pathway_network.png` and `.svg`.
- 2026-05-21: Re-scoped the pathway visualization from component nodes to gene nodes. Added `data/processed/nglyco_gene_gene_edges.tsv`, where each edge connects source and target genes and carries a metabolite, glycoprotein intermediate, donor substrate, quality-control, or complex-context label.
- 2026-05-21: Added source provenance columns to `data/processed/nglyco_gene_gene_edges.tsv` and documented edge abstraction rules in `docs/methods/pathway-edge-curation.md`.
- 2026-05-22: Adapted manuscript planning to the `academic-research-suite` `academic-paper` conventions. Added `docs/manuscript/paper-configuration.md`, `docs/manuscript/outline.md`, `docs/manuscript/argument-blueprint.md`, and `docs/manuscript/figure-plan.md`.
- 2026-05-28: Continued ARS deep-research literature expansion. Added new references on bow-tie/sloppiness theory, sialic-acid and SIGLEC evolution, vertebrate glycan diversity, glycosyltransferase phylogenetic profiling, fucosyltransferase evolution, mucosal/gut glycan interface biology, and initial comparator anchors for MHC/HLA, olfactory receptors, and ER quality control to `docs/concept/literature-matrix.tsv`; updated `docs/concept/literature-review.md` with synthesis notes and revised immediate next tasks.
- 2026-05-30: Added an agentic paper implementation plan, machine-readable agent/gate registry, and inspection script so future work can be organized as small supervised research-agent tasks.
- 2026-05-30: Added Makefile targets for inspecting, checking, and listing ready agentic workflow tasks.
