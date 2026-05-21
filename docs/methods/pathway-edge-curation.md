# N-glycosylation gene-edge curation

Created: 2026-05-21

## Purpose

`data/processed/nglyco_gene_gene_edges.tsv` is a gene-level abstraction of the N-glycosylation pathway for architecture analysis and visualization. Nodes are genes. Edges represent transfer of a glycan intermediate, use of a donor substrate, passage of a glycoprotein intermediate through a processing step, or participation in a complex/checkpoint context.

The table should not be interpreted as a complete atom-level reaction network. Downstream Golgi N-glycan topology is especially combinatorial and incompletely resolved, so several edges intentionally use generic labels such as `branched N-glycan acceptor` or `terminal N-glycan acceptor`.

## Source Hierarchy

Primary source layers:

- Reactome `R-HSA-446203`, Asparagine N-linked glycosylation.
- Reactome `R-HSA-446193`, Biosynthesis of the N-glycan precursor and transfer to a nascent protein.
- Reactome `R-HSA-446219`, Synthesis of substrates in N-glycan biosynthesis.
- Reactome `R-HSA-532668`, N-glycan trimming in the ER and Calnexin/Calreticulin cycle.
- Reactome `R-HSA-964739`, N-glycan trimming and elongation in the cis-Golgi.
- Reactome `R-HSA-975576`, N-glycan antennae elongation in the medial/trans-Golgi.
- KEGG `hsa00510`, N-Glycan biosynthesis, used as supporting pathway-level evidence for donor-substrate and enzyme-class context.

Reactome explicitly notes that the exact downstream N-glycan reaction topology is not fully established and that generic reactions are used for several antenna-modification enzymes. This repository follows that convention for the visualization layer rather than inventing exact glycan structures.

## Edge Classes

- `metabolite_intermediate`: adjacent reactions in LLO assembly and transfer, represented as a directed gene-to-gene chain through a shared LLO intermediate.
- `glycoprotein_intermediate`: processing steps after transfer to protein, represented through generic N-glycoprotein or N-glycan acceptor states.
- `donor_substrate`: substrate biosynthesis genes connected to enzymes that consume the relevant donor pool. These are supporting supply relationships, not direct sequential pathway steps.
- `quality_control_cycle`: recycling or ER quality-control relationships in the calnexin/calreticulin cycle.
- `complex_or_binding_context`: genes that participate in a shared complex or glycoprotein-binding/checkpoint context rather than transforming a metabolite directly.

## Confidence Labels

- `high`: direct curated pathway order or well-defined pathway event, abstracted only from reactions to gene-to-gene edges.
- `moderate`: curated pathway support exists, but the exact downstream topology is generic or incompletely resolved.
- `supporting`: source supports the donor pool or pathway membership, but the edge is an analysis abstraction.

## Known Limitations

- The table is not yet a full BioPAX/SBML-derived reaction graph.
- Edges are gene-level abstractions, so multi-subunit complexes and many-to-many donor relationships are simplified.
- Exact glycan structures are not curated in this pass.
- Donor-substrate edges can inflate graph density and should be treated separately in sensitivity analyses.
- GlyGen, UniProt, HGNC, and GO cross-checks remain pending for a later curation pass.
