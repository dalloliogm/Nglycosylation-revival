# Literature Search Plan

## Purpose

Build the intellectual foundation for a new paper on evolutionary architecture in biological pathways, using N-glycosylation as the primary case study.

The search should answer four questions:

1. What is already known about robustness, evolvability, modularity, degeneracy, and pathway architecture?
2. What is already known about glycan evolution, especially Golgi glycosylation and cell-surface diversity?
3. What evidence supports the idea that downstream glycosylation is an organism-environment interface layer?
4. What evidence supports a disease architecture gradient from severe core defects to subtler interface phenotypes?

## Search Principle

Do not search only for population genetics or selection scans. The paper's center is the systems-level hypothesis that biological pathways may localize evolvability away from catastrophic failure points.

The literature search should therefore integrate:

- evolutionary theory
- systems biology
- glycobiology
- glycoimmunology
- congenital disorders of glycosylation
- complex disease genetics
- network biology
- computational pathway modeling

## Literature Clusters

### 1. Robustness and Evolvability Theory

Goal:

Find the conceptual and theoretical backbone for the paper.

Questions:

- How have robustness and evolvability been defined?
- What mechanisms connect robustness with evolvability?
- What roles do modularity, degeneracy, redundancy, and neutral networks play?
- Are there existing models where biological systems isolate variation from catastrophic failure?
- Are there analogies to bow-tie architecture, layered protocols, or fault-tolerant engineering?

Seed references and leads:

- Kitano-style biological robustness literature.
- Reviews on robustness/evolvability in living systems.
- Degeneracy as a bridge between robustness and evolvability.
- Sloppiness, robustness, and evolvability in systems biology.
- Bow-tie architecture and highly optimized tolerance in biological systems.

Search terms:

- `biological robustness evolvability review`
- `robustness evolvability modularity degeneracy biological systems`
- `bow tie architecture biological networks robustness evolvability`
- `neutral networks robustness evolvability systems biology`
- `fault tolerance biological pathways evolvability`

### 2. Glycan Evolution and Golgi Diversification

Goal:

Establish that cell-surface glycan diversity is evolutionarily important and especially connected to the Golgi/downstream machinery.

Questions:

- Why are cell-surface glycans universal and diverse?
- What selective forces shape Golgi glycosylation?
- How do terminal glycan modifications vary across species, tissues, and environments?
- Are glycosyltransferases and glycosidases plausible evolvability machinery?

Seed references and leads:

- Varki's work on evolutionary forces shaping Golgi glycosylation.
- Essentials of Glycobiology chapters on N-glycans and glycan evolution.
- Reviews on sialic acid evolution and host-pathogen conflict.
- Prior N-glycosylation pathway annotation and primate evolution papers.

Search terms:

- `evolutionary forces Golgi glycosylation machinery`
- `cell surface glycans evolution host pathogen`
- `sialic acid evolution host pathogen glycan`
- `N-glycosylation pathway evolution primates`
- `glycosyltransferase evolution mammalian glycans`

### 3. Glycans as Organism-Environment Interface

Goal:

Support the claim that downstream glycosylation is an interface layer connecting organism and environment.

Questions:

- How do glycans mediate pathogen recognition and infection?
- How do glycans mediate microbiome interactions?
- How does glycosylation regulate innate and adaptive immunity?
- How do epithelial, mucosal, and barrier tissues use glycan variation?
- Are glycan changes linked to inflammation, autoimmunity, cancer, and infection susceptibility?

Seed references and leads:

- Glycointeractions in bacterial pathogenesis.
- Mammalian glycosylation in immunity.
- Protein-glycan interactions in innate and adaptive immunity.
- N-glycosylation and inflammation.
- Glycosylation in cancer immune modulation and metastasis.
- IgG glycosylation as immune modulator and biomarker.

Search terms:

- `glycans host pathogen interaction review`
- `glycosylation immunity review N-glycans`
- `N-glycosylation inflammation immune cells review`
- `glycosylation microbiome mucosal immunity review`
- `glycosylation cancer immune modulation metastasis review`
- `IgG glycosylation immune function review`

### 4. Disease Architecture of Glycosylation

Goal:

Test whether core pathway genes produce rare severe disease while downstream/interface genes are linked to subtler or context-dependent disease phenotypes.

Questions:

- Which N-glycosylation genes cause Congenital Disorders of Glycosylation?
- Are CDG genes enriched in upstream/core machinery?
- Are downstream glycosylation genes more often linked to cancer, immune regulation, inflammatory disease, infection, or quantitative traits?
- How should Mendelian and complex disease evidence be weighted?

