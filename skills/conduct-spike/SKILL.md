---
name: conduct-spike
description: Run spike investigations that turn uncertainty into findings pairs, ADRs, and a solution document. Use when scoping, clarifying, challenging, investigating, deciding, formalizing, re-investigating, continuing, or syncing a spike.
---

<when-to-use-this-skill>
- Clarify or challenge an ambiguous spike request before accepting it, and re-challenge it when evidence contradicts the goal
- Conduct a spike investigation that reduces uncertainty and produces ADRs plus a solution document
- Scope a large problem into areas, each holding its decision problems ("How to …"), starting from the current implementation
- Formalize pre-existing investigation findings, or continue a previous spike into areas not fully resolved
- Discuss an ADR whose outcome depends on unverified assumptions, unknown feasibility, or missing evidence
- Re-investigate a decided ADR after implementation revealed a problem, and sync findings, ADR, and solution doc on new evidence
- Do NOT load for quick answers, decided implementation work, trivial scope, POC builds, or plain ADR drafting, solution-doc writing, or code investigation
</when-to-use-this-skill>
<knowledge>

<spike-definition>
A spike reduces uncertainty via research and analysis; its output is **documented decisions, not production code**:

| Artifact | Role |
|---|---|
| **Findings pair** (per area) | A publishable human doc plus an evidence doc — ledger, `file:line`, confidence, searched-negatives. Guide: **reference/findings-document-guide.md** |
| **ADRs** | One per problem — a "How to …" decision — tagged with its area |
| **1 Solution Document** | Target-state architecture (C4, API contracts, RAID, RACI) — decision-only; ADRs mirrored into canonical sections |
</spike-definition>
<spike-artifact-layout>
`spikes/<spike-name>/` holds `scope.md`, `adrs/adr-<area>-<NN>-<problem>.md`, `solution.md`, and the pair `docs/findings-<area>.md` + `docs/evidence-<area>.md`.
`spikes/` anchors the write boundary. Unresolved root → `resolve-artifact-location`.
</spike-artifact-layout>
<write-boundary>
Writes stay inside `**/spikes/**` — never code, config, tests, or outside files; never build POCs (`orchestrate-feature-delivery` delivers them).
Check after every write: **reference/write-boundary-guide.md**.
</write-boundary>
<scope-acceptance-gate>
No `scope.md` or findings compilation until `clarify-request`'s intake gate passes — on **every** entry path: new, continued, user-supplied, uncertainty.
Apply its **intake-gate** and **assumption-admission**; do not restate them.
The gate is the only scope-acceptance pause.
Fold the proposed area/problem split and each problem's driver question into its one confirmation, then record the outcome in `scope.md`.
User-supplied notes that arrive after acceptance are gated before they are compiled. Procedure: **reference/define-spike-scope-procedure.md**.
</scope-acceptance-gate>
<scope-map>
The spike's **area → problem map** and status in `scope.md`; each problem maps to one ADR with its `Area:` tag.
Problem (stored): `investigating` → `deciding` → `done`.
Area (derived, never stored): `preparing` → `spiking` → `done`.
A `done` problem has its ADR; an area is never `done` with an open problem. Model: **reference/scope-map-guide.md**.
</scope-map>
<greenfield-scenarios>
No existing implementation: research approaches, comparables, constraints.
</greenfield-scenarios>
<multi-agent-orchestration>
One `spike-area-analyst` session per area writes the pair and the ADRs and returns once; dispatch the solution doc separately.
Verify each return on an independent seat — never the producing session — by blast radius, cap 2 rounds, tag residual uncertainty.
Never split an area's phases across agents.
Pattern: **reference/multi-agent-orchestration.md**; brief: **reference/area-analyst-brief.md**.
Resume and receipts: **reference/dispatch-briefs.md**; model routing: **reference/dispatch-discipline.md**.
</multi-agent-orchestration>
<problem-decomposition-guide>
Decompose into **areas** (shared-subject groupings), each holding **problems** — "How to …?" decisions, one ADR each.
Narrow or split an oversized spike. Rubric: **reference/decomposition-rubric.md**.
</problem-decomposition-guide>
<adr-uncertainty-signals>
Suggest a spike when the decision hinges on what reasoning alone cannot settle:
- **unverified assumption**
- **unknown feasibility**
- **missing measurement**
- **undecidable comparison**
- **uninvestigated dependency**
- **reviewer disagreement**
</adr-uncertainty-signals>
<artifact-maintenance-doctrine>
Chain **Findings Docs → ADRs → Solution Doc** stays current: findings pairs update in place; ADRs and the solution doc are rewritten to the latest decision.
No version markers; notes live only in evidence docs and conversation.
Propagation stops at the first unaffected artifact. Guide: **reference/artifact-maintenance-guide.md**.
</artifact-maintenance-doctrine>
<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Full end-to-end spike | Walkthrough | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Starting from pre-existing findings | No re-investigation | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Status transitions | Status lifecycle | [examples/scope-status-lifecycle.md](examples/scope-status-lifecycle.md) |
| Continuing a spike | Revise in place | [examples/continue-prior-spike.md](examples/continue-prior-spike.md) |
| Multi-area parallel spike | Parallel dispatch | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| ADR discussion on unverified assumptions | Spike suggestion example | [examples/adr-uncertainty-spike-suggestion.md](examples/adr-uncertainty-spike-suggestion.md) |
| Fact/decision change propagated through artifacts | Sync walkthrough | [examples/sync-update-across-artifacts.md](examples/sync-update-across-artifacts.md) |
| Handing artifacts to delivery, or placing a fact | Two-plane map, handoff, ownership, routing | [reference/artifact-map.md](reference/artifact-map.md) |
</context-loading-guide>
</knowledge>
<capabilities>

