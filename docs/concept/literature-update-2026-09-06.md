# Literature Update Through 2026-09-06

## Scope and decision

This update searches for work published or posted after the last documented literature expansion on 2026-05-28 to 2026-05-31. The search window was 2026-06-01 through 2026-09-06. It is a targeted update of the six existing literature clusters, not a new systematic review of the whole field.

The new literature strengthens the current architecture model but does not require a change in thesis. The strongest additions are mechanistic evidence for glycan-dependent ER triage and quality control, new severe Mendelian phenotypes caused by early N-glycosylation defects, and evidence that later glycan states are responsive to tissue, immune, infectious, and metabolic context. None of the newly identified studies directly tests an upstream-to-downstream robustness/evolvability gradient across the N-glycosylation pathway. They therefore support individual links in the argument rather than validating the complete model.

## Search protocol

Databases searched on 2026-09-11, with results restricted to the requested 2026-09-06 cutoff:

- PubMed, using NCBI E-utilities, with publication dates restricted to 2026-06-01 through 2026-09-06.
- Europe PMC, including MED-indexed papers and PPR preprints, using `FIRST_PDATE` restricted to the same window.
- OpenAlex, using full-text metadata search and the same publication-date window to recover records not yet indexed in PubMed.
- bioRxiv was checked directly for the most relevant preprints surfaced by Europe PMC and OpenAlex.

The following concept combinations were run in title/abstract fields where supported:

1. `(glycosylation OR glycan) AND (evolution OR evolvability OR diversification)`
2. `(N-glycosylation OR glycan) AND (immunity OR pathogen OR microbiome OR mucosal)`
3. `(congenital disorders of glycosylation OR N-linked glycosylation) AND (constraint OR genetic OR disease)`
4. `(glycome OR IgG N-glycosylation) AND (GWAS OR genetic OR variation)`
5. `(pathway architecture OR biological network) AND (robustness OR evolvability OR constraint)`

PubMed returned 222 records across the five searches before cross-query deduplication. Europe PMC returned 187 records across the first four searches. OpenAlex returned 796 ranked results across four broader searches; the first 50 results per search were title-screened. Records were deduplicated by DOI or PMID during screening. Searches were intentionally sensitive and produced many irrelevant records about viral sequence surveillance, plant secondary-metabolite glycosylation, glycomaterials, analytical chemistry, and non-human microbiome studies.

Inclusion required a direct contribution to at least one live project claim or method: pathway topology and mutation effects; N-glycosylation core/quality control; severe CDG architecture; tissue or regulatory deployment; glycan-mediated immunity or host-environment interaction; or glycome genetics. Sixteen records were retained in the literature matrix: 12 peer-reviewed papers and four preprints. Citation metadata and DOIs were checked against PubMed and/or Crossref; the IgG-cognition DOI was confirmed in PubMed but was not resolvable through Crossref on 2026-09-11.

## Highest-priority additions

### Core machinery, quality control, and severe disease

Galeone et al. identify TUSC3 as a dosage-sensitive gatekeeper controlling glucose trimming, entry into ER quality control, and the decision between secretion and ER-associated degradation for BMP4/Dpp. This is unusually direct support for the paper's claim that early N-glycosylation contains high-consequence checkpoints. It should be considered for the Introduction or Discussion and for interpretation of checkpoint proximity, but it is substrate-specific rather than a pathway-wide test.

Ng et al. establish biallelic loss of RPN1, an oligosaccharyltransferase component, as a severe neurodevelopmental CDG with selective impairment of OST-A substrates. Marquez et al. add a nine-person ALG14 cohort with congenital myasthenia, epilepsy, contractures, and developmental abnormalities plus functional evidence in Xenopus. Together these papers strengthen the upstream severe-disease layer with causal and mechanistic evidence. They should be checked against the curated CDG table and manuscript disease citations.

