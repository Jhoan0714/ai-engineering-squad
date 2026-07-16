import fs from "node:fs";
import path from "node:path";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import {
  ALL_KINDS,
  EXAMPLES_DIR,
  detectKind,
  schemaPathForKind,
} from "./kinds.mjs";

/**
 * @typedef {{
 *   ok: boolean,
 *   file: string,
 *   kind: string | null,
 *   changeId?: string,
 *   errors: Array<{ path: string, message: string, keyword?: string }>
 * }} ValidateResult
 */

function createAjv() {
  const ajv = new Ajv2020({
    allErrors: true,
    strict: false,
  });
  addFormats(ajv);
  return ajv;
}

/** @type {Map<string, import('ajv').ValidateFunction>} */
const validatorCache = new Map();
const ajv = createAjv();

/**
 * @param {import('./kinds.mjs').HandoffKind} kind
 */
function getValidator(kind) {
  if (validatorCache.has(kind)) return validatorCache.get(kind);
  const schemaPath = schemaPathForKind(kind);
  const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
  const validate = ajv.compile(schema);
  validatorCache.set(kind, validate);
  return validate;
}

/**
 * @param {string} filePath
 * @param {{ kind?: string }} [options]
 * @returns {ValidateResult}
 */
export function validateFile(filePath, options = {}) {
  const absolute = path.resolve(filePath);
  /** @type {ValidateResult} */
  const result = {
    ok: false,
    file: absolute,
    kind: null,
    errors: [],
  };

  if (!fs.existsSync(absolute)) {
    result.errors.push({ path: "", message: `File not found: ${absolute}` });
    return result;
  }

  let data;
  try {
    data = JSON.parse(fs.readFileSync(absolute, "utf8"));
  } catch (err) {
    result.errors.push({
      path: "",
      message: `Invalid JSON: ${err instanceof Error ? err.message : String(err)}`,
    });
    return result;
  }

  const kind =
    (options.kind && ALL_KINDS.includes(options.kind) ? options.kind : null) ||
    detectKind(data, absolute);

  result.kind = kind;
  if (data && typeof data === "object" && "changeId" in data) {
    result.changeId = String(/** @type {{ changeId: unknown }} */ (data).changeId);
  }

  if (!kind) {
    result.errors.push({
      path: "/producedBy",
      message:
        "Could not detect handoff kind. Pass --kind or set producedBy to a known role.",
    });
    return result;
  }

  const validate = getValidator(/** @type {import('./kinds.mjs').HandoffKind} */ (kind));
  const ok = validate(data);
  if (ok) {
    result.ok = true;
    return result;
  }

  result.errors = (validate.errors || []).map((e) => ({
    path: e.instancePath || "/",
    message: e.message || "validation failed",
    keyword: e.keyword,
  }));
  return result;
}

/**
 * @param {string} dirPath
 * @returns {ValidateResult[]}
 */
export function validateDirectory(dirPath) {
  const absolute = path.resolve(dirPath);
  if (!fs.existsSync(absolute) || !fs.statSync(absolute).isDirectory()) {
    return [
      {
        ok: false,
        file: absolute,
        kind: null,
        errors: [{ path: "", message: `Not a directory: ${absolute}` }],
      },
    ];
  }

  const files = fs
    .readdirSync(absolute)
    .filter((f) => f.endsWith(".json"))
    .map((f) => path.join(absolute, f))
    .sort();

  if (files.length === 0) {
    return [
      {
        ok: false,
        file: absolute,
        kind: null,
        errors: [{ path: "", message: "No .json files found in directory" }],
      },
    ];
  }

  return files.map((f) => validateFile(f));
}

/**
 * Validate bundled contract examples in this repository.
 * @returns {ValidateResult[]}
 */
export function validateExamples() {
  return validateDirectory(EXAMPLES_DIR);
}

/**
 * Cross-check that all results sharing a changeId are consistent when multiple files pass.
 * @param {ValidateResult[]} results
 * @returns {{ ok: boolean, message: string }}
 */
export function assertSharedChangeId(results) {
  const ids = [
    ...new Set(
      results.filter((r) => r.ok && r.changeId).map((r) => /** @type {string} */ (r.changeId)),
    ),
  ];
  if (ids.length <= 1) {
    return { ok: true, message: ids[0] ? `changeId=${ids[0]}` : "no changeId" };
  }
  return {
    ok: false,
    message: `Multiple changeId values in batch: ${ids.join(", ")}`,
  };
}