<run-spike-workflow>
**Objective**: Run a spike from an unaccepted request to a consistent, decision-only artifact bundle.
1. Apply the workflow per **reference/run-spike-workflow-procedure.md**.
2. Honor its four user checkpoints — scope gate, findings confirmation, ADR review, solution-doc approval — and never pause between an area session's phases.
</run-spike-workflow>
<continue-prior-spike>
**Objective**: Add, adjust, or remove scope on a prior spike without re-investigating settled work.
1. Apply the continuation procedure per **reference/continue-prior-spike-procedure.md** — gate the delta, revise in place, sync downstream.
</continue-prior-spike>
<define-spike-scope>
**Objective**: Turn the request into an accepted, recorded area → problem map.
1. Apply the scope-definition procedure per **reference/define-spike-scope-procedure.md** — one gate confirmation carrying the inference list, the proposed split, and each problem's driver question.
</define-spike-scope>
<dispatch-area-session>
**Objective**: Produce each area's verified findings pair and ADRs.
1. Apply the area-session procedure per **reference/dispatch-area-session-procedure.md**.
2. Dispatch the full brief (gate, drivers, known locations), verify the single return, then present the pair and ADRs for review.
</dispatch-area-session>
<confirm-problem-adrs>
**Objective**: Confirm each area's ADRs and record the accepted decision.
1. Apply the ADR confirmation procedure per **reference/confirm-problem-adrs-procedure.md** — confirm or revise the returned ADRs, then validate each against the ADR checklist.
</confirm-problem-adrs>
<compile-solution-doc>
**Objective**: Consolidate the accepted ADRs into the solution document.
1. Apply the solution-doc compilation procedure per **reference/solution-doc-compilation.md** — dispatch, verify, save, validate, present.
</compile-solution-doc>
<compile-findings-doc>
**Objective**: Confirm each area's findings pair before it grounds a decision.
1. Apply the findings-doc compilation procedure per **reference/findings-doc-compilation.md** — one pair per area, validated, confirmed, and linked in `scope.md`.
</compile-findings-doc>
<sync-update-artifacts>
**Objective**: Propagate a changed fact or decision through every affected artifact.
1. Apply the sync procedure per **reference/artifact-maintenance-guide.md** — it owns the propagation matrix, the no-note scan, and the consistency checklist.
</sync-update-artifacts>
<suggest-spike-on-adr-uncertainty>
**Objective**: Offer a focused spike when an ADR rests on unverified evidence.
1. Detect the signals in **adr-uncertainty-signals**, name the uncertainty, and offer the spike — never start without the user's confirmation.
2. Apply the procedure per **reference/suggest-spike-on-adr-uncertainty-procedure.md**.
</suggest-spike-on-adr-uncertainty>
</capabilities>
<rules>
<rule>When the user initiates a spike investigation from scratch, apply **run-spike-workflow**.</rule>
<rule>Dispatch one `spike-area-analyst` session per area — never split its phases — and verify its single return on an independent seat: not the producer, not a bare evidence map.</rule>
<rule>Before `scope.md` is written, a continuation starts, user-supplied notes are compiled, or an uncertainty spike begins, apply **scope-acceptance-gate**.</rule>
<rule>When the gate runs, accept only `ACCEPTED` or `ACCEPTED-WITH-ASSUMPTIONS`, and only after the inference list was shown.</rule>
<rule>When the user supplies pre-existing investigation material, apply **compile-findings-doc** directly, skipping **dispatch-area-session** — after the gate.</rule>
<rule>When the user resumes a prior spike or re-investigates a decided ADR, apply **continue-prior-spike**.</rule>
<rule>When a fact or decision changes after spike artifacts exist, or an area question is answered, apply **sync-update-artifacts**.</rule>
<rule>When an ADR hinges on unverified assumptions or missing evidence, apply **suggest-spike-on-adr-uncertainty** before finalizing it.</rule>
<rule>When an ADR, findings doc, or solution doc must change, apply its owning skill (`draft-adr`, `document-findings`, `write-solution-doc`) — never hand-edit.</rule>
<rule>When the artifact base root is unresolved, apply `resolve-artifact-location` before the scope map is saved.</rule>
<rule>When any write capability completes, run the own-writes boundary check per **reference/write-boundary-guide.md**; stop and report on newly written out-of-folder paths.</rule>
</rules>
