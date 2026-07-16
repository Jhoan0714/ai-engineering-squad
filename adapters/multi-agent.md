# Multi-agent runtime adapters (CrewAI-first)

**Status:** ready (backlog **E3**)

Map each AI Engineering Squad **role** to a **CrewAI** `Agent`, and the feature-delivery workflow to a **sequential** `Crew` (pipeline — not a roundtable chat).

Canonical content stays in this repo (`roles/`, `skills/`, `contracts/`). CrewAI is the orchestration runtime.

> CrewAI APIs evolve. Confirm imports against [CrewAI docs](https://docs.crewai.com/) for your installed version.

## Principle

| Squad concept | CrewAI concept |
|---------------|----------------|
| `roles/<id>/AGENT.md` | `Agent` `role` / `goal` / `backstory` (load from the file) |
| `skills/*` | Tools, knowledge, or prompt appendices |
| `contracts/*` | Expected JSON outputs of each `Task` |
| `workflows/feature-delivery.md` | `Process.sequential` task order |
| `packages/aesquad` | Post-task validation (CLI subprocess or MCP) |

**Rule:** do not fork divergent long-term copies of `AGENT.md`. Load or cite the kit path.

## MVP crew (four agents)

| Agent id | Kit role pack | Typical task output |
|----------|---------------|---------------------|
| `product_manager` | `roles/product-manager/AGENT.md` | `acceptance-package.json` |
| `senior_software_engineer` | `roles/senior-software-engineer/AGENT.md` | OpenSpec + `implementation-handoff.json` (+ code in real runs) |
| `qa_engineer` | `roles/qa-engineer/AGENT.md` | `risk-notes.json` |
| `automation_engineer` | `roles/automation-engineer/AGENT.md` | `check-mapping.json` (+ run-checks) |

Human remains responsible for **`signoff.json`** (merge / go-no-go).

## Pipeline (not roundtable)

```text
PM task  → acceptance-package.json
SE task  → OpenSpec + implementation-handoff.json
QA task  → risk-notes.json
Automation task → check-mapping.json
Human    → signoff.json
```

Each task receives prior outputs via CrewAI `context=[...]`. Agents do not need free-form multi-party chat.

## Runnable example

See [examples/crewai/](../examples/crewai/):

```bash
cd examples/crewai
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...   # or your provider key / CrewAI LLM config
python run_squad.py --change-id demo-crewai-spike --idea "Add due dates to todos"
```

That writes handoffs under `examples/crewai/handoffs/<changeId>/` and can validate them with `aesquad`.

## Mapping snippet

```python
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def load_role(role_id: str) -> str:
    return Path(f"../../roles/{role_id}/AGENT.md").read_text()

pm = Agent(
    role="Product Manager",
    goal="Produce a testable acceptance-package JSON for the change.",
    backstory=load_role("product-manager"),
    verbose=True,
)

# … SE, QA, Automation similarly …

crew = Crew(
    agents=[pm, se, qa, automation],
    tasks=[pm_task, se_task, qa_task, automation_task],
    process=Process.sequential,
)
```

## Tool / permission intent

| Agent | Prefer | Avoid |
|-------|--------|--------|
| Product Manager | Write AC JSON | Architecture / production code |
| Senior SE | Code + OpenSpec | Rewriting product AC |
| QA | Risk notes / scenarios | Framework-first automation |
| Automation | Checks + check-mapping | Inventing AC |

Express this in prompts/`AGENT.md` boundaries; optionally restrict CrewAI tools per agent.

## Validate handoffs

```bash
node ../../packages/aesquad/bin/aesquad.mjs validate --dir ./handoffs/<changeId>
```

## What this adapter is not

- Not a fork of CrewAI
- Not automatic merge without human signoff
- Not a requirement to use OpenAI — configure any LLM CrewAI supports
- Not the place to redefine roles (edit `roles/*/AGENT.md`)

## Related

- Example crew: [examples/crewai/](../examples/crewai/)
- Portable IDE wiring: [portable.md](portable.md)
- Workflow: [workflows/feature-delivery.md](../workflows/feature-delivery.md)
- Validate: [packages/aesquad/README.md](../packages/aesquad/README.md)
