# Comparator Pathways — Methods and Curation

Date drafted: 2026-06-09

Decision: Include 1–3 lightweight comparator pathways as a specificity-check module.
The comparators test whether the N-glycosylation architecture (severe disease
concentrated upstream, glycan/interface traits downstream) is specific to pathways
with a catastrophic shared core followed by an organism-environment interface layer,
or whether it appears generically in any well-studied pathway.

---

## Design Principles

A good comparator pathway for this paper:

1. Has a **strongly ordered linear or quasi-linear core** — each step depends on the
   output of the previous, minimising redundancy at the core.
2. Has **clear disease-gene annotation** — Mendelian disease genes are known and
   interpretable as pathway-position effects.
3. Has a **downstream region with qualitatively different biology** from the core —
   ideally including interface-facing, tissue-specific, or environmentally-responsive
   outputs, OR (as a negative control) a pathway that is uniformly catastrophic with
   no interface layer.
4. Has **enough human genes** for the analysis (~10–30) without being so large that
   curation becomes a major project.

The comparator analysis applies a **lightweight version** of the same analytical
framework as N-glycosylation: gene classification, architecture features, constraint
gradient, and disease burden by pathway region. It does not require a full GWAS or
pop-gen analysis.

---

## Selected Comparators

### Comparator 1: Heme Biosynthesis (primary comparator)

**Rationale:** Heme biosynthesis is a compact, sequential, 8-enzyme pathway from
succinyl-CoA + glycine to heme. It is one of the best-characterized ordered metabolic
pathways in human biology. Partial enzymatic defects cause porphyrias, each with a
distinct phenotype that often reflects accumulation of the toxic intermediate upstream
of the block. This makes it a useful contrast to N-glycosylation: it has a clear
catastrophic-sensitivity logic (accumulation of porphyrin intermediates is toxic) but
NO downstream combinatorial or organism-environment interface layer analogous to
N-glycosylation's glycan-output layer.

Expected architecture under the model:
- Severe disease burden should be high throughout the pathway (every block is
  pathogenic), not concentrated in one half.
- There should be no glycome-type or immune/interface GWAS enrichment downstream.
- Coding constraint should be moderate to high throughout.

If the N-glycosylation architecture is specific to pathways with an interface layer,
heme biosynthesis should NOT show the same upstream/downstream disease separation.

**Genes (8 core enzymes):**

| Symbol | Role | Pathway step | Disease |
|---|---|---|---|
| ALAS1 | 5-aminolevulinate synthase 1 (ubiquitous) | Step 1: ALA synthesis | X-linked sideroblastic anemia (ALAS2 form) |
| ALAS2 | 5-aminolevulinate synthase 2 (erythroid) | Step 1: ALA synthesis (RBC) | X-linked sideroblastic anemia |
| ALAD | ALA dehydratase | Step 2: porphobilinogen synthesis | ALA dehydratase-deficient porphyria |
| HMBS | Hydroxymethylbilane synthase | Step 3: hydroxymethylbilane | Acute intermittent porphyria |
| UROS | Uroporphyrinogen III synthase | Step 4: uroporphyrinogen III | Congenital erythropoietic porphyria |
| UROD | Uroporphyrinogen decarboxylase | Step 5: coproporphyrinogen III | Porphyria cutanea tarda; HEP |
| CPOX | Coproporphyrinogen oxidase | Step 6: protoporphyrinogen IX | Hereditary coproporphyria |
| PPOX | Protoporphyrinogen oxidase | Step 7: protoporphyrin IX | Variegate porphyria |
| FECH | Ferrochelatase | Step 8: heme | Erythropoietic protoporphyria |

Additional: UROS and UROD are not strictly sequential in the same sense (both act on
the uroporphyrinogen ring); ALAS1 vs ALAS2 is a tissue-specificity split, not a
pathway branch.

For the comparator analysis:
- All 9 genes are classified as "core_sequential" — there is no downstream
  interface layer to contrast with.
- The expected finding is that severe disease burden is present at nearly every step.

**Source:** OMIM porphyria entries; Reactome R-HSA-189451 (Heme biosynthesis).

---

### Comparator 2: Coenzyme Q / Ubiquinone Biosynthesis (secondary; conditional)

**Rationale:** CoQ biosynthesis is a mitochondrial pathway of ~10–12 human enzymes
(COQ2–COQ9, PDSS1, PDSS2, COQ7) that synthesises the isoprenoid tail and
benzoquinone ring of ubiquinone. All known human disease-causing variants cause
primary CoQ deficiency, usually presenting as severe, early-onset mitochondrial
disease. Like heme, it lacks an interface output layer. Unlike heme, some of the
later ring-modification enzymes (COQ5, COQ6, COQ7) are less well-characterised
disease genes and may show lower clinical penetrance — making it a useful secondary
comparator with slight downstream-tolerance variation.

**Include if:** heme comparator is insufficient to distinguish N-glycosylation's
interface-layer architecture from a generic pathway effect.

**Genes (provisional):** PDSS1, PDSS2, COQ2, COQ3, COQ4, COQ5, COQ6, COQ7,
COQ8A (ADCK3), COQ8B (ADCK4), COQ9, COQ10A, COQ10B (~13 genes).

---

## Analysis Plan for Each Comparator

For each comparator pathway, apply the same lightweight pipeline as N-glycosylation:

1. **Gene curation**: collect gene list from Reactome + OMIM/NCBI Gene; assign
   pathway-step order and a region label (for heme: all "core_sequential"; for CoQ:
   "core_sequential" or "late_ring_modification").
2. **Architecture features**: pathway step order, catastrophic-potential prior,
   disease gene status.
3. **Constraint**: join to gnomAD v4.1 constraint metrics (same script as
   `build_nglyco_constraint_summary.py`, parameterised for a different gene list).
4. **Disease burden**: join to the same CDG/ClinVar/GWAS Catalog tables already
   built for N-glycosylation; count by pathway step.
5. **Region summary**: summarise gene-level constraint and disease metrics; compare
   descriptively across pathway positions.

The lightweight comparator analysis does NOT require:
- Full pathway edge table
- Network visualization
- GWAS candidate audit
- Pop-gen analysis

These analyses are reserved for N-glycosylation unless a result is striking enough
to justify expansion.

---

## Planned Outputs

- `docs/methods/comparator-pathways.md` (this file)
- `data/processed/comparator_gene_table.tsv` — gene table for all comparators
- `data/processed/comparator_constraint_metrics.tsv`
- `data/processed/comparator_disease_annotations.tsv`
- `results/tables/comparator_architecture_summary.tsv`
- `results/figures/comparator_constraint_gradient.*`
- `results/figures/comparator_disease_architecture.*`
- `results/reports/comparator-interpretation.md`

---

## Claim Limits

- Comparator pathways are included as a specificity check, not as a second major
  finding. If the N-glycosylation architecture pattern does not replicate, that is
  informative but does not invalidate the N-glycosylation case study.
- Heme biosynthesis is expected to differ from N-glycosylation; if it shows a
  similar pattern, that would require explanation.
- Do not over-interpret small-n comparisons (heme has 9 genes).
- Comparator analyses use the same claim-level framework as the main analysis.
