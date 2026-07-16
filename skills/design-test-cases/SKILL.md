---
name: design-test-cases
description: >-
  Design risk-ordered test scenarios against acceptance criteria for QA and
  automation handoffs. Use when planning coverage, exploratory charters,
  acceptance review, or filling contracts/risk-notes scenarios and
  automationCandidates.
---

# Design test cases

## Instructions

1. Take **AC** (and OpenSpec/verification notes when present) as the source of truth.
2. List risks first: what hurts the user/business if wrong (`impact` × `likelihood`).
3. Derive scenarios covering, as relevant:
   - Happy path
   - Negatives / authz
   - Boundaries and states
   - High-impact edge cases
4. Prioritize by risk — a short ordered list beats a giant unprioritized matrix.
5. For each scenario record: id, title, related `AC-*`, and later `result` (`pass`|`fail`|`blocked`|`deferred`).
6. Mark **automationCandidates** only for stable, high-value scenarios (suggested level: `unit`|`api`|`ui`|`other`).
7. Always state **residualGaps** — what remains untested and why.
8. When producing a formal handoff, align to `contracts/schemas/risk-notes.schema.json`.

## Scenario sketch

| id | title | AC | why it matters |
|----|-------|----|----------------|
| S-1 | Happy path reset | AC-1, AC-2 | Core outcome |
| S-2 | Expired link rejected | AC-3 | Security / integrity |

## Rules

- Do not start with framework choice (Playwright/Robot/…).
- Unit tests in the PR ≠ AC accepted.
- Escalate untestable or missing AC to Product Manager.

## Anti-patterns

- Coverage % as the goal
- “Automate everything” as the design output
- Scenarios that restate AC without failure modes
- Hiding residual risk
