"""Offline tests: pipeline + role loading (no LLM / CrewAI kickoff)."""

from __future__ import annotations

import unittest
from pathlib import Path

from aesquad_crew.kit import default_pipeline_path, find_kit_root
from aesquad_crew.pipeline import load_pipeline
from aesquad_crew.role_loader import discover_role_ids, load_role


class RoleAndPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.kit = find_kit_root(Path(__file__).resolve())

    def test_discovers_mvp_roles(self) -> None:
        ids = discover_role_ids(self.kit / "roles")
        for expected in (
            "product-manager",
            "senior-software-engineer",
            "qa-engineer",
            "automation-engineer",
        ):
            self.assertIn(expected, ids)

    def test_role_goal_from_mission(self) -> None:
        role = load_role(
            self.kit / "roles",
            "product-manager",
            skills_root=self.kit / "skills",
        )
        self.assertEqual(role.title, "Product Manager")
        self.assertIn("what", role.goal.lower())
        self.assertIn("write-acceptance-criteria", role.skills)
        self.assertIn("Skill: `write-acceptance-criteria`", role.backstory)

    def test_feature_delivery_pipeline(self) -> None:
        pipeline = load_pipeline(default_pipeline_path(self.kit))
        self.assertEqual(pipeline.id, "feature-delivery")
        self.assertEqual(len(pipeline.steps), 4)
        self.assertEqual(pipeline.steps[0].role, "product-manager")
        self.assertEqual(pipeline.steps[-1].handoff, "check-mapping")
        # Context graph: later steps see earlier ones
        self.assertEqual(
            pipeline.steps[1].context_from, ("product-manager",)
        )


if __name__ == "__main__":
    unittest.main()