Seed references and leads:

- GeneReviews on congenital disorders of N-linked glycosylation.
- CDG reviews and disease gene tables.
- ClinVar/OMIM disease annotations.
- GWAS Catalog for glycosylation, IgG glycosylation, inflammation, immunity, cancer, and infection traits.

Search terms:

- `congenital disorders N-linked glycosylation review`
- `N-glycosylation genes congenital disorders glycosylation table`
- `glycosyltransferase cancer GWAS immune disease`
- `IgG N-glycosylation GWAS`
- `glycosylation autoimmune disease genetic variation`

### 5. Pathway and Network Biology

Goal:

Find methods and concepts for treating pathway position as an explanatory variable.

Questions:

- How are pathway topology, depth, branch points, redundancy, flux, and controllability linked to evolutionary constraint?
- What network features predict essentiality or disease burden?
- Are there graph-learning or pathway-learning approaches that predict evolutionary regimes?
- What null models are appropriate for pathway-level claims?

Seed references and leads:

- Network-level molecular evolution papers.
- Metabolic network structure and enzyme evolution.
- Protein interaction network centrality and constraint literature.
- Modern graph machine learning for biological networks, but only after simple baselines.

Search terms:

- `pathway topology evolutionary constraint genes`
- `metabolic network structure enzyme evolution constraint`
- `network centrality gene essentiality disease evolutionary rate`
- `graph neural network biological network evolutionary constraint`
- `pathway depth evolutionary constraint disease genes`

### 6. Comparative Pathway Framing

Goal:

Decide whether to generalize beyond N-glycosylation.

Questions:

- Which pathways are good examples of robustness-heavy cores?
- Which pathways are good examples of evolvable interfaces?
- Can a small comparator set strengthen the paper without turning it into an overlarge atlas?

Candidate comparators:

- Core ER protein folding and ER-associated degradation.
- Ribosome/translation or central metabolism as constrained-core controls.
- MHC/antigen presentation or immune receptor systems as interface controls.
- Olfactory receptors as a high-variation environmental sensing system.
- Mucins and glycocalyx-related pathways as adjacent glycan-interface systems.

Search terms:

- `immune receptor evolution diversification review`
- `MHC evolution balancing selection review`
- `olfactory receptor evolution human variation review`
- `core metabolism evolutionary constraint human disease genes`
- `ER protein folding pathway disease evolutionary constraint`

## Screening Rules

Prioritize:

- reviews that define the conceptual field
- primary papers with reusable data or clear quantitative methods
- papers that provide tables of genes, disease annotations, or pathway structure
- papers with direct relevance to N-glycosylation or glycan-mediated interface biology

Deprioritize:

- selection-scan papers without functional or architectural interpretation
- broad glycosylation reviews that do not distinguish pathway regions
- disease association papers with no clear gene-level or pathway-level evidence
- machine-learning papers without interpretable features or convincing baselines

## Evidence Extraction Template

For each important paper, record:

- citation
- DOI or URL
- literature cluster
- main claim
- relevance to robustness/evolvability architecture
- genes/pathways/data used
- whether it supports upstream-core, downstream-interface, disease-gradient, or general-architecture claims
- limitations
- whether it should be cited in introduction, methods, results, or discussion

## Initial Seed Sources

These sources were identified in the first pass and should be checked carefully:

- Biological robustness, Nature Reviews Genetics.
- Pervasive robustness in biological systems, Nature Reviews Genetics.
- The causes of evolvability and their evolution, Nature Reviews Genetics.
- Degeneracy as a link between evolvability, robustness, and complexity in biological systems.
- Sloppiness, robustness, and evolvability in systems biology.
- Evolutionary forces shaping the Golgi glycosylation machinery, Cold Spring Harbor Perspectives in Biology.
- Glycointeractions in bacterial pathogenesis, Nature Reviews Microbiology.
- Mammalian glycosylation in immunity, Nature Reviews Immunology.
- Protein-glycan interactions in innate and adaptive immune responses, Nature Immunology.
- The Glycoscience of Immunity.
- N-glycosylation and inflammation.
- Congenital Disorders of N-Linked Glycosylation and Multiple Pathway Overview, GeneReviews.
- Centralized modularity of N-linked glycosylation pathways in mammalian cells.

## Immediate Next Step

Create a structured bibliography table:

`docs/concept/literature-matrix.tsv`

Columns:

- `citation_key`
- `year`
- `title`
- `authors`
- `journal`
- `doi_or_url`
- `cluster`
- `paper_role`
- `main_claim`
- `supports_claim`
- `important_genes_or_pathways`
- `limitations`
- `priority`

