# Orchestration Guide

Tables read by the orchestration capabilities and **agent-recovery**. Statuses and readiness: **reference/state-machine.md**; index schema: **reference/delivery-index-format.md**; briefs: **reference/dispatch-briefs.md**.

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

## Recovery ladder

A stall, question, or failure is the orchestrator's problem before it is the user's — it holds the record the agent needs. Match the signal to the cheapest rung that clears it; one rung per attempt.

| Rung | Signal | Action | Extra dispatches |
|---|---|---|---|
| **1 Answer** | The agent asks what the record already settled (index, ADR, `context.md`, plan, prior verdicts) | Reply with the digest and let the agent continue — no re-dispatch | 0 |
| **2 Investigate** | A code fact is missing, contradicted, or guessed | Dispatch **code-investigator** (L1) with that question; feed the evidence back | 1 |
| **3 Re-brief** | A path, intake field, dependency contract, or convention was missing — the agent searched or re-asked | Return the corrected brief to the same agent; completed steps stay done | 0 |
| **4 Re-route** | Wrong agent or rung, or a pending plan step is wrong or obsolete | Planner **amends** the same `plan.md`; ADR drift → **adr-writer**; cell stays **in-progress** — no new plan folder, file, or cell | 1 |
| **5 Clear record** | Stale status, missing plan file, wrong base or branch, unrecorded dependency | Correct the index or dispatch order, then continue — never code | 0 |
| **6 Retry** | Transient error, no diagnosis, work unchanged | Re-dispatch the same brief once | 1 |
| **Escalate** | A trigger below | Ask with the trail and a recommendation; **blocked** only when the cell cannot proceed without the answer | 0 |

- A rung that already failed for the same cause is never repeated; two attempts on one cause, or a spec gap recurring after a gate round (**verification-gate** cap), ends recovery.
- Never invent an answer: a question the record does not settle is rung 2 or an escalation.
- Resume an interrupted agent from the last completed step in the active `rework-<date>.md` (or `plan.md`), skipping ✅ and ⏭.
- No follow-up channel → re-dispatch with the completed steps and the digest; a resumed cell never restarts.
- Record `<cell> — <cause> → <rung>` in the index `## Notes` when the status changed; detail stays in the plan, rework file, and git.

## Escalation triggers (the only interrupts)

- The **epic's** scope changes: feature set, wave order, a cell's done-means, priority, or an accepted `Assumption`. Enabling work inside a cell is delegated — see **Delegated scope**.
- A governing ADR decision is challenged, or a trade-off needs choosing — **adr-writer** drafts, the user decides.
- POC **adopted** / **rejected**; a gate waiver; push, PR, or merge approval.
- Credentials, access, cost, or capacity the orchestrator cannot obtain.
- An irreversible or destructive action outside the plan.
- Evidence conflict that an independent verifier cannot settle.

An escalation carries the cell, the attempt trail, the decision needed, options with cost, and one recommendation.
Batch escalations at the next wave boundary; interrupt immediately only when a cell cannot proceed, or the pending action is irreversible.

## Delegated scope

A cell often needs enabling work its plan did not list. Approve it and continue when every check holds — approval is a decision, not work: the planner still plans it and the executor builds it.

| Approve (delegated) | Escalate |
|---|---|
| Enables the cell's existing done-means | Changes a feature, wave, or a cell's done-means |
| Additive — no delivered contract, public API, or schema semantics change | Changes a decided contract, or forces another cell to change |
| Same repo, branch, cell, and governing ADR decision | New repo, service, dependency, infra, migration, or deploy |
| Reversible on the cell branch; no data or deployment impact | Would need its own PR or cell to be reviewable |
| A plan amendment, not a new feature or cell | That class was denied before, or the work belongs to another cell's done-means |

- Record `Scope +<what> (delegated, <date>)` in the cell brief and have the planner amend `plan.md`; the delta travels to the verifier — an unrecorded bump returns as **Extra**.
- A class the user pre-authorized in `## Notes` is never asked again.
- A new outcome is a feature, not a bump; approval never widens the epic.
- Two bumps on one cell mean the plan missed the work — re-plan, do not keep patching.

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
