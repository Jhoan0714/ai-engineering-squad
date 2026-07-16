# Multi-agent runtime adapters (CrewAI-first)

**Status:** ready (backlog **E3**)

Map each AI Engineering Squad **role** to a **CrewAI** `Agent`, and each `*.pipeline.yaml` workflow to a **sequential** `Crew` (pipeline — not a roundtable chat).

Canonical content stays in this repo (`roles/`, `skills/`, `workflows/`, `contracts/`). CrewAI is the orchestration runtime via [`packages/aesquad-crew`](../packages/aesquad-crew/).

> CrewAI APIs evolve. Confirm imports against [CrewAI docs](https://docs.crewai.com/) for your installed version.

## Principle

| Squad concept | CrewAI concept |
|---------------|----------------|
| `roles/<id>/AGENT.md` | `Agent` title / goal (Mission) / backstory (full pack + skills) |
| `skills/*` | Appended into agent backstory when listed in the role |
| `contracts/schemas/*` | Shape each `Task` must produce |
| `workflows/*.pipeline.yaml` | Step order, handoffs, `contextFrom` graph |
| `packages/aesquad` | Post-run validation (CLI / MCP) |
| `packages/aesquad-crew` | Dynamic crew builder + CLI |

**Rule:** do not hard-code agent rosters in Python. Edit `roles/` and the pipeline YAML; the runtime discovers them.

## Dynamic crew (not a hard-coded list)

```bash
cd packages/aesquad-crew
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e .
python -m aesquad_crew list --llm llama3.1:latest
# Ollama must be running: ollama serve
python -m aesquad_crew run \
  --change-id demo-crewai-spike \
  --idea "Add due dates to todos" \
  --out-dir ./out \
  --llm llama3.1:latest
```

To add a role later: create `roles/<id>/AGENT.md` and a step in `workflows/<id>.pipeline.yaml`. No roster edits in code.

## Pipeline (not roundtable)

Machine-readable source: [workflows/feature-delivery.pipeline.yaml](../workflows/feature-delivery.pipeline.yaml)

```text
PM task  → acceptance-package.json
SE task  → OpenSpec + implementation-handoff.json
QA task  → risk-notes.json
Automation task → check-mapping.json
Human    → signoff.json
```

Each task receives prior outputs via CrewAI `context=[...]` from `contextFrom`.

## Validate handoffs

```bash
node packages/aesquad/bin/aesquad.mjs validate --dir ./out/handoffs/<changeId>
```

## What this adapter is not

- Not a fork of CrewAI
- Not automatic merge without human signoff
- Not a requirement to use OpenAI — configure any LLM CrewAI supports
- Not the place to redefine roles (edit `roles/*/AGENT.md`)
- Not a hard-coded four-agent script

## Related

- Runtime package: [packages/aesquad-crew/](../packages/aesquad-crew/)
- Portable IDE wiring: [portable.md](portable.md)
- Workflow (prose): [workflows/feature-delivery.md](../workflows/feature-delivery.md)
- Validate: [packages/aesquad/README.md](../packages/aesquad/README.md)
