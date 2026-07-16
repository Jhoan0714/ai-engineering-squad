---
name: write-acceptance-criteria
description: >-
  Write testable acceptance criteria and acceptance-package fields for product
  changes. Use when clarifying requirements, scoping MVP slices, reviewing weak
  AC, or producing the Product Manager handoff (contracts/acceptance-package).
---

# Write acceptance criteria

## Instructions

1. Start from **outcome** (user/business result), not from UI chrome or tech tasks.
2. Split **in scope** vs **out of scope** before writing AC.
3. Write each criterion so QA can pass/fail it without guessing:
   - Prefer Given / When / Then (or equivalent observable statements).
   - One behavior per criterion; assign stable ids (`AC-1`, `AC-2`, …).
   - Mark priority: `must` | `should` | `could`.
4. Add **successDefinition**: how we know the change worked after release/use.
5. Emit an instance aligned to `contracts/schemas/acceptance-package.schema.json` when producing a formal handoff.
6. If facts are missing, ask — do not invent business rules.

## Quality bar

| Good | Bad |
|------|-----|
| Observable result | “Works well”, “fast”, “intuitive” |
| Explicit actor + trigger + outcome | Implementation details (classes, frameworks) |
| Failures are clear | Soft “should try to…” |

## Example (AC fragment)

```json
{
  "id": "AC-1",
  "statement": "Given a registered email, when the user requests a reset, then they receive a time-limited link.",
  "priority": "must"
}
```

## Anti-patterns

- Stories without measurable AC
- Bundling multiple behaviors in one AC
- Encoding stack choices into AC
- Expanding scope mid-write without updating outOfScope
