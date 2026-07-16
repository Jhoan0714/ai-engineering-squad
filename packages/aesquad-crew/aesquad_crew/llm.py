"""Resolve CrewAI LLM config (Ollama, OpenAI, etc.)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"


@dataclass(frozen=True)
class LlmConfig:
    """User-facing LLM settings for aesquad-crew."""

    model: str
    base_url: str | None = None
    api_key: str | None = None
    temperature: float = 0.2

    @property
    def display(self) -> str:
        if self.base_url:
            return f"{self.model} @ {self.base_url}"
        return self.model


def normalize_model(model: str) -> str:
    """
    Accept friendly names and expand to LiteLLM/CrewAI form.

    Examples:
      llama3.1:latest      -> ollama/llama3.1:latest
      ollama/llama3.1      -> ollama/llama3.1
      gpt-4o-mini          -> gpt-4o-mini (unchanged)
    """
    raw = model.strip()
    if not raw:
        raise ValueError("LLM model name must not be empty")
    if "/" in raw:
        return raw
    # Bare Ollama-style tags (name or name:tag) → ollama/<name>
    if ":" in raw or raw.lower().startswith(("llama", "qwen", "mistral", "phi", "gemma", "kimi")):
        return f"ollama/{raw}"
    return raw


def resolve_llm_config(
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float | None = None,
) -> LlmConfig | None:
    """
    Resolve LLM settings from CLI args and environment.

    Env (CLI wins when both set):
      AESQUAD_LLM              e.g. ollama/llama3.1:latest
      AESQUAD_LLM_BASE_URL     e.g. http://localhost:11434
      AESQUAD_LLM_API_KEY      optional
      AESQUAD_LLM_TEMPERATURE  optional float

    Returns None when nothing is configured (CrewAI default / OpenAI path).
    """
    resolved_model = model or os.environ.get("AESQUAD_LLM") or None
    if not resolved_model:
        return None

    resolved_base = base_url or os.environ.get("AESQUAD_LLM_BASE_URL") or None
    resolved_key = api_key or os.environ.get("AESQUAD_LLM_API_KEY") or None

    temp = temperature
    if temp is None:
        raw_temp = os.environ.get("AESQUAD_LLM_TEMPERATURE")
        temp = float(raw_temp) if raw_temp else 0.2

    normalized = normalize_model(resolved_model)
    if normalized.startswith("ollama/") and not resolved_base:
        resolved_base = DEFAULT_OLLAMA_BASE_URL

    return LlmConfig(
        model=normalized,
        base_url=resolved_base,
        api_key=resolved_key,
        temperature=temp,
    )


def build_llm(config: LlmConfig) -> Any:
    """Instantiate a CrewAI LLM from config."""
    from crewai import LLM

    kwargs: dict[str, Any] = {
        "model": config.model,
        "temperature": config.temperature,
    }
    if config.base_url:
        kwargs["base_url"] = config.base_url
    if config.api_key:
        kwargs["api_key"] = config.api_key
    elif config.model.startswith("ollama/"):
        # Some stacks still probe for a key; Ollama local ignores it.
        kwargs["api_key"] = config.api_key or "ollama"

    return LLM(**kwargs)
