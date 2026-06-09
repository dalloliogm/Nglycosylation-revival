# Architecture Metrics

Date drafted: 2026-05-31

Agentic work unit: `define_architecture_metrics`

Agent role: `architecture_agent`

## Purpose

This note defines the pathway-architecture variables that will later be computed or curated for each N-glycosylation gene. The goal is to convert the robustness/evolvability thesis into measurable features before running constraint, disease, trait, or regulatory analyses.

Primary future output:

- `data/processed/nglyco_architecture_features.tsv`

Primary inputs:

- `data/processed/nglyco_gene_table.tsv`
- `data/processed/nglyco_gene_gene_edges.tsv`
- `docs/methods/pathway-curation.md`
- `docs/methods/pathway-edge-curation.md`
- `docs/concept/claims-register.md`

## Unit Of Analysis

The default unit is a human gene in `data/processed/nglyco_gene_table.tsv`.

Use all genes in the table for annotation, but define analysis scopes explicitly:

- `primary_analysis`: genes with `include_primary = yes`.
- `sensitivity_analysis`: genes with `include_sensitivity = yes`, especially substrate-support genes and low-specificity terminal-modification enzymes.
- `excluded_from_primary_contrast`: substrate biosynthesis, donor-supply, broad transport, cargo, or low-specificity support genes unless a specific test includes them.

The default contrast is `upstream_core` versus `downstream_diversification`. `checkpoint_layer` and `substrate_support` should remain separate unless a model explicitly merges them.

## Core Columns

The architecture feature table should include these identity and provenance columns:

| Column | Type | Source | Notes |
| --- | --- | --- | --- |
| `symbol` | string | gene table | HGNC symbol. |
| `ensembl_gene_id` | string | gene table | Provisional until Ensembl/HGNC validation is complete. |
| `primary_region` | category | gene table | Fine pathway label. |
| `analysis_group` | category | gene table | Coarse hypothesis label. |
| `include_primary` | yes/no | gene table | Main analysis eligibility. |
| `include_sensitivity` | yes/no | gene table | Sensitivity analysis eligibility. |
| `curation_confidence` | category | gene table | Existing gene-label confidence. |
| `architecture_version` | string | new | Version tag for this feature build. |
| `architecture_notes` | string | new | Short rationale or caveat for ambiguous genes. |

## Pathway-Position Features

These features test whether position in the biochemical process predicts constraint, disease burden, or glycan-output variation.

| Column | Type | Definition | Source or rule |
| --- | --- | --- | --- |
| `pathway_depth_rank` | integer or null | Ordered position from substrate support/LLO assembly through terminal modification. | Curated from `primary_region` and gene-edge graph. |
| `pathway_depth_scaled` | numeric or null | `pathway_depth_rank` scaled 0-1 within the primary pathway graph. | Derived after depth ranking. |
| `is_upstream_core` | boolean | `analysis_group = upstream_core`. | Gene table. |
| `is_checkpoint_layer` | boolean | `analysis_group = checkpoint_layer`. | Gene table. |
| `is_downstream_diversification` | boolean | `analysis_group = downstream_diversification`. | Gene table. |
| `is_substrate_support` | boolean | `analysis_group = substrate_support`. | Gene table. |

Depth should be interpreted as an ordered pathway descriptor, not as evidence of causality. Downstream Golgi reactions are combinatorial and partly generic in Reactome, so exact depths for branching and terminal enzymes should be binned rather than over-precise.

Recommended first-pass depth bins:

1. `substrate_support`
2. `llo_assembly`
3. `ost_transfer`
4. `er_quality_control`
5. `golgi_core_processing`
6. `golgi_branching`
7. `terminal_modification`

## Robustness And Catastrophic-Potential Features

These features operationalize the "robustness layer" without claiming evolved design.

