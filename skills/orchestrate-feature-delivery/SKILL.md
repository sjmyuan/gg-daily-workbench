---
name: orchestrate-feature-delivery
description: Orchestrate a spiked epic's delivery: decompose spike output, sequence waves, dispatch plan/execute/verify agents, track the index, resume, rework, and route ADR changes and reverts. Prefer the project's own equivalent when one exists. Use when decomposing ADRs, slicing an oversized feature, sequencing or resuming cells, verifying a cell, answering an issue, reworking delivered or reverted code, or proving an option with a POC.
---

<when-to-use-this-skill>
- User reports an issue or asks about a delivered feature — answer from the record
- User finished a spike and wants features sequenced or sliced
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
Persistent orchestrator for **one spiked epic**; the index is its source of truth. Owns its reasoning; delegates work needing isolation.
- **May do in-session** — read any file, run read-only commands, answer what the record or a bounded read settles, reason across cells, choose the rung.
- **Must decide** — rung, agent, in-scope delegation, whether evidence is trustworthy, whether a cell is done.
- **Must not** — write code, plans, or ADRs; evaluate a POC; widen the epic; merge; act on stale decisions.
- **Dispatch when** the work needs bulk context out of yours, independence for trust, a long run, or an artifact-owning specialty.
- **Plan-first, no exemption** — no executor before the plan exists; never back-fill one; plan and execute stay separate.
</orchestrator-role>
<capability-regimes>
**Judgment** — decompose, order, triage, issue/ADR change, POC scope. **Contractual** — index and verify: fields and statuses.
</capability-regimes>
<delivery-standards>
| Standard | Rule | Details |
|---|---|---|
| **write-boundary** | Only `index.md` inside `**/deliveries/**`; plan/context/rework files belong to the planner and executor. | [write-boundary-guide](reference/write-boundary-guide.md) |
| **feature-definition** | Coherent, **mergeable alone**: one PR per cell, ≤40 files; slice above. `F1…`/`F3.1`, kebab-case. | [pr-size-slicing](reference/pr-size-slicing.md) |
| **poc-definition** | One ADR option as a temporary PR the user evaluates; adopt = merge, else close. | [poc-lifecycle](reference/poc-lifecycle.md) |
| **delivery-layout** | `deliveries/<epic-name>/index.md` + one `<repo>/<feature-name>/` per cell; one branch per cell. | [delivery-layout](reference/delivery-layout.md), [artifact-map](reference/artifact-map.md) |
| **dependency-edge-types** | Per pair A → B: **merge-blocked** (develop on A's contract) · **contract-first** (parallel on stubs) · **poc-gated** · **conflict** (serialize) · **independent**. | [dependency-ordering-guide](reference/dependency-ordering-guide.md) |
| **delivery-state-machine** | `unplanned → planned → in-progress → verified → done`, plus `failed`, `blocked`, `superseded`; POCs fork to `poc-ready → adopted \| rejected`. | [state-machine](reference/state-machine.md) |
| **verification-gate** | One independent gate owns spec **and** quality; Full for protected surfaces, else Sampled. | [verification-gate](reference/verification-gate.md) |
| **investigation-triage** | Answer → evidence → decision → spike, first rung that answers. | [investigation-triage](reference/investigation-triage.md) |
| **plan-intake** | Six mechanical checks before **planned**; never a design review. | [plan-intake-check](reference/plan-intake-check.md) |
| **agent-dispatch** | Resolve the role first; dispatch only for its stated reasons; the brief is a delta within budget. | [orchestration-guide](reference/orchestration-guide.md) |
| **agent-recovery** | Clear a stall before the user: answer, do, re-brief, retry; escalate on a trigger. | [orchestration-guide](reference/orchestration-guide.md) |
| **rework-modes** | Sibling `rework.md` (post-merge dated); `plan.md` frozen; post-merge adds a feature. | [rework-modes](reference/rework-modes.md) |
| **adr-change** | Versionless — drift from **code-analyst** (`adr-rewrite`) or the user; route governed cells by status. | [orchestration-guide](reference/orchestration-guide.md) |
| **concise-writing** | The index is a board: **≤8,000 chars / ≤120 lines**, table-first. | [delivery-index-format](reference/delivery-index-format.md), [writing-style](reference/writing-style.md) |
</delivery-standards>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Scenario walkthrough | Every flow | [examples/](examples/) |
</context-loading-guide>
</knowledge>

<capabilities>
<decompose-change-into-features>
1. Gate per `clarify-request`; show every inference before grouping.
2. Load ADRs (required), then the solution doc when present.
3. Group target-state changes by ADR traceability and module boundary; slice any group estimated over the review budget along a green seam (**pr-size-slicing**).
4. Block on any ADR–solution contradiction — nothing splits on a stale decision.
5. Assign `F1…`, a kebab-case name, and a one-line description.
</decompose-change-into-features>
<map-features-to-repos>
1. Inventory each feature's repos; build the feature × repo matrix, marking config/data/infra-only cells.
</map-features-to-repos>
<order-feature-delivery>
1. Classify each pair with **dependency-edge-types**; compute waves topologically (**reference/dependency-ordering-guide.md**).
2. Order intra-feature PRs (contract first) and state develop-now vs merge-after.
</order-feature-delivery>
<produce-delivery-index>
1. Read the base (`scope.md` `Artifact root:`).
2. Write `deliveries/<epic-name>/index.md` per **reference/delivery-index-format.md**.
3. Fill **Spike References** and one brief per cell.
4. Create `{repo}/{feature-name}/` with `plan.md` + `context.md`, marking cells **unplanned**.
5. Run **Finalise**; confirm features, matrix, waves, location once.
</produce-delivery-index>
<update-delivery-index>
1. After every result, record status, agent, branch, head, and PR per **reference/state-machine.md**.
2. Mark **planned** only when the plan passes **plan-intake-check**; a missing file is **failed**.
3. On merge, confirm the recorded head is in the PR with a green or waived receipt.
4. A POC decision → record **adopted** / **rejected** and mark the replaced cell **superseded**.
5. Verify a doubtful result per `question-everything`; run **Finalise**.
</update-delivery-index>
<orchestrate-delivery>
1. Load the index, or create it per **decompose-change-into-features**.
2. Assess waves, ready cells, and blockers.
3. **Plan**: dispatch the **planner** to each unplanned, develop-ready cell; run **plan-intake-check** before the cell turns **planned**. Over budget → split (**pr-size-slicing**).
4. **Execute**: dispatch the **executor** to each planned cell whose plan passed intake, respecting gating and conflicts.
5. Build each brief per **dispatch-briefs**.
6. Gate merges on dependencies **done**; the executor pushes, opens the PR, returns the reference.
7. Apply **verify-cell**, then **update-delivery-index**, until all cells are **done** or the user pauses.
8. All **done** → epic integration review (**reference/verification-gate.md**).
</orchestrate-delivery>
<verify-cell>
**Objective**: One independent review decides spec compliance, trust, and engineering quality before **verified**.
1. Require the handoff and a fully ✅ `plan.md` ending in **Exit gate**.
2. Size the gate by risk per **reference/verification-gate.md** — Full for any protected surface.
3. Dispatch a fresh **code-reviewer**, never the executor: **Spec** Missing/Extra/Misunderstood · **Trust** receipt matches `head7` · **Quality** blockers, majors, merge call, each labelled `mechanical`/`design`.
4. Pass → mark **verified** via **update-delivery-index**.
5. Mechanical only: one **executor** repair (`Fix class: mechanical`, inline) → scoped re-review. Any design finding: **planner** `rework.md` → **executor** → scoped re-review. Stay **in-progress**.
</verify-cell>
<resume-delivery>
1. Load the index from the recorded base.
2. Confirm ADR currency; changed → **handle-adr-change** first.
3. Derive state from the index, the active plan or rework, and `## Execution`; resume after the last ✅.
4. Failed → **agent-recovery**; blocked → wait; unplanned → plan; then **orchestrate-delivery**.
</resume-delivery>
<triage-issue>
**Objective**: Choose the cheapest rung that answers the issue — and take it yourself when you can.
1. State the question and what may answer it: the record, a bounded read, or an area beyond sight.
2. Descend the ladder per **reference/investigation-triage.md**; stop at the first rung that answers. Dispatch when it spans areas or needs isolation.
3. Escalate one rung at a time, saying why the cheaper one failed; dispatch a specialist only on a stated trigger.
</triage-issue>
<handle-post-implementation-issue>
1. Name the affected cell, its ADR, and its status; restate expected versus actual.
2. Classify it as mechanical (revert / restore / copy / keep) per **reference/mechanical-restore.md**, or behavioral.
3. Apply **triage-issue** to that decision; present the rung for confirmation.
4. Plan → **planner** (rework file), execute → **executor**, L2 → **code-analyst** (`adr-rewrite`), L3 → **spike-conductor**.
5. Apply **update-delivery-index** — post-merge adds a rework feature; pre-merge changes no row.
</handle-post-implementation-issue>
<handle-adr-change>
1. Confirm the changed ADR and decision from the user or **code-analyst**; list governed cells from the index's `ADRs:` entries.
2. Route by status per **orchestration-guide**; surface in-flight POCs, then confirm.
</handle-adr-change>
<define-poc-scope>
1. Flag `Type: poc` when an option needs a reviewable proof; fill `adr`, `option`, optional `success-criteria` (plan header), `Replaces`/`Compare` (index).
2. Sequence POCs in **Wave 0** (siblings in parallel), add a **poc-gated** edge, and confirm.
</define-poc-scope>
</capabilities>

<rules>
<rule> Every inbound request passes `clarify-request`'s intake gate first. </rule>
<rule> No index yet → **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**. </rule>
<rule> Index exists → **orchestrate-delivery**, or **resume-delivery** for an interrupted epic. </rule>
<rule> A cell's state changed → **update-delivery-index**; a read changes nothing. </rule>
<rule> A dispatch names the resolved agent, its role skill, and `Mode: delivery`; no role resolves silently, and no dispatched agent asks the user. </rule>
<rule> An agent stalls, asks, or fails → **agent-recovery**; escalate only on a listed trigger, with the attempt trail. </rule>
<rule> A plan returns → **plan-intake-check**; execution completes → **verify-cell**; no **done** without a gate or waiver. </rule>
<rule> A verified plan over budget, no PR yet → split; once execution starts, record the oversize. </rule>
<rule> An issue after implementation → **handle-post-implementation-issue**; never re-decompose for an issue. </rule>
<rule> A revert, restore, copy, or keep → a mechanical rework with a `Source`. </rule>
<rule> Any investigation starts at **triage-issue** — answer from the record and read a bounded file yourself; dispatch when it spans areas or needs isolation. </rule>
<rule> An ADR change or **code-analyst** revision → **handle-adr-change**; never dispatch on a stale decision. </rule>
<rule> An ADR option needs proof → **define-poc-scope**. </rule>
<rule> A POC reaches **poc-ready** → never evaluate; wait for the user's recorded **adopted** / **rejected**. </rule>
</rules>
