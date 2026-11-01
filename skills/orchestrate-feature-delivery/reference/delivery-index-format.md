# Delivery Index Format

The index is written at **`<base>/deliveries/<epic-name>/index.md`** — one folder per epic, named after the spiked epic. Its base is the spike's recorded `scope.md` `Artifact root:` (inherited, never re-resolved; `resolve-artifact-location` only when the record is missing). Layout and naming: **reference/delivery-layout.md**. The spike's artifacts stay untouched in `spikes/<spike-name>/` and are referenced from **Spike References** — never copied. Map: **reference/artifact-map.md**.

The index is the epic's **single source of truth for state**: the orchestrator reads it to decide next actions, updates it as agents report, and briefs every dispatch from it.

## Size budget

The index is a **board**, not a report: **≤8,000 chars / ≤120 lines**; style rules in **reference/writing-style.md**.

- **Summary**: one line — `N features · M repos · W waves · critical path: F_x → F_y`.
- One **feature table row** per feature — never a multi-line section per feature.
- Detail lives in `<repo>/<feature-name>/context.md`; history lives in git/PR.
- Archive a fully done wave to `archive/index-wave-<n>.md`; leave one pointer row. Never delete.
- No narrative sections ("Outcome", incident retellings): keep ≤5 lines in `## Notes`.
- Measure `wc -l` and `wc -m` after every write; over budget blocks the update.

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

POC feature rows add a `Type` column set to `poc` — see **POC cells** below.

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

Plan locations use the feature's **kebab-case name** (`wallet-contracts`), never its ID (`F1`). **Branch**, **PR**, and **Commit** are pointers, always tracked and easy to verify; work history stays in `plan.md` / git. The branch is recorded when the cell is planned, the head **Commit** from the first execution handoff, the **PR** reference once opened — `—` until then.

The index tracks **status only**: verification findings go straight to the planner/executor and the `rework-<date>.md` file is their record (see **verify-cell**). Statuses, transitions, and readiness predicates: **reference/state-machine.md**.

## Per-cell scope brief

Each cell carries a brief that seeds **plan-development-task** and every later dispatch for that cell. Fill each item by mode — path, digest, or inline — per **reference/dispatch-briefs.md**.

- **Feature**: ID + name + goal from the Features table
- **Repo**: repo name
- **Scope**: ADR refs + target-state section
- **Plan location**: the feature folder the planner writes `plan.md` + `context.md` into and the executor reads them from
- **Charter**: `context.md` — why, must-hold invariants, unknowns, done criteria, pointers (not restated inline)
- **Spike references**: the file paths + section pointers from **Spike References**
- **Dependency context**: what must merge before this cell's PR, plus the **delivered contract surface** of any planned/done dependency (interfaces, endpoints, PR, head) as a digest
- **Known locations**: `file:line` and symbols already located for this cell — never re-searched by the agent
- **Ruled out**: rungs already failed, options already rejected, questions already answered for this cell
- **Constraints**: one PR per repo per feature (soft — may merge with other features when convenient)
- **Branch**: the branch name for this cell, per the repo's convention; created during the agent's Prepare Environment step, pushed only after user confirmation
- **Integration**: push and open the PR after user approval; return the PR reference in the executor handoff
- **PR / Commit**: recorded **after** work, from the handoff — never dispatch context

## POC cells

Record `Type: poc` in the feature row and `replaces` / `compare` as index metadata; the cell's `plan.md` header carries `**Type**`, `**ADR**`, `**Option**`, and the optional `**Success criteria**`; `context.md` holds the ADR/solution pointers. Lifecycle, decision gate, and adoption: **reference/poc-lifecycle.md**.

## ADR changes and rework

ADRs are **versionless** — drift comes from the **adr-writer** return or the user, never a file diff. Routing by status: **reference/orchestration-guide.md** (ADR changes); record each cell's re-route in the index before dispatching.

Rework adds no work history: **post-merge** (cell **done**) adds a rework feature `F2-r1` in a new wave with `**Rework of**: F2` and its plan location pointing at `rework-<date>.md`, original stays **done**; **pre-merge** (cell **in-progress**) changes no index row. Modes and lineage: **reference/rework-modes.md**.
