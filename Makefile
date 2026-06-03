.PHONY: help agentic-inspect agentic-check agentic-next agentic-prompt architecture-features constraint-summary constraint-gradient ti

PYTHON ?= uv run python
AGENTIC_REGISTRY ?= workflow/agentic_paper_system.json
TASK ?=
CONSTRAINT_METRICS ?=
CONSTRAINT_DATASET_VERSION ?= gnomAD_v4.1.1

help:
	@printf "%s\n" "Available targets:"
	@printf "  %-18s %s\n" "agentic-inspect" "Summarize agents, gates, and ready backlog items."
	@printf "  %-18s %s\n" "agentic-check" "Compile the inspector and validate the agentic registry."
	@printf "  %-18s %s\n" "agentic-next" "Show the next ready agentic paper tasks."
	@printf "  %-18s %s\n" "agentic-prompt" "Create a Codex prompt for TASK=<task id>, or the first ready task."
	@printf "  %-18s %s\n" "architecture-features" "Build first-pass N-glycosylation architecture feature tables."
	@printf "  %-18s %s\n" "constraint-summary" "Join a local constraint TSV and summarize by pathway region."
	@printf "  %-18s %s\n" "constraint-gradient" "Analyze and plot provisional constraint gradients."
	@printf "  %-18s %s\n" "ti" "Alias for agentic-inspect."

agentic-inspect:
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY)

agentic-check:
	$(PYTHON) -m py_compile scripts/inspect_agentic_system.py
	$(PYTHON) -m py_compile scripts/create_agentic_task_prompt.py
	$(PYTHON) -m py_compile scripts/build_nglyco_architecture_features.py
	$(PYTHON) -m py_compile scripts/build_nglyco_constraint_summary.py
	$(PYTHON) -m py_compile scripts/analyze_constraint_gradient.py
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

ti: agentic-inspect
