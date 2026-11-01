# Orchestration Guide

Rules for **orchestrate-delivery**, **resume-delivery**, and **update-delivery-index** in `orchestrate-feature-delivery`.

## Agent dispatch

- **Always delegate delivery work — never do it yourself.** The orchestrator only dispatches and tracks. Reading recorded artifacts to answer a question is orchestration, not delivery — apply **triage-issue** first. Every delivery task maps to a dedicated agent:

| Task | Delegated agent (role → example) | Applies | Result |
|---|---|---|---|
| Answer a question (L0) | orchestrator reads the record | **investigation-triage** | answer, no artifacts |
| Investigate a code fact (L1) | investigation agent → **code-investigator** | **investigate-code** | evidence answer with `file:line` |
| Spike a decision (L2/L3; incl. rework) | ADR agent → **adr-writer** (L2), spike agent → **spike-conductor** (L3) | **draft-adr** / **conduct-spike** | revised ADR, or focused findings / solution-doc updates |
| Plan a cell | planning agent → **planner** | **plan-development-task** | `plan.md` + `context.md` |
| Execute a cell | execution agent → **executor** | **execute-plan** | code changes + commits; push + PR |
| Verify a cell | review agent → **code-reviewer** | **review-code** | spec-compliance + trust verdict |
| Update solution doc | solution-doc agent → **solution-doc-writer** | **write-solution-doc** | revised sections, rewrite in place |
| Update ADR | ADR agent → **adr-writer** | **draft-adr** | revised ADR, rewrite in place |

- **One cell per agent.** The planner writes `<epic>/<repo>/<feature-name>/plan.md` + `context.md` (kebab-case folder); the executor runs that plan.
- **Plan-first gate**: separate agents. Dispatch the **planner**, verify its plan file on disk, then the **executor**. Never one agent for both; never execute without a verified plan; never append a plan after execution.
- **No simplicity exemption**: every cell, however simple, is planned then executed by separate agents; never implement directly.
- **Artifact updates are delegated too.** When a plan or execution surfaces changes to the spike's solution doc or ADRs, dispatch a **solution-doc-writer** / **adr-writer** agent for the update — never edit those artifacts from the orchestrator.
- **Write boundary.** Writes stay inside `**/deliveries/**`; code comes only from a dispatched **executor**. Run the write-boundary check after every index write (**reference/write-boundary-guide.md**).
- **Full context in every brief.** Inventory the orchestrator's state first — ask and answers, index, spike artifacts already read, L0/L1 answers, prior cells' delivered contracts, gate findings, detected conventions, absolute paths — then fill each item by **path**, **digest**, or **inline**, and feed the callee's intake fields. Contract and completeness check: **reference/dispatch-briefs.md**; cell fields: **reference/delivery-index-format.md**.
- **Persist references to context.md.** Planning agents record the spike references and the contract surface the cell delivers in `context.md`, so execution, verification, and later cells load a digest instead of re-deriving it.
- Dispatch agents **in parallel** across cells, subject to:
  - **Develop-gating**: dispatch cells whose dependency cells are **planned** (contracts agreed); contract-first and independent cells develop in parallel.
  - **Merge-gating**: a cell merges only after its dependency cells are **done** (merged).
  - **No conflict in parallel**: never run two cells that touch the same repo with a conflict edge at the same time — serialize them.
  - **Capacity**: match the number of parallel agents to what the platform supports; ask the user when unsure.
- Use the platform's agent/sub-agent mechanism — detect what is available (e.g., planner / executor agents) and dispatch accordingly. If no agent mechanism exists, ask the user how to proceed — never fall back to doing the work yourself.
- **Branches**: one per repo per cell, named per the repo's convention (detect; never assume a prefix). Record the branch, PR, and head commit in the index; the executor creates the branch and commits small-step (**branch-and-push-conventions**).
- **Push gating**: the **executor** owns push approval and PR creation; the orchestrator never pushes or opens the PR and records only the returned reference.

## Orchestration loop

1. Load the index, or create it via decompose → map → order → produce.
2. Assess state (per-cell status + develop/merge gating).
3. Phase 1 — dispatch the **planner** to each unplanned, develop-ready cell (skip done; note blocked).
4. Verify the **plan-first gate** — confirm each planner's plan file exists on disk before the cell advances.
5. Phase 2 — dispatch the **executor** to each planned cell whose plan file is verified.
6. Collect results; apply **verify-cell** (spec compliance + trust) to each completed execution, then apply **update-delivery-index**.
7. Re-assess and repeat until all cells are done or the user pauses.
8. When all cells are **done**, run the epic integration review — one cross-cell review + integration test pass, deferred-Minor triage (see **reference/verification-gate.md**).

