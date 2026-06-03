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
- `[~]` Expand glycome genetics and glyco-gene regulatory references.
- `[ ]` Expand comparator-pathway references.
- `[ ]` Extract structured notes from high-priority papers.
- `[x]` Write `docs/concept/paper-thesis.md`.
- `[x]` Create a claims register distinguishing what the paper shows, suggests, and does not show.
- `[ ]` Create a reviewer-risk checklist from the original paper criticisms.
- `[ ]` Decide the paper type: primary analysis, conceptual synthesis plus analysis, or perspective with computational case study.

Key files:

- `docs/concept/literature-search-plan.md`
- `docs/concept/literature-matrix.tsv`
- `docs/concept/literature-review.md`
- `docs/concept/paper-thesis.md`

Immediate next tasks:

1. Extract structured notes from the highest-priority pathway-core papers into `docs/concept/literature-matrix.tsv`.
2. Extract Montanucci et al., Zoldos et al., Lauc and Zoldos, and post-2010 glycome/IgG N-glycome GWAS papers into `docs/concept/literature-matrix.tsv`.
3. Read and extract the new sialic-acid evolution, glycosyltransferase evolution, mucosal glycan interface, and comparator-anchor papers added on 2026-05-28.

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

- `[x]` Define architecture features.
- `[x]` Create `docs/methods/architecture-metrics.md`.
- `[x]` Compute or curate pathway depth.
- `[x]` Annotate branch point status.
- `[x]` Annotate terminal modification status.
- `[x]` Annotate checkpoint proximity.
- `[x]` Annotate substrate biosynthesis involvement.
- `[x]` Annotate redundancy or paralog family membership.
- `[x]` Compute graph metrics.
- `[ ]` Test whether centrality metrics are robust across graph encodings before using them in the manuscript.
- `[ ]` Add expression breadth and tissue specificity metrics.
- `[ ]` Add essentiality metrics.
- `[x]` Create combined architecture feature table.

Expected outputs:

- `docs/methods/architecture-metrics.md`
- `data/processed/nglyco_architecture_features.tsv`
- `results/tables/architecture_feature_summary.tsv`

## Phase 4: Constraint and Human Variation

- `[x]` Identify current best constraint datasets.
- `[x]` Create `docs/methods/constraint-analysis.md`.
- `[x]` Create constraint metric importer and join-audit script.
- `[x]` Add gene-level constraint metrics.
- `[x]` Add loss-of-function intolerance metrics.
- `[x]` Add missense constraint metrics.
- `[ ]` Add standing variation metrics.
- `[x]` Compare upstream/core vs downstream/interface regions.
- `[ ]` Build matched-null controls.
- `[x]` Test sensitivity to gene-region labels.
- `[ ]` Test sensitivity to covariates such as gene length and expression breadth.
- `[x]` Report effect sizes and uncertainty, not only p-values.
- `[ ]` Test whether architecture features add information beyond a simple upstream/downstream binary.
- `[x]` Create constraint-gradient figure.
- `[x]` Create pathway network figures colored by constraint metrics.

Expected outputs:

- `docs/methods/constraint-analysis.md`
- `scripts/build_nglyco_constraint_summary.py`
- `data/processed/nglyco_constraint_metrics.tsv`
- `results/tables/constraint_join_audit.tsv`
- `results/tables/constraint_summary.tsv`
- `results/tables/constraint_group_comparisons.tsv`
- `results/figures/constraint_gradient.*`
- `results/figures/nglyco_pathway_constraint_*.{png,svg}`
- `results/reports/constraint-gradient-interpretation.md`

## Phase 5: Disease Architecture

- `[x]` Identify disease annotation sources.
- `[x]` Create `docs/methods/disease-annotation.md`.
- `[x]` Curate known Congenital Disorders of Glycosylation genes.
- `[ ]` Add OMIM-style Mendelian annotations.
- `[ ]` Add ClinVar pathogenic/likely pathogenic evidence.
- `[ ]` Add GWAS Catalog associations.
- `[~]` Classify disease evidence by severity and confidence.
- `[~]` Separate high-confidence causal disease genes from broad or weak association evidence.
- `[~]` Compare severe Mendelian burden across pathway regions.
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
- `[x]` Document optional 1-3 pathway comparator module for the first paper.
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
- `[x]` Create a prompt generator that turns a backlog item into an executable Codex task packet.
- `[x]` Draft `docs/concept/paper-thesis.md` using the hypothesis agent role.
- `[x]` Draft `docs/concept/claims-register.md` using the critic and hypothesis agent roles.
- `[x]` Draft `docs/methods/architecture-metrics.md` using the architecture agent role.
- `[ ]` Use the registry to choose and commit small agentic work units.

