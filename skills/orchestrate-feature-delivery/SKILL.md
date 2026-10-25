---
name: orchestrate-feature-delivery
description: Orchestrate spiked-epic delivery by decomposing, sequencing, triaging issues, dispatching agents, verifying, resuming, reworking, and tracking a delivery index. Use when proving an ADR option with a POC, handling an ADR change, or deciding whether to answer an issue or run a spike.
---

<when-to-use-this-skill>
- User reports an issue in a sentence or two and the report must be clarified before a rung is chosen
- User finished a spike and wants to decompose its solution doc / ADRs into features or phases (creates the delivery index)
- User wants to prove an ADR option with a POC before deciding — define and gate POC cells (see **define-poc-scope**)
- User wants to sequence which features run in parallel and which wait for another feature's PR to merge
- User wants to dispatch parallel agents to plan (plan-development-task) or execute (execute-plan) feature × repo cells of an epic
- User wants to resume or continue delivery of an existing spiked epic — load the index and derive next actions from its status
- User wants a completed cell independently verified for spec compliance and report trust before it is marked done
- User asks a question about a delivered feature or reports unexpected behavior — answer from the record before investigating
- User found an issue after a feature was implemented (a cell is done, or implemented but not yet pushed/merged) and wants rework — focused spike on the governing ADR, a sibling rework file, and its execution
- User reports an ADR decision changed mid-delivery — re-route the cells governed by it (see **handle-adr-change**)
- User asks to revert a delivered change or keep a file as the base branch has it — route it as a mechanical rework
- Do NOT load before a spike's solution doc / ADRs exist — let conduct-spike produce them first
- Do NOT load to plan or execute a single, already-scoped change — plan-development-task and execute-plan handle single cells
- Do NOT load to run a standalone spike — conduct-spike runs spikes; this skill only triggers focused rework spikes
</when-to-use-this-skill>

<knowledge>
<orchestrator-role>
Persistent orchestrator for **one spiked epic**; input is the **delivery index** plus the spike output (solution doc, ADRs). It decomposes, sequences, dispatches, and tracks — never plans or codes, and writes only delivery docs (see **agent-dispatch**, **write-boundary**). The index is the source of truth.

