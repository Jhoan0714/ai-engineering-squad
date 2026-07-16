"""Load machine-readable pipeline YAML from workflows/."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class PipelineStep:
    id: str
    role: str
    handoff: str
    artifact: str
    context_from: tuple[str, ...] = ()
    task_hint: str = ""
    openspec_path_template: str | None = None


@dataclass(frozen=True)
class HumanGate:
    handoff: str = "signoff"
    artifact: str = "signoff.json"


@dataclass(frozen=True)
class Pipeline:
    schema_version: str
    id: str
    title: str
    process: str
    steps: tuple[PipelineStep, ...]
    human: HumanGate = field(default_factory=HumanGate)
    description: str = ""

    def step_by_id(self, step_id: str) -> PipelineStep:
        for step in self.steps:
            if step.id == step_id:
                return step
        raise KeyError(f"Unknown step id: {step_id}")


def _as_str_list(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(v) for v in value)


def load_pipeline(path: Path) -> Pipeline:
    if not path.is_file():
        raise FileNotFoundError(f"Pipeline not found: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Pipeline must be a mapping: {path}")

    steps_raw = raw.get("steps") or []
    if not steps_raw:
        raise ValueError(f"Pipeline has no steps: {path}")

    steps: list[PipelineStep] = []
    seen: set[str] = set()
    for item in steps_raw:
        if not isinstance(item, dict):
            raise ValueError("Each pipeline step must be a mapping")
        step_id = str(item["id"])
        if step_id in seen:
            raise ValueError(f"Duplicate step id: {step_id}")
        seen.add(step_id)
        steps.append(
            PipelineStep(
                id=step_id,
                role=str(item["role"]),
                handoff=str(item["handoff"]),
                artifact=str(item["artifact"]),
                context_from=_as_str_list(item.get("contextFrom")),
                task_hint=str(item.get("taskHint") or "").strip(),
                openspec_path_template=(
                    str(item["openspecPathTemplate"])
                    if item.get("openspecPathTemplate")
                    else None
                ),
            )
        )

    order = [s.id for s in steps]
    known = set(order)
    for step in steps:
        for ref in step.context_from:
            if ref not in known:
                raise ValueError(
                    f"Step '{step.id}' contextFrom references unknown step '{ref}'"
                )
            if order.index(ref) >= order.index(step.id):
                raise ValueError(
                    f"Step '{step.id}' contextFrom '{ref}' must be an earlier step"
                )

    human_raw = raw.get("human") or {}
    human = HumanGate(
        handoff=str(human_raw.get("handoff") or "signoff"),
        artifact=str(human_raw.get("artifact") or "signoff.json"),
    )

    process = str(raw.get("process") or "sequential").lower()
    if process != "sequential":
        raise ValueError(
            f"Unsupported process '{process}' (only sequential is supported today)"
        )

    return Pipeline(
        schema_version=str(raw.get("schemaVersion") or "1.0.0"),
        id=str(raw.get("id") or path.stem),
        title=str(raw.get("title") or raw.get("id") or path.stem),
        process=process,
        steps=tuple(steps),
        human=human,
        description=str(raw.get("description") or "").strip(),
    )
