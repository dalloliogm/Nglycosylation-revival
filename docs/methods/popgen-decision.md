# Population Genetics Analysis Plan

Date drafted: 2026-06-09

Decision: Include full population-genetics analysis (FST, iHS, PBS) as a supporting
evidence layer in the paper. Pop-gen should not become the paper's center of gravity,
but it can test whether pathway architecture predicts evolutionary differentiation
signals, and it connects the work to the original 2012 paper.

---

## Scope and Framing

Population-genetic signals are treated as a **hypothesis-generating supporting layer**,
not as the paper's primary evidence. The main architecture claims rest on disease
architecture (CDG/ClinVar) and constraint/conservation gradients. Pop-gen adds a third
independent line of evidence asking whether the same pathway regions that are
differentially constrained and disease-enriched also differ in their patterns of
human population differentiation or candidate selection signals.

Claim level: **consistent with / hypothesis-generating**. No pop-gen result in this
analysis will be described as "demonstrated adaptation" or "proven selection event."

---

## Data Sources

### Genotype data
- **1000 Genomes Project Phase 3** (GRCh37/hg19)
  - Release: 20130502
  - Per-chromosome VCFs: `ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/`
  - File pattern: `ALL.chr{N}.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz`
  - Population panel: `integrated_call_samples_v3.20130502.ALL.panel`
  - n ≈ 2504 individuals, 5 superpopulations (AFR, AMR, EAS, EUR, SAS)

