---
name: orchestrate-feature-delivery
description: Orchestrate a spiked epic's delivery: decompose spike output, sequence waves, dispatch plan/execute/verify agents, track the index, resume, rework, and route ADR changes and reverts. Prefer the project's own equivalent when one exists. Use when decomposing ADRs, sequencing or resuming cells, verifying a cell, answering an issue, reworking delivered or reverted code, or proving an option with a POC.
---

<when-to-use-this-skill>
- User reports an issue or asks about a delivered feature — answer from the record
- User finished a spike and wants features sequenced
- User wants the index updated or delivery resumed
- User wants a cell verified before **done**
- An ADR decision changed mid-delivery
- User asks to revert, restore, or keep the base
- User wants to prove an ADR option with a POC
- Do NOT load before a spike's ADRs exist
- Do NOT load for a single scoped change — plan-development-task and execute-plan own it
- Do NOT load to run a standalone spike — conduct-spike runs spikes
</when-to-use-this-skill>

<knowledge>
<orchestrator-role>
Persistent orchestrator for **one spiked epic**; the index is its source of truth. It owns the epic's reasoning and delegates the work that needs isolation.
- **May do in-session** — read any file, run read-only commands, answer what the record or a bounded read settles, reason across cells' contracts, diagnose, choose the rung.
- **Must decide** — rung, agent, in-scope delegation, whether evidence is trustworthy, whether a cell is done.
- **Must not** — write code, plans, or ADRs; evaluate a POC; widen the epic; merge; act on a stale decision.
- **Dispatch when** the work needs bulk context kept out of yours, independence for trust, a long run, or an artifact-owning specialty.
- **Plan-first, no exemption** — no executor before the plan file exists; never back-fill a plan; every cell runs planned then executed by separate agents.
</orchestrator-role>
<capability-regimes>
**Judgment** — decompose, order, triage, issue/ADR change, POC scope: you own the route, read or answer first. **Contractual** — index and verify: exact statuses, fields, gate inputs.
</capability-regimes>
<delivery-standards>
| Standard | Rule | Details |
|---|---|---|
| **write-boundary** | Only `index.md` inside `**/deliveries/**`; plan/context/rework files belong to the planner and executor. | [write-boundary-guide](reference/write-boundary-guide.md) |
| **feature-definition** | Coherent, independently valuable, across repos: `F1…`, kebab-case, one line, one PR per repo (soft). | — |
| **poc-definition** | One ADR option as a temporary MR the user evaluates; never measured. Adopt = merge; else close. | [poc-lifecycle](reference/poc-lifecycle.md) |
| **delivery-layout** | `deliveries/<epic-name>/index.md` + one `<repo>/<feature-name>/` per cell; one branch per repo per cell, named by convention. | [delivery-layout](reference/delivery-layout.md), [artifact-map](reference/artifact-map.md) |
| **dependency-edge-types** | Per pair A → B: **merge-blocked** (develop on A's contract) · **contract-first** (parallel on stubs) · **poc-gated** · **conflict** (serialize) · **independent**. | [dependency-ordering-guide](reference/dependency-ordering-guide.md) |
| **delivery-state-machine** | `unplanned → planned → in-progress → verified → done`, plus `failed`, `blocked`, `superseded`; POCs fork to `poc-ready → adopted \| rejected`. | [state-machine](reference/state-machine.md) |
| **verification-gate** | One independent gate owns spec **and** quality, risk-proportioned: full for contract or irreversible surfaces, sampled otherwise. | [verification-gate](reference/verification-gate.md) |
| **investigation-triage** | Answer → evidence → decision → spike, first rung that answers; a bounded read is yours. | [investigation-triage](reference/investigation-triage.md) |
| **agent-dispatch** | Dispatch for isolation, independence, a long run, or an artifact-owning specialty; otherwise do it yourself. | [orchestration-guide](reference/orchestration-guide.md), [dispatch-briefs](reference/dispatch-briefs.md) |
| **agent-recovery** | Clear a stall or failure before the user — answer, do, re-brief, retry once; escalate on a listed trigger. | [orchestration-guide](reference/orchestration-guide.md) |
| **rework-modes** | Append-only sibling `rework-<date>.md` carrying the delta; `plan.md` frozen; post-merge adds a feature. | [rework-modes](reference/rework-modes.md) |
| **adr-change** | Versionless — drift comes from **adr-writer** or the user; route governed cells by status. | [orchestration-guide](reference/orchestration-guide.md) |
| **concise-writing** | The index is a board: **≤8,000 chars / ≤120 lines**, table-first, no narration | [delivery-index-format](reference/delivery-index-format.md), [writing-style](reference/writing-style.md) |
</delivery-standards>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Walking a scenario end to end | Triage, decomposition, a round, verification, resume, rework, POC | [examples/](examples/) |
</context-loading-guide>
</knowledge>

<capabilities>
<decompose-change-into-features>
1. Gate per `clarify-request`; show every inference before grouping.
2. Load ADRs (required), then the solution doc and notes when present.
3. Group target-state changes by ADR traceability and module boundary.
4. Block on any ADR–solution contradiction — nothing splits against a stale decision.
5. Assign `F1…`, a kebab-case name, and a one-line description.
</decompose-change-into-features>
<map-features-to-repos>
1. Inventory the repos each feature touches; build the feature × repo matrix — one cell per PR (soft), marking config/data/infra-only cells.
</map-features-to-repos>
<order-feature-delivery>
1. Classify each pair with **dependency-edge-types**; compute waves by topological order (**reference/dependency-ordering-guide.md**).
2. Order intra-feature PRs (contract first) and state develop-now vs merge-after.
</order-feature-delivery>
<produce-delivery-index>
1. Read the base (`scope.md` `Artifact root:`).
2. Write `deliveries/<epic-name>/index.md` per **reference/delivery-index-format.md**.
3. Fill **Spike References** and one brief per cell.
4. Create `{repo}/{feature-name}/` with `plan.md` + `context.md`, marking cells **unplanned**.
5. Run the **Finalise** checklist; confirm features, matrix, waves, and location in one pass.
</produce-delivery-index>
<update-delivery-index>
1. After every result, record status, agent, branch, head, and PR per **reference/state-machine.md**.
2. Mark **planned** only when the plan file exists; a missing file is **failed**.
3. On merge, confirm the recorded head is in the PR with a green or waived receipt.
4. A POC decision → record **adopted** / **rejected** and mark the replaced cell **superseded**.
5. Verify a doubtful result per `question-everything`, then run the **Finalise** checklist.
</update-delivery-index>
<orchestrate-delivery>
1. Load the index, or create it per **decompose-change-into-features**.
2. Assess waves, ready cells, and blockers.
3. **Plan**: dispatch the **planner** to each unplanned, develop-ready cell; verify each plan on disk.
4. **Execute**: dispatch the **executor** to each planned cell with a verified plan, respecting gating and conflicts.
5. Build each brief with scope, **spike references**, and **branch name**.
6. Gate merges on dependencies **done**; the executor pushes, opens the PR, and returns the reference.
7. Apply **verify-cell**, then **update-delivery-index**, until all cells are **done** or the user pauses.
8. All **done** → epic integration review per **reference/verification-gate.md**.
</orchestrate-delivery>
<verify-cell>
**Objective**: One independent review decides spec compliance, trust, and engineering quality before **verified**.
1. Require the handoff and a fully ✅ `plan.md` ending in **Exit gate**.
2. Size the gate by risk per **reference/verification-gate.md** — full review for a contract, API, schema, migration, or irreversible surface; sampled otherwise.
3. Dispatch a fresh **code-reviewer**, never the executor: **Spec** Missing/Extra/Misunderstood · **Trust** receipt matches `head7` · **Quality** blockers, majors, merge call.
4. Pass → mark **verified** via **update-delivery-index**.
5. A gap, Blocker, or Major → **planner** (`rework-<date>.md`) → **executor** → scoped re-review; stay **in-progress**.
</verify-cell>
<resume-delivery>
1. Load the index from the recorded base.
2. Confirm ADR currency; changed → **handle-adr-change** first.
3. Derive state from the index, the active plan or rework, and `## Execution`; resume after the last ✅.
4. Failed → **agent-recovery**; blocked → wait; unplanned → plan; then **orchestrate-delivery**.
</resume-delivery>
<triage-issue>
**Objective**: Choose the cheapest rung that answers the issue — and take it yourself when you can.
1. State the question and what may answer it: the record, a bounded read, or an area beyond your sight.
2. Descend the ladder per **reference/investigation-triage.md**; stop at the first rung that answers. Read the code yourself when the read is bounded; dispatch when it spans areas or needs an independent pass.
3. Escalate one rung at a time, saying why the cheaper one failed; dispatch a specialist only on a stated trigger.
</triage-issue>
<handle-post-implementation-issue>
1. Name the affected cell, its governing ADR, and its status; restate expected versus actual.
2. Classify it as mechanical (revert / restore / copy / keep) per **reference/mechanical-restore.md**, or behavioral.
3. Apply **triage-issue**, scope to that decision, and present the rung for confirmation.
4. Plan → **planner** (`rework-<date>.md`), execute → **executor**, L2 → **adr-writer**, L3 → **spike-conductor**.
5. Apply **update-delivery-index** — post-merge adds a rework feature; pre-merge changes no row.
</handle-post-implementation-issue>
<handle-adr-change>
1. Confirm the changed ADR and its decision from the user or **adr-writer**; list governed cells from the index's `ADRs:` entries.
2. Route by status per **reference/orchestration-guide.md**, surface in-flight POCs, then confirm.
</handle-adr-change>
<define-poc-scope>
1. Flag `Type: poc` when an ADR option needs a reviewable working slice; fill `adr`, `option`, and optional `success-criteria` in the header, `Replaces`/`Compare` in the index.
2. Sequence POCs in **Wave 0** (siblings in parallel), add a **poc-gated** edge, and confirm.
</define-poc-scope>
</capabilities>

<rules>
<rule> Every inbound request passes `clarify-request`'s intake gate first. </rule>
<rule> No index yet → **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**. </rule>
<rule> Index exists → **orchestrate-delivery**, or **resume-delivery** for an interrupted epic. </rule>
<rule> A cell's state changed → **update-delivery-index** before more dispatches; a read changes nothing. </rule>
<rule> An agent stalls, asks, or fails → **agent-recovery**; escalate only on a listed trigger, with the attempt trail. </rule>
<rule> Execution completes → **verify-cell** before the index advances; no **done** without a gate or waiver. </rule>
<rule> An issue after implementation → **handle-post-implementation-issue**; never re-decompose the epic. </rule>
<rule> A revert, restore, copy, or keep request → a mechanical rework with a `Source`. </rule>
<rule> Any investigation starts at **triage-issue** — answer from the record and read a bounded file yourself; dispatch when it spans areas or needs isolation. </rule>
<rule> An ADR change or **adr-writer** revision → **handle-adr-change**; never dispatch on a stale decision. </rule>
<rule> An ADR option needs proof → **define-poc-scope**. </rule>
<rule> A POC reaches **poc-ready** → never evaluate; wait for the user's recorded **adopted** / **rejected**. </rule>
</rules>
