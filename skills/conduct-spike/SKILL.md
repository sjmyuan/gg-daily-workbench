---
name: conduct-spike
description: Run decision-first spikes that investigate just enough and produce template-conformant ADRs passing an acceptance gate, with investigation notes and architecture docs only for a named consumer. Use when running, scoping, continuing, or re-investigating a spike, or deciding a question that reasoning alone cannot settle.
---

<when-to-use-this-skill>
- Run a spike when reasoning alone cannot settle the question — feasibility, a measurement, a comparison, a dependency
- Scope a spike into areas holding its decision problems ("How to …") before investigating
- Decide a one-off technical question that needs code evidence — the fast path, one ADR
- Continue a prior spike into unresolved areas, or turn pre-existing investigation notes into ADRs
- Re-investigate a decided ADR after implementation revealed a problem
- Produce investigation notes or an architecture overview that has a named consumer
- Do NOT load for one code fact (`investigate-code`) or an ADR from settled evidence (`draft-adr`)
- Do NOT load to build a POC or deliver a feature (`orchestrate-feature-delivery`)
</when-to-use-this-skill>
<knowledge>

<spike-definition>
A spike settles decisions; documents are a by-product. Investigate only until the decision is credible, then stop.

| Artifact | Required | Rule |
|---|---|---|
| ADR per problem | Always | Passes **adr-acceptance**; the primary output |
| `scope.md` | When ≥2 problems or a continuation is likely | The fast path keeps the scope in the ADR's Context |
| Investigation notes | Optional | One human doc, only when evidence must outlive the session or a consumer asked |
| Architecture overview (`solution.md`) | Optional | Only for a named consumer; references ADRs, never mirrors them |

Never write production code, config, tests, or a POC — a spike ends at decisions.
</spike-definition>
<spike-layout>
`<base>/spikes/<spike-name>/` holds `scope.md`, `adrs/`, optional `notes-<area>.md` and `solution.md`.
Writes stay inside `**/spikes/**`; unresolved root → `resolve-artifact-location`. Detail: **reference/consumer-artifacts.md**.
</spike-layout>
<adr-contract>
Every ADR follows `draft-adr`'s template and passes the **adr-acceptance** gate before presentation or adoption.
Gate essentials: template order · `Option N` labels reused · `HC n`/`SP n` drivers with metric and threshold.
Also: every option against every driver · decision-flipping claims cited or **unverified** · the ADR stands alone.
A short ADR that passes beats a long one that does not. Checks: **reference/adr-acceptance.md**.
</adr-contract>
<evidence-sufficiency>
Enough evidence: every claim that could flip the chosen option is verified against a primary source.

- Cite `file:line` at the claim; no separate ledger is required.
- Confidence is a tag, not a document: **verified** / **inferred** / **unverified** with what would settle it.
- Verify only what the decision turns on; never present inference as fact.
Detail and anti-patterns: **reference/evidence-sufficiency.md**.
</evidence-sufficiency>
<investigation-notes>
Optional, one `notes-<area>.md`, readable top-down: what exists, entry points, flows, constraints.
Claims cite `file:line` inline; tag confidence only where it flips a decision; never a claim ledger or paired doc.
Notes never restate a decision. Detail: **reference/consumer-artifacts.md**.
</investigation-notes>
<scale-routing>
Default: run in-session. Dispatch only when areas ≥2, or one area's reading would crowd the orchestrator's context.

- One area session investigates, writes its ADRs, and returns once; never split its phases across agents.
- Verify a return on an independent seat only when the decision is cross-area or load-bearing.
- Never dispatch scope definition or the ADR review.
Thresholds and brief: **reference/scale-and-dispatch.md**.
</scale-routing>
<spike-lifecycle>
Propose → scope gate → decide → ADR review → optional artifacts → handoff.
Problem `open` → `decided`; area status is derived, never stored; one review per ADR set.
Scope model: **reference/spike-scope-guide.md**.
</spike-lifecycle>
<review-pacing>
The ADR set is the one artifact review: each chosen option, its winning drivers, its cost, what stays unverified.
Apply `brief-human-reviewer` when the set is large or code-dense.
</review-pacing>
<adr-uncertainty-signals>
Offer a spike when a decision hinges on what reasoning alone cannot settle:
- **unverified assumption** · **unknown feasibility** · **missing measurement**
- **undecidable comparison** · **uninvestigated dependency** · **reviewer disagreement**
</adr-uncertainty-signals>
<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| The whole skill on one fast-path decision, with a gate-passing ADR | Single-decision walkthrough and decision spine | [examples/single-decision-spike.md](examples/single-decision-spike.md) |
| Two or more areas, or a decision to dispatch | Dispatch, area return, ADR set, review | [examples/multi-area-spike.md](examples/multi-area-spike.md) |
| Resume, pre-existing notes, or a reversal | Re-investigate and rewrite an adopted ADR | [examples/continue-spike.md](examples/continue-spike.md) |
| An ADR rests on an unverified claim | Offer, scope, and decide a bounded spike | [examples/suggest-spike.md](examples/suggest-spike.md) |
| Judging an ADR ready to present or adopt | The acceptance gate and its failure modes | [reference/adr-acceptance.md](reference/adr-acceptance.md) |
| Deciding how much investigation is enough | Sufficiency test, confidence tags, verification depth | [reference/evidence-sufficiency.md](reference/evidence-sufficiency.md) |
| Scoping, decomposing, or continuing a spike | `scope.md` skeleton, area/problem split, statuses | [reference/spike-scope-guide.md](reference/spike-scope-guide.md) |
| Choosing in-session work or a dispatch | Thresholds, area brief, return contract | [reference/scale-and-dispatch.md](reference/scale-and-dispatch.md) |
| Someone asked for notes or an architecture overview | Consumer tests, notes shape, handoff map | [reference/consumer-artifacts.md](reference/consumer-artifacts.md) |
| An ADR review reaches the user | Route, prediction, self-check | `brief-human-reviewer` skill |
</context-loading-guide>
</knowledge>
<capabilities>

