.PHONY: help agentic-inspect agentic-check agentic-next agentic-prompt architecture-features constraint-summary constraint-gradient constraint-network-plots disease-seed-table clinvar-disease-layer gwas-trait-layer disease-architecture-plot downstream-gwas-audit ti

PYTHON ?= uv run python
AGENTIC_REGISTRY ?= workflow/agentic_paper_system.json
TASK ?=
CONSTRAINT_METRICS ?=
CONSTRAINT_DATASET_VERSION ?= gnomAD_v4.1.1
CLINVAR_VARIANT_SUMMARY ?= data/external/clinvar/variant_summary.txt.gz
GWAS_CATALOG_ASSOCIATIONS ?= data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip

help:
	@printf "%s\n" "Available targets:"
	@printf "  %-18s %s\n" "agentic-inspect" "Summarize agents, gates, and ready backlog items."
	@printf "  %-18s %s\n" "agentic-check" "Compile the inspector and validate the agentic registry."
	@printf "  %-18s %s\n" "agentic-next" "Show the next ready agentic paper tasks."
	@printf "  %-18s %s\n" "agentic-prompt" "Create a Codex prompt for TASK=<task id>, or the first ready task."
	@printf "  %-18s %s\n" "architecture-features" "Build first-pass N-glycosylation architecture feature tables."
	@printf "  %-18s %s\n" "constraint-summary" "Join a local constraint TSV and summarize by pathway region."
	@printf "  %-18s %s\n" "constraint-gradient" "Analyze and plot provisional constraint gradients."
	@printf "  %-18s %s\n" "constraint-network-plots" "Plot full pathway network colored by LOEUF and missense Z."
	@printf "  %-18s %s\n" "disease-seed-table" "Build first-pass CDG seed annotations from GeneReviews."
	@printf "  %-18s %s\n" "clinvar-disease-layer" "Add ClinVar germline P/LP counts to disease annotations."
	@printf "  %-18s %s\n" "gwas-trait-layer" "Add GWAS Catalog mapped/reported gene trait categories."
	@printf "  %-18s %s\n" "disease-architecture-plot" "Plot CDG, ClinVar, and GWAS trait evidence layers."
	@printf "  %-18s %s\n" "downstream-gwas-audit" "Audit downstream GWAS/glycome candidate examples."
	@printf "  %-18s %s\n" "ti" "Alias for agentic-inspect."

agentic-inspect:
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY)

agentic-check:
	$(PYTHON) -m py_compile scripts/inspect_agentic_system.py
	$(PYTHON) -m py_compile scripts/create_agentic_task_prompt.py
	$(PYTHON) -m py_compile scripts/build_nglyco_architecture_features.py
	$(PYTHON) -m py_compile scripts/build_nglyco_constraint_summary.py
	$(PYTHON) -m py_compile scripts/analyze_constraint_gradient.py
	$(PYTHON) -m py_compile scripts/plot_nglyco_constraint_network.py
	$(PYTHON) -m py_compile scripts/build_nglyco_disease_seed_table.py
	$(PYTHON) -m py_compile scripts/add_nglyco_clinvar_layer.py
	$(PYTHON) -m py_compile scripts/add_nglyco_gwas_trait_layer.py
	$(PYTHON) -m py_compile scripts/plot_disease_architecture.py
	$(PYTHON) -m py_compile scripts/audit_downstream_gwas_candidates.py
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY)

agentic-next:
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY) | sed -n '/Near-term backlog/,$$p'

agentic-prompt:
	$(PYTHON) scripts/create_agentic_task_prompt.py --registry $(AGENTIC_REGISTRY) $(if $(TASK),--task $(TASK),)

architecture-features:
	$(PYTHON) scripts/build_nglyco_architecture_features.py

constraint-summary:
	@test -n "$(CONSTRAINT_METRICS)" || (printf "%s\n" "Set CONSTRAINT_METRICS=/path/to/gnomad.constraint_metrics.tsv"; exit 2)
	$(PYTHON) scripts/build_nglyco_constraint_summary.py --constraint-metrics "$(CONSTRAINT_METRICS)" --dataset-version "$(CONSTRAINT_DATASET_VERSION)"

constraint-gradient:
	$(PYTHON) scripts/analyze_constraint_gradient.py

constraint-network-plots:
	$(PYTHON) scripts/plot_nglyco_constraint_network.py --metric loeuf --output-png results/figures/nglyco_pathway_constraint_loeuf.png --output-svg results/figures/nglyco_pathway_constraint_loeuf.svg
	$(PYTHON) scripts/plot_nglyco_constraint_network.py --metric mis_z --output-png results/figures/nglyco_pathway_constraint_mis_z.png --output-svg results/figures/nglyco_pathway_constraint_mis_z.svg

disease-seed-table:
	$(PYTHON) scripts/build_nglyco_disease_seed_table.py

clinvar-disease-layer:
	@test -f "$(CLINVAR_VARIANT_SUMMARY)" || (printf "%s\n" "Set CLINVAR_VARIANT_SUMMARY=/path/to/variant_summary.txt.gz"; exit 2)
	$(PYTHON) scripts/add_nglyco_clinvar_layer.py --clinvar-variant-summary "$(CLINVAR_VARIANT_SUMMARY)"

gwas-trait-layer:
	@test -f "$(GWAS_CATALOG_ASSOCIATIONS)" || (printf "%s\n" "Set GWAS_CATALOG_ASSOCIATIONS=/path/to/gwas_catalog_associations.zip"; exit 2)
	$(PYTHON) scripts/add_nglyco_gwas_trait_layer.py --gwas-catalog-zip "$(GWAS_CATALOG_ASSOCIATIONS)"

disease-architecture-plot:
	$(PYTHON) scripts/plot_disease_architecture.py

downstream-gwas-audit:
	$(PYTHON) scripts/audit_downstream_gwas_candidates.py

ti: agentic-inspect
