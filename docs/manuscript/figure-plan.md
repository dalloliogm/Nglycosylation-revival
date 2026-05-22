# Figure Plan

ARS workflow: `academic-paper`, Visualization planning support.

## Figure 1: Conceptual Architecture Model

**Purpose**: Show the paper's core hypothesis visually.

**Content**: A pathway-layer schematic separating conserved upstream/core machinery, OST/checkpoint and ER quality-control layers, Golgi diversification, terminal modification, and organism-environment interface functions.

**Evidence status**: Conceptual; should be explicitly labeled as the tested model, not a result.

## Figure 2: Curated N-glycosylation Pathway Graph

**Purpose**: Define the case study and show the curated graph used for architecture features.

**Content**: Current pathway network visualization from `results/figures/nglyco_pathway_network.*`, revised for manuscript readability if needed.

**Evidence status**: Existing first version available; needs database cross-check and visual refinement.

## Figure 3: Constraint and Tolerated Variation Gradient

**Purpose**: Test the robustness-layer prediction.

**Content**: Gene-level constraint and tolerated variation metrics by pathway region, with uncertainty and matched-null or covariate-adjusted summaries.

**Evidence status**: Planned.

## Figure 4: Disease Architecture Gradient

**Purpose**: Test severe Mendelian burden upstream versus complex/context-dependent trait burden downstream.

**Content**: Region-level burden of CDG/Mendelian disease, ClinVar pathogenic evidence, and GWAS/trait categories separated by evidence confidence.

**Evidence status**: Planned.

## Figure 5: Interface Trait and Tissue Profile

**Purpose**: Show whether downstream/interface regions are enriched for immune, infection, inflammation, cancer, microbiome, barrier-tissue, or tissue-identity signals.

**Content**: Heatmap or dot plot of trait categories and expression/tissue features by pathway region.

**Evidence status**: Planned.

## Figure 6: Evidence Matrix

**Purpose**: Keep interpretation disciplined.

**Content**: Rows as predictions; columns as evidence streams. Cells distinguish supported, mixed, unsupported, or not tested. Separate robust architecture-level findings from hypothesis-generating candidate signals.

**Evidence status**: Planned; should be updated late in drafting.

## Optional Figure 7: Population-Genetic Supporting Signals

**Purpose**: Include only if modern analysis adds controlled, interpretable evidence.

**Content**: Region-level differentiation or selection summaries with strict caveats, plus candidate-locus inspection only for replicated signals.

**Evidence status**: Decision pending.
