.PHONY: help agentic-inspect agentic-check agentic-next ti

PYTHON ?= uv run python
AGENTIC_REGISTRY ?= workflow/agentic_paper_system.json

help:
	@printf "%s\n" "Available targets:"
	@printf "  %-18s %s\n" "agentic-inspect" "Summarize agents, gates, and ready backlog items."
	@printf "  %-18s %s\n" "agentic-check" "Compile the inspector and validate the agentic registry."
	@printf "  %-18s %s\n" "agentic-next" "Show the next ready agentic paper tasks."
	@printf "  %-18s %s\n" "ti" "Alias for agentic-inspect."

agentic-inspect:
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY)

agentic-check:
	$(PYTHON) -m py_compile scripts/inspect_agentic_system.py
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY)

agentic-next:
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY) | sed -n '/Near-term backlog/,$$p'

ti: agentic-inspect
