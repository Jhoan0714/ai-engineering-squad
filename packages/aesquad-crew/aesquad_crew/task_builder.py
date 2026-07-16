"""Build CrewAI Task descriptions from role + schema + examples + fixed refs."""

from __future__ import annotations

import json
from pathlib import Path

from aesquad_crew.pipeline import PipelineStep
from aesquad_crew.role_loader import RoleSpec

# Relative paths written into handoffs (stable contract for refs).
REF_TEMPLATES = {
    "acceptance-package": "handoffs/{changeId}/acceptance-package.json",
    "implementation-handoff": "handoffs/{changeId}/implementation-handoff.json",
    "risk-notes": "handoffs/{changeId}/risk-notes.json",
    "check-mapping": "handoffs/{changeId}/check-mapping.json",
}


def schema_path_for_handoff(schemas_root: Path, handoff: str) -> Path:
    path = schemas_root / f"{handoff}.schema.json"
    if not path.is_file():
        raise FileNotFoundError(f"Missing schema for handoff '{handoff}': {path}")
    return path


def example_path_for_handoff(examples_root: Path, handoff: str) -> Path | None:
    path = examples_root / f"{handoff}.example.json"
    return path if path.is_file() else None


def ref_for(handoff: str, change_id: str) -> str:
    template = REF_TEMPLATES.get(handoff)
    if not template:
        return f"handoffs/{change_id}/{handoff}.json"
    return template.format(changeId=change_id)


def fixed_refs_for_step(step: PipelineStep, change_id: str) -> dict[str, str]:
    """Known path refs this step must emit (string paths, never nested objects)."""
    refs: dict[str, str] = {}
    if step.handoff == "implementation-handoff":
        refs["acceptancePackageRef"] = ref_for("acceptance-package", change_id)
    elif step.handoff == "risk-notes":
        refs["acceptancePackageRef"] = ref_for("acceptance-package", change_id)
        refs["implementationHandoffRef"] = ref_for("implementation-handoff", change_id)
    elif step.handoff == "check-mapping":
        refs["acceptancePackageRef"] = ref_for("acceptance-package", change_id)
        refs["riskNotesRef"] = ref_for("risk-notes", change_id)
    return refs


def _adapt_example(raw: dict, change_id: str, step: PipelineStep) -> dict:
    data = json.loads(json.dumps(raw))  # deep copy
    data["changeId"] = change_id
    if "producedBy" in data and step.role:
        # Keep example producedBy if it matches role; otherwise force role id
        data["producedBy"] = step.role
    for key, path in fixed_refs_for_step(step, change_id).items():
        data[key] = path
    if step.openspec_path_template and isinstance(data.get("openSpec"), dict):
        data["openSpec"]["path"] = step.openspec_path_template.format(changeId=change_id)
    return data


def schema_shape_notes(schema: dict) -> str:
    """Human-readable nested shape reminders models often get wrong."""
    notes: list[str] = []
    props = schema.get("properties") or {}

    def walk(name: str, node: dict, prefix: str = "") -> None:
        path = f"{prefix}{name}" if not prefix else f"{prefix}.{name}"
        t = node.get("type")
        if t == "array":
            items = node.get("items") or {}
            if items.get("type") == "string":
                notes.append(f"- `{path}` must be an array of strings (NOT objects).")
            elif items.get("type") == "object":
                req = items.get("required") or []
                notes.append(
                    f"- `{path}[]` objects require: {', '.join(req) or '(see schema)'}."
                )
                if items.get("additionalProperties") is False:
                    notes.append(f"- `{path}[]` must NOT include extra properties.")
        elif t == "object":
            req = node.get("required") or []
            if req:
                notes.append(f"- `{path}` object requires: {', '.join(req)}.")
            if node.get("additionalProperties") is False:
                notes.append(f"- `{path}` must NOT include extra properties.")
            for child_name, child in (node.get("properties") or {}).items():
                if isinstance(child, dict):
                    walk(child_name, child, path)

        if "const" in node:
            notes.append(f"- `{path}` must be exactly `{node['const']}`.")
        if "enum" in node:
            notes.append(f"- `{path}` must be one of: {', '.join(map(str, node['enum']))}.")

    for prop_name, prop in props.items():
        if isinstance(prop, dict):
            walk(prop_name, prop)

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for line in notes:
        if line not in seen:
            seen.add(line)
            unique.append(line)
    return "\n".join(unique[:40])  # keep prompt bounded


