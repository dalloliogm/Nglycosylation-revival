# Reproducibility Statement

Date: 2026-06-16

This repository contains scripts, curated tables, and generated outputs for the N-glycosylation evolutionary-architecture manuscript. The analysis is reproducible from committed scripts plus external public datasets that are intentionally not committed when large.

## Runtime

The project uses `uv` with dependencies declared in `pyproject.toml`.

Recommended command prefix:

```bash
uv run python <script>
```

The Makefile exposes stable targets for the main reusable analyses:

```bash
make architecture-features
make constraint-summary CONSTRAINT_METRICS=data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv
make constraint-gradient
make constraint-network-plots
make disease-seed-table
make clinvar-disease-layer CLINVAR_VARIANT_SUMMARY=data/external/clinvar/variant_summary.txt.gz
make gwas-trait-layer GWAS_CATALOG_ASSOCIATIONS=data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip
make disease-architecture-plot
make downstream-gwas-audit
make downstream-gwas-locus-review GWAS_CATALOG_ASSOCIATIONS=data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip
make interface-expression-essentiality DEPMAP_GENE_EFFECT=data/external/depmap/CRISPRGeneEffect.csv
make interface-essentiality-regression
```

## Required External Files

These files are excluded from git because of size or because they are re-downloadable external resources.

| Dataset | Expected local path | Used for | Documentation |
| --- | --- | --- | --- |
| gnomAD v4.1 constraint metrics | `data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv` | LOEUF, missense Z, constraint summaries | `data/README.md`; `docs/methods/constraint-analysis.md` |
| ClinVar variant summary | `data/external/clinvar/variant_summary.txt.gz` | Germline pathogenic/likely pathogenic variant counts | `data/README.md`; `docs/methods/disease-annotation.md` |
| GWAS Catalog associations v1.0.2, e115_r2026-06-01 | `data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip` | GWAS trait categories, downstream locus audit, null models | `data/README.md`; `docs/methods/disease-annotation.md` |
| Human Protein Atlas GTEx RNA tissue table | `data/raw/hpa_rna_tissue_gtex.tsv` | Expression breadth, tissue-specificity tau, barrier/immune proxy expression | `data/README.md`; `docs/methods/interface-layer-analysis.md` |
| DepMap CRISPR gene-effect matrix | `data/external/depmap/CRISPRGeneEffect.csv` | Cell-line essentiality and covariate-control analysis | `data/README.md`; `docs/methods/interface-layer-analysis.md` |
| 1000 Genomes Phase 3 population and VCF slices | `data/raw/popgen/` | FST and PBS summaries | `docs/methods/popgen-decision.md` |
| PopHuman iHS BigWigs | fetched/cached by `scripts/extract_pophuman_ihs.py` | iHS summaries | `docs/methods/popgen-decision.md` |

## Generated Outputs

Most files under `data/processed/`, `results/tables/`, `results/figures/`, and `results/reports/` are generated. The repository tracks selected small outputs that are directly referenced by the manuscript or useful for review. Larger or trivially reproducible outputs remain ignored by `.gitignore`.

Primary generated-output map:

- `docs/manuscript/supplementary-table-inventory.md` lists result tables and producing scripts.
- `docs/manuscript/evidence-matrix.md` maps claims to evidence and wording limits.
- `STUDY.md` records task completion and dated changes.

## Network-Dependent Steps

These scripts may require network access and can be slower or intermittently fail:

- `scripts/build_nglyco_conservation_metrics.py`: Ensembl/BioMart/UCSC REST calls.
- `scripts/fetch_popgen_data.py`: coordinate liftover and 1000G VCF fetching.
- `scripts/extract_pophuman_ihs.py`: PopHuman BigWig download.
- `scripts/analyze_loeuf_regression.py`: may fetch HPA GTEx and Ensembl paralog counts if local caches are missing.

For final archival reproducibility, save release IDs, source URLs, access dates, and checksums for the external files above.

## Reproducibility Caveats

- Some analyses depend on public databases that update over time; reruns with newer source versions may change counts.
- GWAS Catalog gene assignments are treated as annotation evidence, not causal locus resolution.
- DepMap CRISPR scores are cancer-cell-line fitness effects, not organismal lethality.
- Population-genetic results are exploratory context and should not be interpreted as demonstrated adaptation.
- Comparator pathways are lightweight specificity checks and not fully matched controls.

## Minimal Review Checklist

Before submission:

1. Re-run all Makefile targets that do not require long network jobs.
2. Re-run or document the latest successful run for network-dependent scripts.
3. Confirm every numerical claim in `docs/manuscript/draft.md` appears in `docs/manuscript/supplementary-table-inventory.md` or `docs/manuscript/evidence-matrix.md`.
4. Add checksums for the required external files.
5. Freeze a repository release or tag after final figures and manuscript text are synchronized.
