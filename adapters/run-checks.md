# Run-checks adapter contract

**Status:** ready (backlog **F5**)

Pluggable contract so Automation (and CI) can run project checks **without** the kit mandating a test framework.

## Interface

A consumer provides an executable entrypoint that:

| Requirement | Detail |
|-------------|--------|
| **Invoke** | `./run-checks.sh` or `run-checks` on `PATH`, from the project root (or path configured by the consumer) |
| **Args** | Optional: none required for MVP. Future: `--suite smoke` etc. |
| **Exit code** | `0` = all required checks passed · non-zero = failure |
| **Stdout/stderr** | Human-readable summary; failures should be actionable |
| **Env** | May use project-local venv/deps; document in the project README |

The kit does **not** require Robot, Playwright, pytest, etc. The sample app ships **one** reference implementation using pytest (demo-only).

## Reference implementation

| Path | Stack |
|------|--------|
| [examples/demo-todo/run-checks.sh](../examples/demo-todo/run-checks.sh) | Python + pytest |

## Mapping to handoffs

Automation Engineer records how to run checks in `check-mapping.howToRun` (see [contracts/schemas/check-mapping.schema.json](../contracts/schemas/check-mapping.schema.json)), typically pointing at this entrypoint.

## Non-goals

- Installing global CI vendors
- Replacing `aesquad validate` (handoff JSON validation is separate)
- Mandating a single language for all consumers
