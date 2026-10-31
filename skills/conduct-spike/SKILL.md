---
name: conduct-spike
description: Conduct spike investigations producing ADRs, findings, and solution docs. Use when clarifying, challenging, scoping, investigating, evaluating, authoring ADRs, formalizing findings, continuing a spike, or syncing updates.
---

<when-to-use-this-skill>
- Clarify or challenge an ambiguous spike request before accepting it, and re-challenge it when evidence contradicts the goal
- Conduct a spike investigation — research, evaluate, and compare approaches before committing
- Produce ADRs (one per problem, grouped by area) and a consolidated solution document
- Discuss an ADR whose outcome depends on unverified assumptions, unknown feasibility, or missing evidence
- Understand the current implementation as an investigation area before deciding
- Break a large technical problem into areas, each holding its decision problems ("How to …")
- Formalize pre-existing investigation findings into ADRs and a solution document
- Continue a previous spike into areas not fully resolved
- Re-investigate a decided ADR after implementation revealed a problem (focused rework spike)
- Sync findings docs, ADR, and solution doc on new evidence or a changed decision
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike reduces uncertainty via research and analysis; its output is **documented decisions, not production code**:

| Artifact | Role |
|---|---|
| **Findings Docs** (per area) | A publishable human doc (question-style explanation) + an evidence doc (ledger, `file:line`, confidence, searched-negatives) |
| **ADRs** | One per problem — a "How to …" decision — tagged with its area |
| **1 Solution Document** | Target-state architecture (C4, API contracts, RAID, RACI) — decision-only; ADRs mirrored into canonical sections |
</spike-definition>

<spike-artifact-layout>
One folder per spike — `spikes/<spike-name>/` with `scope.md`, `adrs/adr-<area>-<NN>-<problem>.md`, `solution.md`, `docs/findings-<area>.md` + `docs/evidence-<area>.md`. `spikes/` anchors the write boundary. Unnamed root → `resolve-artifact-location`; record `Artifact root:` atop `scope.md`.
</spike-artifact-layout>

<write-boundary>
Writes are confined to the spike folder (`**/spikes/**`) — never code, config, tests, or files outside it; never build POCs (`orchestrate-feature-delivery` delivers them). Run the boundary check after every write: **reference/write-boundary-guide.md**.
</write-boundary>

<scope-acceptance-gate>
No `scope.md` and no findings compilation until the request passes `clarify-request`'s intake gate — on **every** entry path: new, continued, user-supplied, uncertainty. The gate returns an acceptance record: restatement, itemized inferences, gate state. Nothing inferred → `ACCEPTED`; anything inferred → show the list and ask before decomposing. Record each default under `## Accepted assumptions` as `Assumption (user-accepted, unverified)`. It replaces the scope confirmation — never a second checkpoint. Procedure: **reference/define-spike-scope-procedure.md**.
</scope-acceptance-gate>

<scope-map>
The spike's **area → problem map** and status dashboard. Each problem maps to one ADR with its `Area:` tag; `scope.md` groups by area, `solution.md` mirrors decisions into canonical sections. Record at **define-spike-scope**; edit at **continue-prior-spike**.
</scope-map>

<scope-map-status>
Problem (stored): `investigating` → `deciding` → `done`; area (derived): `preparing` → `spiking` → `done`. A `done` problem has its ADR; an area is never `done` with an open problem; new evidence reopens `done` → `deciding`. Model: **reference/scope-map-guide.md**.
</scope-map-status>

<inappropriate-scenarios>
Do NOT use for quick answers, already-decided implementation work, trivial scope, immediate POC builds, or plain ADR drafting / solution-doc writing / code investigation — `draft-adr`, `write-solution-doc`, `investigate-code` own those.
</inappropriate-scenarios>

<findings-document>
The spike's findings pair (via `document-findings`): a human doc plus an evidence doc holding the ledger, claim IDs, and confidence. One pair per area. Guide: **reference/findings-document-guide.md**.
</findings-document>

<continuation-mode>
Another round seeded with prior artifacts: read `scope.md` for open work, gate the delta, run **revise-in-place**, then **sync-update-artifacts**.
</continuation-mode>

<greenfield-scenarios>
No existing implementation: research approaches, comparables, constraints.
</greenfield-scenarios>

<multi-agent-orchestration>
Dispatch every spike unit — including a single-task spike — to sub-agents. Details: **reference/multi-agent-orchestration.md**; model routing, waits, fallback: **reference/dispatch-discipline.md**.
</multi-agent-orchestration>

<sub-agent-verification>
Depth scales with blast radius: one independent verifier pass for evidence, a fidelity check against the verified ledger for synthesis, the full loop only for load-bearing ADR decisions. Cap 2 rounds; tag residual uncertainty. Rules: **reference/multi-agent-orchestration.md**.
</sub-agent-verification>

<problem-decomposition-guide>
Decompose into **areas** (shared-subject groupings, target 2–5 — one is valid), each holding **problems** ("How to …?" decisions, target 1–3; one ADR each). >5 areas or >~8 problems → narrow or split. Rubric: **reference/decomposition-rubric.md**.
</problem-decomposition-guide>

<adr-uncertainty-signals>
Suggest a spike when the decision hinges on what reasoning alone cannot settle: **unverified assumption**, **unknown feasibility**, **missing measurement**, **undecidable comparison**, **uninvestigated dependency**, **reviewer disagreement**.
</adr-uncertainty-signals>

<professional-doc-authoring>
ADRs, findings docs, and the solution doc are always written by `draft-adr`, `document-findings`, `write-solution-doc` — never hand-edited. Option tech details come from **detail-options-tech**, grounded in the ledger.
</professional-doc-authoring>

