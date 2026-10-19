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
| Execute a cell | execution agent → **executor** | **execute-plan** | code changes + commits |
| Verify a cell | review agent → **code-reviewer** | **review-code** | spec-compliance + trust verdict |
| Update solution doc | solution-doc agent → **solution-doc-writer** | **write-solution-doc** | revised sections, rewrite in place |
| Update ADR | ADR agent → **adr-writer** | **draft-adr** | revised ADR, rewrite in place |

- **One cell per agent.** The planner writes `<epic>/<repo>/<feature-name>/plan.md` + `context.md` (kebab-case folder); the executor runs that plan.
- **Plan-first gate**: separate agents. Dispatch the **planner**, verify its plan file on disk, then the **executor**. Never one agent for both; never execute without a verified plan; never append a plan after execution.
- **No simplicity exemption**: every cell, however simple, is planned then executed by separate agents; never implement directly.
- **Artifact updates are delegated too.** When a plan or execution surfaces changes to the spike's solution doc or ADRs, dispatch a **solution-doc-writer** / **adr-writer** agent for the update — never edit those artifacts from the orchestrator.
- **Write boundary.** Writes stay inside `**/deliveries/**`; code comes only from a dispatched **executor**. Run the write-boundary check after every index write (**reference/write-boundary-guide.md**).
- **Full context in every brief.** Each brief carries the cell's scope brief + **spike references**, filled by **path** for persisted info and **inline** for orchestrator-only context (rule: **reference/delivery-index-format.md**, per-cell scope brief); never inline a whole spike artifact.
- **Persist references to context.md.** Planning agents record the spike references in `context.md`, so execution and resume agents have durable distilled context and can load referenced artifacts when needed.
- Dispatch agents **in parallel** across cells, subject to:
  - **Develop-gating**: dispatch cells whose dependency cells are **planned** (contracts agreed); contract-first and independent cells develop in parallel.
  - **Merge-gating**: a cell merges only after its dependency cells are **done** (merged).
  - **No conflict in parallel**: never run two cells that touch the same repo with a conflict edge at the same time — serialize them.
  - **Capacity**: match the number of parallel agents to what the platform supports; ask the user when unsure.
- Use the platform's agent/sub-agent mechanism — detect what is available (e.g., planner / executor agents) and dispatch accordingly. If no agent mechanism exists, ask the user how to proceed — never fall back to doing the work yourself.
- **Branches**: one per repo per cell, named per the repo's convention (detect; never assume a prefix). Record the branch, PR, and head commit in the index; the executor creates the branch and commits small-step (**branch-and-push-conventions**).
- **Push gating**: never push a branch or open a PR automatically — after a cell's work is complete and ready to integrate, ask the user for confirmation first.

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

- After every agent result, update the cell status; record the **head commit** from each execution handoff; when a PR is opened, record its reference; when it merges, confirm the recorded head commit is in the merged PR before marking **done**, then re-check downstream cells for develop/merge-readiness.
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
| in-progress | pre-merge rework if the change touches the cell's decision (sibling `rework-<date>.md`) |
| done | post-merge rework (new rework feature `F2-r1`) |
| poc cell | surface to the user — the change may invalidate success criteria |

Never dispatch a planned cell on a stale decision.

## Resume

- On resume, confirm ADR currency first (apply **handle-adr-change** if changed). Skip completed waves; resume in-progress from the active `rework-<date>.md` (or `plan.md`); re-plan/retry failed; wait on blocked.
- Report what is resumed vs skipped before dispatching.

## Failure handling

| State | Meaning | Recovery |
|---|---|---|
| **failed** | agent hit an error (record reason) | ask the user: re-plan (plan-development-task) or retry |
| **blocked** | waiting on an unmerged dependency or a user decision (record blocker) | do not dispatch until the blocker clears |
| **in-progress** | agent was interrupted mid-execution | resume from the last completed step in the active `rework-<date>.md` (or `plan.md` if no rework) |

## POC cells

A POC proves one option of one ADR as a standalone feature (see **poc-definition**). It is planned and executed like any cell, then stops at a **decision gate** instead of merging.

- **Dispatch**: plan → **planner** (plan-development-task, POC mode); execute → **executor** (execute-plan, POC mode). Include `type: poc` + success criteria in the brief.
- **Compare POCs**: sibling POC cells (one per option) run in parallel in an early wave.
- **Decision gate**: at **poc-ready**, present the evaluation report vs success criteria to the user — the user/team decides adopt/reject, never auto-decide.
- **Adopt**: dispatch **adr-writer** (draft-adr) to record the validated option; **POC-as-implementation** — ask before pushing/PR, merge the branch, mark the `replaces` cell **superseded**; **POC-as-decision-input** — close the POC, dispatch the **poc-gated** feature with the decided option.
- **Reject**: dispatch **adr-writer** to record the outcome; close the cell **rejected**; archive or discard the branch (ask the user); delivery proceeds on the other option.
- **Sequencing**: never dispatch a **poc-gated** feature before its POC's decision.

## Rework after implementation

Two modes, chosen by the cell's status (see **rework-modes** in the SKILL.md knowledge).

**Post-merge** (cell **done** — merged/verified): history is shipped and preserved.

1. **Triage**: apply **triage-issue**. A single wrong decision goes straight to **adr-writer** (L2). Dispatch **spike-conductor** (L3) only when the decision space changed or ≥2 decisions/areas are involved; scope it as a delta. Never re-open the whole epic.
2. **Delegate artifact updates**: ADR changes → **adr-writer** (draft-adr); solution-doc changes → **solution-doc-writer** (write-solution-doc).
3. **Update the index**: record only the rework cell (`F2-r1`, `Rework of: F2`) in a new wave + its plan-location pointer — the original cell stays **done**; spike focus, ADR revision, and rework steps live in the sibling `rework-<date>.md` / `context.md`.
4. **Write the rework plan**: dispatch the **planner** (**plan-development-task**) to write a sibling `rework-<date>.md` in the feature folder — `plan.md` stays the frozen original, implemented steps never modified.
5. **Execute the rework plan**: dispatch the **executor** (**execute-plan**) to run only the new rework steps.
6. Update the index; ask the user before pushing / opening a PR.

**Rework lineage**: rework features chain to the state they rework — `F2-r1` reworks `F2`; `F2-r2` reworks `F2-r1` (the latest delivered state); `Rework of:` names that state. Rework files key by date — on a same-day collision suffix `-2`, `-3` (`rework-2026-08-24-2.md`). The `context.md` `## Reworks` manifest is the canonical chain.

**Pre-merge** (cell **in-progress** — implemented but not pushed/merged): nothing is merged yet, same append-only rule.

1. **Scope**: apply **triage-issue**. Default to L1 (evidence) or L2 (ADR revision); dispatch **spike-conductor** only when the issue challenges the governing ADR decision across ≥2 decisions/areas.
2. **Write the rework plan**: dispatch the **planner** (**plan-development-task**) to write a sibling `rework-<date>.md` in the feature folder — `plan.md` stays the frozen original, implemented steps never modified; no new rework feature/wave (rework stays on the same cell).
3. **Execute the rework plan**: dispatch the **executor** (**execute-plan**) to run only the new rework steps on the unmerged work.
4. No index change (cell stays **in-progress**; the sibling `rework-<date>.md` is the record); ask the user before pushing / opening a PR.
