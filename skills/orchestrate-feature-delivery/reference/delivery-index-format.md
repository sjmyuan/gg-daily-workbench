# Delivery Index Format

The delivery index is written at **`<base>/deliveries/<epic-name>/index.md`** — one folder per epic (no `docs/` prefix), named after the spiked epic (`<epic-name>` = spike name). The delivery base is the spike's recorded artifact base (`scope.md` `Artifact root:`), so `deliveries/` is a sibling of the spike's `spikes/`; it is inherited, never re-resolved, with `resolve-artifact-location` as fallback only when the record is missing. The spike's own artifacts stay untouched in the spike folder (`spikes/<spike-name>/`; ADRs in `adrs/`, solution doc at the root, findings in `docs/`) and are referenced from the index via **Spike References** — references only, never copies. Boundary map: **reference/artifact-map.md**. The index is the epic's **single source of truth for state** — the orchestrator reads it to decide next actions, updates it as agents report, and uses its **Spike References** so every agent brief can point agents at the full spike output.

## Concise writing and size budget

The index is a **board**, not a report: **≤8,000 chars / ≤120 lines**. Table-first; prose states takeaways only (see **reference/writing-style.md**).

- **Summary**: one line — `N features · M repos · W waves · critical path: F_x → F_y`.
- **Feature goal**: ≤8 words; dependencies/statuses live in tables.
- One **feature table row** per feature — never a multi-line section per feature.
- Detail lives in `<repo>/<feature-name>/context.md`; history lives in git/PR.
- Archive a fully done wave to `archive/index-wave-<n>.md`; leave one pointer row. Never delete.
- No narrative sections ("Outcome", incident retellings): keep ≤5 lines in `## Notes`.
- Measure `wc -l` and `wc -m` after every write; over budget blocks the update.

## Delivery layout

```
deliveries/<epic-name>/               # one folder per epic (no docs/ prefix)
├── <repo-name>/                      # one folder per repo
│   ├── <feature-name>/               # one folder per feature for this repo
│   │   ├── context.md                # charter + latest handoff (40–60 lines target; 8k ceiling)
│   │   └── plan.md                   # TDD plan (plan-development-task)
│   └── ...
└── index.md                          # delivery index (single source of truth)
```

The verification gate reuses these docs: `plan.md` step statuses, the **latest** `context.md` `## Execution` handoff (status, `base7..head7`, PR, one-line evidence, one-line review outcome), and persistent `## Open concerns`; prior rounds are in git/PR. The code-reviewer fetches the diff from git, and findings go straight to the planner as a `rework-<date>.md` (see **reference/verification-gate.md**).

## Structure

```markdown
# Delivery Index: [Spike Goal]

Artifact base: `[<base>]` · [one-line epic scope]

## Summary
[N features · M repos · W waves · critical path: F_x → F_y]

## Spike References
- **Solution doc**: [path — target-state section per feature]
- **ADRs**: [paths — one per decision problem (area-prefixed)]

## Repos
- repo-a — [what changes here]
- repo-b — [...]

## Features
| ID | Name | Wave | Repos | Dependencies | ADRs | Rework of | Goal |
|---|---|---|---|---|---|---|---|
| F1 | wallet-contracts | 0 | repo-a | — | adr-wallet-01 | — | Wallet DTOs + envelope |
| F2 | wallet-service | 1 | repo-b | F1 (merge-blocked) | adr-wallet-01 | — | Wallet service + ledger |

POC cells add `Type: poc` to the feature row; see **POC cells** below for where each field lives.

## Waves
| Wave | Features | Merge gate |
|---|---|---|
| 0 | F1 | — |
| 1 | F2 | after F1 merges |

## Cell plan status
| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| repo-a/F1 | 1234-f1-api | — | — | planned | agent-A | deliveries/<epic-name>/repo-a/wallet-contracts/ |
| repo-b/F2 | f2-schema | #42 | e5f6a7b | in-progress | agent-B | deliveries/<epic-name>/repo-b/wallet-service/ |
| repo-c/F3 | 1234-f3-gateway | #43 | c7d8e9f | verified | code-reviewer-A | deliveries/<epic-name>/repo-c/wallet-api-gateway/ |
| repo-c/F4 | — | — | — | unplanned | — | — |

## Notes
- [current decision or blocker + date; ≤5 lines]
```

Plan locations use the feature's **kebab-case name** (e.g. `wallet-contracts` for F1), never its ID (`F1`). **Branch**, **PR**, and **Commit** are pointers — always tracked in the index (easy to find, easy to verify); work history stays in `plan.md` / git. The branch is recorded when the cell is planned; the **Commit** (head commit from the execution handoff) once the cell first commits; the PR reference (number or URL) once a PR is opened — `—` until then. A cell is **done** only when its merged PR includes the recorded head commit (or the user confirms verified).

The index tracks **status only** — verification findings are not recorded here; the orchestrator dispatches them straight to the planner/executor and the `rework-<date>.md` file is the record (see **verify-cell**).

## Per-cell scope brief

Each cell carries a brief that seeds **plan-development-task** and every later dispatch for that cell. Fill each item by where the info lives:

- **By reference** — persisted in an artifact (index, `context.md`, spike/plan/rework file): feature, repo, scope, branch, plan location, spike references, dependency/wave context → the **path + section**; never inline a whole spike artifact.
- **Inline** — orchestrator/user-only context: global constraints not yet persisted, prior gate findings → the **value** (see **reference/verification-gate.md**).

Brief items:

