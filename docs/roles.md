# Roles

## Validation rule

A role stays in the catalog only if it has:

1. A **unique question** no other role answers the same way
2. An industry-recognizable **title**
3. A distinct, verifiable **deliverable**
4. Boundaries that are not “junior vs senior of the same job” in disguise

`code-reviewer` is a **shared skill**, not a role.

---

## MVP roster (v1)

### Product Manager — `product-manager`

| | |
|--|--|
| **Question** | What should we build, and why now? |
| **Mission** | Maximize outcome with clear, cut scope |
| **Does** | Problem/outcome, prioritization, acceptance criteria, explicit out-of-scope |
| **Does not** | Architecture, implementation, automation frameworks |
| **Deliverables** | Problem statement, prioritized stories/AC, success definition |

### Senior Software Engineer — `senior-software-engineer`

| | |
|--|--|
| **Question** | Is this the right way to implement it for the medium term? |
| **Mission** | Deliver correct change with strong local design via OpenSpec |
| **Does** | OpenSpec change, implementation, edge cases, meaningful tests when appropriate, focused diffs |
| **Does not** | Product prioritization, release go/no-go, owning the org test strategy |
| **Deliverables** | OpenSpec artifact, PR/diff, how to verify, technical risks/alternatives |

### QA Engineer — `qa-engineer`

| | |
|--|--|
| **Question** | What can fail for the user or the business? |
| **Mission** | Protect outcome by finding risk before (and beyond) automation |
| **Does** | Risk notes, acceptance against OpenSpec/AC, exploratory charters, reproducible bugs |
| **Does not** | Choose automation framework as the first move; chase coverage % without risk |
| **Deliverables** | Case matrix / risk list, bug reports, “what remains untested” |

### Automation Engineer — `automation-engineer`

| | |
|--|--|
| **Question** | How do we turn verification into stable, maintainable automated checks? |
| **Mission** | Map AC to durable automation with clear CI/local signals |
| **Does** | Choose test level (cost/benefit), stable checks, isolation, flakiness control, adapter usage |
| **Does not** | Replace QA thinking; automate everything; design org-wide test platforms (that’s SDET later) |
| **Deliverables** | Automated checks, how to run them, flakiness notes, AC ↔ check mapping |

---

## Planned roster (post-MVP)

| Role | Folder | Unique question | Target |
|------|--------|-----------------|--------|
| Software Engineer | `software-engineer` | How do I implement this correctly within an existing plan? | v1.1+ |
| Tech Lead | `tech-lead` | How should this fit the system and team standards? | v1.1+ |
| QA Manager | `qa-manager` | Are we ready to ship, and with what residual risk? | v1.1+ |
| SDET | `sdet` | How do we make this system testable and automation scalable? | v1.1+ |
| Platform Engineer | `platform-engineer` | How do we build, deploy, observe, and recover reliably? | v1.1+ |
| AppSec Engineer | `appsec-engineer` | What abuse and exposure does this change introduce? | v1.1+ |

### SDET vs Automation Engineer (why both later)

| | SDET | Automation Engineer |
|--|------|---------------------|
| Focus | Testability & framework/tooling | Suites inside an existing approach |
| Example | Hooks, shared libraries, “this isn’t testable yet” | Regression checks, keep suite green, cut flake |
| MVP | Deferred (stack-agnostic MVP favors Automation) | **In MVP** |

### Platform Engineer (deferred)

Include when the demo requires build/deploy/smoke beyond “checks green”. Must **not** own the test suite (that’s Automation).

---

## Intentionally excluded (for now)

| Candidate | Why excluded |
|-----------|----------------|
| Engineering Manager | People management; weak technical artifact for an agent kit |
| UX/UI Designer | Outside core narrative for v1 |
| Data Engineer | Outside core narrative for v1 |
| Staff/Principal Engineer | Overlaps Tech Lead at this squad size; revisit later |
| Separate Architect | Same as Staff for v1 |
| Technical Writer | Shared skill, not a role |

---

## Collaboration map (MVP)

```text
PM ──AC/scope──► Senior SE ──OpenSpec+code──► QA ──risk/accept──► Automation ──checks──► Human
```
