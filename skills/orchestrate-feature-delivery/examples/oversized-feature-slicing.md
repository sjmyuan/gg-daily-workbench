# Example: Slicing an Oversized Feature

**Scenario**: decomposition produced `F6 invoice-export` for `billing-service`; its plan is verified on disk and lists 61 files.
The files: CSV writer, export job, upload, historic backfill, endpoint switch, tests.
The user says: "That's too big for one PR — split it, and we'll land it incrementally."

**Applies**: **decompose-change-into-features** (review budget) → **orchestrate-delivery** (plan-time split)

## 1. Check the budget

- 61 changed files, tests included — over the default 40.
- The 3,000-line diff is **not** the signal: most of it is one generated client and a wide test matrix.
- The contract surfaces are three, not one: the CSV format, the export job's idempotency, and the public endpoint — so the whole-contract exemption does not apply.

## 2. Find the green seam

Slices in shape order, each green on its own:

| Slice | Shape | Carries | Files |
|---|---|---|---|
| **F6.1 invoice-csv** | Additive | Writer + formatter; nothing calls it yet | 18 |
| **F6.2 invoice-export-job** | Additive | Job + upload, behind an off flag | 21 |
| **F6.3 invoice-backfill** | Wire | Historic invoices through the job, flag off | 12 |
| **F6.4 invoice-export-endpoint** | Flip + Cleanup | New endpoint becomes the default; old export deleted | 10 |

- F6.4 touches a public API → **Full** tier at its gate; the additive slices stay **Sampled**.
- F6.4 is not sliced further: switching the endpoint and deleting the old export must land together, or the product serves two formats.

## 3. Rewrite the index

Replace the single F6 row; the slices are cells, so no new columns.

| ID | Name | Wave | Repos | Dependencies | ADRs | Rework of | Goal |
|---|---|---|---|---|---|---|---|
| F6.1 | invoice-csv | 0 | billing-service | — | adr-export-01 | — | Writer + formatter, unused |
| F6.2 | invoice-export-job | 1 | billing-service | F6.1 (conflict) | adr-export-02 | — | Job + upload, flag off |
| F6.3 | invoice-backfill | 2 | billing-service | F6.2 (conflict) | adr-export-02 | — | Historic rows, flag off |
| F6.4 | invoice-export-endpoint | 3 | billing-service | F6.3 (conflict) | adr-export-03 | — | Endpoint switch, old path deleted |

- Same repo and overlapping files → **conflict** edges: the four slices serialize.
- **Summary** becomes `critical path: F6.1 → F6.2 → F6.3 → F6.4`; every consumer of the export names `F6.4`, never `F6`.
- The epic gets four `## Cell plan status` rows instead of one — archive a done wave early to hold the index budget.

## 4. Run the split

1. The orchestrator delineates the seam and confirms the four IDs and waves with the user in one pass.
2. The **planner** retires the original `plan.md` and writes one plan per slice into `billing-service/invoice-csv/`, `.../invoice-export-job/`, and so on; all four become **planned**.
3. The index is rewritten and passed through **Finalise**.
4. **orchestrate-delivery** runs from F6.1; each slice executes, verifies, and merges before the next.

## 5. What keeps it honest

- **Green, not partial**: F6.1 adds code nothing calls; F6.3 writes rows the old path ignores. No slice opens a broken window.
- **Not a rework**: a gate gap in F6.2 becomes `rework-<date>.md` in the F6.2 folder; F6.3 waits.
- **Window closes at execution**: once F6.1's executor pushes, no further split — an oversize is recorded in `## Notes` and the remainder routes as a new feature.
- **Under budget**: a 31-file F6 stays whole. The split decision reads the plan's `Expected files`, never a hunch at decomposition.
