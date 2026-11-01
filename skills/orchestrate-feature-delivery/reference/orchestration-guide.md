# Orchestration Guide

Rules for **orchestrate-delivery**, **resume-delivery**, and **update-delivery-index** in `orchestrate-feature-delivery`. Statuses and readiness: **reference/state-machine.md**; index schema: **reference/delivery-index-format.md**; briefs: **reference/dispatch-briefs.md**.

## Agent dispatch

- **Always delegate delivery work — never do it yourself.** Reading recorded artifacts to answer a question is orchestration, not delivery — apply **triage-issue** first.

| Task | Delegated agent | Applies | Result |
|---|---|---|---|
| Answer a question (L0) | orchestrator reads the record | **investigation-triage** | answer, no artifacts |
| Investigate a code fact (L1) | **code-investigator** | **investigate-code** | evidence answer with `file:line` |
| Revise one ADR (L2) | **adr-writer** | **draft-adr** | revised ADR, rewrite in place |
| Spike decisions (L3; incl. rework) | **spike-conductor** | **conduct-spike** | focused findings / solution-doc updates |
| Plan a cell | **planner** | **plan-development-task** | `plan.md` + `context.md` |
| Execute a cell | **executor** | **execute-plan** | code changes + commits; push + PR |
| Verify a cell | **code-reviewer** | **review-code** | spec-compliance + trust verdict |
| Update the solution doc | **solution-doc-writer** | **write-solution-doc** | revised sections, rewrite in place |

- **One cell per agent.** The planner writes `<epic>/<repo>/<feature-name>/plan.md` + `context.md`; the executor runs that plan.
- **Plan-first gate**: dispatch the **planner**, verify its plan file on disk, then the **executor** — never one agent for both, never execute without a verified plan, never append a plan after execution. **No simplicity exemption**: every cell is planned then executed by separate agents.
- **Artifact updates are delegated too** — dispatch `solution-doc-writer` / `adr-writer`; never edit those artifacts from the orchestrator.
- **Write boundary**: writes stay inside `**/deliveries/**`; code comes only from a dispatched executor. Check after every index write (**reference/write-boundary-guide.md**).
- **Full context in every brief**: inventory the orchestrator's state, fill each item by path / digest / inline, feed the callee's intake fields — contract in **reference/dispatch-briefs.md**; cell fields in **reference/delivery-index-format.md**.
- **Persist references to `context.md`** so execution, verification, and later cells load a digest instead of re-deriving it.
- Dispatch agents **in parallel** across cells, subject to:
  - **Develop-gating**: cells whose dependency cells are **planned** (contracts agreed); contract-first and independent cells develop in parallel.
  - **Merge-gating**: a cell merges only after its dependency cells are **done**.
  - **No conflict in parallel**: never run two cells with a conflict edge at the same time — serialize them.
  - **Capacity**: match the number of parallel agents to the platform; ask the user when unsure.
- Use the platform's agent mechanism; if none exists, ask the user how to proceed — never fall back to doing the work yourself.
- **Branches**: one per repo per cell, named per the repo's convention (detect; never assume a prefix).
- **Push gating**: the executor owns push approval and PR creation; the orchestrator records only the returned reference.

## Orchestration loop

1. Load the index, or create it via decompose → map → order → produce.
2. Assess state (per-cell status + develop/merge gating).
3. Phase 1 — dispatch the **planner** to each unplanned, develop-ready cell (skip done; note blocked).
4. Verify the **plan-first gate** — confirm each planner's plan file exists on disk before the cell advances.
5. Phase 2 — dispatch the **executor** to each planned cell whose plan file is verified.
6. Collect results; apply **verify-cell** to each completed execution, then **update-delivery-index**.
7. Re-assess and repeat until all cells are done or the user pauses.
8. When all cells are **done**, run the epic integration review (**reference/verification-gate.md**).

## Status updates

- After every agent result, update the cell status and record the head commit / PR reference; on merge, confirm the recorded head commit is in the merged PR before **done**, then re-check downstream readiness.
- A completed execution reaches **verified** only after **verify-cell** passes — never **done** or **poc-ready** without the gate or a recorded waiver.
- Dispatch each gate finding straight to the planner — a fix is a pre-merge rework planned then executed, never a direct executor edit; the index tracks status only.
- A returned result that looks inconsistent (status vs plan files, claimed merge vs branch state) → verify with `question-everything`'s **verify-sub-agent-results** via a NEW evidence-matched agent before recording.
- Never let conversation text be the source of truth — the index is. Run the write-boundary check after each index update.

## ADR changes

ADRs are **versionless** — drift is signaled by the **adr-writer** return or the user's report, never by diffing the ADR (see **handle-adr-change**). Route governed cells by status:

| Status | Route |
|---|---|
| unplanned | no action — planned against the current ADR when dispatched |
| planned | re-plan in place (**plan-development-task**) — nothing implemented, no history to preserve |
| in-progress | amend pending steps in place if only unexecuted work is affected; pre-merge rework if executed work is affected |
| done | post-merge rework (new rework feature `F2-r1`) |
| poc cell | surface to the user — the change may invalidate success criteria |

Never dispatch a planned cell on a stale decision.

## Failure handling

| Signal | Meaning | Recovery |
|---|---|---|
| **failed** | agent hit an error (record reason) | ask the user: retry, or dispatch the planner to amend the same plan when the error is a plan defect |
| **blocked** | waiting on an unmerged dependency or a user decision (record blocker) | do not dispatch until the blocker clears |
| **plan defect** | a pending step is wrong, missing, or obsolete | dispatch the planner to **amend** the same `plan.md`; the cell stays **in-progress** — no new plan folder, file, or cell |
| **in-progress** | agent was interrupted mid-execution | resume from the last completed step in the active `rework-<date>.md` (or `plan.md`), skipping ✅ and ⏭ |

## POC cells

A POC proves one option of one ADR as a standalone feature (see **poc-definition**). Plan with `plan-poc`, execute normally, then stop at the decision gate instead of merging. Rules, decision gate, and adoption models: **reference/poc-lifecycle.md**. Compare POCs run in parallel in an early wave; never dispatch a **poc-gated** feature before its POC's decision.

## Rework after implementation

Two modes by cell status: **post-merge** (cell **done** — new rework feature in a new wave; the original stays **done**) and **pre-merge** (cell **in-progress** — same cell, no index change). Sequence either way: **triage-issue** → delegate artifact updates → planner writes the sibling `rework-<date>.md` → executor runs only its steps → record the PR reference. Append-only rules and lineage: **reference/rework-modes.md**.
