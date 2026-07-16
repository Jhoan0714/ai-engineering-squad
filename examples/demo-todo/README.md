# demo-todo (Python sample)

**Demo-only** Flask Todo API used to exercise the AI Engineering Squad happy path.

> This stack is **not** a product requirement. Consumers may use any language; see [adapters/run-checks.md](../../adapters/run-checks.md).

## Quick start

```bash
cd examples/demo-todo
./run-checks.sh
```

## Feature under demo

`changeId`: **`demo-add-todo-priority`** — optional `priority` on todos (`low`|`medium`|`high`).

| Artifact | Path |
|----------|------|
| OpenSpec | [openspec/changes/demo-add-todo-priority/proposal.md](openspec/changes/demo-add-todo-priority/proposal.md) |
| Handoffs | [handoffs/](handoffs/) |
| 15-minute script | [DEMO.md](DEMO.md) |

## Validate handoffs

```bash
cd ../../packages/aesquad && npm install
node ./bin/aesquad.mjs validate --dir ../../examples/demo-todo/handoffs
```
