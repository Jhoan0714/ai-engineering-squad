"""Parse roles/*/AGENT.md into structured RoleSpec (no hard-coded roster)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class RoleSpec:
    """Runtime view of one role pack."""

    id: str
    title: str
    goal: str
    backstory: str
    skills: tuple[str, ...] = ()
    agent_path: Path = field(default=Path("."), repr=False)

    @property
    def produced_by(self) -> str:
        return self.id


_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_SKILL_TICK_RE = re.compile(r"`([a-z0-9][a-z0-9-]*)`")


def _sections(text: str) -> dict[str, str]:
    matches = list(_SECTION_RE.finditer(text))
    out: dict[str, str] = {}
    for i, m in enumerate(matches):
        name = m.group(1).strip().lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[name] = text[start:end].strip()
    return out


def _first_paragraph(body: str) -> str:
    chunks = [c.strip() for c in re.split(r"\n\s*\n", body) if c.strip()]
    if not chunks:
        return ""
    # Skip blockquotes / lists for goal if first chunk is empty of prose
    for chunk in chunks:
        if chunk.startswith(">") or chunk.startswith("-") or chunk.startswith("*"):
            continue
        line = chunk.split("\n")[0].strip()
        if line:
            return line
    return chunks[0].split("\n")[0].strip()


def _skill_ids(skills_section: str) -> tuple[str, ...]:
    ids: list[str] = []
    for match in _SKILL_TICK_RE.finditer(skills_section):
        sid = match.group(1)
        if sid not in ids:
            ids.append(sid)
    return tuple(ids)


def load_skill_text(skills_root: Path, skill_id: str) -> str | None:
    path = skills_root / skill_id / "SKILL.md"
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def discover_role_ids(roles_root: Path) -> list[str]:
    """All role packs that have AGENT.md (dynamic discovery)."""
    if not roles_root.is_dir():
        return []
    ids = []
    for child in sorted(roles_root.iterdir()):
        if child.is_dir() and (child / "AGENT.md").is_file():
            ids.append(child.name)
    return ids


def load_role(
    roles_root: Path,
    role_id: str,
    *,
    skills_root: Path | None = None,
) -> RoleSpec:
    path = roles_root / role_id / "AGENT.md"
    if not path.is_file():
        available = discover_role_ids(roles_root)
        raise FileNotFoundError(
            f"Missing role pack: {path}. Available: {', '.join(available) or '(none)'}"
        )

    text = path.read_text(encoding="utf-8")
    h1 = _H1_RE.search(text)
    title = h1.group(1).strip() if h1 else role_id.replace("-", " ").title()

    sections = _sections(text)
    mission = _first_paragraph(sections.get("mission", ""))
    goal = mission or f"Execute the {title} responsibilities and definition of done."

    skill_ids = _skill_ids(sections.get("skills to load", ""))
    backstory_parts = [text.strip()]

    if skills_root is not None:
        loaded: list[str] = []
        for sid in skill_ids:
            skill_body = load_skill_text(skills_root, sid)
            if skill_body:
                backstory_parts.append(
                    f"\n\n---\n# Skill: `{sid}`\n\n{skill_body.strip()}\n"
                )
                loaded.append(sid)
        if loaded:
            backstory_parts.append(
                "\n\nUse the skill packs appended above when they apply to this task.\n"
            )

    return RoleSpec(
        id=role_id,
        title=title,
        goal=goal,
        backstory="".join(backstory_parts),
        skills=skill_ids,
        agent_path=path,
    )
