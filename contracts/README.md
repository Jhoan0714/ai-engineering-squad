# Contracts

Handoff artifact **shapes** between roles. Instances are JSON; shapes are **JSON Schema** (Draft 2020-12).

Designed so a future H0 `validate` entrypoint can check handoffs without rewriting role content.

## Decision

| Choice | Value |
|--------|-------|
| Format | JSON instances + JSON Schema |
| Schema draft | 2020-12 |
| Contract `schemaVersion` | `1.0.0` on each handoff |

Markdown is not the machine contract (optional human notes may live elsewhere).

## Handoff chain

```text
PM                → acceptance-package
Senior SE         → implementation-handoff
QA Engineer       → risk-notes
Automation Eng.   → check-mapping
Human             → signoff
```

All instances for one change share the same `changeId`.

## Schemas

| Schema | Producer | Consumer |
|--------|----------|----------|
| [schemas/acceptance-package.schema.json](schemas/acceptance-package.schema.json) | Product Manager | Senior SE, QA, Automation |
| [schemas/implementation-handoff.schema.json](schemas/implementation-handoff.schema.json) | Senior Software Engineer | QA |
| [schemas/risk-notes.schema.json](schemas/risk-notes.schema.json) | QA Engineer | Automation, human |
| [schemas/check-mapping.schema.json](schemas/check-mapping.schema.json) | Automation Engineer | human / CI |
| [schemas/signoff.schema.json](schemas/signoff.schema.json) | Human | audit / release record |

## Examples

See [examples/](examples/) for a single demo `changeId` (`demo-password-reset`) flowing through the chain.

## Validation (H0)

Use the shared **aesquad** CLI / MCP package:

```bash
cd packages/aesquad
npm install
node ./bin/aesquad.mjs validate --examples
node ./bin/aesquad.mjs validate --dir ./examples   # from contracts/, adjust path
```

See [packages/aesquad/README.md](../packages/aesquad/README.md).
