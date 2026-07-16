# Portable adapters (Cursor, Claude Code, Copilot)

**Status:** ready (backlog **E2**)

Wire this repository’s **canonical** `roles/`, `skills/`, `workflows/`, and `AGENTS.md` into IDE coding agents. Adapters **link or copy** — they must not become a second source of truth.

## Principle

| Canonical (edit here) | Tool discovery (install-time) |
|----------------------|-------------------------------|
| `skills/<id>/SKILL.md` | Cursor / Claude skill dirs |
| `roles/<id>/AGENT.md` | Prompted via “Act as …” or project instructions |
| `AGENTS.md` | Project root index (many tools read this) |
| `workflows/*.md` | Human / agent reference |

## Quick install (symlink skills)

From the **consumer project** (or globally for personal agents):

```bash
# Clone once
git clone https://github.com/Jhoan0714/ai-engineering-squad.git ~/ai-engineering-squad

# Cursor: project skills (recommended for team repos)
mkdir -p .agents/skills
ln -s ~/ai-engineering-squad/skills/write-acceptance-criteria .agents/skills/write-acceptance-criteria
ln -s ~/ai-engineering-squad/skills/openspec-change .agents/skills/openspec-change
ln -s ~/ai-engineering-squad/skills/design-test-cases .agents/skills/design-test-cases
ln -s ~/ai-engineering-squad/skills/reduce-flakiness .agents/skills/reduce-flakiness

# Optional: also expose under .cursor/skills for older layouts
mkdir -p .cursor/skills
ln -s ~/ai-engineering-squad/skills/write-acceptance-criteria .cursor/skills/write-acceptance-criteria
# …repeat for other skills as needed
```

Copy instead of symlink if your environment forbids links:

```bash
cp -R ~/ai-engineering-squad/skills/write-acceptance-criteria .agents/skills/
```

Re-copy after upstream updates, or prefer symlink + `git pull` in the clone.

## Cursor

1. Put or symlink skills under `.agents/skills/<skill-id>/SKILL.md` (and/or `.cursor/skills/`).
2. Keep a project `AGENTS.md` that points at this kit (or vendor a short copy of the index).
3. Invoke a **role** by prompt, for example:

```text
Act as the Product Manager from ai-engineering-squad
(roles/product-manager/AGENT.md). Load skill write-acceptance-criteria.
Produce an acceptance-package JSON for changeId=…
```

4. Optionally register the **aesquad MCP** validate server (see [packages/aesquad/README.md](../packages/aesquad/README.md)) so the agent can validate handoffs.

## Claude Code

1. Symlink or copy skills into `.claude/skills/<skill-id>/` (same `SKILL.md` layout).
2. Add a short `CLAUDE.md` (or project instructions) that points to:

   - this repo’s `AGENTS.md`
   - `workflows/feature-delivery.md`
   - role paths under `roles/`

3. Same “Act as \<role\>” pattern as Cursor.
4. Optional: MCP entry for `aesquad` validate (stdio), same as Cursor.

## GitHub Copilot

1. Ensure the consumer repo has an `AGENTS.md` (link to or summarize this kit).
2. Optionally add `.github/copilot-instructions.md`:

```markdown
Follow AI Engineering Squad workflows when asked to act as a squad role.
Roles: roles/*/AGENT.md in the ai-engineering-squad kit (or vendored copy).
Handoffs must match contracts/schemas (JSON). Validate with aesquad when available.
```

3. Copilot does not always auto-load Cursor-style skill folders; prefer explicit role prompts + `AGENTS.md`.

## Invoking the MVP squad

| Role | Canonical file | Typical skills |
|------|----------------|----------------|
| Product Manager | `roles/product-manager/AGENT.md` | `write-acceptance-criteria` |
| Senior Software Engineer | `roles/senior-software-engineer/AGENT.md` | `openspec-change` |
| QA Engineer | `roles/qa-engineer/AGENT.md` | `design-test-cases` |
| Automation Engineer | `roles/automation-engineer/AGENT.md` | `reduce-flakiness` |

Happy path: [workflows/feature-delivery.md](../workflows/feature-delivery.md).

## Handoffs

Agents should write JSON instances under a path your team chooses (e.g. `handoffs/<changeId>/`), conforming to [contracts/schemas/](../contracts/schemas/). Validate with:

```bash
cd ~/ai-engineering-squad/packages/aesquad && npm install
node ./bin/aesquad.mjs validate --dir /path/to/handoffs/<changeId>
```

## What this adapter is not

- Not an auto-orchestrator of four agents in one IDE chat
- Not a replacement for OpenClaw / multi-agent runtimes (see [multi-agent.md](multi-agent.md))
- Not a fork of role content into tool-specific prose (link the canonical `AGENT.md`)
