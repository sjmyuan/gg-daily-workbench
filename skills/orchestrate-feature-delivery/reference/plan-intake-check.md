# Plan Intake Check

Backs the **planned** transition — the orchestrator's gate between a planner's return and an executor dispatch.

## What it is, and is not

- **Is**: a mechanical contract read of one plan file (≤120 lines), six rows, one verdict.
- **Is not**: a design review. The approach belongs to the planner (**plan-rubric**); the outcome belongs to **verify-cell**. Never re-derive the spec, never rewrite the plan.

## The six checks

| # | Check | A fail means |
|---|---|---|
| 1 | The file exists at the recorded path | There is no plan |
| 2 | Header complete: `Type`, `Branch`, `Test strategy`, `Gate` (three commands), `Autonomy` | The executor guesses commands or cadence |
| 3 | `## Scope Boundary` carries `May change` + `Must not change`, behavior-based; `Protected zones` stated | The boundary is unenforceable |
| 4 | `## Risk` names an assumption with the step that tests it, plus `Expected to break first` | Risk is unfalsifiable |
| 5 | Step 1 = environment + baseline; last step = Exit gate; every step carries its six fields | The gate cannot go green |
| 6 | The plan answers the brief's done-means and cites the governing ADR without contradicting it | Right work, wrong outcome |

## Verdicts

| Verdict | Action |
|---|---|
| **Pass** | Record **planned**; dispatch the executor |
| **Fail** | Return the failed rows to the **planner** as an amendment of the same file; never dispatch |
| **Fail twice on one plan** | Escalate to the user with both rows and the attempt trail |

- A missing file is **failed**, never **planned**.
- A gate narrowed, invented, or unratified is a row-2 fail — never a waiver.
- A row-6 contradiction blocks: nothing runs on a stale decision.
- Record `plan-intake: pass` in the cell's `## Notes` only when a row was arguable.
- A pass is not an endorsement: the plan's quality is graded by the planner's rubric, and the diff by the gate.
