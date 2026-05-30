.PHONY: help agentic-inspect agentic-check agentic-next agentic-prompt ti

PYTHON ?= uv run python
AGENTIC_REGISTRY ?= workflow/agentic_paper_system.json
TASK ?=

help:
	@printf "%s\n" "Available targets:"
	@printf "  %-18s %s\n" "agentic-inspect" "Summarize agents, gates, and ready backlog items."
	@printf "  %-18s %s\n" "agentic-check" "Compile the inspector and validate the agentic registry."
	@printf "  %-18s %s\n" "agentic-next" "Show the next ready agentic paper tasks."
	@printf "  %-18s %s\n" "agentic-prompt" "Create a Codex prompt for TASK=<task id>, or the first ready task."
	@printf "  %-18s %s\n" "ti" "Alias for agentic-inspect."

agentic-inspect:
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY)

agentic-check:
	$(PYTHON) -m py_compile scripts/inspect_agentic_system.py
	$(PYTHON) -m py_compile scripts/create_agentic_task_prompt.py
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY)

agentic-next:
	$(PYTHON) scripts/inspect_agentic_system.py --registry $(AGENTIC_REGISTRY) | sed -n '/Near-term backlog/,$$p'

agentic-prompt:
	$(PYTHON) scripts/create_agentic_task_prompt.py --registry $(AGENTIC_REGISTRY) $(if $(TASK),--task $(TASK),)

ti: agentic-inspect