| Column | Type | Definition | Interpretation |
| --- | --- | --- | --- |
| `checkpoint_proximity` | category | `direct`, `adjacent`, `distant`, or `not_applicable` relative to ER quality-control processing. | Tests whether quality-control proximity correlates with constraint or severe disease. |
| `ost_or_lbo_core_member` | boolean | Gene participates in LLO assembly or OST transfer. | Expected catastrophic-core feature. |
| `er_quality_control_member` | boolean | Gene participates in ER trimming, reglucosylation, or calnexin/calreticulin-related glycan processing. | Checkpoint-layer feature. |
| `catastrophic_potential_prior` | category | `high`, `moderate`, `low`, or `unknown` based only on pathway role, not disease results. | Prior feature for later testing against disease/constraint. |

Do not assign `catastrophic_potential_prior` using ClinVar, OMIM, or gnomAD results, because those are outcomes to be tested. Use pathway role only.

First-pass rule:

- `high`: LLO assembly, OST transfer, or direct ER quality-control glycan processing.
- `moderate`: Golgi core processing genes that affect broad maturation routes.
- `low`: terminal or tissue/context-specific modification genes.
- `unknown`: substrate-support or ambiguous genes unless a specific role is clear.

## Evolvability And Interface Features

These features operationalize downstream/interface potential while avoiding claims of adaptation.

| Column | Type | Definition | Interpretation |
| --- | --- | --- | --- |
| `branching_role` | category | `branch_initiation`, `branch_extension`, `not_branching`, or `unknown`. | Tests whether branch-related genes show weaker constraint or richer trait links. |
| `terminal_modification_role` | boolean | Gene adds or modifies terminal glycan features. | Proxy for interface-facing glycan output. |
| `interface_layer_prior` | category | `high`, `moderate`, `low`, or `unknown`. | Prior classification for environment-facing glycan output. |
| `glycan_output_layer` | boolean | Gene plausibly changes mature glycan structures rather than precursor/core transfer only. | Used for glycome GWAS and trait mapping. |
| `regulatory_or_trans_layer_candidate` | boolean | Gene is not necessarily an enzyme in the pathway but may regulate glycan output if included in later glycome genetics evidence. | Mostly false in the current pathway table; relevant for later mapped GWAS loci. |

First-pass `interface_layer_prior` rule:

- `high`: terminal modification and low-specificity cell-surface glycan elaboration genes.
- `moderate`: Golgi branching and complex/hybrid processing genes.
- `low`: LLO assembly, OST transfer, and ER quality-control genes.
- `unknown`: substrate-support genes unless glycan-output evidence justifies a separate label.

## Redundancy And Paralog Features

These features test whether redundancy and paralogy are associated with tolerated variation or interface-facing glycan diversity.

| Column | Type | Definition | Source or rule |
| --- | --- | --- | --- |
| `has_paralog_family` | boolean | Gene belongs to an enzyme family with multiple human paralogs in the curated pathway or close glyco-gene family. | Curate from symbols, HGNC families, UniProt, or GlyGen. |
| `paralog_family_name` | string or null | Family label, such as `ALG`, `ST3GAL`, `ST6GAL`, `B4GALT`, `FUT`, `MGAT`. | Curated. |
| `redundancy_prior` | category | `high`, `moderate`, `low`, or `unknown`. | Based on family size and reaction overlap, not variation outcomes. |
| `low_specificity_terminal_enzyme` | boolean | Terminal-modification gene has broad substrate or glycan-class specificity. | Used for sensitivity analyses. |

Low-specificity terminal enzymes should remain flagged because they may drive apparent downstream signals without being N-glycan-specific.

## Graph Features

Graph features should be computed from `data/processed/nglyco_gene_gene_edges.tsv` only after choosing an edge set.

Define at least three graph encodings:

| Graph encoding | Included edges | Purpose |
| --- | --- | --- |
| `primary_reaction_graph` | `metabolite_intermediate`, `glycoprotein_intermediate`, `quality_control_cycle`, `complex_or_binding_context`; exclude `donor_substrate`. | Main pathway topology without donor-supply inflation. |
| `full_support_graph` | all edge classes. | Sensitivity analysis including substrate support. |
| `downstream_processing_graph` | Golgi processing, branching, and terminal-modification edges only. | Tests whether downstream topology has its own architecture. |

