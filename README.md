# AI Engineering Squad

**Role-based agents for AI-assisted software delivery and quality engineering.**

A portable engineering squad you can run with coding tools (Cursor, Claude Code, Copilot) and multi-agent runtimes (e.g. OpenClaw). Each role has a clear mission, hard boundaries, and concrete deliverables — so agents collaborate like a real delivery team instead of swapping job titles on the same prompt.

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
- An “autonomous company” of ten bots from day one
- A full orchestration runtime in the MVP (H0 is validate-only; rich orchestration is post-MVP)

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
| [docs/backlog.md](docs/backlog.md) | Prioritized backlog |
| [docs/roles.md](docs/roles.md) | Full roster + role boundaries |
| [docs/open-questions.md](docs/open-questions.md) | Decisions still open |

## Language

Repository content is **English** (agents, skills, docs).

## Status

**Planning** — structure and product definition in progress; agent packs and adapters not shipped yet.

## License

[Apache License 2.0](LICENSE)
