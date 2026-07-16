# MVP

Status: **defined** (implementation not started)

## Goal

Ship a usable **four-role engineering squad** that takes a small change from product intent to human-approved merge, with OpenSpec on the engineering path and automated checks as a quality gate.

## Product direction

| Layer | What ships | Timing |
|-------|------------|--------|
| Content | Roles, skills, workflows | MVP (Wave 1) |
| Contracts | Handoff shapes + pluggable adapter APIs | MVP (Wave 1) |
| **Early embed proof** | `packages/aesquad` **CLI + MCP** `validate` (shared core) | MVP (Wave 2) — done |
| Full embed suite | Richer CLI, GitHub Action, broader MCP orchestration | Post-MVP (Wave 5) |

MVP includes a **thin embeddable entrypoint** so third parties can try integration before the kit is fully polished. It does **not** include a full multi-agent orchestrator.

## In scope

### Dual runtime (day one design)

| Surface | Purpose |
|---------|---------|
| **Portable kit** | Roles/skills/workflows consumable by Cursor, Claude Code, Copilot, etc. |
| **Multi-agent runtime** | Same roles as a sequential CrewAI crew (pipeline handoffs) |

Canonical content lives once; adapters map discovery paths per tool. Neither runtime is optional in the design — both are first-class.

### Roles (exactly four)

1. `product-manager`
2. `senior-software-engineer`
3. `qa-engineer`
4. `automation-engineer`

### Workflow

1. PM clarifies outcome, cuts scope, writes acceptance criteria
2. Senior SE authors an **OpenSpec** change and implements it
3. QA validates risk and acceptance against the OpenSpec / AC
4. Automation Engineer adds or updates automated checks mapped to AC (stack via adapter)
5. Human performs merge / go-no-go

### Stack policy

- **Stack-agnostic**: no required language, browser runner, or CI vendor
- Provide a **pluggable adapter contract** (e.g. “how to run checks”, “how to report results”)
- Ship one **example adapter** for the sample app (implementation detail later; not a product lock-in)

### Independence

This repo does **not** depend on other personal projects (e.g. Vibium, MCP tools). Optional references may appear later as community adapters, not core requirements.

## Out of scope (MVP)

- Tech Lead, QA Manager, SDET, Platform/DevOps, AppSec as first-class roles
- Full autonomous merge/release without human approval
- Jira / Linear / Slack product sync
- Multi-repo orchestration
- Mandatory Robot / Playwright / Vibium / specific cloud CI
- Perfect parity of every feature across every IDE on day one (adapters may land incrementally, but the dual-runtime *model* is in scope)

## Definition of done (MVP)

The MVP is done when all of the following are true:

1. **Role packs** exist for the four MVP roles (`AGENT.md` / equivalent + clear out-of-scope)
2. **Shared skills** exist for at least: OpenSpec-oriented change, acceptance criteria, test design, flaky-signal hygiene, and code review basics
3. **Workflow doc** describes `feature-delivery` end-to-end
4. **Adapters** documented for:
   - at least one portable coding tool
   - at least one multi-agent runtime
5. **Example** project demonstrates: intent → OpenSpec → implementation → QA notes → automated checks → human signoff
6. **README** install path works in ≤15 minutes for a new user on a clean machine (documented assumptions OK)
7. **Handoff contracts** are explicit and versionable
8. **H0 embed proof:** `aesquad validate` (CLI) and MCP tools validate handoffs; documented for third-party use in ~5 minutes

## Success metrics (early)

| Signal | Why it matters |
|--------|----------------|
| External clone + successful demo | Adoption beyond the author |
| Someone runs H0 `validate` outside this repo | Early signal that embeddable direction has value |
| Clear issue reports on role boundaries | Product is being used for real |
| Medium / LinkedIn write-up with concrete workflow | Portfolio / visibility |

## Non-goals for “success”

- Star count as a primary KPI
- Claiming the squad replaces a human team
