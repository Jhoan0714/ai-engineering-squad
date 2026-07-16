# Repository layout

Status: **decided** (backlog E1)

## Decision

Canonical content lives at the **repository root** in tool-agnostic folders. Tool-specific paths (Cursor, Claude Code, OpenClaw, etc.) are documented under `adapters/` and may copy or symlink into place — they are not the source of truth.

We do **not** bury the kit only under `.agents/` or `.cursor/`, so GitHub browsing and multi-runtime use stay clear.

## Canonical tree

```text
ai-engineering-squad/
├── AGENTS.md                 # Index: roles, skills, workflows
├── LICENSE
├── README.md
├── roles/                    # Role packs (one folder per role)
│   └── <role-id>/
│       └── AGENT.md          # Mission, boundaries, DoD, skills to load
├── skills/                   # Shared skills (SKILL.md format)
│   └── <skill-id>/
│       └── SKILL.md
├── workflows/                # Multi-role collaboration recipes
│   └── <workflow-id>.md
├── contracts/                # Handoff shapes (templates / schemas)
│   └── ...
├── adapters/                 # How to wire canonical content into each tool
│   ├── README.md
│   ├── portable.md           # Cursor / Claude / Copilot (E2)
│   └── multi-agent.md        # e.g. OpenClaw (E3)
├── examples/                 # Demo apps and walkthroughs (F*)
├── docs/                     # Product docs (MVP, backlog, roles catalog, …)
└── (future) bin/ or packages/  # H0+ embeddable surfaces — not part of E1
```

## Naming

| Kind | Folder / file | Convention |
|------|---------------|------------|
| Role | `roles/<kebab-case>/AGENT.md` | Industry title in prose; id in kebab-case |
| Skill | `skills/<kebab-case>/SKILL.md` | YAML frontmatter `name` + `description` |
| Workflow | `workflows/<kebab-case>.md` | One workflow per file |
| Contract | `contracts/<kebab-case>.*` | Prefer versionable schemas when H0 validates (see open questions) |

## Adapter rule

1. **Edit canonical files only** under `roles/`, `skills/`, `workflows/`, `contracts/`.
2. Adapters **reference or sync** those paths; do not fork divergent copies long-term.
3. Optional local discovery dirs (e.g. `.cursor/skills`, `.agents/skills`) are install-time artifacts, not upstream content.

## Out of scope for this layout milestone

- Full `AGENT.md` / `SKILL.md` bodies (B*, C*)
- Adapter how-tos (E2, E3)
- H0 CLI/Action binary layout (Wave 2)
