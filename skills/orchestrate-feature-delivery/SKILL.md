---
name: orchestrate-feature-delivery
description: Orchestrate a spiked epic's delivery: decompose spike output, sequence waves, dispatch plan/execute/verify agents, track the index, resume, rework, and route ADR changes and reverts. Use when decomposing ADRs, sequencing or resuming cells, verifying a cell, answering an issue, reworking delivered or reverted code, or proving an option with a POC.
---

<when-to-use-this-skill>
- User reports an issue or asks about a delivered feature — clarify, then answer from the record
- User finished a spike and wants features sequenced — parallel versus waiting on a PR
- User wants the index updated, agents dispatched, or delivery resumed
- User wants a completed cell independently verified before it is marked done
- User found an issue after implementation and wants rework
- User reports an ADR decision changed mid-delivery
- User asks to revert a change, restore a file, or keep the base version
- User wants to prove an ADR option with a POC before deciding
- Do NOT load before a spike's solution doc / ADRs exist — conduct-spike produces them first
- Do NOT load for a single, already-scoped change — plan-development-task and execute-plan own single cells
- Do NOT load to run a standalone spike — conduct-spike runs spikes
</when-to-use-this-skill>

<knowledge>
<orchestrator-role>
Persistent orchestrator for **one spiked epic**; the index is its source of truth. Never plans or codes.
- **Never perform delivery work** — every plan, execute, verify, and artifact update is dispatched.
- **Answering from the record is orchestration** — read the index, ADRs, and plans first.
- **Push and PR creation belong to the executor** — it asks for approval and returns the reference.
- **Plan-first gate** — no executor before the plan file exists; never back-fill a plan after execution.
- **No simplicity exemption** — every cell runs the full flow, planned then executed by separate agents.
</orchestrator-role>
<delivery-standards>
| Standard | Rule | Details |
|---|---|---|
| **write-boundary** | Only `index.md` inside `**/deliveries/**`; the plan, context, and rework files there belong to the planner and executor. | [write-boundary-guide](reference/write-boundary-guide.md) |
| **feature-definition** | A coherent, independently valuable deliverable across repos: `F1…`, kebab-case name, one line, one PR per repo (soft). | — |
| **poc-definition** | One ADR option implemented temporarily as an MR the user evaluates; the skill never measures. Adopt = merge; otherwise close it. | [poc-lifecycle](reference/poc-lifecycle.md) |
| **delivery-layout** | `deliveries/<epic-name>/index.md` plus one `<repo>/<feature-name>/` folder per cell, base from `scope.md` `Artifact root:`; one branch per repo per cell, named per the repo's convention (detect). | [delivery-layout](reference/delivery-layout.md), [artifact-map](reference/artifact-map.md) |
| **dependency-edge-types** | Per pair A → B: **merge-blocked** (develop after A's contract, merge after A) · **contract-first** (parallel on stubs, merge after A) · **poc-gated** · **conflict** (serialize) · **independent**. | [dependency-ordering-guide](reference/dependency-ordering-guide.md) |
| **delivery-state-machine** | `unplanned → planned → in-progress → verified → done`, plus `failed`, `blocked`, `superseded`; POCs fork to `poc-ready → adopted \| rejected`. Develop-ready = deps planned; merge-ready = deps done. | [state-machine](reference/state-machine.md) |
| **verification-gate** | **Verified** needs an independent local gate — spec compliance plus report trust; quality review stays with **execute-plan**. | [verification-gate](reference/verification-gate.md) |
| **request-intake** | `clarify-request`'s gate runs before any classification: restate the ask, never the suspected cause; accepted defaults go in the cell brief, labeled `Assumption`. | [investigation-triage](reference/investigation-triage.md) |
| **investigation-triage** | Answer → evidence → decision → spike, stopping at the first rung that answers; intake is no rung. | [investigation-triage](reference/investigation-triage.md) |
| **agent-dispatch** | Delegate every task: investigate → **code-investigator**, spike → **spike-conductor**, plan → **planner**, execute → **executor**, verify → **code-reviewer**, docs → **solution-doc-writer**, ADR → **adr-writer**. | [orchestration-guide](reference/orchestration-guide.md), [dispatch-briefs](reference/dispatch-briefs.md) |
| **rework-modes** | Append-only, cell-scoped sibling `rework-<date>.md` carrying the delta; `plan.md` frozen; post-merge adds a feature, pre-merge stays on the cell. | [rework-modes](reference/rework-modes.md) |
| **adr-change** | Versionless — drift comes from **adr-writer** or the user, never a file diff; route governed cells by status first. | [orchestration-guide](reference/orchestration-guide.md) |
| **concise-writing** | The index is a board: **≤8,000 chars / ≤120 lines**, table-first, atomic, no narration. | [delivery-index-format](reference/delivery-index-format.md), [writing-style](reference/writing-style.md) |
</delivery-standards>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Walking a scenario end to end | Triage, decomposition, a round, verification, resume, rework, ADR change, POC | [examples/](examples/) |
</context-loading-guide>
</knowledge>

<capabilities>
<decompose-change-into-features>
1. Gate the ask per **request-intake**; show every inference before grouping.
2. Load the spike artifacts: solution doc, ADRs, findings.
3. Group target-state changes into features by ADR traceability and module boundary.
4. Block on any contradiction between an ADR and the solution doc — nothing splits against a stale decision.
5. Assign `F1…`, a kebab-case name, and a one-line description.
</decompose-change-into-features>
<map-features-to-repos>
1. Inventory the repos each feature touches.
2. Build the feature × repo matrix — one cell per PR (soft); mark config/data/infra-only cells.
</map-features-to-repos>
<order-feature-delivery>
1. Classify each pair with **dependency-edge-types**.
2. Compute waves by topological order (**reference/dependency-ordering-guide.md**).
3. Order intra-feature PRs (contract first) and state develop-now vs merge-after.
</order-feature-delivery>
<produce-delivery-index>
1. Read the base (`scope.md` `Artifact root:`).
2. Write `deliveries/<epic-name>/index.md` per **reference/delivery-index-format.md**.
3. Fill **Spike References** and one brief per cell.
4. Create `{repo}/{feature-name}/` with `plan.md` + `context.md`, marking cells **unplanned**.
5. Run the **Finalise** checklist; confirm the features, matrix, waves, and location in one pass before delivery starts.
</produce-delivery-index>
<update-delivery-index>
1. After every result, record status, agent, branch, head, and PR per **reference/state-machine.md**.
2. Mark **planned** only when the plan file exists; a missing file is **failed**.
3. On merge, confirm the recorded head is in the PR with a green or waived receipt.
4. A POC decision → record **adopted** / **rejected** and mark the replaced cell **superseded**.
5. Verify a doubtful result per `question-everything` before recording it.
6. Run the **Finalise** checklist.
</update-delivery-index>
<orchestrate-delivery>
1. Gate the ask per **request-intake**; load the index, or create it via **decompose-change-into-features**.
2. Assess waves, ready cells, and blockers.
3. **Plan**: dispatch the **planner** to each unplanned, develop-ready cell; verify each plan on disk.
4. **Execute**: dispatch the **executor** to each planned cell with a verified plan, respecting gating and conflicts.
5. Build every brief with scope, **spike references**, and **branch name**.
6. Gate merges on dependencies **done**; the executor pushes, opens the PR, and returns the reference.
7. Apply **verify-cell**, then **update-delivery-index**, until all cells are **done** or the user pauses.
8. All cells **done** → epic integration review per **reference/verification-gate.md**.
</orchestrate-delivery>
<verify-cell>
**Objective**: Independently verify spec compliance and report trust before **verified**.
1. Require the handoff and a fully ✅ `plan.md` ending in **Exit gate**.
2. Dispatch a fresh **code-reviewer** per **reference/verification-gate.md** — never the executor.
3. **Spec compliance**: Missing / Extra / Misunderstood. **Trust**: receipt matches `head7`; evidence matches the diff.
4. Pass → mark **verified** via **update-delivery-index**.
5. Gap or Critical/Important → **planner** (`rework-<date>.md`) → **executor** → scoped re-review; stay **in-progress**.
</verify-cell>
<resume-delivery>
1. Load the index from the recorded base (`scope.md` `Artifact root:`).
2. Confirm ADR currency; a changed ADR → **handle-adr-change** first.
3. Derive state from the index, the active plan or rework, and `## Execution`; resume after the last ✅.
4. Failed → retry or amend; blocked → wait; unplanned → plan. Confirm the resume set, then **orchestrate-delivery**.
</resume-delivery>
<triage-issue>
**Objective**: Choose the cheapest rung that answers the issue.
1. State the question and the artifacts that may answer it; restate the behavior per **request-intake**.
2. Descend the ladder per **reference/investigation-triage.md**; stop at the first rung that answers.
3. Escalate one rung at a time, saying why the cheaper rung failed; dispatch only on a stated trigger.
</triage-issue>
<handle-post-implementation-issue>
1. Identify the affected cell, its governing ADR, and its status — **done** or **in-progress**.
2. Restate expected versus actual per **request-intake**.
3. Classify it as mechanical (revert / restore / copy / keep) per **reference/mechanical-restore.md**, or behavioral.
4. Scope to that decision, apply **triage-issue**, and present the rung for confirmation.
5. Plan → **planner** (`rework-<date>.md`), execute → **executor**, L2 → **adr-writer**, L3 → **spike-conductor**.
6. Apply **update-delivery-index** — post-merge adds a rework feature in a new wave; pre-merge changes no row.
</handle-post-implementation-issue>
<handle-adr-change>
1. Confirm the changed ADR and its decision from the user or **adr-writer**.
2. List governed cells from the index's `ADRs:` entries.
3. Route by status per **reference/orchestration-guide.md**, surface in-flight POCs, then update and confirm.
</handle-adr-change>
<define-poc-scope>
1. Flag `Type: poc` when an ADR option needs a reviewable working slice.
2. Fill `adr`, `option`, and optional `success-criteria` in the plan header; `Replaces` / `Compare` in the index.
3. Sequence POCs in **Wave 0** (compare siblings in parallel) and add a **poc-gated** edge; confirm.
</define-poc-scope>
</capabilities>

<rules>
<rule> Every inbound request passes **request-intake** first. </rule>
<rule> No index yet → **decompose-change-into-features**
→ **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**. </rule>
<rule> Index exists → **orchestrate-delivery**, or **resume-delivery** for an interrupted epic. </rule>
<rule> A cell's state changed → **update-delivery-index** before more dispatches; L0/L1 change nothing. </rule>
<rule> Execution completes → **verify-cell** before the index advances; no **done** without a gate or waiver. </rule>
<rule> An issue after implementation → **handle-post-implementation-issue**; never re-decompose the epic. </rule>
<rule> A revert, restore, copy, or keep request → a mechanical rework with a `Source`. </rule>
<rule> Before any investigation dispatch → **triage-issue**, answering from the record first. </rule>
<rule> An ADR change or **adr-writer** revision → **handle-adr-change**; never dispatch on a stale decision. </rule>
<rule> An ADR option needs proof → **define-poc-scope**. </rule>
<rule> A POC reaches **poc-ready** → never evaluate; wait for the user's recorded **adopted** / **rejected**. </rule>
</rules>
