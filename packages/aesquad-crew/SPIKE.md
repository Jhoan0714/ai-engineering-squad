# aesquad-crew spike checklist

## Prerequisites

- [ ] Python 3.10+
- [ ] `pip install -r packages/aesquad-crew/requirements.txt && pip install -e packages/aesquad-crew`
- [ ] LLM credentials for CrewAI
- [ ] `packages/aesquad` ready (`npm install`)

## Inspect (offline)

```bash
cd packages/aesquad-crew
source .venv/bin/activate
python -m aesquad_crew list
```

Confirm goals/titles come from `roles/*/AGENT.md`, not hard-coded strings.

## Run

```bash
python -m aesquad_crew run \
  --change-id spike-$(date +%Y%m%d) \
  --idea "Describe the change outcome" \
  --out-dir ./out
```

## Validate

```bash
node ../aesquad/bin/aesquad.mjs validate --dir ./out/handoffs/<changeId>
```

## Done when

- [ ] `list` shows four dynamic steps for feature-delivery
- [ ] Run writes one JSON per pipeline step
- [ ] `aesquad validate` passes for those handoffs
- [ ] Human `signoff.json` still manual

## Not in scope

- Roundtable multi-party chat
- Autonomous merge without human signoff
- Hard-coded agent rosters in Python
