# PR Size Slicing

Backs **feature-definition**, **decompose-change-into-features**, and the plan-time split in **orchestrate-delivery**.
A cell ships as one PR; this file decides when a feature must become several cells instead.

## Review budget

| Signal | Rule |
|---|---|
| **Changed files** | Default **≤40 files per PR**, tests included; the user may set another number for the epic |
| **Diff lines** | Never a signal — a lockfile or generated file is still one file |
| **Whole-contract change** | Judged by **surface count**, not files — one contract per PR; many consumers of one contract do not split it |

- The budget binds at the **plan**: `Expected files` plus the step `Files` lists give the count.
- A non-default budget is a `## Notes` line in the index and travels in every brief; resume never re-asks.
- The solution doc and L1 findings flag only obvious splits; the estimate is heuristic, the plan is the check.
- A cell under budget stays whole — never slice for tidiness.

## Green slice

A slice is a **cell** — a PR-sized part of one feature, with its own branch, plan, gate, and index row.
- Every slice leaves the repo green — build, tests, and a working product.
- A slice that cannot be green is not a slice: find another seam, or keep the cell whole and say so.
- Never merge a slice that opens a broken window for the next one.

## Slice shapes

Order slices so each merges on its own:

| Shape | Slice carries | After merge |
|---|---|---|
| **Additive** | New module, type, or endpoint — unused or behind an off flag | Nothing calls it yet |
| **Wire** | Caller uses the new surface; old path still live | Both paths work |
| **Flip** | Default, flag, or env switches to the new path | Old path unused |
| **Cleanup** | Delete the old path, its tests, and shims | One path remains |

Data variant: additive schema → dual write → backfill → read flip → drop the old column.

## IDs, index, and dependencies

- ID gains a part suffix — `F3.1`, `F3.2`; each slice takes a kebab-case `Name` (`invoice-csv`).
- Slices are cells: one `## Cell plan status` row and one folder each (`<repo>/<slice-name>/`). No new columns.
- A dependent names the **exact slice** that delivers the surface it consumes (`F3.2`), never the bare series.
- Same repo, overlapping files → **conflict** edge: serialize in shape order.
- Disjoint files or different repos → parallel under the usual edge types (**reference/dependency-ordering-guide.md**).
- A serialized series sits on the critical path: show `F3.1 → F3.2` in **Summary**; archive a done wave to hold the index budget.

## Plan-time split

The only legal re-decomposition. It runs when all three hold:
- The cell is **planned** and its plan is verified on disk.
- `Expected files` plus the step `Files` lists exceed the budget.
- No executor has pushed; no PR exists.

1. Delineate the seam per **Slice shapes**; confirm the slice IDs and new waves with the user in one pass.
2. Dispatch the **planner** to retire the original `plan.md` and write one plan per slice into its folder; each plan is verified before its executor runs.
3. Rewrite the index: replace the row with `F3.1…`, then waves and edges; run **Finalise**.
4. Continue **orchestrate-delivery** from slice 1.

- The union of slices equals the original cell — a split never widens scope.
- Retiring the original plan matters: it still describes every slice, and an executor given it would build the whole cell at once.
- Once execution starts the window closes: finish the cell, record the oversize in `## Notes`, and route any remainder as a new feature — never re-split an open PR.
- A rework is not a slice; a POC is not a slice; an issue is not a slice.

## Gate per slice

- Each slice gets its own **verify-cell** gate; the smaller diff keeps **Sampled** viable.
- A Full-tier protected surface stays **Full** on every slice that touches it.
- Every dispatch carries the slice order, this slice's green rule, the consumed and delivered contract surfaces, and the exact slice a dependency names — never the series.
