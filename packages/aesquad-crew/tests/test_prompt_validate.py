"""Tests for enriched task prompts and schema validation."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from aesquad_crew.kit import find_kit_root
from aesquad_crew.pipeline import load_pipeline
from aesquad_crew.role_loader import load_role
from aesquad_crew.schema_validate import validate_handoff_data
from aesquad_crew.task_builder import (
    build_task_description,
    fixed_refs_for_step,
    ref_for,
)


class PromptAndValidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.kit = find_kit_root(Path(__file__).resolve())
        cls.pipeline = load_pipeline(
            cls.kit / "workflows" / "feature-delivery.pipeline.yaml"
        )

    def test_refs_are_strings(self) -> None:
        step = self.pipeline.steps[1]  # SE
        refs = fixed_refs_for_step(step, "demo-x")
        self.assertEqual(
            refs["acceptancePackageRef"],
            "handoffs/demo-x/acceptance-package.json",
        )

    def test_prompt_includes_example_and_schema(self) -> None:
        step = self.pipeline.steps[0]
        role = load_role(self.kit / "roles", step.role, skills_root=self.kit / "skills")
        prompt = build_task_description(
            step=step,
            role=role,
            change_id="demo-x",
            idea="Test idea",
            schemas_root=self.kit / "contracts" / "schemas",
            examples_root=self.kit / "contracts" / "examples",
        )
        self.assertIn("inScope", prompt)
        self.assertIn("array of strings", prompt)
        self.assertIn("Canonical example", prompt)
        self.assertIn('"changeId": "demo-x"', prompt)
        self.assertIn("additionalProperties", prompt)

    def test_canonical_examples_validate(self) -> None:
        schemas = self.kit / "contracts" / "schemas"
        examples = self.kit / "contracts" / "examples"
        for handoff in (
            "acceptance-package",
            "implementation-handoff",
            "risk-notes",
            "check-mapping",
        ):
            data = json.loads((examples / f"{handoff}.example.json").read_text())
            result = validate_handoff_data(data, handoff=handoff, schemas_root=schemas)
            self.assertTrue(result.ok, f"{handoff}: {result.error_lines}")

    def test_bad_inscope_fails(self) -> None:
        schemas = self.kit / "contracts" / "schemas"
        examples = self.kit / "contracts" / "examples"
        data = json.loads((examples / "acceptance-package.example.json").read_text())
        data["inScope"] = [{"id": "AC-1", "statement": "bad"}]
        result = validate_handoff_data(
            data, handoff="acceptance-package", schemas_root=schemas
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("inScope" in e for e in result.error_lines))

    def test_ref_helper(self) -> None:
        self.assertEqual(
            ref_for("risk-notes", "abc"),
            "handoffs/abc/risk-notes.json",
        )


if __name__ == "__main__":
    unittest.main()
