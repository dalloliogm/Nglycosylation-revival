# Argument Blueprint

ARS workflow: `academic-paper` Phase 3, Argument Builder output.

## Central Thesis

This paper argues that N-glycosylation is a useful case study for a broader pathway-architecture principle: biological systems may localize robustness near catastrophic core machinery while localizing evolvability in downstream, branching, tissue-specific, and organism-environment interface layers. The claim should be tested through convergent evidence from pathway topology, constraint, disease architecture, standing variation, tissue/trait associations, and, only if useful, modern population-genetic signals.

## Sub-Arguments

### Sub-Argument 1: N-glycosylation has a biologically meaningful upstream-to-downstream architecture.

- **Evidence**: Pathway curation separates precursor synthesis, OST transfer, ER quality control, Golgi branching, terminal modification, and interface-facing glycan diversification.
- **Evidence**: Core glycobiology sources describe upstream N-glycosylation as linked to protein folding, ER quality control, and conserved glycoprotein maturation.
- **Reasoning**: A robustness/evolvability hypothesis requires a real functional gradient, not an arbitrary gene split. If the pathway regions map to different biochemical roles and failure consequences, region-level evolutionary predictions become meaningful.
- **Counter-argument**: Region labels may be subjective, database-dependent, or sensitive to multifunctional genes.
- **Rebuttal**: Use documented classification rules, database cross-checks, ambiguity flags, primary/sensitivity gene sets, and alternative region-label sensitivity analyses.
- **Argument Strength**: Strong in concept; requires completion of database cross-checks before being manuscript-ready.

### Sub-Argument 2: Upstream and checkpoint regions should show stronger constraint and severe disease burden because perturbations have catastrophic pathway consequences.

- **Evidence**: ER N-glycosylation and quality-control literature links upstream machinery to folding surveillance and glycoprotein maturation.
- **Evidence**: CDG and clinical genetics sources can test whether severe Mendelian disease burden concentrates in core or checkpoint regions.
- **Evidence**: Modern constraint metrics can test depletion of tolerated damaging variation.
- **Reasoning**: If core pathway failure disrupts many proteins or essential folding processes, damaging variation should be selected against and surviving pathogenic mutations should more often present as rare severe disease.
- **Counter-argument**: Disease-gene discovery is biased toward severe early-onset phenotypes and well-studied genes.
- **Rebuttal**: Separate disease ascertainment from constraint evidence, use multiple data streams, and explicitly model/report annotation intensity where feasible.
- **Argument Strength**: Strong if constraint and disease gradients align; currently a testable prediction, not a conclusion.

### Sub-Argument 3: Downstream branching and terminal modification genes are plausible evolvability/interface zones rather than simply weakly constrained enzymes.

- **Evidence**: Glycan interface literature links cell-surface glycans to host-pathogen interaction, immune modulation, inflammation, tissue identity, cancer biology, and glycoprotein signaling.
- **Evidence**: IgG glycosylation and glycoimmunology studies provide trait-level examples where glycosylation variation has immune and inflammatory relevance.
- **Reasoning**: Downstream glycan-processing machinery affects structures exposed to ecological, microbial, immune, and tissue-specific contexts. That makes downstream variation more likely to be tolerated, conditionally useful, or trait-modifying than upstream disruption.
- **Counter-argument**: Interface biology does not prove adaptation or evolvability for each downstream gene.
- **Rebuttal**: Avoid universal or adaptive claims. Test for enrichment of tolerated variation, tissue specificity, and trait categories, and describe results as architecture-level patterns.
- **Argument Strength**: Moderate to strong; needs gene-level trait and expression evidence.

### Sub-Argument 4: Population-genetic signals should be optional supporting evidence, not the manuscript's foundation.

- **Evidence**: The 2012 paper provides the historical hypothesis but used older data and methods vulnerable to demography, LD, SNP-array ascertainment, and window-assignment artifacts.
- **Evidence**: Modern selection-scan literature emphasizes interpretive caution and population-structure controls.
- **Reasoning**: A robust architecture paper can stand on pathway definition, constraint, disease, and trait evidence. Population genetics should be included only if it adds controlled, interpretable support.
- **Counter-argument**: Removing population genetics may weaken continuity with the original paper.
- **Rebuttal**: Preserve the original paper as historical context, then explain that the stronger modern contribution is a multi-evidence architecture framework.
- **Argument Strength**: Strong as a design principle.

### Sub-Argument 5: Generalization beyond N-glycosylation requires either comparator pathways or careful limitation.

- **Evidence**: Robustness/evolvability theory predicts general principles, but a single pathway cannot establish universality.
- **Evidence**: Comparator-pathway planning has identified possible constrained-core and adaptive-interface examples.
- **Reasoning**: The paper can either make a modest case-study claim or include a lightweight comparator analysis to support broader architecture claims.
- **Counter-argument**: Comparator pathways may expand scope too much and delay the first manuscript.
- **Rebuttal**: Treat comparator analysis as a decision point. If omitted, phrase generalization as a research program and include comparators in future work.
- **Argument Strength**: Adequate until the comparator decision is made.

## Logical Flow

1. **Problem**: Biology needs both robustness and evolvability, but the spatial organization of these properties within pathways is under-tested.
2. **Model**: Pathways may localize catastrophic core functions away from evolvable interface functions.
3. **Case**: N-glycosylation has a functional upstream/downstream architecture suitable for testing this model.
4. **Predictions**: Upstream/core regions should show constraint and severe disease; downstream/interface regions should show tolerated variation and context-dependent trait links.
5. **Tests**: Curated pathway graph, constraint metrics, disease annotations, tissue/trait profiles, and optional modern population-genetic evidence.
6. **Synthesis**: If multiple evidence streams align, N-glycosylation supports a pathway-architecture model; if not, the result narrows or falsifies the model.
7. **Boundary**: The paper should claim support for a testable architecture framework, not proof of adaptation at specific loci.

## Argument Strength Assessment

| Sub-Argument | Evidence Strength | Logic Validity | Counter-Arg Risk |
|--------------|-------------------|----------------|------------------|
| Functional pathway architecture | Strong but still needs database cross-checks | Valid | Medium |
| Upstream constraint and severe disease | Potentially strong; empirical tests pending | Valid | Medium |
| Downstream interface/evolvability layer | Moderate; needs trait/expression integration | Qualified | Medium |
| Population genetics as optional support | Strong | Valid | Low |
| Generalization beyond case study | Adequate until comparator decision | Qualified | High |

## Notes for Draft Writer

- Use cautious evidence language: "consistent with", "supports", "candidate", "hypothesis-generating", and "testable model".
- Do not imply that all downstream variation is adaptive.
- Do not let individual gene examples replace architecture-level tests.
- Keep substrate biosynthesis genes analytically separate unless a specific analysis justifies inclusion.
- Make the original 2012 paper part of the introduction and motivation, not the methodological center.
- Include a claims register before drafting results so the manuscript keeps evidence, inference, and speculation separate.
