# Orchestration Guide

Tables the orchestration capabilities read. Statuses and readiness: **reference/state-machine.md**; index schema: **reference/delivery-index-format.md**; briefs: **reference/dispatch-briefs.md**.

## Agent dispatch

| Task | Delegated agent | Applies | Result |
|---|---|---|---|
| Answer a question (L0) | orchestrator reads the record | **investigation-triage** | answer, no artifacts |
| Investigate a code fact (L1) | **code-investigator** | **investigate-code** | evidence answer with `file:line` |
| Revise one ADR (L2) | **adr-writer** | **draft-adr** | revised ADR, in place |
| Spike decisions (L3; incl. rework) | **spike-conductor** | **conduct-spike** | focused findings / solution-doc updates |
| Plan a cell | **planner** | **plan-development-task** | `plan.md` + `context.md` |
| Execute a cell | **executor** | **execute-plan** | code changes + commits; push + PR |
| Verify a cell | **code-reviewer** | **review-code** | spec-compliance + trust verdict |
| Update the solution doc | **solution-doc-writer** | **write-solution-doc** | revised sections, in place |

- **One cell per agent**; the planner writes the feature folder's `plan.md` + `context.md`, the executor runs that plan.
- **Artifact updates are delegated too** — `solution-doc-writer` / `adr-writer`; never edited from the orchestrator.
- Use the platform's agent mechanism; if none exists, ask the user — never fall back to doing the work.

## Parallel gating

| Gate | Condition |
|---|---|
| **Develop-gating** | A cell develops once its dependencies are **planned** (contracts agreed); contract-first and independent cells run in parallel |
| **Merge-gating** | A cell merges only after its dependencies are **done** |
| **No conflict** | Never run two cells with a conflict edge at once — serialize them |
| **Capacity** | Match parallel agents to the platform; ask the user when unsure |

## Failure handling

| Signal | Meaning | Recovery |
|---|---|---|
| **failed** | Agent hit an error (record the reason) | Ask the user: retry, or dispatch the planner to amend the same plan when the error is a plan defect |
| **blocked** | Waiting on an unmerged dependency or a user decision (record the blocker) | Do not dispatch until the blocker clears |
| **plan defect** | A pending step is wrong, missing, or obsolete | Dispatch the planner to **amend** the same `plan.md`; the cell stays **in-progress** — no new plan folder, file, or cell |
| **in-progress** | The agent was interrupted mid-execution | Resume from the last completed step in the active `rework-<date>.md` (or `plan.md`), skipping ✅ and ⏭ |

## ADR changes

ADRs are **versionless** — drift is signaled by the **adr-writer** return or the user's report, never by diffing the ADR. Route governed cells by status:

| Status | Route |
|---|---|
| unplanned | No action — planned against the current ADR when dispatched |
| planned | Re-plan in place (**plan-development-task**) — nothing implemented, no history to preserve |
| in-progress | Amend pending steps in place if only unexecuted work is affected; pre-merge rework if executed work is affected |
| done | Post-merge rework (new feature `F2-r1`) |
| poc cell | Surface to the user — the change may invalidate the success criteria |

Never dispatch a planned cell on a stale decision. POC rules: **reference/poc-lifecycle.md**; rework rules: **reference/rework-modes.md**.

## Recording results

- After every agent result, update the cell status and record the head commit / PR reference.
- On merge, confirm the recorded head commit is in the merged PR before **done**, then re-check downstream readiness.
- A result that looks inconsistent (status vs plan files, claimed merge vs branch state) → verify per `question-everything` with a NEW evidence-matched agent before recording.
- Conversation text is never the source of truth — the index is.
