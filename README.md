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

## Agentic Workflow Commands

The repository includes a lightweight Makefile interface for running the paper's agentic workflow checks from the local workspace.

```bash
make agentic-inspect
```

Prints the full agentic workflow registry: the available research-agent roles, their expected inputs and outputs, the quality gates, and the current near-term backlog. Use this when you want to understand how the paper implementation is organized.

```bash
make agentic-check
```

Runs a basic validation pass. It compiles `scripts/inspect_agentic_system.py` and then runs the inspector against `workflow/agentic_paper_system.json`. Use this after editing the agent registry, Makefile, or inspector script.

```bash
make agentic-next
```

Prints only the near-term backlog section from the registry inspection. Use this when you want to choose the next ready agentic work unit without reading the full registry output.

```bash
make agentic-prompt
```

Creates a ready-to-paste Codex prompt for the first ready incomplete backlog task. This is the bridge from workflow metadata to actual work: paste the generated prompt into Codex, and Codex should act as the specified research agent, read the required inputs, create the expected outputs, run validation, update `STUDY.md`, and commit the work unit.

```bash
make agentic-prompt TASK=draft_paper_thesis
```

Creates a Codex prompt for a specific backlog task. Use the task ids shown by `make agentic-next`.

## Repository Layout

- `STUDY.md`: live project checklist and decision tracker.
- `data/`: raw, external, interim, and processed datasets.
- `docs/`: concept notes, original-paper context, methods decisions, and manuscript drafts.
- `notebooks/`: exploratory analyses that should call reusable scripts where possible.
- `results/`: generated figures, tables, and reports.
- `scripts/`: repeatable command-line analyses and data transformations.
- `src/`: package code if scripts grow into reusable modules.
- `workflow/`: workflow definitions such as Snakemake, Nextflow, or Make targets.
