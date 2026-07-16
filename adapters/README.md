# Adapters

Maps canonical `roles/`, `skills/`, and `workflows/` into tool-specific discovery paths.

| Doc | Backlog | Purpose |
|-----|---------|---------|
| [portable.md](portable.md) | E2 | Cursor, Claude Code, Copilot |
| [multi-agent.md](multi-agent.md) | E3 | Multi-agent runtimes (OpenClaw-first) |

**Rule:** adapters sync or document links to canonical content — they do not become a second source of truth.

## Install summary

1. Clone this repo (or vendor a release).
2. **Portable:** symlink `skills/*` into `.agents/skills` / `.claude/skills` — see [portable.md](portable.md).
3. **Multi-agent:** create one isolated agent per MVP role pointing at `roles/*/AGENT.md` — see [multi-agent.md](multi-agent.md).
4. **Validate handoffs:** [packages/aesquad](../packages/aesquad/README.md) (CLI or MCP).

Prefer **symlink + `git pull`** over copying skill/role files so upstream fixes flow through.