Expected outputs:

- `docs/methods/agentic-system-plan.md`
- `workflow/agentic_paper_system.json`
- `scripts/inspect_agentic_system.py`
- `scripts/create_agentic_task_prompt.py`
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
- 2026-05-30: Added a prompt generator and `make agentic-prompt` target to turn registry backlog items into concrete Codex work instructions.
- 2026-06-03: Added `compute_architecture_features` to the agentic backlog and implemented `scripts/build_nglyco_architecture_features.py`, producing first-pass architecture features and a summary table from the curated gene and edge tables.
- 2026-06-03: Added `build_constraint_importer` and `compute_constraint_summary` agentic backlog tasks plus `scripts/build_nglyco_constraint_summary.py`, a reproducible importer for local gnomAD-style constraint metric TSVs with Ensembl-ID joins, symbol-mismatch audit, LOEUF threshold labeling, and pathway-region summaries.
- 2026-06-03: Ran the provisional gnomAD v4.1 constraint summary from `data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv`. Generated per-gene constraint metrics, a join audit, and group summaries; 95 of 101 genes matched by Ensembl ID, with six missing constraint metrics in this file.
- 2026-06-03: Added `analyze_constraint_gradient` and `scripts/analyze_constraint_gradient.py`, generating provisional LOEUF/missense-Z comparison effect sizes and `constraint_gradient` figures for the gnomAD v4.1 constraint run.
- 2026-06-03: Added a written constraint-gradient interpretation note and full pathway network plots colored by LOEUF and missense Z to make the provisional constraint result inspectable gene by gene.
- 2026-06-03: Started the disease-architecture work package by adding `docs/methods/disease-annotation.md`, defining GeneReviews CDG, ClinVar P/LP, and GWAS Catalog evidence tiers plus disease output schemas and claim limits.
- 2026-06-03: Completed the first conservative CDG seed curation from GeneReviews Table 1 using `scripts/build_nglyco_disease_seed_table.py`. Generated `data/processed/nglyco_disease_annotations.tsv` for 101 pathway genes and `results/tables/disease_architecture_summary.tsv`; ClinVar, OMIM-style breadth, and GWAS layers remain pending.
- 2026-05-30: Completed agentic work unit `draft_paper_thesis` with `docs/concept/paper-thesis.md`, formalizing the robustness/evolvability thesis as a testable model with competing hypotheses, prediction-to-evidence mapping, claim levels, and critic safeguards.
- 2026-05-31: Documented an optional first-paper comparator module using 1-3 pathways as a specificity check, with heme biosynthesis, CoQ / ubiquinone biosynthesis, and GPI-anchor biosynthesis as the recommended minimal candidates.
- 2026-05-31: Updated the thesis, project plan, and literature review to position Montanucci et al. and Zoldos/Lauc glyco-regulation work as direct predecessors, and to shift the expected evolvability signal toward regulatory, glycan-output, tissue, disease, and trait layers rather than coding-sequence acceleration.
- 2026-05-31: Added structured literature-matrix summaries for direct-predecessor, glyco-gene regulation, and glycome/IgG N-glycome GWAS papers, with relevance and limitations recorded for each.
- 2026-05-31: Added one standalone paper-summary file per priority glycome regulation/evolution paper in `docs/concept/paper-summaries/`.
- 2026-05-31: Added `docs/concept/claims-register.md` to control claim strength across thesis, prior art, constraint, disease, regulatory/glycome-output, population-genetic, and comparator-pathway claims.
- 2026-05-31: Added `docs/methods/architecture-metrics.md` defining planned gene-level architecture features, graph encodings, sensitivity analyses, and claim limits before computing architecture tables.
- 2026-06-02: Added `docs/methods/constraint-analysis.md` scoping gnomAD v4.1.1 constraint metrics, join rules, covariates, matched-null strategy, sensitivity analyses, and claim limits for the constraint work package.
