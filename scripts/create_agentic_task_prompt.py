#!/usr/bin/env python3
"""Create a Codex task prompt from an agentic workflow backlog item."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_registry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_by_id(items: list[dict], item_id: str, item_type: str) -> dict:
    for item in items:
        if item["id"] == item_id:
            return item
    available = ", ".join(item["id"] for item in items)
    raise SystemExit(f"Unknown {item_type} '{item_id}'. Available: {available}")


def first_ready_task(registry: dict, repo_root: Path) -> dict:
    for task in registry["near_term_backlog"]:
        missing_prereqs = [
            item for item in task["prerequisites"] if not (repo_root / item).exists()
        ]
        missing_outputs = [
            item for item in task["outputs"] if not (repo_root / item).exists()
        ]
        if not missing_prereqs and missing_outputs:
            return task
    raise SystemExit("No ready incomplete near-term backlog task found.")


def format_list(items: list[str]) -> str:
    return "\n".join(f"- `{item}`" for item in items)


def create_prompt(registry: dict, repo_root: Path, task_id: str | None) -> str:
    task = (
        find_by_id(registry["near_term_backlog"], task_id, "task")
        if task_id
        else first_ready_task(registry, repo_root)
    )
    agent = find_by_id(registry["agents"], task["agent"], "agent")
    gate_lookup = {gate["id"]: gate for gate in registry["gates"]}
    gate_lines: list[str] = []
    for gate_id in agent["gates"]:
        gate = gate_lookup[gate_id]
        checks = "; ".join(gate["requires"])
        gate_lines.append(f"- `{gate_id}`: {checks}")

    return f"""Use the agentic paper workflow to do one concrete work unit.

Task: `{task["id"]}`
Agent role: `{agent["id"]}`

Role description:
{agent["role"]}

Required inputs:
{format_list(agent["inputs"])}

Expected outputs:
{format_list(task["outputs"])}

Prerequisites:
{format_list(task["prerequisites"])}

Quality gates:
{chr(10).join(gate_lines)}

Execution rules:
- Read `STUDY.md` and the listed input files first.
- Make the smallest useful implementation that satisfies the task outputs.
- Use scripts or documented curation rules where possible.
- Update `STUDY.md` with the task status and a dated changelog entry.
- Run a relevant validation command.
- Commit only the files needed for this work unit.
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a Codex prompt for an agentic workflow task."
    )
    parser.add_argument(
        "--registry",
        default="workflow/agentic_paper_system.json",
        help="Path to the agentic workflow registry.",
    )
    parser.add_argument(
        "--task",
        help="Near-term backlog task id. Defaults to the first ready incomplete task.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    registry = load_registry(repo_root / args.registry)
    print(create_prompt(registry, repo_root, args.task))


if __name__ == "__main__":
    main()