Candidate graph columns:

| Column | Type | Definition | Required caveat |
| --- | --- | --- | --- |
| `graph_in_degree` | integer | Number of incoming edges in selected graph. | Depends on graph encoding. |
| `graph_out_degree` | integer | Number of outgoing edges in selected graph. | Depends on graph encoding. |
| `graph_total_degree` | integer | In-degree plus out-degree. | Donor-substrate edges can inflate degree. |
| `graph_betweenness` | numeric | Betweenness centrality in selected graph. | Exploratory only. |
| `graph_closeness` | numeric | Closeness centrality in selected graph. | Exploratory only. |
| `graph_component_id` | string | Connected component label. | Useful for disconnected graph encodings. |

Centrality must not be used as the main explanatory claim unless results are robust across graph encodings and a sensible null model. Prefer interpretable features such as depth, branch role, checkpoint proximity, terminal modification, and substrate-support flags.

## External Features To Add Later

These are architecture-adjacent features that should be documented in their own methods notes when sourced:

| Feature | Future source | Use |
| --- | --- | --- |
| expression breadth | GTEx or comparable expression atlas | Control and tissue-deployment feature. |
| tissue specificity | GTEx, Human Protein Atlas, or glyco-relevant expression resource | Interface-layer test. |
| immune-cell expression | immune-cell expression atlas | Glycoimmunology/interface test. |
| essentiality | DepMap, mouse knockout, or curated essential-gene resource | Robustness/catastrophic-potential test. |
| glycome GWAS locus membership | literature extraction and GWAS Catalog/manual curation | Glycan-output/regulatory layer test. |
| eQTL/TWAS/methylation evidence | GTEx/eQTL Catalog/EWAS literature | Regulatory evolvability test. |

Do not mix these into the architecture table without provenance columns, source versions, and access dates.

## Planned Output Schema

Minimum first version of `data/processed/nglyco_architecture_features.tsv`:

```text
symbol
ensembl_gene_id
primary_region
analysis_group
include_primary
include_sensitivity
pathway_depth_rank
pathway_depth_scaled
is_upstream_core
is_checkpoint_layer
is_downstream_diversification
is_substrate_support
checkpoint_proximity
ost_or_lbo_core_member
er_quality_control_member
catastrophic_potential_prior
branching_role
terminal_modification_role
interface_layer_prior
glycan_output_layer
has_paralog_family
paralog_family_name
redundancy_prior
low_specificity_terminal_enzyme
architecture_version
architecture_notes
```

Graph metric columns should either use a suffix naming the graph encoding, such as `graph_total_degree_primary_reaction`, or live in a separate graph-metrics table to avoid ambiguity.

## Sensitivity Analyses

Run or document these sensitivity comparisons before making architecture claims:

1. Primary genes only versus primary plus sensitivity genes.
2. Excluding substrate-support genes.
3. Excluding low-specificity terminal-modification genes.
4. Treating `checkpoint_layer` separately versus merging it with `upstream_core`.
5. Graph metrics with and without `donor_substrate` edges.
6. Downstream Golgi genes binned broadly versus assigned exact depth ranks.
7. Region labels from current Reactome curation versus labels after GlyGen/UniProt/GO cross-check.

## Claim Limits

- Architecture features are predictors or descriptors, not proof of evolutionary mechanism.
- Constraint or severe disease enrichment can support catastrophic-potential claims, but does not prove selection for robustness.
- Richer downstream trait or glycome-output evidence can support an interface/evolvability model, but does not prove adaptive evolution.
- Population-genetic signals must remain candidate or hypothesis-generating unless independently validated.
- Network centrality is exploratory until robust across encodings and null models.

## Next Implementation Step

Create a script or documented curation pass that reads `data/processed/nglyco_gene_table.tsv` and writes the minimum first version of `data/processed/nglyco_architecture_features.tsv`. Manual fields such as paralog family, redundancy, and low-specificity terminal-enzyme status should either be curated in a separate TSV or added with explicit decision rules.
