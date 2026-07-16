# Add todo priority

## Context

Product wants users to distinguish urgent work from later work when creating todos.
`changeId`: `demo-add-todo-priority`.

Acceptance criteria: see `handoffs/acceptance-package.json` (`AC-1` … `AC-3`).

## Proposal

Extend the Todo API so create (and update) accept an optional `priority` field:
`low` | `medium` | `high`, default `medium`.

## Out of scope (technical)

- Persistence (DB)
- Auth
- UI

## Approach

- Validate priority on `POST /todos` and `PATCH /todos/<id>`
- Store `priority` on the in-memory todo record
- Cover with pytest via `./run-checks.sh`

## Acceptance criteria covered

- AC-1, AC-2, AC-3

## Verification

- `./run-checks.sh`
- Manual: `POST /todos` with `priority=high` and list todos

## Risks / alternatives

- Alternative: free-text priority — rejected for weak validation
