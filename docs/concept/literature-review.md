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
- Varki, "Biological roles of glycans".
- Varki, "Uniquely human evolution of sialic acid genetics and biology".
- Suzuki, "Glycan diversity in the course of vertebrate evolution".
- Tomono et al., "Investigation of glycan evolution based on a comprehensive analysis of glycosyltransferases using phylogenetic profiling".
- Kim, Lee, and Jeong, "Centralized Modularity of N-Linked Glycosylation Pathways in Mammalian Cells".
- Dall'Olio et al., the 2012 BMC Evolutionary Biology paper, as historical context and hypothesis generator.
- Montanucci et al., "Molecular Evolution and Network-Level Analysis of the N-Glycosylation Metabolic Pathway Across Primates".

The new glycan-evolution additions strengthen a key distinction for the manuscript: ER-linked N-glycosylation supports conserved maturation and quality control, while later glycan elaboration and terminal modification are repeatedly implicated in lineage-specific and interface-facing diversity. Tomono et al. are especially useful because they analyze glycosyltransferases directly and argue that non-reducing terminal glycan synthesis is associated with more recently evolved enzymes. This should be treated as support for a downstream evolvability hypothesis, not as proof that every downstream N-glycosylation enzyme is adaptive.

Montanucci et al. should be treated as a direct predecessor rather than a peripheral citation. Their primate comparative analysis found strong purifying selection across N-glycosylation genes and no clear positive-selection signal, while showing that pathway/network structure is associated with evolutionary constraint. This narrows the new paper's prediction: downstream/interface evolvability should not be framed primarily as faster protein-coding evolution. It should instead be tested in regulatory, glycan-output, tissue, disease, and trait layers.

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
- Varki and Gagneux, "Multifarious roles of sialic acids in immunity".
- Dias et al., "Glycans as critical regulators of gut immunity in homeostasis and disease".
- Josenhans et al., "How bacterial pathogens of the gastrointestinal tract use the mucosal glyco-code to harness mucus and microbiota".
- Pinho et al., "Mucosal glycans: key drivers of the development of inflammatory bowel disease and a potential new therapeutic target".
- Shen et al., "Multivariate discovery and replication of five novel loci associated with Immunoglobulin G N-glycosylation".
- Klaric et al., "Glycosylation of immunoglobulin G is regulated by a large network of genes pleiotropic with inflammatory diseases".

The mucosal and sialic-acid papers broaden the organism-environment interface argument beyond generic immune recognition. They make clear that glycans participate in barrier integrity, host-microbiota crosstalk, pathogen binding or mimicry, Siglec-mediated self-recognition, and inflammatory tuning. The limitation is equally important: several of these sources emphasize mucins, sialic acids, O-glycans, or lectin receptors rather than N-glycosylation enzymes. They should support the interface-layer framing while gene-level claims remain tied to N-glycosylation-specific evidence.

## Glyco-Gene Regulation and Glycome Genetics

The Zoldos, Grgurevic, and Lauc review on epigenetic regulation of protein glycosylation is highly relevant because it makes a key distinction the manuscript should now adopt: core N-glycosylation is essential, while glycan antenna modification and terminal elaboration can contribute to individual variation and environmental response. The related Lauc and Zoldos review, "Protein glycosylation - an evolutionary crossroad between genes and environment", makes the same point in evolutionary terms: glycan structures are not directly template-encoded and can vary through the coordinated activity and regulation of many glyco-genes.

Post-2010 glycome genetics gives this project a modern evidence layer that did not exist in the older evolutionary papers. Huffman et al. identified HNF1A and fucosyltransferase loci as regulators of plasma N-glycome variation. Later plasma N-glycome GWAS work expanded the number of replicated loci and showed overlap between total plasma protein and IgG glycosylation, including loci containing direct glycosylation enzymes and broader regulatory candidates. IgG N-glycome GWAS papers identified glycosyltransferase loci such as ST6GAL1, B4GALT1, FUT8, and MGAT3, as well as immune and inflammatory disease loci. Recent multivariate IgG work and large plasma N-glycome GWAS studies strengthen the link between glycan-output variation, immune function, liver biology, inflammatory disease, and regulatory architecture.

These papers should reshape the evidence plan. They suggest that the strongest modern test of downstream/interface evolvability may be in glycan trait architecture, regulatory loci, tissue-specific expression, immune pleiotropy, and disease associations, not in coding-sequence acceleration.

Post-2010 anchors identified in the 2026-05-31 search:

- Lauc and Zoldos, "Protein glycosylation - an evolutionary crossroad between genes and environment".
- Lauc, Kristic, and Zoldos, "Glycans - the third revolution in evolution".
- Huffman et al., first glycome GWAS identifying HNF1A as a regulator of plasma protein fucosylation.
- Lauc et al. and later reviews on complex genetic regulation of protein glycosylation.
- Shen et al., IgG N-glycosylation GWAS and immune/inflammatory pleiotropy.
- Klaric et al., large-network regulation of IgG glycosylation and inflammatory disease pleiotropy.
- Shadrina et al., multivariate IgG N-glycosylation GWAS.
- Suhre et al., fine-mapping the human plasma N-glycome onto the proteome.
- Sharapov and colleagues' large plasma N-glycome GWAS linking glycome traits to liver disease and anti-inflammatory proteins.

### Newly Tracked Paper Summaries

The 2026-05-31 tracker update added structured summaries for the following papers to `docs/concept/literature-matrix.tsv`.

