# Constraint Gradient Interpretation

Date: 2026-06-03

Dataset: provisional `gnomAD_v4.1` gene constraint metrics joined to the curated N-glycosylation architecture table.

## Short Result

The first constraint analysis does not support a simple "upstream equals more constrained, downstream equals less constrained" model.

In this run, upstream-core genes have higher median LOEUF than downstream-diversification genes, meaning they appear less loss-of-function constrained as a group. The checkpoint layer is more LoF-constrained than the upstream-core bin and is closer to the downstream-diversification median. Missense Z is higher in downstream-diversification genes than in upstream-core genes in the primary contrast.

## Interpretation

This result argues against treating pathway depth alone as the architecture signal. A sharper hypothesis is that constraint concentrates at high-dependency or catastrophic-impact nodes, including OST transfer, ER quality-control/checkpoint genes, and some downstream branching or terminal genes that affect many mature glycan outputs.

The result also suggests that downstream diversification should not be equated with weak coding constraint. Downstream evolvability may instead appear through regulatory variation, tissue-specific deployment, trait associations, glycan-output variation, or disease architecture rather than simple tolerance of coding disruption.

## Examples

Genes with strong LoF-constraint signals include `RPN1`, `STT3A`, `STT3B`, `GANAB`, `CALR`, `PDIA3`, `MGAT5`, and `B4GALT5`. This spans OST transfer, ER quality control, and downstream glycan-output layers.

Six genes lacked matched metrics in the provisional gnomAD v4.1 file: `GNPNAT1`, `ALG13`, `RPN2`, `MAGT1`, `CANX`, and `MGAT4B`.

## Claim Level

Treat this as a provisional architecture result and a hypothesis-refinement step. It should not be used to claim that downstream genes are generally more constrained or that the robustness/evolvability model is wrong. The correct next test is whether disease architecture, essentiality, expression breadth, and trait/glycome evidence separate catastrophic-core biology from interface-layer biology more clearly than LOEUF alone.
