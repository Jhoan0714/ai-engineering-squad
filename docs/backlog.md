# Backlog

## How to read this

| Signal | Meaning |
|--------|---------|
| **P0 / P1 / P2** | Real priority — **P0 wins over epic letter order** |
| **Epic (A–H)** | Thematic grouping only |
| **Depends on** | Hard prerequisite before the item can start |

Execute by **priority waves**, not “finish Epic A before Epic B”.

Status legend: `todo` · `in_progress` · `done` · `blocked`

---

## Execution waves (source of truth)

### Wave 0 — Definition (done)

Product framing, license, MVP/roles docs.

### Wave 1 — Squad content (P0)

Roles + core skills + workflow + handoff **contracts**. Nothing embeddable runs without this.

| Order | IDs | Why this order |
|------|-----|----------------|
| 1 | E1 | Canonical layout so B/C/D land in the right place |
| 2 | B1–B4 | Four MVP role packs |
| 3 | D3 | Handoff contracts (schemas/templates) — embeddable foundation |
| 4 | D1 | `feature-delivery` workflow using those contracts |
| 5 | C1–C4 | Core skills the roles load |

### Wave 2 — Early embed proof (P0)

**Thin slice only:** prove a third party can call *something* before polishing the full kit.

| Order | IDs | Why |
|------|-----|-----|
| 6 | H0a–H0c | Minimal embeddable entrypoint that validates handoffs / checklist |

Depends on: **D3** (and ideally D1). Does **not** wait for full demo or rich adapters.

### Wave 3 — Make it usable everywhere (P0)

| Order | IDs | Why |
|------|-----|-----|
| 7 | E2, E3 | Portable + multi-agent adapter docs |
| 8 | F5, F1–F4 | Adapter stub + sample app + 15-min demo |

### Wave 4 — Polish (P1)

A6, B5, C5–C7, D2, …

### Wave 5 — Expand (P2)

Extra roles (G) and richer embed surfaces (H1+) — after MVP DoD, or in parallel only if Wave 1–3 are healthy.

```text
Wave 0 (done)
    → Wave 1: layout → roles → contracts → workflow → skills
    → Wave 2: H0 thin embed (validate early value)
    → Wave 3: adapters + demo
    → Wave 4: polish
    → Wave 5: more roles / full embed suite
```

---

## Epic A — Product definition

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| A1 | README pitch, scope, non-goals | P0 | done | — |
| A2 | MVP doc | P0 | done | — |
| A3 | Roles catalog | P0 | done | — |
| A4 | Open questions log | P0 | done | — |
| A5 | License: Apache-2.0 | P0 | done | — |
| A7 | Product direction: kit → contracts → embed | P0 | done | — |
| A6 | CONTRIBUTING + Code of Conduct | P1 | todo | — |

---

## Epic B — Canonical role packs (MVP)

Each `AGENT.md`: mission, when to use, responsibilities, out of scope, working style, DoD, skills to load, example prompts.

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| B1 | `roles/product-manager/AGENT.md` | P0 | done | E1 |
| B2 | `roles/senior-software-engineer/AGENT.md` | P0 | done | E1 |
| B3 | `roles/qa-engineer/AGENT.md` | P0 | done | E1 |
| B4 | `roles/automation-engineer/AGENT.md` | P0 | done | E1 |
| B5 | Per-role example prompts (expand) | P1 | todo | B1–B4 |

---

## Epic C — Shared skills

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| C1 | `skills/write-acceptance-criteria` | P0 | done | E1 |
| C2 | `skills/openspec-change` | P0 | done | E1 |
| C3 | `skills/design-test-cases` | P0 | done | E1 |
| C4 | `skills/reduce-flakiness` | P0 | done | E1 |
| C5 | `skills/code-review` | P1 | todo | E1 |
| C6 | `skills/minimal-diff` | P1 | todo | E1 |
| C7 | `skills/bug-report-quality` | P1 | todo | E1 |

---

## Epic D — Workflows & contracts

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| D3 | Handoff contracts (AC, OpenSpec ref, risk notes, check mapping, signoff) | P0 | done | E1 |
| D1 | `workflows/feature-delivery.md` | P0 | done | D3, B1–B4 |
| D2 | `workflows/bug-triage.md` | P1 | todo | D1 |

---

## Epic E — Dual runtime adapters

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| E1 | Canonical repo layout (`AGENTS.md`, roles/, skills/, …) | P0 | done | — |
| E2 | Portable adapter docs (Cursor / Claude / Copilot) | P0 | done | E1, B1–B4 |
| E3 | Multi-agent runtime: CrewAI adapter + `packages/aesquad-crew` | P0 | done | E1, B1–B4 |
| E4 | Install path / symlink-or-copy notes | P1 | done | E2 or E3 |

---

## Epic F — Example / demo

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| F5 | Pluggable “run checks” adapter contract + one reference impl | P0 | done | D3 |
| F1 | Minimal sample app (demo-only stack) | P0 | done | — |
| F2 | Sample OpenSpec change | P0 | done | F1, C2 |
| F3 | QA notes + Automation checks via adapter | P0 | done | F1, F5, D3 |
| F4 | 15-minute demo script | P0 | done | F2, F3, H0b |

---

## Epic H — Embeddable surfaces

Split on purpose: **validate early** (H0), then **expand** (H1+).

### H0 — Thin slice (MVP / Wave 2)

One callable entrypoint a third party can embed. Not a full orchestrator.

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| H0a | Choose first surface: **CLI + MCP** (Action deferred) | P0 | done | — |
| H0b | Implement minimal `validate` (CLI + MCP shared core) | P0 | done | D3, H0a |
| H0c | Document “embed this in 5 minutes” for H0b | P0 | done | H0b |

### H1+ — Full suite (post-MVP / Wave 5)

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| H1 | Versioned installable package of roles/skills | P2 | todo | MVP kit stable |
| H2 | Richer CLI (`init`, run workflow helpers) | P2 | todo | H0b |
| H3 | GitHub Action (if not chosen as H0a) or Action v2 | P2 | todo | H0b |
| H4 | Richer MCP server (beyond validate) | P2 | todo | H0b |
| H5 | Public contract semver policy | P2 | todo | D3, H0b |

---

## Epic G — Post-MVP roles

| ID | Item | Priority | Status | Depends on |
|----|------|----------|--------|------------|
| G1 | `software-engineer` | P2 | todo | MVP roles stable |
| G2 | `tech-lead` | P2 | todo | MVP |
| G3 | `qa-manager` | P2 | todo | MVP |
| G4 | `sdet` | P2 | todo | MVP |
| G5 | `platform-engineer` | P2 | todo | MVP |
| G6 | `appsec-engineer` | P2 | todo | MVP |
| G7 | Workflows: `release-readiness`, `security-sensitive-change` | P2 | todo | G3+ |

---

## P0 checklist (flat)

Use this when pulling work — ignore epic letters:

- [x] A1–A5, A7
- [x] E1
- [x] B1
- [x] B2
- [x] B3
- [x] B4
- [x] D3
- [x] D1
- [x] C1 C2 C3 C4
- [x] H0a H0b H0c
- [x] E2 E3 E4
- [x] F5 F1 F2 F3 F4

---

## Parking lot

- Community adapters for specific stacks (Robot, Playwright, …) without making them core
- Optional notes for personal OSS tools (out of MVP core)
- Public walkthrough (Medium / LinkedIn) after the demo works
