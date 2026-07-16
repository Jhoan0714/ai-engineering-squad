# Open questions

Decisions still open before or during implementation. Update status as they close.

**Priority note:** backlog work follows **P0 waves**, not epic letter order. See [backlog.md](backlog.md).

| # | Question | Options / notes | Status |
|---|----------|-----------------|--------|
| 1 | Exact OpenSpec convention in-repo | Upstream OpenSpec layout vs lightweight `openspec/` subset documented here | open |
| 5 | Sample app stack for demo only | e.g. small Node/Python app — must stay clearly “example only” | open |
| 7 | Repo visibility timeline | Public from first commit vs private until demo works | open |

## Already decided

| Decision | Choice |
|----------|--------|
| Project name | `ai-engineering-squad` |
| Language | English |
| License | **Apache License 2.0** |
| Product direction | Kit + contracts → **H0 thin embed in MVP** → full embed suite post-MVP |
| Backlog rule | **P0 over epic order**; epics are thematic only |
| Canonical layout | Root `roles/`, `skills/`, `workflows/`, `contracts/`, `adapters/`, `examples/` + `AGENTS.md` ([docs/layout.md](layout.md)); adapters sync, not fork |
| Handoff contracts | **JSON + JSON Schema (Draft 2020-12)**; `schemaVersion` `1.0.0` ([contracts/](../contracts/)) |
| H0 surfaces | **CLI + MCP** sharing `packages/aesquad` validate core (GitHub Action deferred) |
| Portable adapters (E2) | Document Cursor + Claude Code + Copilot in parallel ([adapters/portable.md](../adapters/portable.md)) |
| Multi-agent adapter (E3) | **OpenClaw-first** mapping guide ([adapters/multi-agent.md](../adapters/multi-agent.md)) |
| MVP roles | PM, Senior SE, QA, Automation Engineer |
| Dual runtime | Portable kit **and** multi-agent runtime |
| OpenSpec | Required on Senior SE path |
| Stack | Agnostic / pluggable adapters |
| Independence | No hard dependency on other personal OSS repos |
| SDET / Platform / leads | Post-MVP (Epic G) |
| DevOps in MVP | No (deferred as Platform Engineer) |
| Full CLI/Action/MCP suite in MVP | No — H0 is validate-only (CLI + MCP); richer orchestration post-MVP |
| PR practice | One PR per backlog feature / milestone |
| Commit practice | Prefer one commit per file within a feature PR |
