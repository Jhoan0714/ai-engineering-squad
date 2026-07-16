"""Validate handoff JSON against contracts/schemas (in-process)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aesquad_crew.task_builder import schema_path_for_handoff


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def format(self) -> str:
        return f"{self.path}: {self.message}" if self.path else self.message


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    kind: str
    errors: tuple[ValidationIssue, ...] = ()

    @property
    def error_lines(self) -> list[str]:
        return [e.format() for e in self.errors]


def validate_handoff_data(
    data: dict[str, Any],
    *,
    handoff: str,
    schemas_root: Path,
) -> ValidationResult:
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise ImportError(
            "jsonschema is required for in-process validation. "
            "Install with: pip install jsonschema"
        ) from exc

    schema_path = schema_path_for_handoff(schemas_root, handoff)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors: list[ValidationIssue] = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = "/" + "/".join(str(p) for p in err.path) if err.path else "/"
        errors.append(ValidationIssue(path=path, message=err.message))
    return ValidationResult(ok=not errors, kind=handoff, errors=tuple(errors))
