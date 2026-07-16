#!/usr/bin/env python3
"""Run the AI Engineering Squad as a sequential CrewAI crew (pipeline)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from crewai import Agent, Crew, Process, Task

KIT_ROOT = Path(__file__).resolve().parents[2]
ROLES_DIR = KIT_ROOT / "roles"
OUT_ROOT = Path(__file__).resolve().parent


def load_role(role_id: str) -> str:
    path = ROLES_DIR / role_id / "AGENT.md"
    if not path.exists():
        raise FileNotFoundError(f"Missing role pack: {path}")
    return path.read_text(encoding="utf-8")


def extract_json_block(text: str) -> dict:
    """Parse the first JSON object from model output."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in agent output")
    return json.loads(match.group(0))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def maybe_validate(handoff_dir: Path) -> None:
    aesquad = KIT_ROOT / "packages" / "aesquad" / "bin" / "aesquad.mjs"
    if not aesquad.exists():
        print(f"Skip validate: missing {aesquad}", file=sys.stderr)
        return
    cmd = ["node", str(aesquad), "validate", "--dir", str(handoff_dir)]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=False)


def build_crew(change_id: str, idea: str) -> Crew:
    pm = Agent(
        role="Product Manager",
        goal="Produce a valid acceptance-package JSON for the change.",
        backstory=load_role("product-manager"),
        verbose=True,
        allow_delegation=False,
    )
    se = Agent(
        role="Senior Software Engineer",
        goal="Produce OpenSpec notes and a valid implementation-handoff JSON.",
        backstory=load_role("senior-software-engineer"),
        verbose=True,
        allow_delegation=False,
    )
    qa = Agent(
        role="QA Engineer",
        goal="Produce a valid risk-notes JSON for the change.",
        backstory=load_role("qa-engineer"),
        verbose=True,
        allow_delegation=False,
    )
    automation = Agent(
        role="Automation Engineer",
        goal="Produce a valid check-mapping JSON for the change.",
        backstory=load_role("automation-engineer"),
        verbose=True,
        allow_delegation=False,
    )

    pm_task = Task(
        description=(
            f"changeId must be exactly `{change_id}`.\n"
            f"Idea: {idea}\n\n"
            "Write ONLY a JSON object matching the kit acceptance-package schema "
            "(schemaVersion 1.0.0, producedBy product-manager, testable acceptanceCriteria with ids AC-1..).\n"
            "No markdown fences unless required; prefer raw JSON."
        ),
        expected_output="A single acceptance-package JSON object.",
        agent=pm,
    )
    se_task = Task(
        description=(
            f"changeId must be `{change_id}`.\n"
            "Using the PM acceptance-package from context, produce ONLY an implementation-handoff JSON "
            "(schemaVersion 1.0.0, producedBy senior-software-engineer). "
            "Set openSpec.path to "
            f"`openspec/changes/{change_id}/proposal.md` and summarize the technical approach. "
            "Assume implementation will target examples/demo-todo unless the idea clearly differs. "
            "Do not invent different acceptance criteria."
        ),
        expected_output="A single implementation-handoff JSON object.",
        agent=se,
        context=[pm_task],
    )
    qa_task = Task(
        description=(
            f"changeId must be `{change_id}`.\n"
            "Using PM and SE handoffs from context, produce ONLY a risk-notes JSON "
            "(schemaVersion 1.0.0, producedBy qa-engineer) with risks, scenarios, residualGaps, "
            "and automationCandidates. Prefer accept or accept-with-risks."
        ),
        expected_output="A single risk-notes JSON object.",
        agent=qa,
        context=[pm_task, se_task],
    )
    automation_task = Task(
        description=(
            f"changeId must be `{change_id}`.\n"
            "Using prior handoffs, produce ONLY a check-mapping JSON "
            "(schemaVersion 1.0.0, producedBy automation-engineer) mapping AC ids to checks. "
            "Set howToRun.local to `./run-checks.sh` for the demo-todo adapter when applicable."
        ),
        expected_output="A single check-mapping JSON object.",
        agent=automation,
        context=[pm_task, se_task, qa_task],
    )

    return Crew(
        agents=[pm, se, qa, automation],
        tasks=[pm_task, se_task, qa_task, automation_task],
        process=Process.sequential,
        verbose=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AI Engineering Squad via CrewAI")
    parser.add_argument("--change-id", required=True, help="Shared changeId for all handoffs")
    parser.add_argument("--idea", required=True, help="Short product idea / outcome")
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Do not run aesquad validate after writing handoffs",
    )
    args = parser.parse_args()

    handoff_dir = OUT_ROOT / "handoffs" / args.change_id
    openspec_dir = OUT_ROOT / "openspec" / "changes" / args.change_id
    openspec_dir.mkdir(parents=True, exist_ok=True)

    crew = build_crew(args.change_id, args.idea)
    result = crew.kickoff()

    # Persist task outputs in pipeline order
    task_outputs = []
    if hasattr(result, "tasks_output") and result.tasks_output:
        task_outputs = [t.raw if hasattr(t, "raw") else str(t) for t in result.tasks_output]
    elif hasattr(result, "tasks") and result.tasks:
        task_outputs = [
            (t.output.raw if getattr(t, "output", None) and hasattr(t.output, "raw") else str(t))
            for t in result.tasks
        ]
    else:
        # Fallback: only final raw available
        task_outputs = [str(result)]

    names = [
        "acceptance-package.json",
        "implementation-handoff.json",
        "risk-notes.json",
        "check-mapping.json",
    ]

    if len(task_outputs) < 4:
        # Best-effort: write final blob for debugging
        debug_path = handoff_dir / "crew-raw-final.txt"
        handoff_dir.mkdir(parents=True, exist_ok=True)
        debug_path.write_text(str(result), encoding="utf-8")
        print(
            f"Warning: expected 4 task outputs, got {len(task_outputs)}. "
            f"Wrote {debug_path}",
            file=sys.stderr,
        )
    else:
        for name, raw in zip(names, task_outputs[:4]):
            data = extract_json_block(str(raw))
            write_json(handoff_dir / name, data)

        # Lightweight OpenSpec stub from SE summary if present
        impl = extract_json_block(str(task_outputs[1]))
        proposal = openspec_dir / "proposal.md"
        summary = (
            impl.get("openSpec", {}).get("summary")
            if isinstance(impl.get("openSpec"), dict)
            else None
        ) or "See implementation-handoff.json"
        proposal.write_text(
            f"# {args.change_id}\n\n## Context\n\n{args.idea}\n\n## Proposal\n\n{summary}\n",
            encoding="utf-8",
        )
        print(f"Wrote handoffs to {handoff_dir}")
        print(f"Wrote OpenSpec stub to {proposal}")

    # Human signoff is intentionally NOT produced by the crew
    print("Human next: write signoff.json after review (see SPIKE.md).")

    if not args.skip_validate and (handoff_dir / "acceptance-package.json").exists():
        maybe_validate(handoff_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
