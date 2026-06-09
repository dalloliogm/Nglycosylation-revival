# Conservation Analysis

Date drafted: 2026-06-08

Agentic work unit: `build_conservation_metrics`

Agent role: `data_provenance_agent`

## Purpose

This note defines the cross-species evolutionary conservation and human population
differentiation evidence streams to be added to the N-glycosylation architecture
analysis. The goal is to test whether pathway-region predicts evolutionary constraint
across timescales, and whether downstream/terminal genes carry signals consistent with
adaptive diversification or relaxed purifying selection.

Primary future outputs:

- `data/processed/nglyco_conservation_metrics.tsv`
- `results/tables/conservation_join_audit.tsv`
- `results/tables/conservation_summary.tsv`
- `results/reports/conservation-interpretation.md`

Primary inputs:

- `data/processed/nglyco_gene_table.tsv`
- `data/processed/nglyco_architecture_features.tsv`

---

## Tier 1: Cross-Species Evolutionary Conservation

### 1a. dN/dS — Ensembl Comparative Genomics

**Metric**: dN/dS ratio (also called Ka/Ks) for the canonical human transcript relative
to the one-to-one ortholog in each target species.

**Target species for primary analysis**:
- *Mus musculus* (mouse) — primary target; diverged ~90 Mya; dense functional data.
- *Pan troglodytes* (chimpanzee) — secondary target; diverged ~6 Mya; detects very
  recent relaxation.

**Data source**: Ensembl REST API, comparative genomics endpoint.

```
GET https://rest.ensembl.org/homology/id/{ensembl_gene_id}
    ?target_species={species}
    ;type=orthologues
    ;content-type=application/json
```

Access date: to be recorded at run time.

Ensembl release: to be recorded at run time (check `/info/software`).

**Processing rules**:
- Use one-to-one orthologues only (`type == "ortholog_one2one"`). Many-to-one or
  one-to-many relationships involve paralog contamination and should not be mixed into
  the primary dN/dS summary.
- If multiple transcripts are returned, select the entry matching the canonical
  transcript if available; otherwise take the entry with the lowest `dn_ds`.
- A `dn_ds` value of `null` or `None` in the Ensembl response means no synonymous
  substitutions were detected (dS ≈ 0) or the alignment was insufficient. Record as
  missing rather than zero or infinity.
- Record `dn_ds_missing_reason` for any gene without a valid value.
- A `dn_ds > 1` is theoretically consistent with positive selection, but gene-level
  dN/dS is a blunt instrument: averaging over the whole gene and long evolutionary time
  masks site-specific or episodic selection. Do not use gene-level dN/dS > 1 as
  evidence of positive selection in the manuscript.

**Covariates to record**:
- `ortholog_type` (one2one / one2many / many2one)
- `target_species`
- `ensembl_release` at access time

**Claim limit**: dN/dS < 1 confirms purifying selection at the gene level; it does not
localise constraint to specific sites or domains. dN/dS ≈ 1 indicates neutral
evolution on average; it does not rule out local positive selection. Do not interpret
the gradient as a proxy for adaptive evolution without additional evidence.

---

### 1b. PhyloP100 — UCSC 100-Way Vertebrate Conservation

**Metric**: Mean PhyloP score over the gene body (GRCh38 coordinates from the gene
table), computed from the UCSC 100-way vertebrate PhyloP track (`phyloP100way`).

PhyloP scores are log-scale likelihood-ratio scores derived from a PHAST model trained
on a 100-vertebrate multiple alignment. Positive scores indicate evolutionary constraint
(fewer substitutions than expected under neutrality); negative scores indicate
acceleration. The scale is approximately: > 1.0 = moderate constraint; > 2.0 = strong
constraint.

**Data source**: UCSC Genome Browser REST API, bigWig data endpoint.

```
GET https://api.genome.ucsc.edu/getData/track
    ?genome=hg38
    &track=phyloP100way
    &chrom={chr_with_prefix}    # e.g. chr20
    &start={grch38_start}
    &end={grch38_end}
```

Access date: to be recorded at run time.

**Processing rules**:
- Query the full gene body (gene table start/end coordinates). This includes introns
  but is the most practical level of aggregation given the gene table does not contain
  exon-level coordinates.
- Compute: mean, median, minimum, and 5th-percentile PhyloP over all positions
  returned.
- Minimum and 5th-percentile capture whether any coding sub-region is rapidly
  evolving, complementing the mean.
