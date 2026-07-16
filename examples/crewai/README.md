# CrewAI squad example

Run the AI Engineering Squad as a **sequential CrewAI crew** (pipeline).

This replaces any OpenClaw-oriented multi-agent path. Canonical roles/skills/contracts stay in the kit root.

## Pipeline

```text
Product Manager      → acceptance-package.json
Senior Software Eng. → implementation-handoff.json (+ OpenSpec stub)
QA Engineer          → risk-notes.json
Automation Engineer  → check-mapping.json
Human                → signoff.json (not automated)
```

## Setup

```bash
cd examples/crewai
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Configure an LLM key for CrewAI (example for OpenAI):

```bash
export OPENAI_API_KEY=sk-...
# Or set your provider per CrewAI docs / .env
```

## Run

```bash
python run_squad.py \
  --change-id demo-crewai-spike \
  --idea "Add optional due dates to todos in the demo API"
```

Outputs:

- `handoffs/<changeId>/*.json`
- `openspec/changes/<changeId>/proposal.md`

Validate:

```bash
cd ../../packages/aesquad && npm install
node ./bin/aesquad.mjs validate --dir ../../examples/crewai/handoffs/demo-crewai-spike
```

## Notes

- Agents load `backstory` from `roles/*/AGENT.md`.
- The crew does **not** auto-merge or write `signoff.json` — that stays human.
- For a deterministic demo without an LLM, use [examples/demo-todo/DEMO.md](../demo-todo/DEMO.md) instead.

## Related

- Adapter: [adapters/multi-agent.md](../../adapters/multi-agent.md)
- Spike checklist: [SPIKE.md](SPIKE.md)