## Status updates

- After every agent result, update the cell status; record the **head commit** from each execution handoff; when the executor reports a PR, record its reference; when it merges, confirm the recorded head commit is in the merged PR before marking **done**, then re-check downstream cells for develop/merge-readiness.
- A completed execution advances to **verified** only after **verify-cell** passes — never mark a cell **done** or **poc-ready** without the gate (see **reference/verification-gate.md**).
- Dispatch each gate finding straight to the planner — a fix is a pre-merge rework planned (**plan-development-task**, sibling `rework-<date>.md`) then executed (**execute-plan**), never a direct executor edit; the index tracks status only.
- When a returned result looks inconsistent (status vs plan files, claimed merge vs branch state), verify it with `question-everything`'s **verify-sub-agent-results** — a NEW evidence-matched agent carrying the recorded artifacts as known context, never the original instance — before recording.
- Never let conversation text be the source of truth — the delivery index is.
- Run the delivery write-boundary check after each index update — an own-writes snapshot delta: only paths newly written by the orchestrator outside `**/deliveries/**` are violations; stop and report those.

## ADR changes

ADRs are **versionless** — drift is signaled by the **adr-writer** agent's return or the user's report, never by diffing the ADR (see **handle-adr-change**). Route governed cells by status:

| Status | Route |
|---|---|
| unplanned | no action — planned against the current ADR when dispatched |
| planned | re-plan in place (**plan-development-task**) — nothing implemented, no history to preserve |
| in-progress | amend pending steps in place if only unexecuted work is affected; pre-merge rework if executed work is affected (sibling `rework-<date>.md`) |
| done | post-merge rework (new rework feature `F2-r1`) |
| poc cell | surface to the user — the change may invalidate success criteria |

Never dispatch a planned cell on a stale decision.

## Resume

- On resume, confirm ADR currency first (apply **handle-adr-change** if changed). Skip completed waves; resume in-progress from the active `rework-<date>.md` (or `plan.md`), skipping ✅ and ⏭; retry failed; amend a defective pending step in the same plan; wait on blocked.
- Report what is resumed vs skipped before dispatching.

## Failure handling

| Signal | Meaning | Recovery |
|---|---|---|
| **failed** | agent hit an error (record reason) | ask the user: retry, or dispatch the planner to amend the same plan when the error is a plan defect |
| **blocked** | waiting on an unmerged dependency or a user decision (record blocker) | do not dispatch until the blocker clears |
| **plan defect** | a pending step is wrong, missing, or obsolete | dispatch the planner to **amend** the same `plan.md`; the cell stays **in-progress** — no new plan folder, file, or cell |
| **in-progress** | agent was interrupted mid-execution | resume from the last completed step in the active `rework-<date>.md` (or `plan.md` if no rework), skipping ✅ and ⏭ |

## POC cells

A POC proves one option of one ADR as a standalone feature (see **poc-definition**). It is planned and executed like any cell, then stops at a **decision gate** instead of merging.

- **Dispatch**: plan → **planner** (plan-development-task `plan-poc`); execute → **executor** (normal execution). Include the POC metadata (`**Type**: poc`, ADR, option) and the optional success criteria in the brief. The executor offers an MR after approval; the user evaluates it.
- **Compare POCs**: sibling POC cells (one per option) run in parallel in an early wave.
- **Decision gate**: at **poc-ready**, present the open MR to the user — they review/test it (optionally against `success-criteria`) and decide adopt/reject manually, never auto-decide.
- **Adopt**: dispatch **adr-writer** (draft-adr) to record the validated option; **POC-as-implementation** — the executor pushes and opens the PR, merge the branch, mark the `replaces` cell **superseded**; **POC-as-decision-input** — close the POC, dispatch the **poc-gated** feature with the decided option.
- **Reject**: dispatch **adr-writer** to record the outcome; close the cell **rejected**; archive or discard the branch (ask the user); delivery proceeds on the other option.
- **Sequencing**: never dispatch a **poc-gated** feature before its POC's decision.

## Rework after implementation

Two modes by cell status: **post-merge** (cell **done** — a new rework feature in a new wave; the original stays **done**) and **pre-merge** (cell **in-progress** — same cell, no index change). Sequence either way: **triage-issue** → delegate artifact updates → planner writes the sibling `rework-<date>.md` → executor runs only its steps → record the PR reference. Append-only rules, lineage, brief contents, and index handling: **reference/rework-modes.md**.