- Positions with missing values in the bigWig (e.g. assembly gaps) should be excluded
  from summary statistics and the fraction of missing positions recorded.
- For very large genes (> 500 kb), the UCSC API response may be large or slow. Apply
  a timeout of 60 s per request and record a `phylop_query_status` flag
  (`ok` / `timeout` / `api_error` / `empty`).
- Record `phylop_positions_total` and `phylop_positions_missing` for traceability.

**Claim limit**: Gene-body PhyloP averages over introns. Transcript- or exon-level
analyses would be more precise but require exon coordinate data not currently in the
gene table. Report this as a gene-body approximation and flag any genes where the
result may be dominated by a large intronic region.

---

## Tier 2: Human Population Differentiation (planned, not yet implemented)

The following analyses are deferred until appropriate pre-computed data sources are
identified and downloaded. See Phase 7 of `STUDY.md` for decision criteria.

### 2a. Pairwise FST across 1000 Genomes Superpopulations

**Metric**: Per-gene maximum or mean pairwise FST across 1000G Phase 3 superpopulations
(AFR, EUR, EAS, SAS, AMR).

**Planned data source**: 1000 Genomes Project Phase 3 population-stratified allele
frequency data, or pre-computed FST summary from the PopHuman database
(https://pophuman.uab.cat/).

**Decision rule**: Include if pre-computed gene-level FST is available for all major
superpopulation contrasts. Do not compute FST from raw VCFs unless pipeline capacity
is confirmed.

### 2b. Selective Sweep Signals (iHS, PBS)

**Metric**: Integrated haplotype score (iHS) and Population Branch Statistic (PBS)
from 1000G Phase 3 phased haplotypes.

**Planned data source**: Pre-computed sweep statistics from a published population
genomics resource (e.g. PopHuman, Ferrer-Admetlla et al. 2014, or equivalent 1000G
Phase 3 scan paper).

**Decision rule**: Include if per-gene summary statistics are available from a
published, peer-reviewed scan. Do not run a primary scan without validation against an
independent method and a matched neutral null. See Phase 7 guidance in `STUDY.md`.

---

## Join Rules

Primary join key: `ensembl_gene_id` from `data/processed/nglyco_gene_table.tsv`.

Cross-check: `symbol` for audit.

Genes missing dN/dS or PhyloP should be recorded in the join audit and excluded from
group comparisons for the affected metric only.

---

## Analysis Plan

1. Join conservation metrics to the architecture feature table.
2. Compare median dN/dS and mean PhyloP across pathway regions, using the same
   upstream-core vs. downstream-diversification primary contrast as the constraint
   analysis.
3. Test sensitivity with `checkpoint_layer` merged into upstream and with
   low-specificity terminal enzymes excluded from downstream.
4. Report median, IQR, and effect sizes (rank-biserial correlation). Do not rely on
   p-values alone.
5. Interpret in conjunction with the constraint gradient result: if dN/dS and PhyloP
   do not separate regions cleanly, the architecture hypothesis relies more heavily on
   disease and trait-layer evidence.

---

## Output Schema

`data/processed/nglyco_conservation_metrics.tsv` columns:

| Column | Description |
|---|---|
| `symbol` | HGNC symbol |
| `ensembl_gene_id` | Ensembl gene ID |
| `primary_region` | Pathway region label |
| `analysis_group` | Coarse hypothesis group |
| `include_primary` | Primary analysis flag |
| `conservation_version` | Version tag for this run |
| `dn_ds_mouse` | dN/dS vs. *M. musculus* (one2one ortholog) |
| `dn_ds_chimp` | dN/dS vs. *P. troglodytes* (one2one ortholog) |
| `dn_ds_mouse_ortholog_type` | Ortholog relationship type |
| `dn_ds_chimp_ortholog_type` | Ortholog relationship type |
| `dn_ds_mouse_missing_reason` | Reason if dN/dS unavailable |
| `dn_ds_chimp_missing_reason` | Reason if dN/dS unavailable |
| `ensembl_release` | Ensembl release used |
| `phylop100_mean` | Mean PhyloP100 over gene body |
| `phylop100_median` | Median PhyloP100 over gene body |
| `phylop100_min` | Minimum PhyloP100 over gene body |
| `phylop100_p5` | 5th percentile PhyloP100 |
| `phylop100_positions_total` | Positions in query window |
| `phylop100_positions_missing` | Positions with no bigWig value |
| `phylop_query_status` | Query status flag |
| `ucsc_access_date` | Date PhyloP data was fetched |
| `conservation_join_status` | Overall join status |
