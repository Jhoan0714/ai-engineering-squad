# AI Engineering Squad

**Role-based agents for AI-assisted software delivery and quality engineering.**

A portable engineering squad you can run with coding tools (Cursor, Claude Code, Copilot) and multi-agent runtimes (CrewAI-first). Each role has a clear mission, hard boundaries, and concrete deliverables — so agents collaborate like a real delivery team instead of swapping job titles on the same prompt.

> Quality and validation are first-class gates, not an afterthought.

**Product direction:** role kit + stable handoff contracts, then an **early thin embeddable entrypoint** (validate via CLI/Action/MCP) to prove third-party integration value — later a fuller embed suite. No lock-in to a single agent runtime or test stack.

## What this is

- A **canonical role kit** (agents + skills + workflows) shared across tools
- Adapters for **portable IDE agents** and **multi-agent runtimes**
- An opinionated MVP squad focused on **spec → implement → verify → automate → human signoff**
- Stack-agnostic: bring your own framework; adapters plug into your tools
- An **early embed proof** (minimal callable `validate`) plus a later fuller CLI / Action / MCP suite

## What this is not

- A replacement for human judgment on merge/release
- A lock-in to any single agent runtime or test stack
- A full autonomous company of agents — human signoff remains required
- A lock-in to any single LLM vendor

## MVP squad (v1)

| Role | Owns |
|------|------|
| **Product Manager** | Outcome, scope, acceptance criteria, prioritization |
| **Senior Software Engineer** | OpenSpec change, implementation, local design quality |
| **QA Engineer** | Risk, exploratory coverage, acceptance against the spec |
| **Automation Engineer** | Stable automated checks mapped to AC (pluggable stack) |

Leads, managers, SDET, Platform, and AppSec are planned for later releases — see [docs/roles.md](docs/roles.md).

## Happy path (MVP)

```text
Product Manager        → outcome + prioritized scope + AC
Senior Software Eng.   → OpenSpec change + implementation
QA Engineer            → risk + acceptance vs OpenSpec
Automation Engineer    → automated checks mapped to AC
Human                  → merge / go-no-go
```

Target demo: in ~15 minutes, run one change from intent to green checks and human signoff.

## Docs

| Doc | Purpose |
|-----|---------|
| [docs/mvp.md](docs/mvp.md) | MVP scope, DoD, non-goals |
| [docs/backlog.md](docs/backlog.md) | Prioritized backlog (P0 waves) |
| [docs/roles.md](docs/roles.md) | Full roster + role boundaries |
| [docs/layout.md](docs/layout.md) | Canonical folder layout (E1) |
| [docs/open-questions.md](docs/open-questions.md) | Decisions still open |
| [AGENTS.md](AGENTS.md) | Agent index (roles / skills / workflows) |

## Repository layout (summary)

```text
roles/              # Role packs (AGENT.md)
skills/             # Shared skills (SKILL.md)
workflows/          # Multi-role recipes (+ *.pipeline.yaml)
contracts/          # Handoff shapes (JSON Schema)
packages/aesquad/   # H0 CLI + MCP validate
packages/aesquad-crew/  # Dynamic CrewAI runtime
adapters/           # Tool wiring (portable + multi-agent)
examples/           # Demo apps (e.g. demo-todo)
docs/               # Product documentation
```

See [docs/layout.md](docs/layout.md). Canonical content is tool-agnostic; adapters sync into IDE/runtime paths.

## Embed (H0)

Validate handoff JSON with the shared **CLI + MCP** package:

```bash
cd packages/aesquad && npm install
node ./bin/aesquad.mjs validate --examples
```

Full embed notes: [packages/aesquad/README.md](packages/aesquad/README.md).

## CrewAI runtime

Dynamic agents/tasks from kit content (not a hard-coded roster):

```bash
cd packages/aesquad-crew
pip install -r requirements.txt && pip install -e .
python -m aesquad_crew list
```

See [packages/aesquad-crew/README.md](packages/aesquad-crew/README.md).

## Contributing / PRs

Prefer **one pull request per backlog feature or milestone** (e.g. E1 layout, then B1 role pack). Keep PRs reviewable and aligned to a single wave item when practical.

## Language

Repository content is **English** (agents, skills, docs).

## Status

**MVP content shipped** — roles, contracts, skills, feature-delivery workflow, H0 `aesquad` validate, portable + CrewAI adapters, demo-todo, and dynamic `aesquad-crew` runtime.

## License

[Apache License 2.0](LICENSE)
