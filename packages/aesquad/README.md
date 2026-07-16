# aesquad

Thin **CLI + MCP** surface for validating AI Engineering Squad handoff contracts (JSON Schema).

This is backlog **H0**: prove embeddable value early. It does **not** run OpenClaw or orchestrate agents — it only validates handoff JSON.

## Install (from repo root)

```bash
cd packages/aesquad
npm install
```

Optional global link:

```bash
npm link
```

## CLI (5 minutes)

```bash
# Validate bundled demo chain
node ./bin/aesquad.mjs validate --examples

# Validate one file
node ./bin/aesquad.mjs validate ../../contracts/examples/acceptance-package.example.json

# Validate a directory of handoffs
node ./bin/aesquad.mjs validate --dir ../../contracts/examples

# Optional kind override
node ./bin/aesquad.mjs validate ./my.json --kind acceptance-package
```

Exit code `0` = pass, `1` = validation failed, `2` = usage error.

## MCP

Same validate core, exposed as tools over stdio:

| Tool | Purpose |
|------|---------|
| `validate_handoff` | Validate one JSON file |
| `validate_handoffs_dir` | Validate all `*.json` in a directory |
| `validate_contract_examples` | Validate repo `contracts/examples` |
| `list_handoff_kinds` | List supported kinds |

Run:

```bash
node ./bin/aesquad.mjs mcp
# or
npm run mcp
```

Example Cursor MCP config snippet:

```json
{
  "mcpServers": {
    "aesquad": {
      "command": "node",
      "args": ["/absolute/path/to/ai-engineering-squad/packages/aesquad/bin/aesquad.mjs", "mcp"]
    }
  }
}
```

## Shared core

```text
CLI  ─┐
      ├── src/validate.mjs  → contracts/schemas/*.schema.json
MCP  ─┘
```

Kind detection uses `producedBy` (preferred) or filename (`acceptance-package.json`, etc.).
