# Literature Review: Evolutionary Architecture of N-Glycosylation

Date started: 2026-05-20

This file is the readable synthesis of papers found for the project. The machine-readable tracker is `docs/concept/literature-matrix.tsv`; use that file for extraction fields, citation keys, roles, and priority.

## Working Review Question

Can N-glycosylation be used as a case study for a broader evolutionary architecture principle: biological pathways may localize robustness in catastrophic core machinery while localizing evolvability in downstream, branching, tissue-specific, and organism-environment interface layers?

The current search is a scoping and concept-building review, not yet a formal systematic review. Claims below should be treated as provisional until the highest-priority papers have been read in full and evidence extracted into the matrix.

## N-Glycosylation and Glycan Biology

Core pathway references establish the biological separation that the paper wants to test. The Essentials of Glycobiology N-glycan chapter provides the backbone for pathway curation: precursor assembly, transfer by oligosaccharyltransferase, ER processing and quality control, and Golgi diversification. Helenius and Aebi, and Aebi's ER-focused review, support the idea that upstream N-glycosylation is deeply tied to protein folding and quality control rather than only decoration.

Varki's review on evolutionary forces shaping Golgi glycosylation is currently the strongest conceptual bridge between glycobiology and evolution. It directly supports the idea that cell-surface glycans sit at an evolutionary interface, shaped by recognition, conflict, and communication. Kim, Lee, and Jeong's PLoS ONE paper on centralized modularity is also highly relevant because it represents N-linked glycosylation as a network in which modules branch from a common upstream region. That paper should be read carefully because its graph encoding may influence its conclusions, but it gives this project a useful starting model.

Key papers already tracked:

- Stanley et al., "N-Glycans", Essentials of Glycobiology.
- Helenius and Aebi, "Roles of N-linked glycans in the endoplasmic reticulum".
- Aebi, "N-linked protein glycosylation in the ER".
- Varki, "Evolutionary forces shaping the Golgi glycosylation machinery".
- Kim, Lee, and Jeong, "Centralized Modularity of N-Linked Glycosylation Pathways in Mammalian Cells".
- Dall'Olio et al., the 2012 BMC Evolutionary Biology paper, as historical context and hypothesis generator.

## Glycans as an Organism-Environment Interface

The interface argument is well supported at the level of general glycan biology. Marth and Grewal review mammalian glycosylation in immunity, including immune recognition and glycoprotein signaling. Rabinovich, van Kooyk, and Cobb support the broader point that protein-glycan interactions regulate innate and adaptive immunity. Poole et al. show how glycointeractions participate in bacterial pathogenesis, while Smith and Cummings give a structural view of glycans in virus-host interactions.

The strongest version of the project should not claim that every downstream N-glycosylation enzyme is adaptive. The safer claim is that downstream glycan-processing machinery contributes to a biological layer where host-pathogen interaction, immune modulation, tissue identity, and inflammation become plausible routes for tolerated and sometimes advantageous variation.

Key papers already tracked:

- Marth and Grewal, "Mammalian glycosylation in immunity".
- Rabinovich, van Kooyk, and Cobb, "Protein-glycan interactions in the control of innate and adaptive immune responses".
- Poole et al., "Glycointeractions in bacterial pathogenesis".
- Marino et al., "The Glycoscience of Immunity".
- Reily et al., "N-Glycosylation and Inflammation; the Not-So-Sweet Relation".
- Smith and Cummings, "Glycans in virus-host interactions: a structural perspective".
- Wolfert and Boons, "Adaptive immune activation: glycosylation does matter".
- Shen et al., "Multivariate discovery and replication of five novel loci associated with Immunoglobulin G N-glycosylation".
- Klaric et al., "Glycosylation of immunoglobulin G is regulated by a large network of genes pleiotropic with inflammatory diseases".

## Population Genetics

Population genetics should remain supporting evidence, not the center of the paper. The original 2012 paper is useful historically because it framed a pathway-level contrast, but modern interpretation needs stronger controls for demography, LD, recombination, background selection, gene boundaries, SNP density, and local genomic context.

The useful population-genetics literature has two roles. First, methods papers and reviews define what selection scans and differentiation statistics can and cannot establish. Voight et al. and Sabeti et al. are central for haplotype-based recent-selection scans; Nielsen et al. is a high-level review for interpreting human selection signals. Coop et al. is important for geography-aware allele-frequency analyses. Berg and Coop plus the later eLife correction/caution literature are useful for preventing overinterpretation of polygenic or population-structured signals.

Second, modern datasets such as the high-coverage 1000 Genomes release can support a limited re-check of pathway-level standing variation or differentiation, if the analysis plan justifies it. The decision should be made after the conceptual and disease/constraint evidence is stronger.

Key papers already tracked:

- Dall'Olio et al., 2012 BMC Evolutionary Biology original paper.
- Nielsen et al., "Recent and ongoing selection in the human genome".
- Voight et al., "A map of recent positive selection in the human genome".
- Sabeti et al., "Genome-wide detection and characterization of positive selection in human populations".
- Coop et al., "The role of geography in human adaptation".
- Berg and Coop, "A population genetic signal of polygenic adaptation".
- Berg et al., "Reduced signal for polygenic adaptation of height in UK Biobank".
- Byrska-Bishop et al., high-coverage expanded 1000 Genomes Project cohort.

## Network Theory Applied to Genetics

Network biology provides the language for turning pathway position into measurable predictions, but the project needs to avoid simplistic centrality storytelling. Barabasi and Oltvai provide the broad network biology foundation. Jeong et al. motivates the idea that central nodes can have higher essentiality, but Hahn and Kern show why centrality claims are sensitive to network definition and organism/context. Vitkup, Kharchenko, and Wagner are especially relevant because they connect metabolic network structure and function to enzyme evolution.

For this project, network features should be broader than centrality alone: pathway depth, branch-point status, checkpoint proximity, redundancy/paralogy, terminal modification, substrate/product branching, tissue deployment, and quality-control coupling. The N-glycosylation graph should be rebuilt from current Reactome/GlyGen/curated sources before making claims.

Key papers already tracked:

- Barabasi and Oltvai, "Network biology: understanding the cell's functional organization".
- Jeong et al., "Lethality and centrality in protein networks".
- Hahn and Kern, "Comparative genomics of centrality and essentiality in three eukaryotic protein-interaction networks".
- Vitkup, Kharchenko, and Wagner, "Influence of metabolic network structure and function on enzyme evolution".
- Kim, Lee, and Jeong, "Centralized Modularity of N-Linked Glycosylation Pathways in Mammalian Cells".
- Goh et al., "The human disease network".

## Disease, Constraint, and Human Variation

Disease architecture is probably the most direct empirical test of the robustness/evolvability hypothesis. GeneReviews and CDG clinical reviews should be used to curate severe Mendelian disease evidence. gnomAD/ExAC constraint papers provide quantitative measures such as LOEUF and missense constraint. ClinVar and GWAS Catalog can provide complementary clinical and complex-trait evidence, but both need filtering and careful gene assignment.

The project's strongest testable prediction is a gradient: upstream conserved core and quality-control machinery should show stronger constraint and higher severe Mendelian burden, whereas downstream/interface genes may show more tolerated variation and richer immune, inflammatory, infection, cancer, or tissue-context associations. This remains a hypothesis, not a conclusion.

Key papers and sources already tracked:

- Sparks and Krasnewich, GeneReviews on congenital disorders of N-linked glycosylation.
- Park and Marquardt, "Treatment Options in Congenital Disorders of Glycosylation".
- Rymen and colleagues, "Congenital Disorders of Glycosylation: What Clinicians Need to Know?"
- Karczewski et al., gnomAD mutational constraint spectrum.
- Lek et al., ExAC protein-coding variation.
- MacArthur et al., systematic survey of loss-of-function variants.
- Landrum et al., ClinVar.
- Buniello et al., NHGRI-EBI GWAS Catalog.

## Cross-Cutting Theory

The robustness/evolvability framing should be explicit in the introduction rather than implicit. Kitano, Felix and Wagner, Payne and Wagner, and Edelman and Gally provide the conceptual basis for robustness, evolvability, modularity, degeneracy, and buffered variation. These papers do not prove the N-glycosylation hypothesis, but they provide the vocabulary for formal predictions.

Key papers already tracked:

- Kitano, "Biological robustness".
- Felix and Wagner, "Pervasive robustness in biological systems".
- Payne and Wagner, "The causes of evolvability and their evolution".
- Edelman and Gally, "Degeneracy and complexity in biological systems".

## Immediate Reading Priorities

1. Read the pathway-core papers first: Stanley et al., Helenius and Aebi, Aebi, Varki, and Kim et al.
2. Extract a gene/pathway-region vocabulary from pathway-core papers before expanding the bibliography much further.
3. Read gnomAD, GeneReviews/CDG, ClinVar, and GWAS Catalog papers to design the disease/constraint evidence table.
4. Read the population-genetics caution papers before deciding whether to run new selection or differentiation analyses.
5. Read network biology papers with the specific aim of choosing measurable features and null models, not just adding centrality language.

## Open Gaps

- Need a fuller set of primary studies on sialic acid evolution, glycosyltransferase family evolution, and host-pathogen glycan conflict.
- Need direct sources for GlyGen/Reactome pathway curation and stable gene identifiers.
- Need comparator-pathway references for MHC, olfactory receptors, ER folding, and ribosome/translation if the paper generalizes beyond N-glycosylation.
- Need full-text extraction from high-priority papers into the matrix before writing manuscript prose.