**Mandate** — never perform a delivery task; every plan / execute / verify / artifact update is dispatched. **Answering from recorded artifacts is orchestration, not delivery** — read the index, ADRs, findings, plans, and `context.md` first (see **investigation-triage**). **Push and PR creation belong to the executor** — it asks for approval, opens the request, and returns the reference; the orchestrator records it. **Plan-first gate** — no executor until the plan file exists on disk. **Never back-fill** — a plan is written before execution. **No simplicity exemption** — every cell runs the full flow.
</orchestrator-role>
<write-boundary>
Writes are confined to `**/deliveries/**` — never code, config, tests, or files outside it. Code changes come only from a dispatched **executor**; plans only from the **planner**. Where supported, an `edit` permission and a `task` allowlist enforce this; elsewhere doctrine applies. After every index write, run the own-writes snapshot-delta check so unrelated repo changes never stop delivery. Details: **reference/write-boundary-guide.md**.
</write-boundary>
<feature-definition>
A feature is a coherent, independently valuable deliverable spanning one or more repos.
- **One PR per repo per feature** is soft; split if the slice exceeds one reviewable PR.
- Small shared-library changes stay in the **first consuming feature**; only large or widely-shared ones lead.
- IDs `F1`, `F2`, … with kebab-case names and one-line descriptions.
</feature-definition>
<poc-definition>
A POC is a **temporary implementation** of one ADR option — a normal feature slice, delivered as an MR. The **user** evaluates the MR; the skill never measures, evaluates, or writes a report. Cells carry `adr`, `option`, and optional `success-criteria` (the user's review checklist) in the `plan.md` header, and `replaces` / `compare` in the index. Adoption: **POC-as-implementation** (merge the MR on adopt) or **POC-as-decision-input** (close the MR and implement the chosen option). Lifecycle: **reference/poc-lifecycle.md**.
</poc-definition>
<delivery-layout>
One epic = `deliveries/<epic-name>/`, with `index.md` at the root and one `<repo>/<feature-name>/` folder per repo per feature (kebab-case name, never the ID). One artifact, one job: `index` = state · `context` = charter · `plan` = execution · `rework` = delta · git/PR = record; the orchestrator writes only the index. Spike artifacts are the knowledge plane; delivery references them, never copies — map: **reference/artifact-map.md**. Base root and ownership: **reference/delivery-layout.md**.
</delivery-layout>
<dependency-edge-types>
Classify each feature pair (A → B):

| Edge | Develop | Merge |
|---|---|---|
| **merge-blocked** | after A's contract is known | only after A merges |
| **contract-first** | in parallel (against agreed stubs) | after A |
| **poc-gated** | only after the POC decision | after the decision |
| **conflict** | serialize or split (same files/repo) | — |
| **independent** | parallel | any order |

Wave computation + intra-feature merge order: **reference/dependency-ordering-guide.md**.
</dependency-edge-types>
<delivery-state-machine>
Cells follow **unplanned → planned → in-progress → verified → done**, plus recoverable **failed** / **blocked**; POCs fork **verified → poc-ready → adopted | rejected**. **Develop-ready** = dependencies **planned**; **merge-ready** = dependencies **done**. The gate is mandatory; record any user waiver. Details: **reference/state-machine.md**.
</delivery-state-machine>
<verification-gate>
A cell reaches **verified** (then **done** / **poc-ready**) only after an independent gate — spec compliance + trust — passes. Quality review stays with **execute-plan**'s `review-post-execution`. The handoff is the **latest round only** in `context.md` `## Execution` — status, `base7..head7`, PR, one-line test evidence, one-line review outcome; deferred concerns persist in `## Open concerns`; history lives in git/PR. Handoff, verdicts, fix-loop cap, breaker, integration review: **reference/verification-gate.md**.
</verification-gate>
<request-intake>
Clarify before classifying: restate the reported behavior — never the suspected cause — and run `question-everything`'s **challenge-the-ask** when the report is ambiguous. A report stating expected and actual behavior passes on the restatement. Clarification is a precondition, not an L-rung. Protocol: **reference/investigation-triage.md**.
</request-intake>
<investigation-triage>
Restate the report first (**request-intake**), then descend the **answer → evidence → decision → spike** ladder and stop at the first rung that answers the question. L0 answers from recorded artifacts in-session; L1 is one read-only investigator; L2 is a direct ADR revision; L3 is a spike. State the rung and its justification before spending. Full triggers, routes, and artifacts: **reference/investigation-triage.md**.
</investigation-triage>
<agent-dispatch>
Delegate every delivery task. Map: answer (L0, in-session) · investigate → **code-investigator** (L1) · spike → **spike-conductor** (L3) · plan → **planner** · execute → **executor** · verify → **code-reviewer** · solution-doc → **solution-doc-writer** · ADR → **adr-writer**. Plan and execute are separate sessions — never both in one agent, never before a verified plan file. No agent mechanism → ask the user; never do the work yourself. Rules and briefs: **reference/orchestration-guide.md**.
</agent-dispatch>
<branch-and-push-conventions>
Execution agents commit locally in small steps; they push and open the PR only after user confirmation. One branch per repo per cell, named per the repo's convention (detect — never assume a prefix); the index records branch, PR, and head commit from the executor's handoff. A cell is **done** only after its PR merges the recorded head commit, or the user records a waiver. Rules: **reference/delivery-layout.md**.
</branch-and-push-conventions>
<rework-modes>
Rework is **append-only**: implemented steps never change; scoped to the cell (usually its governing ADR). Each rework is a sibling `rework-<date>.md` carrying only the delta — trigger, Scope Boundary, Done means, changed steps; it inherits the cell's `context.md` charter by reference and never creates a second context. `plan.md` stays frozen. Pending-step defects are amended in place by the planner — never reworked or moved to a new plan folder. **Post-merge** (cell **done**) adds a rework feature in a new wave; **pre-merge** (cell **in-progress**) stays on the same cell. Rules and lineage: **reference/rework-modes.md**.
</rework-modes>
<adr-drift>
ADRs are **versionless** — drift comes from the **adr-writer** return or the user, never a file diff. Route cells by status per **reference/orchestration-guide.md** (ADR changes).
</adr-drift>
<concise-writing>
Delivery-index prose follows **reference/writing-style.md**: table-first, atomic bullets, one-sentence descriptions, no narration, So-what test. **rewrite-concise** is the final gate — move facts to tables, then shorten; never present prose that fails a cap.

`index.md` is a board, not a report: **≤8,000 chars / ≤120 lines**. Detail lives in the feature folder; history lives in git/PR. Template, archive rule, and measurement: **[reference/delivery-index-format.md](reference/delivery-index-format.md)**.
</concise-writing>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Answering an issue/question before dispatching an investigation | L-1 clarity check, L0–L3 ladder, triggers, cost and artifacts per rung | [reference/investigation-triage.md](reference/investigation-triage.md) |
| Dispatching parallel agents, gating, status transitions, or failure handling | Agent dispatch, orchestration loop, resume, failure rules | [reference/orchestration-guide.md](reference/orchestration-guide.md) |
| Classifying dependency edges, computing waves, or intra-feature merge order | Edge types, wave algorithm, develop-vs-merge | [reference/dependency-ordering-guide.md](reference/dependency-ordering-guide.md) |
| Writing or updating the delivery index | Index schema, per-cell briefs, status lifecycle | [reference/delivery-index-format.md](reference/delivery-index-format.md) |
| Locating delivery artifacts, naming feature folders, or branching/pushing | Layout, base root, branch/push conventions | [reference/delivery-layout.md](reference/delivery-layout.md) |
| Checking statuses, transitions, or develop/merge readiness | Statuses, transitions, readiness predicates | [reference/state-machine.md](reference/state-machine.md) |
| Handling rework after implementation (post-merge or pre-merge) | Rework modes, lineage, index handling | [reference/rework-modes.md](reference/rework-modes.md) |
| Choosing between answering an issue and running a spike | L0–L3 triage walkthrough | [examples/issue-triage.md](examples/issue-triage.md) |
| Handling a post-merge or pre-merge rework | Sibling rework file, spike routing, execution | [post-implementation-rework.md](examples/post-implementation-rework.md) · [pre-merge-rework.md](examples/pre-merge-rework.md) |
| Handling a revert, restore, copy, or keep request | Mechanical vs behavioral routing, Source enum, ladder, proof | [reference/mechanical-restore.md](reference/mechanical-restore.md) |
| Running a full end-to-end decomposition from spike output to index | End-to-end multi-repo example | [examples/multi-repo-feature-decomposition.md](examples/multi-repo-feature-decomposition.md) |
| Running one orchestration round with parallel agents | Dispatch + status-update walkthrough | [examples/orchestration-round.md](examples/orchestration-round.md) |
| Running the verification gate | Handoff, verdicts, fix-loop cap, breaker | [reference/verification-gate.md](reference/verification-gate.md) |
| Verifying a completed cell | Gate walkthrough | [examples/cell-verification-gate.md](examples/cell-verification-gate.md) |
| Continuing an interrupted epic | Resume walkthrough with mixed statuses | [examples/resume-after-interruption.md](examples/resume-after-interruption.md) |
| Parallel vs merge-blocked features | Dependency-ordering example | [examples/parallel-vs-sequential-waves.md](examples/parallel-vs-sequential-waves.md) |
| Marking, sequencing, or gating POC cells, or handling a user-recorded POC decision | POC definition, lifecycle, adoption models | [reference/poc-lifecycle.md](reference/poc-lifecycle.md) |
| Running a full POC round (compare POCs → user-recorded decision → adopt/reject) | End-to-end POC walkthrough | [examples/adr-option-poc.md](examples/adr-option-poc.md) |
| Index prose | BLUF rules, transforms, banned phrases | [reference/writing-style.md](reference/writing-style.md) |
| Rewriting wordy index prose to its shortest faithful form | Move-then-shorten walkthrough, before/after model | [examples/concise-rewrite.md](examples/concise-rewrite.md) |
| Handling an ADR change mid-delivery, or seeing it walked through with mixed statuses | ADR-change routing, resume currency check, done/planned/in-progress walkthrough | [reference/orchestration-guide.md](reference/orchestration-guide.md) · [examples/adr-change-mid-delivery.md](examples/adr-change-mid-delivery.md) |
| Confining orchestrator writes / running the boundary check | Allowed vs forbidden writes, enforcement layers, own-writes snapshot-delta check, delegation | [reference/write-boundary-guide.md](reference/write-boundary-guide.md) |
| Writing or validating `index.md` size, or checking a `context.md` handoff | Char/line caps, board template, archive rule, latest-only handoff | [reference/delivery-index-format.md](reference/delivery-index-format.md) · [reference/verification-gate.md](reference/verification-gate.md) |
| Deciding whether a fact belongs in the spike artifacts or the delivery docs | Two-plane map, handoff contract, edit ownership, change routing | [reference/artifact-map.md](reference/artifact-map.md) |
</context-loading-guide>

</knowledge>

<capabilities>
<decompose-change-into-features>
1. Load the spike artifacts: solution doc (primary), ADRs, findings.
2. Group target-state changes into coherent, independently valuable features by ADR traceability and module boundary — never 1:1 with scope-map problems (see **reference/artifact-map.md**).
3. Apply **feature-definition**; assign an ID (`F1`, …), kebab-case name, and one-line description.
4. Present the feature list and confirm before proceeding.
</decompose-change-into-features>
<map-features-to-repos>
1. Inventory the repos each feature's target-state changes touch.
2. Build the feature × repo matrix; each cell is one PR (soft — see **feature-definition**). Mark config/data/infra-only cells so plans expect no code PR.
3. Present the matrix and confirm the repo inventory.
</map-features-to-repos>
<order-feature-delivery>
1. Classify each feature pair with **dependency-edge-types**.
2. Build the dependency graph and compute waves by topological order (**reference/dependency-ordering-guide.md**).
3. Set intra-feature PR order (contract lib first, consumers last) and state develop-now vs merge-after per feature.
4. Present the wave plan and confirm.
</order-feature-delivery>
<produce-delivery-index>
1. Read the recorded base (`scope.md` `Artifact root:`); write `deliveries/<epic-name>/index.md` per **reference/delivery-index-format.md** (resolve the base only when missing).
2. Include the **Spike References** block (ADR files, solution-doc sections).
3. Create repo-first folders `.../{repo}/{feature-name}/plan.md` + `context.md`; mark cells **unplanned** with their plan location.
4. Verify structure, statuses, readiness, and the **≤8,000-char / 120-line** index budget per **reference/delivery-index-format.md**; apply **rewrite-concise** and the boundary check.
5. Confirm the location with the user — **orchestrate-delivery** drives from here.
</produce-delivery-index>
<update-delivery-index>
1. After every agent result, update the status per **reference/state-machine.md** — `unplanned → planned → in-progress → verified → done`, plus `failed` / `blocked`.
2. Record agent assignment, plan location, branch, head commit, and the PR reference from the executor handoff (see **branch-and-push-conventions**).
3. **Plan-first gate**: mark **planned** only when the plan file exists; a missing file is **failed**.
4. On merge, confirm the recorded head commit is in the merged PR before **done**; re-check downstream readiness.
5. On a POC decision, record **adopted/rejected** and dispatch follow-ups per **reference/poc-lifecycle.md**.
6. Inconsistent result → verify via `question-everything` before recording.
7. Keep the index the single source of truth; verify it per **reference/delivery-index-format.md**, apply **rewrite-concise**, measure `index.md` (**≤8,000 chars / ≤120 lines** per **reference/delivery-index-format.md**; collapse rows and archive completed waves), and run the write-boundary check.
</update-delivery-index>
<orchestrate-delivery>
1. Load the index — or create it via **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**.
2. Assess statuses, completed waves, ready cells, and blockers.
3. **Plan**: dispatch the **planner** to each unplanned, develop-ready cell; confirm each plan file on disk before advancing.
4. **Execute**: dispatch the **executor** to each planned cell with a verified plan file, respecting develop-gating and no-conflict rules.
5. Brief each agent with scope, **spike references**, and **branch name**; when plan/execution surfaces artifact changes, dispatch the owning agent.
6. Gate merges on dependencies **done**; the executor handles push approval and PR creation, and the orchestrator records the returned reference.
7. Collect results; apply **verify-cell**, then **update-delivery-index**; re-assess and repeat until all cells are done or the user pauses.
8. When all cells are **done**, run the epic integration review (cross-cell review + integration test pass; triage deferred Minors) per **reference/verification-gate.md**.
</orchestrate-delivery>
<verify-cell>
**Objective**: Independently verify spec compliance and report trust before **verified**; never duplicate **execute-plan**'s `review-post-execution` quality review.

1. Require the handoff: `plan.md` all ✅; `context.md` `## Execution` with status, `base7..head7`, PR, one-line test evidence, and one-line review outcome (latest round only — a long appended log is not a pass), plus `## Open concerns`. A POC cell is verified like any other cell; its MR is the user's evaluation vehicle.
2. Dispatch a **fresh code-reviewer** (**review-code**) with the range, plan, context, governing ADR, solution-doc section, and constraints — it fetches the diff; never the executor instance.
3. Require two verdicts: **spec compliance** (Missing / Extra / Misunderstood) and a **trust check** of claimed review/test evidence against the diff (sample Blocker/Major fixes; no suite re-run).
4. Pass → mark **verified** via **update-delivery-index**.
5. Gap or Critical/Important → dispatch **planner** (sibling `rework-<date>.md`), then **executor**, then a scoped re-review; the cell stays **in-progress**.
6. Cap the fix loop at 2 rounds; a finding recurring after round 1 escalates immediately. Roll deferred Minors into the integration review.
</verify-cell>
<resume-delivery>
1. Load the index from the recorded base (`scope.md` `Artifact root:` → `deliveries/<epic-name>/index.md`) plus the spike output.
2. Confirm ADR currency with the user; if a governing ADR changed, apply **handle-adr-change** first.
3. Determine state from the index, the active plan/rework, the **latest** `context.md` `## Execution`, and `## Open concerns` — there is no raw log to load; history is git/PR. Skip completed waves; resume in-progress from the last step (active `rework-<date>.md`, else `plan.md`), skipping ✅ and ⏭ steps; failed → retry, or dispatch the planner to **amend** a defective pending step in the same plan; blocked → wait; unplanned → plan.
4. Apply **orchestrate-delivery** from that state; tell the user what is resumed vs skipped before dispatching.
</resume-delivery>
<triage-issue>
**Objective**: Choose the cheapest rung that answers an issue before any dispatch.

1. State the question in one sentence; list artifacts that may answer it — index, `context.md`, plan/rework, ADR, findings/evidence, git log.
2. Apply **request-intake** — restate the reported behavior and close material ambiguity before choosing a rung.
3. **L0 — Answer**: read them in-session; answer when the record settles it. No dispatch, no artifacts.
4. **L1 — Evidence**: for a missing/contradicted code fact, dispatch one read-only **code-investigator** with artifacts by path; answer with `file:line`.
5. **L2 — Decision**: for exactly one contradicted ADR decision, dispatch **adr-writer** to revise in place; add **solution-doc-writer** only if target state changes; verify new code claims once.
6. **L3 — Spike**: dispatch **spike-conductor** only for ≥2 decisions/areas, new options, or required formal findings; scope as a **delta**.
7. Escalate one rung at a time and state why the cheaper rung failed; if ambiguous, ask the user with each rung's cost. Record the rung only when state changes; validate L3's trigger and that L0/L1 wrote no artifacts.
</triage-issue>
<handle-post-implementation-issue>
1. Identify the affected cell, its governing ADR, and status — **done** or **in-progress**.
2. Restate the reported behavior per **request-intake** — expected versus actual — before classifying.
3. Classify the request: mechanical (revert / restore / copy / keep) per [mechanical-restore](reference/mechanical-restore.md), or behavioral. A mechanical request needs a `Source`, not a feature plan.
4. Scope narrowly to that decision — never the whole epic.
5. Apply **triage-issue**, then present the rung for confirmation — **append-only**: plan → **planner** (sibling `rework-<date>.md`); execute → **executor**; L2 → **adr-writer** / **solution-doc-writer**; L3 → **spike-conductor** (pre-merge only if the governing ADR is challenged).
6. Apply **update-delivery-index** — post-merge adds a rework feature in a new wave (original stays **done**); pre-merge keeps the cell (no index change; the rework file is the record).
7. The executor handles push approval and PR creation; record the returned reference.
</handle-post-implementation-issue>
<handle-adr-change>
1. Confirm the changed ADR and new decision from the user or **adr-writer** (see **adr-drift**).
2. List governed cells from the index's per-feature `ADRs:` entries.
3. Route by status (**reference/orchestration-guide.md**, ADR changes): planned → re-plan; in-progress → pre-merge rework; done → post-merge rework; surface in-flight POCs.
4. Update the index, apply **rewrite-concise**, and confirm routing before dispatching.
</handle-adr-change>
<define-poc-scope>
1. Flag a cell with `Type: poc` during **decompose-change-into-features** when an ADR option needs a working slice the user can review.
2. Fill `adr`, `option`, and optional `success-criteria` (the user's checklist, in the plan header), plus index-level `replaces` / `compare` per **poc-definition**.
3. Sequence POCs in **Wave 0** (`compare` siblings in parallel) and add a **poc-gated** edge.
4. Present the POC cells and optional review criteria; confirm before recording.
</define-poc-scope>
<rewrite-concise>
**Objective**: Rewrite a target doc to the shortest form preserving all facts — the final gate before presenting the index. Never drop a fact to hit a cap.

**Steps**:
1. Draft freely — do not self-edit while writing.
2. Label violations per **reference/writing-style.md** (filler, redundancy, hedge, narration, multi-claim, over-cap).
3. **Move-then-shorten**: move facts into tables, then shorten the rest.
4. Apply the transforms; run the **So-what test** — delete sentences that add no fact.
5. Re-scan to zero violations (max 2 passes).
</rewrite-concise>

</capabilities>

<rules>
<rule> When an issue report or feature request is ambiguous, apply **request-intake** before **triage-issue** — a clarification is a precondition, never a rung. </rule>
<rule> When spike output exists but no delivery index, apply **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**. </rule>
<rule> When a delivery index exists and the user wants to drive or continue delivery, apply **orchestrate-delivery**; apply **resume-delivery** when continuing an epic interrupted in a previous session. </rule>
<rule> After any agent result that changes a cell's state, apply **update-delivery-index** before dispatching further agents — L0/L1 answers change no state. </rule>
<rule> When dispatching any delivery task (investigate, plan, execute, verify, solution-doc, or ADR update), always dispatch the owning agent per **agent-dispatch**. </rule>
<rule> Never dispatch an executor for a cell until its plan file is verified on disk (the **plan-first gate**); never write or append a plan after execution. </rule>
<rule> Plan and execute are always separate dispatches in that order — never let one agent do both for the same cell, and never skip a step because a cell looks simple or easy. </rule>
<rule> When a cell's execution completes, apply **verify-cell** before **update-delivery-index** advances it — never mark a cell **done** or **poc-ready** without a passing verification gate or a recorded user waiver. </rule>
<rule> The verification gate checks spec compliance and report trust only — never duplicate **execute-plan**'s quality review; at the fix-loop cap, stop and escalate to the user. </rule>
<rule> When a verified cell is approved for integration, dispatch the executor to push and open the PR; record only the returned reference — never open the PR from the orchestrator. </rule>
<rule> Never write `plan.md` / `context.md` / `rework-<date>.md` from the orchestrator — the planner and executor own them; dispatch gate findings straight to the planner and track status only in the index. </rule>
<rule> When all cells are **done**, run the epic integration review before declaring the epic delivered (see **reference/verification-gate.md**). </rule>
<rule> When the user asks about a single cell's plan or status, read the delivery index and route the cell to **plan-development-task** or **execute-plan** — do not re-run the whole orchestration. </rule>
<rule> When an issue surfaces after a feature was implemented (a cell is **done** or **in-progress**), apply **handle-post-implementation-issue** — never re-run **decompose-change-into-features** on the whole epic. </rule>
<rule> When the request is to revert, restore, copy, or keep code unchanged, treat it as mechanical per [mechanical-restore](reference/mechanical-restore.md) — dispatch a rework with a `Source`. </rule>
<rule> Before any investigation dispatch, apply **triage-issue** — answer from recorded artifacts first (L0); dispatch an investigator or a spike only when a higher rung is justified. </rule>
<rule> When the user reports an ADR change or an **adr-writer** agent returns a revision, apply **handle-adr-change** — never dispatch a planned cell on a stale decision. </rule>
<rule> When decomposing change items and an ADR option needs proof before a decision, apply **define-poc-scope** to flag and sequence POC cells. </rule>
<rule> When a POC cell reaches **poc-ready**, do not evaluate or decide — the MR is the user's evaluation vehicle; wait for the user to record **adopted**/**rejected** directly in the index, then apply **update-delivery-index** to record it and dispatch the follow-ups. </rule>
<rule> When presenting or confirming any delivery index (new or updated), apply **rewrite-concise** as the final gate — never present a draft that fails a **writing-style.md** cap. </rule>
<rule> When writing or updating `index.md`, apply the **index budget** — keep it ≤8,000 chars / ≤120 lines; collapse feature sections to table rows and archive completed waves instead of growing the file. </rule>
<rule> When verifying a cell, require the **latest** `## Execution` handoff (status, range, PR, one-line evidence, one-line review outcome) plus `## Open concerns` — never treat an appended execution log as the handoff. </rule>
<rule> Confine every orchestrator write to the delivery folder (`**/deliveries/**`) and run the delivery write-boundary check after every index write — an own-writes snapshot delta; never modify code, config, tests, or any file outside it. </rule>
</rules>
