# Multi-agent runtime adapters (OpenClaw-first)

**Status:** ready (backlog **E3**)

Map each AI Engineering Squad **role** to an **isolated agent** in a multi-agent runtime. Primary documented runtime: **OpenClaw**. Canonical content stays in this repo; the runtime only hosts persona files, workspaces, and tool permissions.

> OpenClaw config surfaces evolve. Treat this as a **mapping guide**; confirm field names against current OpenClaw docs when installing.

## Principle

| Squad concept | Multi-agent concept |
|---------------|---------------------|
| `roles/<id>/AGENT.md` | Agent persona / soul / system instructions |
| `skills/*` | Skills or playbooks loaded by that agent |
| `contracts/*` | Artifacts agents must write/validate |
| `workflows/feature-delivery.md` | Orchestration order (human or lead agent) |
| `packages/aesquad` | Shared validate tool (CLI or MCP) for all agents |

**Rule:** do not paste divergent long-term copies of `AGENT.md`. Prefer “include / link / sync from kit path”.

## Recommended OpenClaw agent set (MVP)

Four isolated agents (one per MVP role):

| `agentId` | Role | Canonical instructions |
|-----------|------|-------------------------|
| `product-manager` | Product Manager | `roles/product-manager/AGENT.md` |
| `senior-software-engineer` | Senior Software Engineer | `roles/senior-software-engineer/AGENT.md` |
| `qa-engineer` | QA Engineer | `roles/qa-engineer/AGENT.md` |
| `automation-engineer` | Automation Engineer | `roles/automation-engineer/AGENT.md` |

Optional fifth: a thin **orchestrator** / human channel that only routes work and does not implement features (keeps bindings simple). Many setups use the human chat as orchestrator instead.

## Per-agent workspace layout (suggested)

For each agent workspace (paths illustrative):

```text
~/.openclaw/workspace-product-manager/
  SOUL.md                 # short persona + pointer to kit AGENT.md
  AGENTS.md               # optional local index
  skills/                 # symlinks into kit skills/
  handoffs/               # JSON instances this agent writes/reads
```

### `SOUL.md` pattern (example)

```markdown
# Product Manager

You are the Product Manager agent for AI Engineering Squad.

Follow the canonical role definition:
https://github.com/Jhoan0714/ai-engineering-squad/blob/main/roles/product-manager/AGENT.md
(or the vendored/local clone path).

Load skill: write-acceptance-criteria.

When you finish a change slice, write an acceptance-package JSON that validates
against contracts/schemas/acceptance-package.schema.json.
Validate with aesquad before handoff.
```

Repeat for other roles with their `AGENT.md` and skills.

## Tool allowlists (suggested)

Keep permissions **least privilege** per role:

| agentId | Allow (typical) | Deny (typical) |
|---------|-----------------|----------------|
| `product-manager` | read repo docs, write `handoffs/*/acceptance-package.json` | production deploy, broad shell |
| `senior-software-engineer` | read/write code, OpenSpec paths, tests | changing product AC without PM |
| `qa-engineer` | read code + handoffs, write `risk-notes.json` | merging to main |
| `automation-engineer` | write checks + `check-mapping.json`, run test commands | rewriting product requirements |

Exact OpenClaw allow/deny keys depend on your version — map the **intent** above into your config.

## Bindings / routing

Use deterministic routing so messages do not leak across personas:

- Bind each agent to a distinct channel, account, or peer when possible.
- Prefer most-specific bindings (peer/channel) over a single shared inbox.
- Keep sessions isolated (separate workspace + session history per `agentId`).

Validate routing with your runtime’s agent list / bindings command (see OpenClaw docs).

## Handoff flow inside the runtime

Same chain as the kit:

```text
PM → acceptance-package
SE → implementation-handoff (+ code/PR)
QA → risk-notes
Automation → check-mapping
Human → signoff
```

Shared `changeId` across files. After each write:

```bash
node /path/to/ai-engineering-squad/packages/aesquad/bin/aesquad.mjs validate <file.json>
```

Or expose `aesquad mcp` to agents that support MCP tools.

## Sub-agents vs persistent roles

| Pattern | Use when |
|---------|----------|
| **Persistent role agents** (this doc) | Stable personas with memory and tool policy |
| **Sub-agents / spawn** | One-off research or parallel tasks that report back |

For feature delivery, prefer persistent MVP roles; use sub-agents for side research, not as a substitute for QA/Automation ownership.

## Install sketch

```bash
git clone https://github.com/Jhoan0714/ai-engineering-squad.git ~/ai-engineering-squad
cd ~/ai-engineering-squad/packages/aesquad && npm install

# Then, in OpenClaw config (illustrative):
# - agents.list: four agentIds above
# - each workspace SOUL.md pointing at roles/*/AGENT.md
# - symlink skills into each workspace as needed
# - tool allowlists per table
# - bindings so inbound chat reaches the right agentId
```

## What this adapter is not

- Not a full OpenClaw distribution or fork
- Not automatic multi-agent company simulation
- Not a requirement to use OpenClaw — other runtimes can follow the same mapping
- Not the place to redefine roles (edit `roles/*/AGENT.md` instead)

## Related

- Portable IDE wiring: [portable.md](portable.md)
- Workflow: [workflows/feature-delivery.md](../workflows/feature-delivery.md)
- Validate: [packages/aesquad/README.md](../packages/aesquad/README.md)