### Pre-computed selection statistics
- **PopHuman** (http://pophuman.uab.cat)
  - Build: GRCh37/hg19
  - Statistics: iHS, XP-EHH (selscan), nucleotide diversity, SFS-based tests
  - Window size: 10 kb (accessible genome regions)
  - Download: BigWig/BED format from Resources menu
  - Use: intersect with gene body ± 10 kb to extract per-gene iHS summary
  - **FST and PBS are NOT in PopHuman** — these must be computed

### Coordinate system
- Gene table uses GRCh38. For 1000G/PopHuman work, coordinates must be lifted
  over to GRCh37 using UCSC liftOver or the Ensembl REST liftover endpoint.

---

## Statistics Planned

### FST (Weir & Cockerham)
- Tool: vcftools `--weir-fst-pop`
- Approach: per-variant FST for each pairwise superpopulation contrast
  (AFR-EUR, AFR-EAS, AFR-SAS, EUR-EAS, EUR-SAS, EAS-SAS); then summarise
  per gene as mean/median/max FST across variants in the gene body ± 10 kb
- Populations: all 10 pairwise superpopulation contrasts
- Variant filter: biallelic SNPs, MAF ≥ 0.01 in the pooled sample, PASS filter
- Gene window: gene body + 10 kb flanks (sensitivity: gene body only, ± 50 kb)
- Output: per-gene per-contrast mean FST, max FST, fraction of variants with
  FST > 0.3 (outlier fraction)

### PBS (Population Branch Statistic; Yi et al. 2010)
- Computed from FST values for three-population trios
- Primary trios: (AFR, EUR, EAS), (AFR, EUR, SAS), (AFR, EAS, SAS)
- Formula: PBS_pop = (-log(1 - FST_AB) - log(1 - FST_AC) + log(1 - FST_BC)) / 2
  where B and C are the other two populations
- Output: per-gene PBS for each focal population in each trio

### iHS (integrated haplotype score)
- Source: **PopHuman pre-computed BigWig tracks** (no computation needed)
- Approach: download per-population iHS BigWig, liftover gene windows to hg19,
  extract windowed iHS summary (mean |iHS|, fraction of windows with |iHS| > 2)
  per gene for each of the 26 1000G populations
- Superpopulation summary: take max absolute iHS window across populations
  within each superpopulation group
- Note: PopHuman iHS is at 10 kb resolution; SNP-level iHS is not extracted

### XP-EHH (cross-population EHH)
- Source: PopHuman pre-computed BigWig tracks
- Use as a sensitivity check for iHS; same extraction approach

---

## Null Model and Matched Controls

Raw pathway-level statistics are not interpretable without a null. For each
metric (mean FST, max FST, mean |iHS|, PBS), we will construct a matched null:

- Draw 1000 random sets of genes matched to the pathway gene set on:
  - Gene length (within 2-fold)
  - Transcript count (within 50%)
  - Mean recombination rate (within 1 cM/Mb bin) — from deCODE or HapMap map
  - B-statistic / background selection score (within 0.1 unit bin) — McVicker et al.
- Compute the same FST/iHS summary for each random set
- Use the empirical null distribution to compute pathway-level enrichment p-values

If matched-null controls cannot be fully implemented before submission, the analysis
will be restricted to descriptive region-level comparisons without enrichment claims.

---

## Analysis Strategy

1. **Gene-level data fetching**:
   - Liftover hg38 gene coordinates to hg19 using UCSC liftOver binary or Ensembl REST
   - Tabix-fetch targeted VCF slices for each gene ± 10 kb from 1000G Phase 3
   - Filter to biallelic SNPs, MAF ≥ 0.01, PASS
   - Write per-gene population-stratified VCFs

2. **FST computation**:
   - For each gene VCF and each pair of superpopulations, run vcftools `--weir-fst-pop`
   - Summarise per-gene: mean FST, max FST, n SNPs, FST > 0.3 fraction

3. **PBS computation**:
   - Post-process FST tables using the three-population formula
   - Summarise per gene per focal population

4. **iHS extraction**:
   - Download PopHuman iHS BigWig tracks for each superpopulation
   - Intersect with gene windows to extract windowed |iHS| summaries

5. **Region-level summaries**:
   - Group genes by analysis_group (upstream_core, checkpoint_layer,
     downstream_diversification, substrate_support)
   - Compare FST/PBS/iHS distributions across groups using the same
     Mann-Whitney + rank-biserial framework as constraint analysis

6. **Candidate locus review**:
   - Any gene with max FST > 0.4 or |iHS| > 2.5 in ≥ 2 populations undergoes
     regional LD inspection, nearby-gene annotation, and cross-dataset check
     before being described in the manuscript

---

## Planned Outputs

- `docs/methods/popgen-decision.md` (this file)
- `scripts/liftover_gene_coords.py` — liftover hg38 → hg19
- `scripts/fetch_1000g_gene_vcfs.py` — tabix-fetch per-gene VCF slices
- `scripts/compute_fst_pbs.py` — vcftools FST + PBS post-processing
- `scripts/extract_pophuman_ihs.py` — BigWig intersection for iHS
- `scripts/analyze_popgen_gradient.py` — region-level group comparisons
- `data/processed/nglyco_gene_table_hg19.tsv` — gene coords in GRCh37
- `data/processed/nglyco_fst_per_gene.tsv`
- `data/processed/nglyco_pbs_per_gene.tsv`
- `data/processed/nglyco_ihs_per_gene.tsv`
- `results/tables/popgen_group_comparisons.tsv`
- `results/tables/popgen_candidate_loci.tsv`
- `results/figures/popgen_gradient.*`
- `results/reports/popgen-interpretation.md`

---

## Claim Limits

- FST outliers are not evidence of local adaptation without demographic correction.
- iHS signals at 10 kb resolution cannot be attributed to specific genes without
  LD and regional annotation inspection.
- Do not describe any pop-gen result as "proven selection" or "demonstrated adaptation."
- Population-specific FST can reflect founder effects, bottlenecks, drift, and
  demographic history as well as selection; use language such as "candidate signal,"
  "outlier," "consistent with differentiation."
- PBS is more branch-specific than one-vs-rest FST but still requires matched nulls
  before pathway-level enrichment claims.
- Keep SNP-level, region-level, and gene-set-level claims strictly separate.
