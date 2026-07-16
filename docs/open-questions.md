# Open questions

Decisions still open before or during implementation. Update status as they close.

**Priority note:** backlog work follows **P0 waves**, not epic letter order. See [backlog.md](backlog.md).

| # | Question | Options / notes | Status |
|---|----------|-----------------|--------|
| 1 | Exact OpenSpec convention in-repo | Upstream OpenSpec layout vs lightweight `openspec/` subset documented here | open |
| 3 | First portable tool to optimize for | Cursor vs Claude Code vs both in parallel for E2 | open |
| 4 | First multi-agent runtime to document | OpenClaw first (likely) vs keep runtime-generic longer | open |
| 5 | Sample app stack for demo only | e.g. small Node/Python app — must stay clearly “example only” | open |
| 7 | Repo visibility timeline | Public from first commit vs private until demo works | open |
| 8 | Handoff format | Markdown templates vs JSON schemas — **prefer schemas** if H0 validates programmatically | open |
| 9 | H0 first surface | CLI vs GitHub Action vs tiny MCP — pick before H0b | open |

## Already decided

| Decision | Choice |
|----------|--------|
| Project name | `ai-engineering-squad` |
| Language | English |
| License | **Apache License 2.0** |
| Product direction | Kit + contracts → **H0 thin embed in MVP** → full embed suite post-MVP |
| Backlog rule | **P0 over epic order**; epics are thematic only |
| Canonical layout | Root `roles/`, `skills/`, `workflows/`, `contracts/`, `adapters/`, `examples/` + `AGENTS.md` ([docs/layout.md](layout.md)); adapters sync, not fork |
| MVP roles | PM, Senior SE, QA, Automation Engineer |
| Dual runtime | Portable kit **and** multi-agent runtime |
| OpenSpec | Required on Senior SE path |
| Stack | Agnostic / pluggable adapters |
| Independence | No hard dependency on other personal OSS repos |
| SDET / Platform / leads | Post-MVP (Epic G) |
| DevOps in MVP | No (deferred as Platform Engineer) |
| Full CLI/Action/MCP suite in MVP | No — only H0 `validate` thin slice |
| PR practice | One PR per backlog feature / milestone |
