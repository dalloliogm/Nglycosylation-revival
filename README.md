# N-glycosylation Pathway Evolution

This repository revisits the 2012 BMC Evolutionary Biology N-glycosylation pathway paper as historical context for a modern project on evolutionary architecture in biological pathways.

The working hypothesis is that biological systems can spatially organize robustness and evolvability: conserved upstream N-glycosylation machinery should show stronger constraint and severe disease burden, while downstream branching and terminal modification may tolerate more variation and interact more directly with environmental, immune, and tissue-specific pressures.

## Current Milestone

Use `STUDY.md` as the live execution tracker. It should be updated whenever a task is started, completed, blocked, or re-scoped.

Current priorities:

1. Expand the literature matrix and extract structured notes from high-priority papers.
2. Draft the paper thesis in `docs/concept/paper-thesis.md`.
3. Define pathway-curation rules.
4. Build a machine-readable N-glycosylation gene table with stable IDs, coordinates, pathway class, and evidence source.
5. Run the first constraint and disease-architecture analyses.

Key planning files:

- `STUDY.md`: live task tracker and progress log.
- `docs/concept/project-plan.md`: full project plan.
- `docs/concept/literature-search-plan.md`: literature-search protocol.
- `docs/concept/literature-matrix.tsv`: structured bibliography and evidence matrix.
- `docs/concept/concept-memo.md`: short conceptual framing.
- `docs/methods/analysis-plan.md`: initial analysis principles.

## Repository Layout

- `STUDY.md`: live project checklist and decision tracker.
- `data/`: raw, external, interim, and processed datasets.
- `docs/`: concept notes, original-paper context, methods decisions, and manuscript drafts.
- `notebooks/`: exploratory analyses that should call reusable scripts where possible.
- `results/`: generated figures, tables, and reports.
- `scripts/`: repeatable command-line analyses and data transformations.
- `src/`: package code if scripts grow into reusable modules.
- `workflow/`: workflow definitions such as Snakemake, Nextflow, or Make targets.
