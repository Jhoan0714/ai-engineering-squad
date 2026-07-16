"""Persist crew task outputs as handoff JSON (+ optional OpenSpec stub)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from aesquad_crew.pipeline import Pipeline, PipelineStep


def extract_json_block(text: str) -> dict:
    text = text.strip()
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in agent output")
    data = json.loads(match.group(0))
    if not isinstance(data, dict):
        raise ValueError("Parsed JSON is not an object")
    return data


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def collect_task_outputs(result: object) -> list[str]:
    if hasattr(result, "tasks_output") and result.tasks_output:
        return [
            t.raw if hasattr(t, "raw") else str(t) for t in result.tasks_output
        ]
    if hasattr(result, "tasks") and result.tasks:
        out: list[str] = []
        for t in result.tasks:
            output = getattr(t, "output", None)
            if output is not None and hasattr(output, "raw"):
                out.append(str(output.raw))
            else:
                out.append(str(t))
        return out
    return [str(result)]


def persist_handoffs(
    *,
    pipeline: Pipeline,
    steps: tuple[PipelineStep, ...],
    task_outputs: list[str],
    handoff_dir: Path,
    out_root: Path,
    change_id: str,
    idea: str,
) -> list[Path]:
    handoff_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    if len(task_outputs) < len(steps):
        debug_path = handoff_dir / "crew-raw-final.txt"
        debug_path.write_text("\n\n---\n\n".join(task_outputs), encoding="utf-8")
        print(
            f"Warning: expected {len(steps)} task outputs, got {len(task_outputs)}. "
            f"Wrote {debug_path}",
            file=sys.stderr,
        )
        return written

    for step, raw in zip(steps, task_outputs):
        data = extract_json_block(str(raw))
        path = handoff_dir / step.artifact
        write_json(path, data)
        written.append(path)

        if step.openspec_path_template:
            rel = step.openspec_path_template.format(changeId=change_id)
            proposal = out_root / rel
            proposal.parent.mkdir(parents=True, exist_ok=True)
            summary = None
            open_spec = data.get("openSpec")
            if isinstance(open_spec, dict):
                summary = open_spec.get("summary")
            proposal.write_text(
                f"# {change_id}\n\n## Context\n\n{idea}\n\n"
                f"## Proposal\n\n{summary or 'See implementation-handoff.json'}\n",
                encoding="utf-8",
            )
            print(f"Wrote OpenSpec stub to {proposal}")

    print(f"Wrote handoffs to {handoff_dir}")
    print(
        f"Human next: write {pipeline.human.artifact} after review "
        f"(handoff kind `{pipeline.human.handoff}`)."
    )
    return written
