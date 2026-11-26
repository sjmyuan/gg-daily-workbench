# Rework Modes

Rework rules for `orchestrate-feature-delivery`. Rework is **append-only within a round** — implemented steps never change; a new round starts a new delta. Scoped to the cell (usually its governing ADR), never the whole epic.
Each rework is a sibling file — `rework.md` pre-merge (one active file, overwritten per round; git keeps the previous round), `rework-<date>.md` post-merge (one file per rework). `plan.md` stays the frozen original; execution runs **only** the rework file's steps.
Pending-step defects are **amendments** to the same `plan.md`, never reworks and never a new plan folder.
`context.md` holds a `## Reworks` manifest (date, mode, cell, file, status) and an `## Amendments` table so resume finds the active record.
The index records **state only** — the rework cell + plan pointer; details live in the rework file.

| Mode | When | Handling |
|---|---|---|
| **Post-merge** | cell **done** (merged/verified) | focused spike (**conduct-spike**) + ADR / solution-doc updates; new rework feature (e.g. `F2-r1`) in a new wave |
| **Pre-merge** | cell **in-progress** (implemented, not pushed/merged) | spike + ADR / solution-doc updates only if the issue challenges the ADR decision; rework stays on the same cell — rework steps merge with the original work |

- **Rework scope**: the file carries only the delta and opens per **plan-development-task**'s rework convention — mode, cell, branch, ADR focus, inherited gate,
  then its own Scope Boundary, Done means, and delta steps.
  It inherits `context.md` **Must hold** / **Pointers** by reference and never creates a second `context.md`.
- **Rework lineage**: `F2-r1` reworks `F2`; `F2-r2` reworks `F2-r1`; `Rework of:` names it. Post-merge files key by date — same-day collision suffix `-2`, `-3`; a pre-merge round reuses `rework.md`.
  The `## Reworks` manifest is the canonical chain, one row per rework round; git keeps the rounds a pre-merge file overwrote.
- A **design** verification-gate finding (**verify-cell**) is a **pre-merge** rework trigger while the cell is **in-progress**; the planner writes the sibling `rework.md` — the index tracks status only. A **mechanical** finding is a gate repair: the executor fixes it in place and records it, no rework file.
- **Dispatched briefs**: the focused-spike / rework briefs carry the affected cell (repo + feature), the governing ADR path + decision digest, the surfaced issue (inline),
  a digest of the evidence covering it, and the spike references.
  Never re-scope the whole epic (see **reference/dispatch-briefs.md**).
- **Post-merge index handling**: keep the original cell exactly as-is (**done**); add the rework as a new feature/cell in a new wave with `**Rework of**: F2`.
- **Pre-merge index handling**: no index change; the cell keeps its identity and **in-progress** status.
