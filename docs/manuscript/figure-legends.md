# Figure Legends

## Figure 1 — Conceptual architecture model of N-glycosylation robustness and evolvability

The N-glycosylation pathway is organized into two functionally distinct layers. The upstream core (grey) comprises lipid-linked oligosaccharide (LLO) assembly on the cytoplasmic and luminal faces of the ER membrane, oligosaccharyltransferase (OST) transfer of the 14-sugar precursor to nascent polypeptides, and the ER quality-control cycle (calnexin/calreticulin/UGGT). These steps act on a common precursor whose structure is conserved across eukaryotes and whose disruption causes congenital disorders of glycosylation (CDG) or early lethality. The downstream diversification layer (blue) comprises Golgi mannose trimming, GlcNAc branching, core fucosylation, galactosylation, and terminal sialylation and sulfation. These enzymes act combinatorially on diverse acceptors and generate the mature N-glycan structures displayed at the cell surface and in secreted glycoproteins. The model predicts that robustness — resistance to genetic disruption — concentrates in the upstream core, while evolvability — the capacity to generate heritable phenotypic variation accessible to selection — is expressed through the downstream glycan-output layer. This figure depicts the tested architecture model, not a result.

---

## Figure 2 — Curated N-glycosylation pathway graph (101 genes)

Node-link representation of the curated N-glycosylation gene and reaction network. Nodes are genes (n = 101) colored by coarse pathway region: LLO assembly (dark blue), OST transfer (medium blue), ER quality control (teal), Golgi core processing (green), Golgi branching (orange), terminal modification (red), and substrate biosynthesis (grey). Edges represent shared biochemical intermediates, glycoprotein processing steps, donor-substrate supply relationships, and quality-control cycling interactions, as curated from Reactome (release 96) and KEGG (hsa00510). Graph layout is force-directed; spatial positions do not encode pathway depth. Downstream enzyme families (B4GALT1–6, MAN1A1/A2/C1, ST3GAL and ST6GAL sialyltransferases, MGAT family) are visible as paralog clusters in the lower portion of the graph. Source: `results/figures/nglyco_pathway_network.svg`.

---

## Figure 3 — Constraint gradient by pathway region: LOEUF and missense Z

**(A)** gnomAD v4.1 loss-of-function observed/expected upper confidence bound (LOEUF) by pathway region. Lower LOEUF indicates stronger loss-of-function intolerance. Points are individual genes; boxes show median and IQR. Upstream-core genes (LLO assembly, OST transfer, ER QC) and downstream-diversification genes (Golgi branching, terminal modification) are highlighted. The upstream-core median LOEUF (0.909) is higher than the downstream median (0.740), the opposite of the naive prediction.

**(B)** gnomAD v4.1 missense Z score by pathway region. Higher missense Z indicates stronger depletion of missense variants. The downstream layer shows higher median missense Z than the upstream core.

**(C)** OLS regression of LOEUF on pathway group, log genomic span, log CDS length, expression breadth (GTEx tissues with nTPM ≥ 1), and Ensembl paralog count. Coefficients and 95% confidence intervals are shown. The downstream coefficient is attenuated from −0.20 to −0.13 and becomes non-significant (p = 0.22) after adjustment for log CDS length (Spearman ρ = −0.53 with LOEUF across all primary-analysis genes), supporting gene-length confounding as the primary driver of the apparent inversion. Downstream genes have median genomic span 71 kb versus 48 kb upstream. Source: `results/figures/constraint_gradient.svg`; regression results in `results/tables/loeuf_regression_results.txt`.

---

## Figure 4 — Disease architecture gradient across pathway regions

**(A)** Fraction of genes with curated CDG or overlapping-multiple-pathway Mendelian disease evidence (GeneReviews CDG curation, accessed 2026-06-03) by pathway region. CDG burden is highest in LLO assembly (11/15 genes, 73%) and OST transfer (5/11 genes, 45%) and approaches zero in Golgi branching (0/5, 0%) and terminal modification (1/16, 6%).

**(B)** Fraction of genes with at least one ClinVar germline pathogenic or likely pathogenic variant by pathway region. LLO assembly (14/15) and substrate biosynthesis (23/30) carry the heaviest ClinVar P/LP burden. Golgi branching (0/5) and terminal modification (3/16) carry the least.

**(C)** Fraction of genes with GWAS Catalog evidence in selected trait categories (glycome, immune/inflammation, infection, cancer) by pathway region. Downstream regions (Golgi branching: 4/5 glycome evidence; terminal modification: 5/16 glycome, 14/16 immune/inflammation) carry richer glycan-output and interface-trait evidence than upstream regions, consistent with a downstream evolvability layer.

Bars show region-level fractions. Whiskers are not shown because these are population fractions, not sampling statistics; the pathway gene counts per region are given in parentheses. The two evidence types — curated Mendelian/CDG and GWAS Catalog trait category — are plotted separately because they speak to different biological claims (catastrophic upstream sensitivity vs. downstream phenotypic richness). Source: `results/figures/disease_architecture.svg`.

---

## Figure 5 — Topology-dependence of the disease gradient: N-glycosylation and four comparator pathways

Mendelian disease burden in the upstream core and downstream layer for five pathway architectures.

