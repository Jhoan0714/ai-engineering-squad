---
name: openspec-change
description: >-
  Author or refine an OpenSpec-oriented change artifact aligned to acceptance
  criteria, then support implementation handoff. Use when a Senior Software
  Engineer frames a non-trivial change, creates proposal/spec before coding, or
  fills contracts/implementation-handoff openSpec fields.
---

# OpenSpec change

## Instructions

1. Read the PM **acceptance package** (`changeId`, AC ids, in/out of scope). Stop and escalate if AC are ambiguous.
2. Produce an OpenSpec-oriented change that covers:
   - **Context** — why this change exists (link to outcome/AC)
   - **Proposal** — what will change in the system
   - **Scope boundaries** — what is deliberately not changing
   - **Approach** — brief design; note material alternatives if relevant
   - **Verification** — how to confirm AC (manual + any SE-owned unit/integration tests)
3. Keep the artifact **implementation-ready**: a coder can execute it without inventing product intent.
4. After coding, point `implementation-handoff.openSpec.path` at the artifact and summarize in `openSpec.summary`.
5. Prefer the consumer repo’s OpenSpec layout when present; otherwise use a clear path such as `openspec/changes/<changeId>/`.

## Minimum sections

```markdown
# <change title>

## Context
## Proposal
## Out of scope (technical)
## Approach
## Acceptance criteria covered
## Verification
## Risks / alternatives (if material)
```

## Rules

- OpenSpec **frames** the change; it does **not** replace the PR or production code.
- Do not invent AC — reference `AC-*` ids from the acceptance package.
- Keep blast radius small; split if the proposal exceeds one reviewable slice.

## Anti-patterns

- Spec-only delivery with no implementation path
- Silent product decisions inside the proposal
- Giant redesign unrelated to the AC
- Vague “improve quality” proposals without concrete system changes
