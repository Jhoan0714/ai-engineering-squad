#!/usr/bin/env node
import path from "node:path";
import {
  assertSharedChangeId,
  validateDirectory,
  validateExamples,
  validateFile,
} from "../src/validate.mjs";
import { ALL_KINDS } from "../src/kinds.mjs";

function printHelp() {
  console.log(`aesquad — validate AI Engineering Squad handoff contracts

Usage:
  aesquad validate <file.json> [--kind <kind>]
  aesquad validate --dir <directory>
  aesquad validate --examples
  aesquad mcp

Kinds:
  ${ALL_KINDS.join(", ")}

Exit codes:
  0  all validations passed
  1  validation failed
  2  usage error
`);
}

/**
 * @param {import('../src/validate.mjs').ValidateResult[]} results
 */
function printResults(results) {
  for (const r of results) {
    const label = path.basename(r.file);
    if (r.ok) {
      console.log(`OK  ${label}  kind=${r.kind}${r.changeId ? `  changeId=${r.changeId}` : ""}`);
    } else {
      console.log(`FAIL  ${label}  kind=${r.kind ?? "unknown"}`);
      for (const e of r.errors) {
        console.log(`  - ${e.path}: ${e.message}`);
      }
    }
  }
}

function parseArgs(argv) {
  const args = argv.slice(2);
  if (args.length === 0 || args[0] === "-h" || args[0] === "--help") {
    return { command: "help" };
  }
  const command = args[0];
  if (command === "mcp") {
    return { command: "mcp" };
  }
  if (command !== "validate") {
    return { command: "error", message: `Unknown command: ${command}` };
  }

  /** @type {{ command: string, file?: string, dir?: string, examples?: boolean, kind?: string, message?: string }} */
  const opts = { command: "validate" };
  for (let i = 1; i < args.length; i++) {
    const a = args[i];
    if (a === "--examples") opts.examples = true;
    else if (a === "--dir") opts.dir = args[++i];
    else if (a === "--kind") opts.kind = args[++i];
    else if (a.startsWith("-")) {
      return { command: "error", message: `Unknown option: ${a}` };
    } else if (!opts.file) opts.file = a;
    else return { command: "error", message: `Unexpected argument: ${a}` };
  }
  return opts;
}

async function main() {
  const opts = parseArgs(process.argv);

  if (opts.command === "help") {
    printHelp();
    process.exit(0);
  }

  if (opts.command === "error") {
    console.error(opts.message);
    printHelp();
    process.exit(2);
  }

  if (opts.command === "mcp") {
    await import("../src/mcp.mjs");
    return;
  }

  /** @type {import('../src/validate.mjs').ValidateResult[]} */
  let results = [];

  if (opts.examples) {
    results = validateExamples();
  } else if (opts.dir) {
    results = validateDirectory(opts.dir);
  } else if (opts.file) {
    results = [validateFile(opts.file, { kind: opts.kind })];
  } else {
    console.error("Provide a file, --dir, or --examples");
    printHelp();
    process.exit(2);
  }

  printResults(results);

  if (results.length > 1) {
    const shared = assertSharedChangeId(results);
    if (!shared.ok) {
      console.log(`FAIL  batch: ${shared.message}`);
      process.exit(1);
    }
    if (results.every((r) => r.ok)) {
      console.log(`OK  batch  ${shared.message}`);
    }
  }

  const failed = results.some((r) => !r.ok);
  process.exit(failed ? 1 : 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(2);
});
