#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  assertSharedChangeId,
  validateDirectory,
  validateExamples,
  validateFile,
} from "./validate.mjs";
import { ALL_KINDS } from "./kinds.mjs";

const server = new McpServer({
  name: "aesquad",
  version: "0.1.0",
});

server.tool(
  "validate_handoff",
  "Validate one handoff JSON file against AI Engineering Squad JSON Schema contracts.",
  {
    path: z.string().describe("Absolute or relative path to a handoff JSON file"),
    kind: z
      .enum([
        "acceptance-package",
        "implementation-handoff",
        "risk-notes",
        "check-mapping",
        "signoff",
      ])
      .optional()
      .describe("Optional kind override; otherwise detected from producedBy or filename"),
  },
  async ({ path: filePath, kind }) => {
    const result = validateFile(filePath, kind ? { kind } : {});
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
      isError: !result.ok,
    };
  },
);

server.tool(
  "validate_handoffs_dir",
  "Validate all *.json handoff files in a directory.",
  {
    dir: z.string().describe("Directory containing handoff JSON files"),
  },
  async ({ dir }) => {
    const results = validateDirectory(dir);
    const shared = assertSharedChangeId(results);
    const ok = results.every((r) => r.ok) && shared.ok;
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ ok, shared, results }, null, 2),
        },
      ],
      isError: !ok,
    };
  },
);

server.tool(
  "validate_contract_examples",
  "Validate the repository contracts/examples demo handoff chain.",
  async () => {
    const results = validateExamples();
    const shared = assertSharedChangeId(results);
    const ok = results.every((r) => r.ok) && shared.ok;
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ ok, shared, results }, null, 2),
        },
      ],
      isError: !ok,
    };
  },
);

server.tool(
  "list_handoff_kinds",
  "List supported handoff kinds and their schema filenames.",
  async () => {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ kinds: ALL_KINDS }, null, 2),
        },
      ],
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