- **Feature**: ID + name + goal from the Features table
- **Repo**: repo name
- **Scope**: ADR refs + target-state section
- **Plan location**: the feature folder (`deliveries/<epic-name>/<repo>/<feature-name>/`) the planner writes `plan.md` + `context.md` into and the executor reads them from
- **Charter**: `context.md` — why, must-hold invariants, unknowns, done criteria, pointers (not restated inline)
- **Spike references**: the file paths + section pointers (from **Spike References**) the agent should load for full context
- **Dependency context**: what must be merged before this cell's PR (other repos / features)
- **Constraints**: one PR per repo per feature (soft — may merge with other features when convenient)
- **Branch**: the branch name to use for this cell, matching the **repo's branch convention** (per **branch-and-push-conventions**); created during the agent's Prepare Environment step, pushed only after user confirmation
- **Integration**: push and open the PR after user approval; return the PR reference in the executor handoff (see **branch-and-push-conventions**)
- **PR / Commit** — index pointers recorded **after** work: the PR reference and head commit from the handoff; `—` until recorded, never dispatch context

## Status lifecycle

Transitions: **reference/state-machine.md**. POC fork: **verified** → **poc-ready** → **adopted** | **rejected**.

## Ready-to-dispatch predicate

- **Ready to develop**: all dependency cells are **planned** (contracts agreed — contract-first and independent cells develop in parallel; merge-blocked cells wait for the dependency's contract).
- **Ready to execute**: cell is **planned** AND its plan file is verified on disk at the recorded Plan location (the plan-first gate).
- **Ready to verify**: cell is **in-progress** AND `plan.md` shows every step ✅ or ⏭ with the `## Execution` handoff recorded in `context.md` (→ code-reviewer).
- **Ready to merge**: cell is **verified** AND all dependency cells are **done** (merged).

## Status semantics

| Status | Meaning | Orchestrator action |
|---|---|---|
| **unplanned** | No plan files yet | Dispatch the **planner** (plan-development-task) |
| **planned** | `plan.md` + `context.md` exist (verified on disk) | Dispatch the **executor** (execute-plan) — only after the plan-file gate passes |
| **in-progress** | Execution running or complete, not yet verified | Resume from the last step in the active `rework-<date>.md` (per the `context.md` manifest), or `plan.md` if no rework; apply **verify-cell** when the executor reports |
| **verified** | Independent verification gate passed (spec + trust); awaits merge | Executor pushes and opens the PR; merge when dependencies are **done** |
| **poc-ready** | POC implemented + MR open; gate passed | Wait for the user to review the MR and record **adopted**/**rejected** |
| **adopted** | POC proved the option | Promote (merge → done) or feed the **poc-gated** feature |
| **rejected** | POC failed the criteria | Close the cell; delivery proceeds on the other option |
| **superseded** | Existing implementation replaced by an adopted POC | Skip; keep as history |
| **done** | Merged / user-confirmed (PR + head commit recorded) | Skip; unlock downstream cells |
| **failed** | Agent error (reason recorded) | Ask user: retry; dispatch the **planner** to amend the same plan for a pending-step defect; rework for executed behavior |
| **blocked** | Waiting on blocker (recorded) | Wait; re-check when blocker clears |

## POC cells

Record `Type: poc` in the feature row and `replaces` / `compare` in the index's POC metadata. The cell's `plan.md` header carries `**Type**: poc`, `**ADR**`, `**Option**`, and the optional `**Success criteria**`; `context.md` holds the ADR/solution pointers. Lifecycle and adoption: **reference/poc-lifecycle.md** (see **poc-definition** in the SKILL.md knowledge).

## ADR changes mid-delivery

ADRs are **versionless** — drift is signaled by the **adr-writer** agent's return or the user's report, never by diffing the ADR. Routing by status: **reference/orchestration-guide.md** (ADR changes). Record each cell's re-route (status + note) in the index before dispatching.

## Rework after implementation

The index tracks **state only** — rework never adds work history to a status cell. Record rework per the cell's status (see **rework-modes** in the SKILL.md knowledge); the details (trigger, ADR focus, boundary, done criteria, delta steps) live in a sibling `rework-<date>.md` — written by **plan-development-task**, never repeated in the index. The rework inherits the cell's `context.md` charter by reference and never creates a second context. `plan.md` is the frozen original; each rework gets its own file so it never grows. A `## Reworks` manifest in `context.md` lists every rework file + status, one row each; the rework files themselves remain the history (see **plan-file-format.md** in **plan-development-task**).

An **amendment** is not a rework: it adjusts pending steps in the same `plan.md`, keeps the same plan location, and never adds a cell, wave, or status change. It is recorded in `context.md` `## Amendments`.

**Post-merge (cell done)** — original cell unchanged, rework is its own cell:

- Keep the original cell exactly as-is (status **done**; no note, no history).
- Add the rework as a new feature/cell (e.g., `F2-r1`) in a **new wave** after the original feature, with metadata `**Rework of**: F2`; it depends on the original cell's PR (already merged).
- Its plan location points at the rework file: `deliveries/<epic-name>/order-service/wallet-service/rework-2026-08-08.md`.

**Pre-merge (cell in-progress — implemented but not pushed/merged)** — no index change; includes verification-gate fixes (**verify-cell**):

- Keep the cell's identity and **in-progress** status; no new feature/wave, no note.
- A sibling `rework-<date>.md` is written (implemented steps never modified) — that file is the record; the cell proceeds to push approval after the rework.
