import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** Repo root: packages/aesquad/src -> ../../.. */
export const REPO_ROOT = path.resolve(__dirname, "../../..");

export const SCHEMAS_DIR = path.join(REPO_ROOT, "contracts", "schemas");
export const EXAMPLES_DIR = path.join(REPO_ROOT, "contracts", "examples");

/** @typedef {'acceptance-package' | 'implementation-handoff' | 'risk-notes' | 'check-mapping' | 'signoff'} HandoffKind */

/** @type {Record<HandoffKind, string>} */
export const KIND_TO_SCHEMA = {
  "acceptance-package": "acceptance-package.schema.json",
  "implementation-handoff": "implementation-handoff.schema.json",
  "risk-notes": "risk-notes.schema.json",
  "check-mapping": "check-mapping.schema.json",
  signoff: "signoff.schema.json",
};

/** @type {Record<string, HandoffKind>} */
export const PRODUCED_BY_TO_KIND = {
  "product-manager": "acceptance-package",
  "senior-software-engineer": "implementation-handoff",
  "qa-engineer": "risk-notes",
  "automation-engineer": "check-mapping",
  human: "signoff",
};

/** @type {HandoffKind[]} */
export const ALL_KINDS = Object.keys(KIND_TO_SCHEMA);

/**
 * @param {string} filename
 * @returns {HandoffKind | null}
 */
export function kindFromFilename(filename) {
  const base = path.basename(filename).replace(/\.example\.json$/i, "").replace(/\.json$/i, "");
  if (ALL_KINDS.includes(base)) return /** @type {HandoffKind} */ (base);
  return null;
}

/**
 * @param {unknown} data
 * @param {string} [filename]
 * @returns {HandoffKind | null}
 */
export function detectKind(data, filename) {
  if (data && typeof data === "object" && "producedBy" in data) {
    const producedBy = /** @type {{ producedBy?: string }} */ (data).producedBy;
    if (producedBy && PRODUCED_BY_TO_KIND[producedBy]) {
      return PRODUCED_BY_TO_KIND[producedBy];
    }
  }
  if (filename) return kindFromFilename(filename);
  return null;
}

/**
 * @param {HandoffKind} kind
 */
export function schemaPathForKind(kind) {
  return path.join(SCHEMAS_DIR, KIND_TO_SCHEMA[kind]);
}