- Montanucci et al. (2011): direct predecessor on primate N-glycosylation evolution; relevant because strong coding conservation and network-associated purifying constraint push the new paper away from a simple coding-adaptation model.
- Zoldos, Grgurevic, and Lauc (2010): review on epigenetic regulation of glyco-genes; relevant because it supports the distinction between essential core N-glycosylation and variable antenna/terminal glycan outputs.
- Lauc and Zoldos (2010): conceptual review of glycosylation as a gene-environment interface; relevant because it supports regulatory and environmental responsiveness as the likely evolvability layer.
- Lauc et al. (2010): early evidence for complex genetic regulation of protein glycosylation; relevant because it motivates glycan-output phenotypes as measurable downstream consequences of genetic and regulatory variation.
- Huffman et al. (2011): first plasma N-glycome GWAS; relevant because it shows that plasma glycan-output variation can be genetically mapped and includes regulatory loci such as HNF1A.
- Varki (2011): review of evolutionary forces shaping Golgi glycosylation; relevant because it supports the downstream glycan machinery as an organism-environment interface layer.
- Lauc, Kristic, and Zoldos (2014): broad evolutionary argument for glycans as a distinct biological information layer; relevant as conceptual support, but not direct evidence for N-glycosylation pathway-region gradients.
- Shen et al. (2017): multivariate IgG N-glycosylation GWAS; relevant because it identifies antibody glycan-output loci and supports multivariate glycan traits as a structured phenotype set.
- Klaric et al. (2020): large IgG glycosylation GWAS; relevant because it links distributed glycan regulation with inflammatory disease pleiotropy.
- Lauc et al. (2013): IgG N-glycosylation GWAS with autoimmune and hematological cancer pleiotropy; relevant because antibody glycan variation links downstream glycosylation traits to immune disease architecture.
- Sharapov et al. (2019): expanded plasma N-glycome GWAS; relevant because it strengthens the regulatory and glycan-output evidence stream beyond early small studies.
- Suhre et al. (2019): protein-resolved plasma N-glycome mapping; relevant because it helps interpret bulk plasma glycan signals in relation to specific glycoproteins.
- Shadrina et al. (2021): multivariate IgG N-glycosylation GWAS; relevant because it reinforces distributed genetic control of antibody glycan-output traits.
- Sharapov et al. (2025): large plasma N-glycome GWAS linking glycan traits to liver disease and anti-inflammatory proteins; relevant because it gives a current, high-powered trait/disease evidence layer for regulatory evolvability.

Standalone summaries for these papers are stored in `docs/concept/paper-summaries/`.

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
- Csete and Doyle, "Bow ties, metabolism and disease".
- Friedlander et al., "Evolution of Bow-Tie Architectures in Biology".
- Jeong et al., "Lethality and centrality in protein networks".
- Hahn and Kern, "Comparative genomics of centrality and essentiality in three eukaryotic protein-interaction networks".
- Vitkup, Kharchenko, and Wagner, "Influence of metabolic network structure and function on enzyme evolution".
- Kim, Lee, and Jeong, "Centralized Modularity of N-Linked Glycosylation Pathways in Mammalian Cells".
- Goh et al., "The human disease network".

Bow-tie architecture is a promising analogy for the paper, but it needs discipline. N-glycosylation is not obviously a textbook bow tie in the same way as central metabolism, because its upstream LLO synthesis and downstream Golgi processing are both constrained by biochemical specificity and compartmentalization. The useful contribution of the bow-tie literature is conceptual: architectures can combine robust cores with diverse outputs and characteristic fragilities. The manuscript should translate that idea into measurable N-glycosylation features rather than using "bow tie" as a decorative label.

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
- Daniels et al., "Sloppiness, robustness, and evolvability in systems biology".

The sloppiness literature adds an important alternative explanation: apparent robustness can arise from model geometry and insensitive parameter combinations, not only from directly selected buffering. This is useful for the devil's-advocate side of the paper. If upstream genes are strongly constrained, that result should not automatically be described as an evolved robustness design; it may reflect biochemical indispensability, annotation, or generic network sensitivity.

## Immediate Reading Priorities

1. Read the pathway-core papers first: Stanley et al., Helenius and Aebi, Aebi, Varki, and Kim et al.
2. Extract a gene/pathway-region vocabulary from pathway-core papers before expanding the bibliography much further.
3. Read Montanucci et al. and the Zoldos/Lauc glyco-regulation papers as predecessor literature to refine the novelty claim.
4. Read glycome and IgG N-glycome GWAS papers to design the regulatory/trait evidence table.
5. Read gnomAD, GeneReviews/CDG, ClinVar, and GWAS Catalog papers to design the disease/constraint evidence table.
6. Read the population-genetics caution papers before deciding whether to run new selection or differentiation analyses.
7. Read network biology papers with the specific aim of choosing measurable features and null models, not just adding centrality language.

## Open Gaps

- Need deeper extraction from the new sialic-acid evolution, glycosyltransferase evolution, and mucosal glycan interface papers.
- Need direct sources for GlyGen/Reactome pathway curation and stable gene identifiers.
- Need fuller comparator-pathway extraction if the paper generalizes beyond N-glycosylation. Initial anchors now exist for MHC/HLA, olfactory receptors, and ER protein-folding quality control, but not yet for ribosome/translation or central metabolism controls.
- Need full-text extraction from high-priority papers into the matrix before writing manuscript prose.
- Need structured extraction of post-2010 glycome GWAS and glyco-gene regulatory papers into `docs/concept/literature-matrix.tsv`.