<define-spike-scope>
**Objective**: Get the question and its drivers accepted before any investigation; keep the fast path small.
1. Restate the question and its open inferences; propose `How to …?` problems, grouped into areas at ≥2.
2. Run `clarify-request`'s intake gate once: ≤3 questions plus each problem's drivers and metrics.
3. Record goal, boundaries, drivers, problems in `scope.md` or the ADR's Context; the transcript stays in the session.
**Gate**: the user accepts the question and drivers; a problem without a driver is not ready to investigate.
</define-spike-scope>
<decide-spike-problems>
**Objective**: Settle each problem with an ADR that passes the gate.
1. Investigate to sufficiency — trace only what the options need and verify what could flip the choice.
2. Draft one ADR per problem with `draft-adr` from the accepted drivers; never infer a driver.
3. Each option gets a target-state diagram; the winner's changes carry `file:line`, diff, confidence, verify, rollback.
4. Run **adr-acceptance** on each ADR; fix the ADR, not the checklist.
5. Return the ADR set with its gate result, each unverified claim, and the options the evidence ruled out.
**Gate**: every ADR passes **adr-acceptance**; an unverified decision-flipping claim blocks adoption unless the user accepts the risk.
</decide-spike-problems>
<accept-adrs>
**Objective**: Get the decisions reviewed and adopted.
1. Present the ADR set per **review-pacing**.
2. On feedback, revise the ADR in place and re-run the gate on the changed sections only.
3. Set `Status: adopt`, mark each problem `decided`, and record an implementation need as one handoff line.
**Gate**: each ADR is accepted or explicitly waived, and every adopted ADR passes the gate.
</accept-adrs>
<continue-spike>
**Objective**: Add, re-investigate, or reverse decisions without redoing settled work.
1. Load the existing ADRs and notes; treat `verified` claims and adopted decisions as settled.
2. Re-investigate only the delta; re-open the scope gate only when the question itself changes.
3. Rewrite the ADR in template form with options re-evaluated against the new evidence; re-run **adr-acceptance**.
4. Update each artifact that already cites the changed ADR; produce a new one only if a consumer now exists.
**Gate**: changed ADRs pass the gate; no settled claim is re-verified without new evidence.
</continue-spike>
<produce-optional-artifact>
**Objective**: Produce notes or an architecture overview only when a consumer needs them.
1. Name the consumer and what they will do with the artifact. No consumer → produce nothing, and say so.
2. Notes → **investigation-notes** shape. Overview → `write-solution-doc`, citing decisions, never mirroring them.
3. Link the artifact from the handoff; never let it become a second decision record.
**Gate**: a named consumer exists, and no decision is restated as new content.
</produce-optional-artifact>
<suggest-spike>
**Objective**: Offer a focused spike when a decision rests on unverified evidence.
1. Detect a signal in **adr-uncertainty-signals**, name the uncertainty, offer the spike; never start unconfirmed.
2. Accepted → **define-spike-scope** with that uncertainty as the problem; declined → tag the claim **unverified**.
**Gate**: the user accepted or declined before the ADR is adopted.
</suggest-spike>
</capabilities>
<rules>
<rule>When reasoning cannot settle a question, run **define-spike-scope**, **decide-spike-problems**, **accept-adrs**.</rule>
<rule>Every ADR passes **reference/adr-acceptance.md** before presentation or adoption — never partial or abridged.</rule>
<rule>Before presenting any ADR set, apply **review-pacing**; the ADR review is the only artifact checkpoint.</rule>
<rule>Before notes or an overview, apply **produce-optional-artifact** — a named consumer or nothing.</rule>
<rule>When the user resumes, supplies notes, or a fact changes, apply **continue-spike**.</rule>
<rule>Dispatch only at areas ≥2 or heavy reading volume; never split an area's phases across agents.</rule>
<rule>When an ADR hinges on unverified evidence, apply **suggest-spike** before adopting it.</rule>
<rule>When an ADR must change, apply `draft-adr` — never hand-edit — and gate the result here.</rule>
<rule>Keep every write inside the spike folder per **spike-layout**; stop and report on any outside path.</rule>
<rule>When the artifact base root is unresolved, apply `resolve-artifact-location` before the first write.</rule>
</rules>
