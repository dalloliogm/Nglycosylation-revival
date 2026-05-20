# AGENTS.md

## Project Mission

This repository is for revisiting and improving the 2012 BMC Evolutionary Biology paper:

> Distribution of events of positive selection and population differentiation in a metabolic pathway: the case of asparagine N-glycosylation

The goal is not to closely reproduce the original analysis. The goal is to use the original paper's base concept as a launch point for a new paper about the evolutionary architecture of biological pathways.

Treat the original paper as historical context and a hypothesis generator. Do not spend effort recreating every original statistic unless doing so directly supports the new argument.

## Scientific Objective

Core question:

Do biological pathways organize robustness and evolvability into different regions, and can N-glycosylation serve as a concrete case study of that architecture?

Deeper framing:

The downstream glycosylation machinery can be treated as an interface layer between organism and environment. Glycans mediate pathogen recognition, microbiome interaction, immune modulation, tissue identity, and cell-surface communication. In that sense, downstream glycosylation may resemble other fast-evolving biological interface systems such as immune receptors, olfactory receptors, and MHC diversification.

The strongest modern version of the project is the hypothesis that biological systems may localize evolvability away from catastrophic failure points. In this framing, the N-glycosylation pathway may physically separate robustness and evolvability:

- Upstream core machinery supports robustness: conserved function, folding quality control, and strong intolerance of damaging perturbation.
- Downstream branching and terminal modification support evolvability: tolerated variation, environmental interaction, and exploration of phenotypic glycan space.

This connects the project to robustness/evolvability theory, modular engineering, fault-tolerant architecture, and layered protocols in computer science. The original paper has the seed of this idea, but does not formalize or test it strongly enough.

Key comparison:

- Upstream genes involved in conserved precursor synthesis, oligosaccharyltransferase activity, ER quality control, and calnexin/calreticulin-related processing.
- Downstream genes involved in Golgi branching, glycan diversification, terminal modification, host interaction, and cell-surface variation.
- Substrate biosynthesis genes should be handled separately unless there is a clear reason to include them in either pathway half.

Clinical architecture hypothesis:

- Upstream mutations should be enriched for rare, severe Mendelian disease and strong constraint, as in many Congenital Disorders of Glycosylation.
- Downstream variation should more often contribute to subtler quantitative phenotypes, including immunity, inflammation, cancer, autoimmune risk, infection susceptibility, tissue identity, and host-microbiome interactions.
- Treat this as a testable hypothesis, not a conclusion.

## What To Avoid

Do not let the project collapse back into a narrow population-genetics reanalysis. Population differentiation and selection scans may be useful evidence, but they are not the paper's center of gravity.

Do not overinterpret genomic outlier statistics as demonstrated adaptation. Use language such as "candidate signal", "outlier", "consistent with", or "hypothesis-generating" unless there is functional or fine-mapping evidence.

Specific issues to address:

- Continental groupings are crude and confounded by demography.
- One-vs-rest FST can conflate local differentiation, drift, bottlenecks, and sampling structure.
- Fixed windows around genes can assign signals to the wrong gene.
- Fisher combination of SNP p-values is fragile under LD.
- iHS detects only a subset of recent incomplete sweeps and is sensitive to phasing, SNP ascertainment, recombination, and demography.
- Pathway-level enrichment needs careful control for gene length, SNP density, recombination, background selection, constraint, expression, and local genomic context.
- Network centrality claims need stronger justification, sensitivity analysis, and preferably modern pathway representations.
- Candidate genes require regional inspection, nearby-gene annotation, and cross-dataset replication before biological storytelling.
- The original paper's conceptual idea is stronger than the evidence presented: it lacks formal robustness/evolvability modeling, quantitative systems biology, generalization beyond one pathway, and modern disease/functional integration.

## Analysis Standards

Every analysis should be reproducible from scripts or notebooks committed to the repository. Prefer parameterized scripts for final analyses and notebooks for exploration.

For each result, record:

- Dataset version and source URL or accession.
- Genome build and coordinate system.
- Sample inclusion/exclusion criteria.
- Population labels and grouping rationale.
- Variant filters.
- Gene list version and pathway source.
- Window or regulatory-region definition.
- Statistical method and software version.
- Multiple-testing correction.
- Sensitivity analyses.

Avoid hidden manual steps. If a manual curation step is needed, save the curated table and document the decision rule.

## Recommended Repository Structure

Use this structure unless there is a strong reason to change it:

```text
.
├── AGENTS.md
├── README.md
├── data/
│   ├── raw/                 # downloaded immutable inputs; preferably gitignored if large
│   ├── external/            # external annotations and reference tables
│   ├── interim/             # intermediate generated tables
│   └── processed/           # final analysis-ready datasets
├── docs/
│   ├── concept/             # central hypothesis, figures, paper framing
│   ├── original-paper/      # source PDF, notes, critique, minimal historical context
│   ├── methods/             # methodological notes and design decisions
│   └── manuscript/          # revised paper drafts
├── notebooks/               # exploratory notebooks
├── results/
│   ├── figures/
│   ├── tables/
│   └── reports/
├── scripts/                 # reusable command-line scripts
├── src/                     # package code if the project grows beyond scripts
└── workflow/                # Snakemake/Nextflow/Makefile workflow definitions
```

