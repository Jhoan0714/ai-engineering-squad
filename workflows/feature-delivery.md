# Feature delivery

MVP happy path for the four-role squad: **PM → Senior SE → QA → Automation → Human**.

Use one shared `changeId` per change. Each step produces a JSON handoff validated against [contracts/schemas/](../contracts/schemas/). See [contracts/examples/](../contracts/examples/) for a full demo chain.

## When to use

- A new feature or user-visible change with acceptance criteria
- A scoped slice ready for implementation, verification, automation, and human merge
- You want role boundaries enforced with concrete artifacts, not chat-only collaboration

## Roles

| Step | Role | Agent pack |
|------|------|------------|
| 1 | Product Manager | [roles/product-manager/AGENT.md](../roles/product-manager/AGENT.md) |
| 2 | Senior Software Engineer | [roles/senior-software-engineer/AGENT.md](../roles/senior-software-engineer/AGENT.md) |
| 3 | QA Engineer | [roles/qa-engineer/AGENT.md](../roles/qa-engineer/AGENT.md) |
| 4 | Automation Engineer | [roles/automation-engineer/AGENT.md](../roles/automation-engineer/AGENT.md) |
| 5 | Human | merge / go-no-go authority |

## Flow

```text
┌─────────────────┐
│ Product Manager │  acceptance-package.json
└────────┬────────┘
         ▼
┌─────────────────────────┐
│ Senior Software Engineer│  OpenSpec + code + implementation-handoff.json
└────────┬────────────────┘
         ▼
┌─────────────────┐
│  QA Engineer    │  risk-notes.json
└────────┬────────┘
         ▼
┌──────────────────────┐
│ Automation Engineer  │  check-mapping.json
└────────┬─────────────┘
         ▼
┌─────────────────┐
│     Human       │  signoff.json → merge / reject
└─────────────────┘
```

## Step-by-step

### 1. Product Manager — scope and AC

**Input:** idea, ticket, or ambiguous request.

**Do:**

- Clarify outcome and cut scope
- Write testable acceptance criteria with stable ids (`AC-1`, `AC-2`, …)
- List explicit out-of-scope items and success definition

**Output:** `acceptance-package.json`  
**Schema:** [acceptance-package.schema.json](../contracts/schemas/acceptance-package.schema.json)

**Gate:** Senior SE does not start without this artifact (or escalates back to PM).

---

### 2. Senior Software Engineer — OpenSpec + implementation

**Input:** `acceptance-package.json`

**Do:**

- Author OpenSpec change aligned to AC
- **Implement production code** (OpenSpec does not replace the PR)
- Add meaningful unit/local tests when warranted
- Document how to verify manually

**Output:** OpenSpec artifact + PR + `implementation-handoff.json`  
**Schema:** [implementation-handoff.schema.json](../contracts/schemas/implementation-handoff.schema.json)

**Gate:** QA does not accept without OpenSpec ref, implementation summary, and verification notes.

---

### 3. QA Engineer — risk and acceptance

**Input:** `acceptance-package.json`, `implementation-handoff.json`

**Do:**

- Validate against AC (not only “tests exist”)
- Prioritize risk; run exploratory checks where needed
- File reproducible bugs; state residual gaps
- Recommend automation candidates (stable, high value)

**Output:** `risk-notes.json`  
**Schema:** [risk-notes.schema.json](../contracts/schemas/risk-notes.schema.json)

**Gate:** Automation does not encode checks without QA’s prioritized candidates (unless explicitly waived by human).

---

### 4. Automation Engineer — stable checks

**Input:** `acceptance-package.json`, `risk-notes.json`, project stack/adapter

**Do:**

- Map AC ids to automated checks (stack is project-specific)
- Document how to run locally and in CI
- Note flakiness; do not hide real failures

**Output:** automated checks in repo + `check-mapping.json`  
**Schema:** [check-mapping.schema.json](../contracts/schemas/check-mapping.schema.json)

**Gate:** Human reviews green checks **and** residual risk from QA before merge.

---

### 5. Human — signoff

**Input:** full handoff chain for `changeId`

**Do:**

- Review AC coverage, QA residual gaps, and check mapping
- Decide: `approve`, `approve-with-risks`, or `reject`
- Merge or send back (never delegate merge authority to agents)

**Output:** `signoff.json`  
**Schema:** [signoff.schema.json](../contracts/schemas/signoff.schema.json)

## Suggested file layout per change

Store instances under a change folder (convention; not enforced until H0):

```text
handoffs/<changeId>/
  acceptance-package.json
  implementation-handoff.json
  risk-notes.json
  check-mapping.json
  signoff.json
```

Until `handoffs/` is standardized, paths in `*Ref` fields may point anywhere in the repo.

## Definition of done (workflow)

The feature-delivery workflow is complete for a `changeId` when:

1. All five JSON handoffs exist and validate against their schemas
2. Senior SE delivered OpenSpec + production code
3. QA documented residual risk (even if empty)
4. Automation mapped AC to checks (or documented uncovered AC)
5. Human recorded `signoff.json` with an explicit decision

## Escalation paths

| Situation | Escalate to |
|-----------|-------------|
| Ambiguous or missing AC | Product Manager |
| AC cannot be implemented as written | Product Manager + Senior SE |
| Blocker bugs | Senior SE (fix) + QA (verify) |
| System not testable enough | Senior SE / future SDET — not “automate anyway” |
| Residual risk unacceptable | Human rejects or `approve-with-risks` with documented acceptance |

## Anti-patterns

- Skipping handoff JSON and relying on chat history
- Senior SE implementing without AC
- QA equating unit tests with full acceptance
- Automation automating everything QA listed without prioritization
- Agents merging or shipping without human `signoff.json`

## Related

- Contracts overview: [contracts/README.md](../contracts/README.md)
- Machine-readable pipeline: [feature-delivery.pipeline.yaml](feature-delivery.pipeline.yaml) (consumed by [packages/aesquad-crew](../packages/aesquad-crew/))
- Demo chain: `changeId` `demo-password-reset` in [contracts/examples/](../contracts/examples/)
- Validate: [packages/aesquad](../packages/aesquad/)