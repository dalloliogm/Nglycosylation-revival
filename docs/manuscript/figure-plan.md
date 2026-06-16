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

## Figure 3: Constraint, Essentiality, and Cell-Viability Gradient

**Purpose**: Test whether the catastrophic-core prediction is visible in functional intolerance even when simple coding-constraint metrics are mixed.

**Content**: Gene-level LOEUF and missense Z by pathway region, paired with DepMap CRISPR gene-effect summaries. Include the covariate-controlled DepMap result as an inset or caption statistic: downstream-diversification coefficient remains negative after expression, tissue-specificity, gene-length, and paralog controls.

**Evidence status**: Core result available. Existing constraint figures are `results/figures/constraint_gradient.*`; DepMap expression/essentiality first-pass figure is `results/figures/interface_expression_profile.*`; regression output is `results/tables/interface_essentiality_regression_results.txt`. Needs final main-text visual composition.

## Figure 4: Disease and Trait Architecture Gradient

**Purpose**: Test severe Mendelian burden upstream versus complex/context-dependent trait and glycan-output evidence downstream.

**Content**: Region-level burden of CDG/Mendelian disease, ClinVar pathogenic evidence, GWAS/trait categories, and IgG/plasma glycome locus layer separated by evidence confidence.

**Evidence status**: Existing disease architecture figure available at `results/figures/disease_architecture.*`; glycome and GWAS-null outputs are available in `results/tables/`. Needs final update if IgG locus partitioning is promoted to a panel.

## Figure 5: Interface Trait and Tissue Profile

**Purpose**: Show whether downstream/interface regions are enriched for immune, infection, inflammation, cancer, microbiome, barrier-tissue, or tissue-identity signals.

**Content**: Heatmap or dot plot of trait categories and expression/tissue features by pathway region. Expression tau can be shown as context-deployment support; first-pass barrier/immune bulk-tissue proxy ratios should be visually de-emphasized or left to supplement because they are weak.

**Evidence status**: Expression/essentiality outputs are available. A combined interface trait profile is still pending.

## Figure 6: Evidence Matrix

**Purpose**: Keep interpretation disciplined.

**Content**: Rows as predictions; columns as evidence streams. Cells distinguish supported, mixed, unsupported, or not tested. Separate robust architecture-level findings from hypothesis-generating candidate signals.

**Evidence status**: Planned; should be updated late in drafting.

## Optional Figure 7: Population-Genetic Supporting Signals

**Purpose**: Present population genetics as null/exploratory context, not as a primary support layer.

**Content**: Region-level differentiation or selection summaries with strict caveats. Candidate-locus inspection should be included only as hypothesis-generating context.

**Evidence status**: FST/PBS/iHS outputs are available and mostly null. Include only if the final manuscript needs continuity with the 2012 paper or a transparent negative result.
