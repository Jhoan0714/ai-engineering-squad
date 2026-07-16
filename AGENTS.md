# AI Engineering Squad — Agent Index

Canonical entry point for role-based agents, skills, and workflows in this repository.

## How to use this repo

1. Pick a **role** from [roles/](roles/) for the job at hand.
2. Load the **skills** listed in that role’s `AGENT.md` from [skills/](skills/).
3. Follow a **workflow** from [workflows/](workflows/) when collaborating across roles.
4. Produce **handoff artifacts** shaped by [contracts/](contracts/).
5. Wire the kit into your tool via [adapters/](adapters/).

## MVP roles

| Role | Path | Status |
|------|------|--------|
| Product Manager | [roles/product-manager/](roles/product-manager/) | Ready — [AGENT.md](roles/product-manager/AGENT.md) |
| Senior Software Engineer | [roles/senior-software-engineer/](roles/senior-software-engineer/) | Ready — [AGENT.md](roles/senior-software-engineer/AGENT.md) |
| QA Engineer | [roles/qa-engineer/](roles/qa-engineer/) | Ready — [AGENT.md](roles/qa-engineer/AGENT.md) |
| Automation Engineer | [roles/automation-engineer/](roles/automation-engineer/) | Ready — [AGENT.md](roles/automation-engineer/AGENT.md) |

## Core skills (C1–C4)

| Skill | Path |
|-------|------|
| `write-acceptance-criteria` | [skills/write-acceptance-criteria/](skills/write-acceptance-criteria/) |
| `openspec-change` | [skills/openspec-change/](skills/openspec-change/) |
| `design-test-cases` | [skills/design-test-cases/](skills/design-test-cases/) |
| `reduce-flakiness` | [skills/reduce-flakiness/](skills/reduce-flakiness/) |

See [skills/README.md](skills/README.md).

## Layout

See [docs/layout.md](docs/layout.md) for the canonical tree and adapter mapping rules.

## Language

All agent, skill, workflow, and contract content is **English**.
