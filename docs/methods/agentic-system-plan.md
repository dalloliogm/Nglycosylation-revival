# Agentic System Plan

## Purpose

The paper should be implemented as a supervised agentic research system, not as one autonomous agent that writes a manuscript end to end. The system should decompose the project into explicit research roles, durable artifacts, quality gates, and handoff rules. Each agent should leave evidence in the repository so another agent or human reviewer can audit the work.

The central design constraint is scientific discipline: the system must protect the project from overclaiming adaptation, weak pathway labels, undocumented data choices, and manuscript drift toward a list of interesting genes.

## System Shape

Use a controller plus specialist agents.

- Controller: reads `STUDY.md`, selects the next task, checks prerequisites, and refuses to advance when gates are incomplete.
- Literature agent: expands `docs/concept/literature-matrix.tsv`, extracts evidence fields, and separates conceptual, empirical, and methods papers.
- Hypothesis agent: turns the robustness/evolvability framing into falsifiable predictions, claims, counterclaims, and reviewer risks.
- Pathway-curation agent: maintains the gene table, pathway-region labels, edge tables, aliases, evidence sources, and ambiguous-gene flags.
- Data-provenance agent: records dataset versions, source URLs, genome builds, filters, and access dates before analysis starts.
- Analysis agents: run focused analyses for architecture metrics, constraint, disease burden, tissue/trait profiles, and optional population genetics.
- Critic agent: reviews every result against the original-paper failure modes and checks whether the claim level matches the evidence.
- Manuscript agent: drafts only from approved artifacts, maintaining a claims register and figure-to-evidence mapping.

The controller should not invent results. It should only coordinate tasks, inspect artifact status, and propose the next executable unit of work.

## Artifact Contracts

Every agent should read and write through stable files:

- `STUDY.md`: authoritative task state and changelog.
- `docs/concept/literature-matrix.tsv`: structured bibliography and evidence matrix.
- `docs/concept/paper-thesis.md`: thesis, competing hypotheses, and predictions.
- `docs/concept/claims-register.md`: what the paper shows, suggests, and does not show.
- `data/processed/nglyco_gene_table.tsv`: curated gene list and pathway-region labels.
- `data/processed/nglyco_gene_gene_edges.tsv`: current graph representation.
- `docs/methods/*.md`: methods decisions, data provenance, and sensitivity plans.
- `results/tables/*.tsv`: machine-readable analysis outputs.
- `results/figures/*`: regenerated figures.
- `docs/manuscript/*`: manuscript outline, argument blueprint, figures, and drafts.

Generated claims must trace back to at least one machine-readable table or cited literature row. A manuscript section should not introduce new evidence that is absent from the artifact set.

## Execution Loop

1. Inspect `STUDY.md` and `workflow/agentic_paper_system.json`.
2. Select one task whose prerequisites are satisfied and whose output is missing or stale.
3. Read only the artifact files needed for that task.
4. Execute the task with scripts or documented curation rules.
5. Validate the output against the task gate.
6. Update `STUDY.md` with a dated changelog entry.
7. Run the critic gate for claim strength, provenance, and reproducibility.
8. Commit the small completed unit.

The default unit of work should be small enough to review in one commit: one curation pass, one methods note, one analysis table, one figure, or one manuscript section.

## Quality Gates

### Gate 1: Concept

Before large analyses, the project must have a paper thesis, competing hypotheses, predictions, and a claims register.

### Gate 2: Curation

Before analysis, the primary gene table must record stable identifiers, pathway class, evidence source, coordinate source, and ambiguity flags.

### Gate 3: Provenance

Before using any dataset, a methods note must record version, source URL or accession, genome build, inclusion criteria, filters, and access date.

### Gate 4: Analysis

Every analysis must produce a machine-readable table, a short methods note, and a sensitivity or limitation statement. Statistical outputs should emphasize effect sizes and uncertainty.

### Gate 5: Critic

Before manuscript drafting, a critic pass must check that each claim is labeled as demonstrated, supported, consistent with, hypothesis-generating, or speculative.

### Gate 6: Manuscript

Drafting can proceed only from approved artifacts. Any unsupported claim should either be downgraded, moved to limitations, or converted into a future-test statement.

## Near-Term Implementation

The first practical implementation should be lightweight:

1. Use `workflow/agentic_paper_system.json` as the agent and gate registry.
2. Use `scripts/inspect_agentic_system.py` to summarize agents, artifacts, gates, and next actions.
3. Add task-specific scripts only when an analysis becomes repeatable.
4. Keep manual curation allowed, but require a saved table and documented decision rule.

This avoids premature orchestration infrastructure. A Snakemake, Nextflow, or database-backed controller should wait until the repository has several repeatable analyses.

## First Agentic Sprint

The next sprint should create the paper-control artifacts:

1. Draft `docs/concept/paper-thesis.md`.
2. Draft `docs/concept/claims-register.md`.
3. Draft `docs/methods/architecture-metrics.md`.
4. Cross-check `data/processed/nglyco_gene_table.tsv` identifiers and pathway classes.
5. Define the first constraint-analysis dataset and provenance note.

After this sprint, analysis agents can start generating architecture and constraint tables without leaving the conceptual frame underspecified.