Large raw genotype files should normally not be committed. Put download instructions, checksums, and expected paths in `docs/methods/` or `data/README.md`.

## Candidate Modern Data Sources

Prioritize open, well-documented datasets:

- 1000 Genomes Project high-coverage variant calls.
- HGDP/SGDP modern releases, if accessible and license-compatible.
- gnomAD population allele frequencies for broad validation, with caution about ascertainment and cohort structure.
- Ensembl, GENCODE, NCBI Gene, Reactome, GlyGen, Gene Ontology, and UniProt for gene annotation.
- Recombination maps, background selection maps, constraint metrics, and expression resources such as GTEx where relevant.

Use the original HGDP SNP-array data only if it helps explain where the idea came from. It is not a required analysis pillar.

## Methods To Consider

Concept-first analysis:

- Start by formalizing the robustness/evolvability hypothesis into measurable predictions.
- Define pathway regions as conserved core, processing/checkpoint layer, diversification layer, and environmental interface layer.
- Build evidence across orthogonal data types rather than relying on any single statistic.
- Prefer analyses that test architecture: constraint gradients, disease gradients, network position, pathway depth, redundancy, tissue specificity, and trait association profiles.

Population differentiation:

- Pairwise FST rather than only one-vs-rest.
- PBS or related branch-specific statistics where appropriate.
- Population structure-aware modelling rather than hard continental bins where possible.

Selection scans:

- iHS for incomplete sweeps, but replicate with alternatives such as nSL, XP-EHH, XP-CLR, PBS, singleton-density or allele-frequency spectrum methods where appropriate.
- Separate SNP-level, region-level, and gene-set-level claims.
- Include neutral matched controls and local genomic covariates.

Gene/pathway enrichment:

- Matched null sets by gene length, SNP density, recombination rate, B-statistic/background selection, mutation rate proxy, expression breadth, and mappability if possible.
- Permutation or resampling approaches over naive count tests.
- Sensitivity to gene boundary definitions: exons only, gene body, promoter, ±10 kb, ±50 kb, ±100 kb, candidate regulatory regions.

Network analysis:

- Rebuild the pathway graph from current Reactome/GlyGen/curated sources.
- Treat centrality as exploratory unless sample size and null model are convincing.
- Test whether centrality results survive alternative graph encodings.
- Consider richer graph/system features beyond centrality: pathway depth, redundancy, alternative routes, reaction reversibility, substrate/product branching, controllability, flux relevance, essentiality, tissue specificity, and proximity to quality-control checkpoints.

Modern computational biology angle:

- Test whether graph topology, redundancy, flux structure, tissue specificity, essentiality, disease burden, and evolutionary conservation can predict evolutionary regime.
- Consider graph-learning models only after building strong baseline models. A possible future target is a model that predicts whether a node belongs to a conserved core, adaptive periphery, innovation zone, or catastrophic constraint zone.
- If using GNNs or other machine-learning models, include simple baselines, strict train/test separation across pathways, interpretability checks, and uncertainty estimates.

Functional interpretation:

- For each candidate locus, inspect regional LD, nearby genes, regulatory annotations, known GWAS/ClinVar/OMIM associations, eQTLs, and glycosylation-related evidence.
- Do not claim a population-specific glycosylation phenotype without direct or strongly linked evidence.

Disease architecture:

- Compare upstream and downstream genes using constraint metrics, ClinVar/OMIM disease annotations, GWAS Catalog associations, burden of rare damaging variants, pLI/LOEUF or current equivalent metrics, and known Congenital Disorders of Glycosylation genes.
- Explicitly test whether severe Mendelian disease burden concentrates upstream while complex-trait or regulatory associations are more common downstream.

## First Milestone

Create a reproducible project skeleton and concept note:

1. Preserve the original PDF and write a short critique/context note in `docs/original-paper/`.
2. Draft a concept memo in `docs/concept/` that states the paper thesis, competing hypotheses, predictions, and target figure set.
3. Create a machine-readable gene table with stable IDs, symbols, coordinates, pathway class, and evidence source.
4. Define the modernized multi-evidence analysis plan before running large-scale scans.

Second milestone:

Formalize the robustness/evolvability hypothesis as measurable predictions:

1. Upstream genes should show stronger evolutionary constraint and higher severe Mendelian disease burden.
2. Downstream genes should show greater tolerated standing variation, more population differentiation where robustly replicated, and richer links to immune/environmental quantitative traits.
3. Network locations with high catastrophic potential should be depleted for tolerated variation.
4. Network regions with redundancy, branching, and tissue-specific deployment should be enriched for innovation-zone signals.

## Working Conventions

- Use `rg`/`rg --files` for local search.
- Use scripts for repeatable transformations; notebooks may call scripts but should not become the only source of truth.
- Keep generated results out of version control if they are large or trivially reproducible.
- Commit small, reviewable changes.
- Write methods notes while decisions are being made, not after the fact.
- Prefer clear negative results over weak adaptive narratives.
