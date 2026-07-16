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

## Validation (until H0 ships)

Any JSON Schema Draft 2020-12 validator can check instances, for example:

```bash
# Example with npx (optional; not a repo dependency yet)
npx --yes ajv-cli validate -s contracts/schemas/acceptance-package.schema.json \
  -d contracts/examples/acceptance-package.example.json
```

H0 will wrap this into a stable `validate` entrypoint.