def build_task_description(
    *,
    step: PipelineStep,
    role: RoleSpec,
    change_id: str,
    idea: str,
    schemas_root: Path,
    examples_root: Path | None = None,
    prior_handoffs: dict[str, dict] | None = None,
    repair_errors: list[str] | None = None,
    previous_attempt: dict | None = None,
) -> str:
    schema_file = schema_path_for_handoff(schemas_root, step.handoff)
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    shape = schema_shape_notes(schema)
    schema_json = json.dumps(schema, indent=2)

    examples_root = examples_root or (schemas_root.parent / "examples")
    example_file = example_path_for_handoff(examples_root, step.handoff)
    example_block = ""
    if example_file:
        example = _adapt_example(
            json.loads(example_file.read_text(encoding="utf-8")),
            change_id,
            step,
        )
        example_block = (
            "\nCanonical example (adapt content to the idea; KEEP this shape/keys):\n"
            f"```json\n{json.dumps(example, indent=2)}\n```\n"
        )

    refs = fixed_refs_for_step(step, change_id)
    refs_block = ""
    if refs:
        lines = "\n".join(f'- "{k}": "{v}"' for k, v in refs.items())
        refs_block = (
            "\nFixed string refs (copy exactly — strings only, never nested objects):\n"
            f"{lines}\n"
        )

    openspec_line = ""
    if step.openspec_path_template:
        path = step.openspec_path_template.format(changeId=change_id)
        openspec_line = f"\nSet openSpec.path exactly to `{path}`.\n"

    hint = step.task_hint.strip()
    hint_block = f"\nStep guidance:\n{hint}\n" if hint else ""

    prior_block = ""
    if prior_handoffs:
        prior_block = "\nPrior handoffs already produced for this changeId:\n"
        for name, data in prior_handoffs.items():
            prior_block += f"\n### {name}\n```json\n{json.dumps(data, indent=2)}\n```\n"

    repair_block = ""
    if repair_errors:
        repair_block = (
            "\nPREVIOUS ATTEMPT FAILED SCHEMA VALIDATION. Fix ALL of these errors:\n"
            + "\n".join(f"- {e}" for e in repair_errors)
            + "\n"
        )
        if previous_attempt:
            repair_block += (
                "\nInvalid JSON from previous attempt (repair it; do not invent a new shape):\n"
                f"```json\n{json.dumps(previous_attempt, indent=2)}\n```\n"
            )

    return (
        f"You are acting as **{role.title}** (`{role.id}`).\n"
        f"Pipeline step: `{step.id}`\n"
        f"changeId must be exactly `{change_id}`.\n"
        f"producedBy must be exactly `{role.id}`.\n"
        f"schemaVersion must be exactly `1.0.0`.\n"
        f"Product idea / outcome input:\n{idea}\n"
        f"{openspec_line}"
        f"{hint_block}"
        f"{refs_block}"
        f"{prior_block}"
        f"{repair_block}\n"
        f"Produce ONLY a single JSON object for handoff kind `{step.handoff}`.\n"
        f"It will be saved as `{step.artifact}`.\n"
        "Output raw JSON only (no markdown fences, no commentary).\n\n"
        "Hard shape rules:\n"
        f"{shape}\n\n"
        f"Full JSON Schema ({schema_file.name}) — obey additionalProperties: false:\n"
        f"```json\n{schema_json}\n```\n"
        f"{example_block}"
        "Do not invent conflicting acceptance criteria ids. "
        "Prefer the example's key names exactly."
    )


def build_expected_output(step: PipelineStep) -> str:
    return (
        f"Raw JSON only: one `{step.handoff}` object matching the schema "
        f"and canonical example keys, suitable for `{step.artifact}`."
    )
