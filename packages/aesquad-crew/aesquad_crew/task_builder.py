"""Build CrewAI Task descriptions from role + schema + pipeline step."""

from __future__ import annotations

import json
from pathlib import Path

from aesquad_crew.pipeline import PipelineStep
from aesquad_crew.role_loader import RoleSpec


def schema_path_for_handoff(schemas_root: Path, handoff: str) -> Path:
    path = schemas_root / f"{handoff}.schema.json"
    if not path.is_file():
        raise FileNotFoundError(f"Missing schema for handoff '{handoff}': {path}")
    return path


def schema_summary(schema_path: Path) -> str:
    """Compact required/properties hint so prompts stay bounded."""
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    required = data.get("required") or []
    props = data.get("properties") or {}
    lines = [
        f"Schema title: {data.get('title') or schema_path.name}",
        f"schemaVersion const: {(props.get('schemaVersion') or {}).get('const', '1.0.0')}",
        f"Required fields: {', '.join(required)}",
    ]
    produced = props.get("producedBy") or {}
    if "const" in produced:
        lines.append(f"producedBy must be exactly: {produced['const']}")
    return "\n".join(lines)


def build_task_description(
    *,
    step: PipelineStep,
    role: RoleSpec,
    change_id: str,
    idea: str,
    schemas_root: Path,
) -> str:
    schema_file = schema_path_for_handoff(schemas_root, step.handoff)
    summary = schema_summary(schema_file)

    openspec_line = ""
    if step.openspec_path_template:
        path = step.openspec_path_template.format(changeId=change_id)
        openspec_line = f"\nOpenSpec path for this change: `{path}`\n"

    hint = step.task_hint.strip()
    hint_block = f"\nStep guidance:\n{hint}\n" if hint else ""

    return (
        f"You are acting as **{role.title}** (`{role.id}`).\n"
        f"Pipeline step: `{step.id}`\n"
        f"changeId must be exactly `{change_id}`.\n"
        f"Product idea / outcome input:\n{idea}\n"
        f"{openspec_line}"
        f"{hint_block}\n"
        f"Produce ONLY a single JSON object for handoff kind `{step.handoff}`.\n"
        f"Write it so it can be saved as `{step.artifact}`.\n"
        f"Follow this kit schema ({schema_file.name}):\n{summary}\n\n"
        "Use prior pipeline outputs from context when present. "
        "Do not invent conflicting acceptance criteria. "
        "Prefer raw JSON (no markdown fences)."
    )


def build_expected_output(step: PipelineStep) -> str:
    return f"A single `{step.handoff}` JSON object suitable for `{step.artifact}`."
