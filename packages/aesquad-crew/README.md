# aesquad-crew

Dynamic **CrewAI** runtime for AI Engineering Squad.

Agents and tasks are **not hard-coded**. They are built from:

| Source | What it drives |
|--------|----------------|
| `workflows/*.pipeline.yaml` | Step order, handoff kinds, context graph, task hints |
| `roles/<id>/AGENT.md` | Title, goal (Mission), backstory, skills to load |
| `skills/<id>/SKILL.md` | Appended into the agent backstory when present |
| `contracts/schemas/*.schema.json` | Required fields / `producedBy` for each task prompt |

`packages/aesquad` remains the **validator** only. This package is the **orchestrator**.

## Install

```bash
cd packages/aesquad-crew
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Configure an LLM for CrewAI (example):

```bash
export OPENAI_API_KEY=sk-...
```

## Inspect (no LLM)

From the repo root (or any cwd; kit root is auto-detected):

```bash
python -m aesquad_crew list
```

Shows each pipeline step with role title, goal, skills, and handoff artifact — all loaded dynamically.

## Run

```bash
python -m aesquad_crew run \
  --change-id demo-crewai-spike \
  --idea "Add optional due dates to todos" \
  --out-dir ./out
```

Or after `pip install -e .`:

```bash
aesquad-crew run --change-id demo-crewai-spike --idea "…" --out-dir ./out
```

Outputs:

- `out/handoffs/<changeId>/*.json` (one per pipeline step)
- `out/openspec/changes/<changeId>/proposal.md` when the step defines `openspecPathTemplate`

Then validate:

```bash
node ../aesquad/bin/aesquad.mjs validate --dir ./out/handoffs/demo-crewai-spike
```

Human writes `signoff.json` (never produced by the crew).

## Custom / future pipelines

```bash
python -m aesquad_crew run \
  --pipeline ../../workflows/feature-delivery.pipeline.yaml \
  --change-id … --idea …
```

To add a role to the crew later: add `roles/<id>/AGENT.md` and a step in the pipeline YAML. No Python roster edits required.

## Related

- Adapter docs: [adapters/multi-agent.md](../../adapters/multi-agent.md)
- Pipeline: [workflows/feature-delivery.pipeline.yaml](../../workflows/feature-delivery.pipeline.yaml)
- Validate: [packages/aesquad/README.md](../aesquad/README.md)
- Spike checklist: [SPIKE.md](SPIKE.md)
