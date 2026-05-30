#!/usr/bin/env python3
"""Inspect the paper agent registry and report ready backlog items."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_registry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def path_exists(repo_root: Path, artifact: str) -> bool:
    return (repo_root / artifact).exists()


def summarize(registry: dict, repo_root: Path) -> str:
    lines: list[str] = []
    lines.append(f"Project: {registry['project']}")
    lines.append(f"Registry version: {registry['version']}")
    lines.append("")

    lines.append("Agents")
    for agent in registry["agents"]:
        outputs = ", ".join(agent["outputs"])
        lines.append(f"- {agent['id']}: {agent['role']} Outputs: {outputs}")
    lines.append("")

    lines.append("Gates")
    for gate in registry["gates"]:
        lines.append(f"- {gate['id']}: {len(gate['requires'])} checks")
    lines.append("")

    lines.append("Near-term backlog")
    for task in registry["near_term_backlog"]:
        missing_prereqs = [
            item for item in task["prerequisites"] if not path_exists(repo_root, item)
        ]
        missing_outputs = [
            item for item in task["outputs"] if not path_exists(repo_root, item)
        ]
        status = "ready" if not missing_prereqs and missing_outputs else "blocked"
        if not missing_outputs:
            status = "complete"
        lines.append(
            f"- {task['id']} ({task['agent']}): {status}; "
            f"missing_outputs={missing_outputs}; missing_prerequisites={missing_prereqs}"
        )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize the agentic paper workflow registry."
    )
    parser.add_argument(
        "--registry",
        default="workflow/agentic_paper_system.json",
        help="Path to the agentic workflow registry.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    registry = load_registry(repo_root / args.registry)
    print(summarize(registry, repo_root))


if __name__ == "__main__":
    main()
