# Modernized Analysis Plan

## Principle

Define the pathway architecture and testable predictions before running large scans. Each result should record dataset version, source, genome build, sample inclusion criteria, variant filters, gene list version, pathway classification rule, statistical method, software version, multiple-testing correction, and sensitivity analyses.

## Evidence Streams

- Gene table: stable gene IDs, current symbols, coordinates, pathway class, evidence source, and curation notes.
- Constraint: compare upstream and downstream regions using modern gene-level constraint and intolerance metrics.
- Disease architecture: test whether severe Mendelian disease burden concentrates upstream and whether complex-trait or regulatory associations are more frequent downstream.
- Standing variation: compare tolerated variation and rare damaging variant burden with matched controls.
- Population differentiation: use population-aware and region-aware methods, with careful matched nulls and local genomic covariates.
- Network architecture: rebuild the pathway graph from current sources and test sensitivity to alternative graph encodings.

## Controls and Sensitivities

Matched null sets should account for gene length, SNP density, recombination rate, background selection, mutation-rate proxies, expression breadth, mappability, and local genomic context where possible. Gene-boundary definitions should be tested across exons, gene bodies, promoters, and regulatory windows.
