# Linear Pathway Comparators

Date: 2026-05-21

## Purpose

This note records a future direction discussed during project planning: whether the N-glycosylation robustness/evolvability framework could later be compared with other human pathways that have a strongly ordered, assembly-line-like core.

Decision for now: defer broad cross-pathway expansion. Use this note only to preserve candidate comparators and design logic.

## Why This Matters

The first part of N-glycosylation is unusually useful because it has a directional core: ordered precursor assembly, membrane translocation, oligosaccharyltransferase transfer, and early ER quality-control processing. This makes the pathway easier to interpret as an architecture with a catastrophic core and more evolvable downstream/interface layers.

Other pathways with a similar linear or quasi-linear core could later help test whether this architecture is specific to N-glycosylation or part of a broader systems principle.

## Candidate Human Pathways

These are not yet curated gene sets. They are candidates for later systematic evaluation.

### High-priority candidates

1. **GPI-anchor biosynthesis**

   Rationale: Like N-glycosylation, GPI-anchor biosynthesis is an ordered ER-associated glycan/lipid assembly process. It begins on the cytoplasmic ER leaflet, continues after membrane flipping, and ends with protein attachment and remodeling. It is likely the closest architectural cousin to early N-glycosylation.

   Why useful:

   - stepwise biosynthetic logic
   - membrane-sided topology
   - strong disease relevance through inherited GPI-anchor deficiencies
   - downstream cell-surface/interface relevance

   Main caution: It is not simply linear; later remodeling and protein-context effects complicate the architecture.

2. **Heme biosynthesis**

   Rationale: Heme biosynthesis is a compact ordered enzymatic pathway with well-defined intermediates and clinically interpretable partial defects.

   Why useful:

   - clear linear sequence
   - strong genotype-phenotype interpretability through porphyrias and related disorders
   - good comparator for catastrophic-core logic without being a glycosylation pathway

   Main caution: It may mostly test constraint and toxicity of intermediates rather than interface-layer evolvability.

3. **Cholesterol biosynthesis / sterol synthesis**

   Rationale: Sterol synthesis has ordered biochemical structure and many disease-relevant enzymes, but includes alternative routes and branch points.

   Why useful:

   - developmentally and physiologically important
   - medically well studied
   - has linear stretches plus biologically meaningful branches

   Main caution: It is not as cleanly linear as early N-glycosylation; upstream mevalonate/isoprenoid metabolism feeds many products, and late sterol synthesis can follow alternative routes.

4. **Coenzyme Q / ubiquinone biosynthesis**

   Rationale: CoQ biosynthesis is a mitochondrial pathway with ordered modification of a quinone precursor and severe disease associations.

   Why useful:

   - compact mitochondrial biosynthetic system
   - strong link to energy metabolism and severe inherited disease
   - useful constrained-core comparator

   Main caution: The human pathway includes multiprotein complexes and accessory factors, so simple step order may be harder to encode than in textbook diagrams.

### Medium-priority candidates

5. **Dolichol and dolichol-linked precursor biosynthesis**

   Rationale: This pathway is tightly connected to N-glycosylation substrate supply and congenital disorders of glycosylation.

   Why useful:

   - mechanistically adjacent to the current case study
   - useful for separating substrate biosynthesis from glycan assembly

   Main caution: Because it is adjacent to N-glycosylation, it may not provide an independent comparator.

6. **Glycosaminoglycan linker and chain initiation**

   Rationale: Proteoglycan glycosaminoglycan biosynthesis has ordered initiation steps followed by polymerization and modification.

   Why useful:

   - another glycan-related system with core construction and downstream modification
   - potentially useful for comparing different glycan architectures

   Main caution: Polymerization and modification are more combinatorial than strictly linear.

7. **Nucleotide de novo biosynthesis**

   Rationale: Purine and pyrimidine biosynthesis contain ordered enzymatic sequences and severe metabolic disease biology.

   Why useful:

   - classic linear metabolic architecture
   - good negative or constrained-core comparator

   Main caution: These pathways may lack a clear downstream environmental-interface layer, so they are better controls than positive analogies.

8. **One-carbon / folate cycle modules**

   Rationale: These pathways are highly structured, directional in places, and clinically important.

   Why useful:

   - rich disease and trait literature
   - interacts with methylation, development, and metabolism

   Main caution: Cyclic and network-like structure makes "linear pathway" classification less clean.

## Working Classification

For future comparator work, classify pathways into three buckets:

- **Linear core plus interface layer:** most similar to the N-glycosylation hypothesis. Best candidate: GPI-anchor biosynthesis.
- **Linear constrained core without obvious interface layer:** useful negative or contrastive comparators. Best candidates: heme biosynthesis, nucleotide biosynthesis, CoQ biosynthesis.
- **Quasi-linear core with branching/modular outputs:** useful for testing whether branch points and redundancy alter constraint. Best candidates: cholesterol biosynthesis, glycosaminoglycan biosynthesis, folate/one-carbon metabolism.

## Implications For The Current Paper

The current paper should remain centered on N-glycosylation. A small comparator section could mention one or two pathways only if it helps clarify the architecture framework.

Recommended immediate use:

- Do not curate all comparator pathways now.
- Use GPI-anchor biosynthesis as the strongest future positive comparator.
- Use heme biosynthesis as the strongest future constrained-core contrast.
- Mention broad cross-pathway analysis as a future framework, not a current deliverable.

## Possible Future Analysis

If this becomes a second paper or major extension:

1. Build curated gene and reaction tables for 6-10 comparator pathways.
2. Encode ordered position, branch status, redundancy, checkpoint proximity, and terminal/interface role.
3. Compare constraint, ClinVar/OMIM disease burden, GWAS associations, expression breadth, and tolerated variation.
4. Test whether architecture features explain variation better than pathway identity alone.
5. Only after curated comparators work, scale cautiously to Reactome-wide or MSigDB-wide gene sets.

## Initial Source Anchors To Check Later

- Reactome: GPI-anchor biosynthetic process, synthesis of GPI, and post-translational modification by GPI anchoring.
- Reactome: heme biosynthesis.
- Reactome: cholesterol biosynthesis.
- Reactome / BioCyc / primary reviews: human CoQ10 biosynthesis.
- Essentials of Glycobiology: GPI anchors and glycosaminoglycan biosynthesis chapters.

