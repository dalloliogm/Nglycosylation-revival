# Linear Pathway Comparators

Date: 2026-05-21

## Purpose

This note records a future direction discussed during project planning: whether the N-glycosylation robustness/evolvability framework could later be compared with other human pathways that have a strongly ordered, assembly-line-like core.

Decision for now: defer broad cross-pathway expansion. Preserve a smaller option for the first paper: include 1-3 comparator pathways only as a controlled contrast to N-glycosylation, not as a Reactome-wide or multi-pathway survey.

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

## Option For The Current Paper: 1-3 Comparator Pathways

The current paper can include a small comparator module if it strengthens the central claim without diluting the N-glycosylation case study.

The comparator question should be narrow:

> Does N-glycosylation show a stronger internal core-to-interface gradient than conserved linear pathways whose main function is essential biochemical production?

This module should test specificity, not replace the main analysis. N-glycosylation remains the primary case study; comparator pathways only help distinguish an N-glycosylation-specific architecture from generic properties of essential pathways.

### Recommended Minimal Set

Use no more than three comparator pathways:

1. **Heme biosynthesis** as the cleanest conserved linear metabolic comparator.
2. **CoQ / ubiquinone biosynthesis** as a compact mitochondrial constrained-core comparator.
3. **GPI-anchor biosynthesis** as an optional positive comparator with a glycan/cell-surface interface component.

If the scope must be even smaller, use heme biosynthesis alone as the negative comparator. If the paper needs one positive analogy, add GPI-anchor biosynthesis. CoQ is useful if a second conserved-process comparator is needed.

### In-Scope Comparator Analyses

The lightweight comparator module should use the same evidence categories as the N-glycosylation analysis, but at lower resolution:

- curated pathway gene list and ordered pathway position
- broad region labels such as early/core, late/output, branch/interface, or ambiguous
- constraint and tolerated-variation summaries
- severe Mendelian disease burden
- broad trait-association or interface-phenotype evidence, only where gene assignment is clear

The comparator module should not attempt full population-genetic scans, detailed network centrality, or extensive mechanistic storytelling for every pathway.

### Decision Criteria

Include the 1-3 pathway comparator module in the first paper if:

- N-glycosylation shows an apparent gradient that needs a specificity check.
- Comparator gene sets can be curated with clear source provenance.
- The added analysis can be completed as one compact figure, table, or supplemental result.
- The comparator result clarifies whether the observed pattern is generic essential-pathway constraint or a core/interface architecture signal.

Defer comparator pathways to a second paper if:

- pathway curation becomes ambiguous or slow;
- comparator analysis delays the core N-glycosylation result;
- the evidence would require extensive pathway-specific biological interpretation;
- the first paper is better framed as a focused case study plus a future generalization agenda.

### Claim Limits

Even if included, the comparator module should only support claims such as:

- "N-glycosylation was compared with selected conserved-process pathways as a specificity check."
- "The comparator results suggest whether the observed gradient is generic to essential pathways or stronger in core/interface architectures."
- "Broader pathway generalization remains a future test."

It should not claim that 1-3 pathways prove a universal biological design principle.

## Implications For The Current Paper

The current paper should remain centered on N-glycosylation. A small comparator section could include one to three pathways only if it helps clarify the architecture framework.

Recommended immediate use:

- Do not curate all comparator pathways now.
- Use GPI-anchor biosynthesis as the strongest future positive comparator.
- Use heme biosynthesis as the strongest future constrained-core contrast.
- Treat a 1-3 pathway comparison as optional scope for the first paper, with broad cross-pathway analysis left as a future framework.

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
