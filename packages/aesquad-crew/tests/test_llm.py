"""Tests for LLM config resolution (no CrewAI kickoff)."""

from __future__ import annotations

import os
import unittest
from unittest import mock

from aesquad_crew.llm import normalize_model, resolve_llm_config


class LlmConfigTests(unittest.TestCase):
    def test_normalize_bare_ollama_tag(self) -> None:
        self.assertEqual(normalize_model("llama3.1:latest"), "ollama/llama3.1:latest")

    def test_normalize_already_prefixed(self) -> None:
        self.assertEqual(
            normalize_model("ollama/llama3.1:latest"), "ollama/llama3.1:latest"
        )

    def test_resolve_sets_ollama_base_url(self) -> None:
        cfg = resolve_llm_config(model="llama3.1:latest")
        assert cfg is not None
        self.assertEqual(cfg.model, "ollama/llama3.1:latest")
        self.assertEqual(cfg.base_url, "http://localhost:11434")

    def test_resolve_from_env(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "AESQUAD_LLM": "ollama/llama3.1:latest",
                "AESQUAD_LLM_BASE_URL": "http://127.0.0.1:11434",
            },
            clear=False,
        ):
            cfg = resolve_llm_config()
        assert cfg is not None
        self.assertEqual(cfg.base_url, "http://127.0.0.1:11434")

    def test_resolve_none_without_config(self) -> None:
        env = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith("AESQUAD_LLM")
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertIsNone(resolve_llm_config())


if __name__ == "__main__":
    unittest.main()
