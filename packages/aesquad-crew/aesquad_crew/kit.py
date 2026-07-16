"""Locate kit root and standard paths."""

from __future__ import annotations

from pathlib import Path


def find_kit_root(start: Path | None = None) -> Path:
    """Walk up until roles/ and contracts/ exist (repo root)."""
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "roles").is_dir() and (candidate / "contracts").is_dir():
            return candidate
    # Fallback: packages/aesquad-crew/aesquad_crew/kit.py → repo root
    pkg = Path(__file__).resolve().parents[3]
    if (pkg / "roles").is_dir():
        return pkg
    raise FileNotFoundError(
        "Could not find kit root (expected roles/ and contracts/). "
        "Run from the ai-engineering-squad repo or pass --kit-root."
    )


def roles_dir(kit_root: Path) -> Path:
    return kit_root / "roles"


def skills_dir(kit_root: Path) -> Path:
    return kit_root / "skills"


def schemas_dir(kit_root: Path) -> Path:
    return kit_root / "contracts" / "schemas"


def workflows_dir(kit_root: Path) -> Path:
    return kit_root / "workflows"


def default_pipeline_path(kit_root: Path) -> Path:
    return workflows_dir(kit_root) / "feature-delivery.pipeline.yaml"


def aesquad_bin(kit_root: Path) -> Path:
    return kit_root / "packages" / "aesquad" / "bin" / "aesquad.mjs"
