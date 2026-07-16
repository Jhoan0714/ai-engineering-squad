# CrewAI spike checklist

## Prerequisites

- [ ] Python 3.10+
- [ ] `pip install -r examples/crewai/requirements.txt`
- [ ] LLM API credentials configured for CrewAI
- [ ] `packages/aesquad` ready (`npm install`)

## Run

```bash
cd examples/crewai
source .venv/bin/activate
python run_squad.py --change-id spike-$(date +%Y%m%d) --idea "Describe the change outcome"
```

## Validate

```bash
node ../../packages/aesquad/bin/aesquad.mjs validate --dir ./handoffs/<changeId>
```

## Human signoff

Write `handoffs/<changeId>/signoff.json` using `contracts/schemas/signoff.schema.json`, then re-validate the directory.

## Done when

- [ ] Four sequential tasks completed
- [ ] Four machine handoffs validate with `aesquad`
- [ ] Human signoff recorded
- [ ] Notes captured on CrewAI/LLM friction

## Not in scope

- Agents free-chatting as a roundtable
- Autonomous merge without human signoff
- OpenClaw / SOUL.md workspaces
