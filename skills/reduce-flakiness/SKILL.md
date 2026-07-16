---
name: reduce-flakiness
description: >-
  Diagnose and reduce flaky automated checks while keeping failures meaningful.
  Use when CI is noisy, tests fail intermittently, retries hide races, or an
  Automation Engineer stabilizes suites and documents flakinessNotes in
  contracts/check-mapping.
---

# Reduce flakiness

## Instructions

1. **Reproduce** with evidence: seed, environment, frequency, failing assertion.
2. Classify the cause before “fixing”:
   - Race / timing / shared state
   - Test data collision or order dependence
   - Real product bug (do not silence)
   - Env drift (clock, network, browser, secrets)
3. Prefer fixes in this order:
   1. Deterministic waits / conditions (not blind `sleep`)
   2. Isolation (fresh data, no cross-test coupling)
   3. Stable locators / API contracts
   4. Controlled time/network in test env
   5. Narrow, justified retries — never as the only fix for races
4. Keep failures **actionable**: message should relate to AC/behavior, not only a stack dump.
5. Document remaining flake risk in `check-mapping.flakinessNotes` (and tickets if needed).
6. Re-run enough times to show improvement; note residual rate honestly.

## Decision guide

| Symptom | Likely fix |
|---------|------------|
| Passes alone, fails in parallel | Isolation / shared state |
| Fails only under load/CI slower | Explicit readiness, not fixed sleep |
| Random element not found | Locators, UI timing, app readiness |
| Fails after midnight / DST | Clock control in tests |

## Rules

- Stack stays **pluggable** — apply principles in the project’s runner.
- Do not equate “green after triple retry” with stable.
- If the product is at fault, open/fix the bug; don’t weaken the assertion.

## Anti-patterns

- Blanket retries on the whole suite
- Deleting assertions to go green
- Huge sleeps “to be safe”
- Ignoring flake because “it’s CI”
