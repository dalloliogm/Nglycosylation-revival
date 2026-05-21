# N-glycosylation Pathway Curation

Started: 2026-05-21

## Purpose

This note defines the first-pass gene curation rules for the N-glycosylation evolutionary architecture project. The goal is not to reproduce every Reactome participant under `R-HSA-446203`, because that top-level pathway also pulls in generic ER-Golgi transport, cargo proteins, substrate metabolism, and glycan-binding reactions. The analysis gene set should instead distinguish direct N-glycan biosynthesis and processing enzymes from supporting substrate and quality-control machinery.

Primary output:

- `data/processed/nglyco_gene_table.tsv`

## Source Priority

Primary sources:

- Reactome `R-HSA-446203`, Asparagine N-linked glycosylation, release 96 checked on 2026-05-21.
- Reactome child events:
  - `R-HSA-446193`, biosynthesis of the N-glycan precursor and transfer to a nascent protein.
  - `R-HSA-446209`, transfer of N-glycan to protein.
  - `R-HSA-532668`, ER trimming and calnexin/calreticulin cycle.
  - `R-HSA-948021`, transport to Golgi and subsequent modification.
  - `R-HSA-975576`, N-glycan antennae elongation in medial/trans-Golgi.
  - `R-HSA-975578`, complex N-glycan synthesis.
  - `R-HSA-975574`, hybrid N-glycan synthesis.
- Essentials of Glycobiology, 4th edition, Chapter 9, N-Glycans.

Secondary cross-check sources to add in the next pass:

- GlyGen gene and glycan-pathway records.
- UniProt function records.
- Direct HGNC/Ensembl stable gene identifier and GRCh38 coordinate validation.
- Gene Ontology `GO:0006487` and narrower N-glycan biosynthetic process terms.

Identifier source:

- `data/processed/nglyco_gene_table.tsv` Ensembl IDs and coordinate fields were populated from MyGene.info `symbol`, `ensembl.gene`, and `genomic_pos` fields on 2026-05-21. Treat these as provisional until direct Ensembl/HGNC validation is complete.

## Inclusion Rules

`include_primary = yes` means the gene is eligible for the main architecture analyses.

Include in the primary set when the gene product directly participates in one of these roles:

- Assembly of the lipid-linked oligosaccharide precursor.
- Transfer of the N-glycan to nascent protein by the OST complex.
- Direct ER trimming or reglucosylation of N-glycans in quality control.
- Golgi mannose trimming, GlcNAc branching, core fucosylation, galactosylation, sialylation, or other curated terminal N-glycan modification.

Use `include_primary = no` and `include_sensitivity = yes` for genes that support N-glycosylation but should not drive the main test:

- Nucleotide-sugar or dolichol substrate biosynthesis.
- Broad ERAD or cargo transport genes.
- Glycoprotein cargo proteins.
- General vesicle trafficking genes that Reactome includes because mature glycoproteins move through ER/Golgi.

Exclude from the table for now:

- Generic COPI/COPII, SNARE, cytoskeleton, and cargo-loading genes unless a later analysis explicitly tests transport biology.
- Recipient glycoproteins such as `UMOD`, `CGA`, `LHB`, `F5`, `F8`, or `SERPINA1`.
- Broad lysosomal degradation genes unless the analysis is specifically about N-glycan turnover.

## Region Labels

Use `primary_region` as the main biological label:

- `substrate_biosynthesis`: sugar-nucleotide, dolichol, and transporter genes that supply substrates.
- `llo_assembly`: conserved lipid-linked oligosaccharide assembly before transfer to protein.
- `ost_transfer`: oligosaccharyltransferase complex and accessory subunits.
- `er_quality_control`: ER glycan trimming, reglucosylation, chaperone recognition, and ERAD-proximal glycan processing.
- `golgi_core_processing`: early Golgi trimming and conversion toward hybrid/complex N-glycans.
- `golgi_branching`: GlcNAc branching and bisecting reactions that expand glycan structural space.
- `terminal_modification`: galactosylation, sialylation, fucosylation, sulfation, and terminal/interface modifications.

Use `analysis_group` for coarse hypothesis tests:

- `upstream_core`: `llo_assembly` and `ost_transfer`.
- `checkpoint_layer`: `er_quality_control`.
- `downstream_diversification`: `golgi_core_processing`, `golgi_branching`, and `terminal_modification`.
- `substrate_support`: `substrate_biosynthesis`.

The default primary contrast should be `upstream_core` versus `downstream_diversification`. The `checkpoint_layer` and `substrate_support` groups should be analyzed separately unless the question explicitly motivates merging them.

## Current Limitations

This is a first-pass curation. Ensembl IDs and coordinates have been filled from MyGene.info, but before quantitative analysis they should be cross-checked directly against Ensembl/HGNC and frozen as a named curation version.

Several terminal-modification genes are not N-glycan-exclusive. They are retained because Reactome places their reactions on N-glycan structures, but downstream analyses should test sensitivity to excluding low-specificity enzymes.

The Reactome top-level participant list is broader than the biological gene set used here. This is a feature, not an error: generic trafficking and cargo genes would dilute the pathway-architecture hypothesis.
