# N-glycosylation Pathway Evolution

This repository revisits the 2012 BMC Evolutionary Biology N-glycosylation pathway paper as historical context for a modern project on evolutionary architecture in biological pathways.

The working hypothesis is that biological systems can spatially organize robustness and evolvability: conserved upstream N-glycosylation machinery should show stronger constraint and severe disease burden, while downstream branching and terminal modification may tolerate more variation and interact more directly with environmental, immune, and tissue-specific pressures.

## Current Milestone

1. Preserve and critique the original paper in `docs/original-paper/`.
2. Draft the core concept memo in `docs/concept/`.
3. Build a machine-readable gene table with stable IDs, coordinates, pathway class, and evidence source.
4. Define the multi-evidence analysis plan before running large-scale scans.

Start with the full project plan in `docs/concept/project-plan.md`.

## Repository Layout

- `data/`: raw, external, interim, and processed datasets.
- `docs/`: concept notes, original-paper context, methods decisions, and manuscript drafts.
- `notebooks/`: exploratory analyses that should call reusable scripts where possible.
- `results/`: generated figures, tables, and reports.
- `scripts/`: repeatable command-line analyses and data transformations.
- `src/`: package code if scripts grow into reusable modules.
- `workflow/`: workflow definitions such as Snakemake, Nextflow, or Make targets.