**N-glycosylation** (n = 101 genes): upstream core 73% CDG (LLO assembly), downstream 0–6% CDG (Golgi branching, terminal modification). This is the primary finding.

**Heparan sulfate (HS) biosynthesis** (n = 24 genes): upstream core (linker assembly and chain polymerization, n = 8) 100% Mendelian disease burden (EXT1/2, EXTL genes causing hereditary exostoses and Golabi–Ito–Hall syndrome); downstream HS modification enzymes (NDST, HS2ST, HS3ST, HS6ST, SULF families, n = 16) 0% Mendelian disease burden. Fisher's exact p < 0.0001. Replicates the N-glycosylation pattern.

**Purine de novo synthesis** (n = 10 genes, strictly linear): shared-core genes (n = 6) 33% Mendelian disease; downstream branch enzymes (n = 4, IMPDH1 and ADSS2) 50% disease. Fisher's exact p = 1.0. No gradient; the pattern is absent in this linear pathway.

**GPI-anchor biosynthesis** (n = 21 genes, linear with no combinatorial output layer): disease burden is distributed across the pathway with no significant upstream enrichment (p > 0.3).

**Ceramide/glycosphingolipid biosynthesis** (n = 22 genes): upstream ceramide synthesis 57% Mendelian disease burden; downstream glycolipid synthesis 25% burden (p = 0.20). Partial gradient, attenuated because some downstream glycolipid enzymes (B4GALNT1, ST3GAL5) target critical neurological functions. This comparator shows that the gradient is present but dampened when some downstream enzymes have tissue-restricted essential roles.

Together, the comparator analysis demonstrates that the disease-burden gradient is topology-dependent: present in pathways with a conserved shared core feeding a combinatorial output layer, absent in linear pathways. This distinguishes the N-glycosylation architecture finding from a trivial consequence of shared-step essentiality. Source: comparator data in `results/tables/pathway_null_model_summary.txt`.

---

## Figure 6 — Evidence matrix: predictions tested and outcome summary

Summary of the four architecture model predictions tested in this study and the outcome of each evidence stream.

| Prediction | Evidence stream | Result | Interpretation |
|---|---|---|---|
| Severe disease concentrates upstream | CDG curation (GeneReviews) | Supported | 73% LLO assembly CDG; 0% Golgi branching |
| Severe disease concentrates upstream | ClinVar P/LP burden | Supported | 14/15 LLO assembly; 0/5 Golgi branching |
| Severe disease gradient is topology-dependent | Comparator pathways (HS, purine, GPI, GSL) | Supported | Replicated in HS (p<0.0001); absent in purine/GPI |
| Downstream enriched for glycan-output traits | Genome-wide GWAS null model (982,984 loci) | Supported (with caveat) | Downstream OR=2.47 unmatched; OR=1.63 after hit-count matching (p=0.107) |
| Downstream enriched for glycan-output traits | IgG glycan GWAS locus partitioning | Strongly supported | 7/7 glycan loci downstream; 0 upstream (OR=∞, p=0.003) |
| Coding constraint does not show simple gradient | LOEUF + regression | Supported | Inversion explained by gene-length confounding + Wald survivor bias |
| Coding constraint does not show simple gradient | Human–mouse dN/dS (98 gene pairs) | Supported | Medians 0.075 vs 0.073, p=0.49 |
| Coding constraint does not show simple gradient | Cross-species % identity | Supported | No upstream–downstream coding conservation gradient |

The final column distinguishes results that are architecture-level robust findings from those that are hypothesis-generating. GWAS Catalog gene assignments are not causal; IgG glycan locus assignments require fine mapping and colocalization for per-locus confirmation. CDG and ClinVar evidence reflects ascertainment history and is conservative in the direction of upstream enrichment.

---

## Figure 7 (optional) — Population-genetic gradient analysis

**(A–C)** Pairwise F_ST by pathway region for three continental population pairs from 1000 Genomes Phase 3 (AFR–EUR, AFR–EAS, EUR–EAS). Region-level median F_ST values are shown with IQR. No significant upstream-to-downstream F_ST gradient is detected in any comparison (all Kruskal–Wallis p > 0.05 after correction for genomic background). Candidate outlier loci are annotated where F_ST exceeds the 99th percentile of the matched genomic background.

**(D–F)** Integrated haplotype score (iHS) by pathway region for AFR, EUR, and EAS populations. Absolute |iHS| values above 2.0 (indicative of extended haplotype homozygosity consistent with recent positive selection) are flagged. No pathway region shows a significant excess of |iHS| > 2.0 relative to genome-wide background after correction.

**(G)** Population branch statistic (PBS) for candidate outlier genes identified in the F_ST and iHS scans. PBS quantifies the branch length of population-specific divergence relative to an outgroup. Candidate genes with convergent evidence across multiple statistics (F_ST outlier, iHS outlier, PBS outlier) are named; these are hypothesis-generating only and do not constitute evidence of adaptation without replication, fine mapping, and functional support.

Taken together, the population-genetic analyses do not reveal a systematic upstream-to-downstream gradient in coding-level selection or differentiation, consistent with the view that downstream evolvability is expressed through regulatory and glycan-output channels rather than coding sweeps. Source: `results/figures/popgen_gradient_*.svg`; candidate loci in `results/tables/popgen_candidate_loci.tsv`.