Nilsson et al. use integrated serum/plasma glycoproteomics in PMM2-CDG and report widespread unoccupied sequons plus site-specific immature N-glycans. This makes the molecular consequence of an upstream precursor defect visible across many glycoproteins, but the cohort is small. Mól et al. show that plasma N-glycan profiles can distinguish several type II CDG subtypes, linking downstream-processing defects to distinct glycophenotypes; this is diagnostically useful but does not by itself imply milder disease.

### Network and tissue architecture

Gouy's 2026 review directly connects regulatory-network topology to distributions of mutational phenotypic and fitness effects and to the evolution of robustness under stabilizing selection. It is a strong modern conceptual citation for the genotype-phenotype-map logic of this project, but it remains a general synthesis rather than glycosylation-specific evidence.

Neves et al. analyze 12 CDG genes across GTEx and find that high baseline expression does not reliably predict affected-tissue vulnerability; allele-specific expression and distal eQTL architecture are tissue dependent. This is important for interpreting the project's HPA/GTEx layer: expression breadth and tissue specificity can support deployment context, but should not be presented as direct measures of disease susceptibility or evolvability.

### Immune and environmental interface

Heinke et al. reconstitute glycan-driven MHC-I recycling and show that calreticulin mediates transfer between TAPBPR and tapasin. This paper usefully joins ER quality control to an adaptive-immune output, showing that core surveillance and interface function are coupled rather than cleanly separable.

Alymova et al. show that even low-occupancy N-glycans on influenza H3N2 haemagglutinin can reduce antibody pressure while limiting fitness costs. This is a strong concrete example of a glycan-mediated fitness trade-off at an organism-environment interface. It concerns viral glycosylation-site evolution, not evolution of the host N-glycosylation machinery, so it should be used as an analogy and not as direct pathway evidence.

Gu et al. synthesize evidence that fucosyltransferases affect epithelial integrity, mucus, immune recruitment, inflammation, and senescence in asthma. The review supports the downstream-interface framing, while explicitly noting that several mechanisms remain inferred from related diseases or experimental models.

### Glycan-output and context-responsive variation

Peng et al. connect obesity-associated IgG hypogalactosylation and hyposialylation to B-cell WNT3 regulation in adolescents, cell models, and mice. Wang et al. integrate transcriptome, protein, and IgG glycan QTL data with cognitive-function GWAS and Mendelian randomization. These studies broaden the complex-trait layer, but neither establishes adaptive variation; reverse causation, horizontal pleiotropy, phenotype specificity, and ancestry/sample limitations remain important.

## Preprint watchlist

Four preprints merit tracking but should not yet support strong manuscript claims:

- Cutine et al. report reduced alpha-2,6 sialylation of secretory IgA and B cells in ulcerative colitis and functional effects on IgA plasma-cell differentiation and intestinal inflammation.
- Stölting et al. identify GALE-dependent nucleotide-sugar metabolism as a regulator of RAS-driven N- and O-glycoproteome remodelling and tumour growth.
- Gambarte Tudela et al. report KSHV-driven changes in branching and sialylation involving `MGAT5`, `B3GNT2`, `B4GALT1`, and nucleotide-sugar transporters, with downstream effects on galectin-1 and PDGFRA signalling.
- Ranzinger et al. describe a new GlyGen knowledgebase release integrating glycans, proteins, genes, sites, diseases, biomarkers, and variants with evidence tracking. This is relevant to the pending GlyGen cross-check, but the record was a Research Square preprint on the search date.

## Implications for the project

1. Do not change the central claim: the update adds supportive mechanisms, not a direct pathway-gradient test.
2. Add TUSC3, RPN1, ALG14, and PMM2 glycoproteomics to the next disease/quality-control citation pass.
3. Use the GTEx CDG paper to narrow any language that equates tissue expression with tissue vulnerability.
4. Consider MHC-I recycling as a bridge example showing that robustness-heavy quality control can directly serve an immune interface.
5. Keep viral low-occupancy glycosylation and the four preprints as clearly labeled analogies or watchlist evidence.
6. Recheck the preprint watchlist and the Crossref status of `10.3967/bes2026.043` before manuscript submission.