<artifact-maintenance-doctrine>
Chain **Findings Docs → ADRs → Solution Doc** stays at the latest state: rewrite changed sections in place, delete superseded content (git is history), no version markers or changelogs. Notes live only in evidence docs and conversation. Propagation stops at the first unaffected artifact. Guide: **reference/artifact-maintenance-guide.md**.
</artifact-maintenance-doctrine>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Full end-to-end spike (scope → solution doc) | End-to-end walkthrough | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Starting from pre-existing findings | Workflow without re-investigation | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Watching statuses move through a spike | Status lifecycle walkthrough | [examples/scope-status-lifecycle.md](examples/scope-status-lifecycle.md) |
| Continuing a spike (walkthrough) | Continuation walkthrough (revise-in-place) | [examples/continue-prior-spike.md](examples/continue-prior-spike.md) |
| Heavy multi-area spike with parallel sub-agents | Parallel dispatch walkthrough | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| ADR discussion hinging on unverified assumptions | Uncertainty-spike suggestion example | [examples/adr-uncertainty-spike-suggestion.md](examples/adr-uncertainty-spike-suggestion.md) |
| Fact/decision change propagated through artifacts | Sync walkthrough | [examples/sync-update-across-artifacts.md](examples/sync-update-across-artifacts.md) |
| Placing artifacts into the spike folder | Layout example | [examples/spike-artifact-layout.md](examples/spike-artifact-layout.md) |
| Handing artifacts to delivery, or deciding where a fact belongs | Two-plane map, handoff contract, edit ownership, change routing | [reference/artifact-map.md](reference/artifact-map.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<run-spike-workflow>
1. Apply the spike workflow per **reference/run-spike-workflow-procedure.md** — define-spike-scope → investigate-per-area → compile-findings-doc → draft-problem-adrs → compile-solution-doc, pausing for user confirmation after each capability (skip a pause only if the user requests it).
</run-spike-workflow>

<continue-prior-spike>
1. Apply the continuation procedure per **reference/continue-prior-spike-procedure.md** — load prior artifacts, gate the scope delta per **scope-acceptance-gate**, run revise-in-place, sync downstream.
</continue-prior-spike>

<define-spike-scope>
1. Restate the request as given and itemize every inference it left open — ask nothing yet.
2. Apply **scope-acceptance-gate** — show the inference list and ask before decomposing; stop while `BLOCKED`.
3. Apply the scope-definition procedure per **reference/define-spike-scope-procedure.md** — clarify goal, decompose, record `scope.md`, validate, note greenfield.
</define-spike-scope>

<investigate-per-area>
1. Apply the investigation procedure per **reference/investigate-per-area-procedure.md** — dispatch, brief, verify, hand off evidence maps.
2. When an evidence map contradicts an accepted goal or constraint, re-challenge the affected claims via `clarify-request`'s **re-challenge-the-ask** and rewrite `scope.md`.
</investigate-per-area>

<draft-problem-adrs>
1. Apply the ADR-drafting procedure per **reference/draft-problem-adrs-procedure.md**: dispatch → evaluate + draft via `draft-adr` → verify → sync findings gaps → save → ask → validate.
</draft-problem-adrs>

<compile-solution-doc>
1. Apply the solution-doc compilation procedure per **reference/solution-doc-compilation.md**: dispatch → verify → save → validate → present.
</compile-solution-doc>

<compile-findings-doc>
1. Gate the supplied material per **scope-acceptance-gate** before compiling — user-provided notes are a request, not a settled scope.
2. Apply the findings-doc compilation procedure per **reference/findings-doc-compilation.md** — one per area: dispatch → verify → validate → save (mark each area `spiking` per **scope-map-status**).
</compile-findings-doc>

<sync-update-artifacts>
1. Apply the sync procedure per **reference/artifact-maintenance-guide.md**: capture the change and origin, trace propagation, apply at the origin via the owning skill, run the no-note scan, propagate downstream, validate.
</sync-update-artifacts>

<suggest-spike-on-adr-uncertainty>
1. Detect uncertainty signals via **adr-uncertainty-signals**.
2. Offer: "Would you like to spike this before finalizing the ADR?" — never start without explicit confirmation, then gate the scope per **scope-acceptance-gate**.
3. Apply the procedure per **reference/suggest-spike-on-adr-uncertainty-procedure.md**.
</suggest-spike-on-adr-uncertainty>

</capabilities>

<rules>
<rule>When the user initiates a spike investigation from scratch, apply **run-spike-workflow**.</rule>
<rule>Before `scope.md` is written, a continuation starts, user-supplied material is compiled, or an uncertainty spike begins, apply **scope-acceptance-gate** — accept only `ACCEPTED` or `ACCEPTED-WITH-ASSUMPTIONS`, and only after the inference list was shown.</rule>
<rule>When the user supplies pre-existing investigation material, apply **compile-findings-doc** directly, skipping **investigate-per-area** — after the gate.</rule>
<rule>When the user resumes a prior spike or re-investigates a decided ADR, apply **continue-prior-spike**.</rule>
<rule>When a fact or decision changes after spike artifacts exist, or an area question is answered, apply **sync-update-artifacts**.</rule>
<rule>When ADR discussion hinges on unverified assumptions or missing evidence, apply **suggest-spike-on-adr-uncertainty** before finalizing the ADR.</rule>
<rule>When the artifact base root is unresolved, apply `resolve-artifact-location` before the scope map is saved.</rule>
<rule>When any write capability completes, run the own-writes boundary check per **reference/write-boundary-guide.md**; stop and report on newly written out-of-folder paths.</rule>
</rules>
