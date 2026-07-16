# 15-minute demo (F4)

Walk the MVP squad flow on the **Python** sample app `examples/demo-todo`.

## Prerequisites

- Python 3.10+
- Node 18+ (for `aesquad validate`)
- ~15 minutes

## Script

### 1. Checks green (Automation signal) — 3 min

```bash
cd examples/demo-todo
./run-checks.sh
```

Expect pytest pass. This is the reference [run-checks](../../adapters/run-checks.md) adapter.

### 2. Read the story (PM → SE → QA → Automation) — 5 min

Open in order:

1. [handoffs/acceptance-package.json](handoffs/acceptance-package.json) — PM AC  
2. [openspec/changes/demo-add-todo-priority/proposal.md](openspec/changes/demo-add-todo-priority/proposal.md) — Senior SE OpenSpec  
3. [handoffs/implementation-handoff.json](handoffs/implementation-handoff.json) — SE handoff  
4. [handoffs/risk-notes.json](handoffs/risk-notes.json) — QA  
5. [handoffs/check-mapping.json](handoffs/check-mapping.json) — Automation  
6. [handoffs/signoff.json](handoffs/signoff.json) — Human approve  

### 3. Validate contracts (H0 embed) — 3 min

```bash
cd ../../packages/aesquad
npm install
node ./bin/aesquad.mjs validate --dir ../../examples/demo-todo/handoffs
```

Expect all `OK` and shared `changeId=demo-add-todo-priority`.

### 4. Optional: act as a role in your IDE — 4 min

Using [adapters/portable.md](../../adapters/portable.md), prompt:

```text
Act as QA Engineer (roles/qa-engineer/AGENT.md).
Review examples/demo-todo/handoffs/acceptance-package.json
and suggest one additional residual gap.
```

## Done when

- [ ] `./run-checks.sh` exits 0  
- [ ] `aesquad validate --dir …/handoffs` exits 0  
- [ ] You can explain each handoff in one sentence  

## Related

- Workflow: [workflows/feature-delivery.md](../../workflows/feature-delivery.md)
