# Scope-Map Guide

Full model for `scope.md` — the accepted request it records, its status model, and its transitions. Backs the **scope-map** knowledge entry and the status updates in **define-spike-scope**, **continue-prior-spike**, and **sync-update-artifacts**.

## Status model

| Status | Meaning | Stored / Derived |
|---|---|---|
| Problem `investigating` | No ADR yet | Stored (ground truth) |
| Problem `deciding` | ADR drafted, option awaiting user confirmation | Stored |
| Problem `done` | ADR + user-confirmed option | Stored |
| Area `preparing` | Findings pair not compiled | Derived |
| Area `spiking` | Findings compiled, ≥1 problem not `done` | Derived |
| Area `done` | All problems `done` | Derived |

Area status is derived from its problems + findings-pair link — never stored separately.

## Scope vs delivery index

`scope.md` tracks **spike areas/problems** only. Delivery features, cells, and status live in `deliveries/<epic>/index.md`. The two decompositions are not 1:1 and their statuses are never mirrored. Map: **[artifact-map.md](artifact-map.md)**.

## Transitions

| From | Event | To |
|---|---|---|
| Area `preparing` | Findings pair saved | Area `spiking` |
| Problem `investigating` | ADR saved | Problem `deciding` |
| Problem `deciding` | User confirms option | Problem `done` |
| Area `spiking` | All problems `done` | Area `done` |
| Problem `done` | New evidence / changed decision | Problem `deciding` |

## Scope document

`scope.md` records the **accepted request**, never the acceptance dialogue. The gate state, the restatement, the inference list, the questions asked, and what each round settled stay in the session — this skill takes `clarify-request`'s **acceptance-record** in the session, not in the artifact. Only the settled outcome is persisted, stated as fact:

```
# Spike Scope: <name>
**Artifact root:** <absolute path>

**Goal:** <the decision this spike settles, and what completion looks like — one sentence>

## Accepted request
- **Boundaries:** in <…> · out <…>
- **Constraints:** <binding condition every decision must respect>
- **Done criteria:** <observable test that closes the spike>

## Accepted assumptions
- A1 — Assumption (user-accepted, unverified): <premise> — moves <split | driver | done criteria>

## Area: <name>
**Findings**: docs/findings-<area>.md + docs/evidence-<area>.md
- `investigating` How to …? → (no ADR)

## Cross-area constraints
- <one line per constraint one area's decision puts on another>

## Next actions
- <one bounded implementation need and why>

## In-flight units (recovery)
- _(none)_ | <unit · stage · verification round · open challenges>
```

Nothing else from the gate: no `Confirmed inputs`, no restatement, no question log, no dated or per-round block. A delta rewrites these sections in place.

Findings, ADRs, and the solution doc are generated from these settled statements — goal, boundaries, constraints, done criteria, drivers, premises — never from the transcript that produced them. A brief that carries "what the user said in round 1" hands the sub-agent the dialogue instead of the request.

## Accepted assumptions

The section holds only **scope-owned premises**: an unverified statement the accepted request rests on that the spike cannot settle from code or artifacts.

- The inference list is the gate's evidence and lives in the session: an `ACCEPTED-WITH-ASSUMPTIONS` result with no inferences did not run the gate; `ACCEPTED` legitimately carries none.
- An assumption is admitted only per `clarify-request`'s **assumption-admission**: not obtainable from code or artifacts, decision-relevant, user-held or safely defaulted. A code fact is an investigation target — a Gap in the evidence doc, never a line here.
- **Scope-owned only** — a line earns its place when changing it moves the area/problem split, a problem's driver or option set, or the done criteria. Its trailing clause names that row, never a vague "decision".
- **Scope, not the work** — the section is a premise set, never a step log, request log, or home for one option's rationale:

| Written as an assumption | What it is | Where it belongs |
|---|---|---|
| "intake delegates the decision, so the ADR is recorded `accepted`" | recording convention | nowhere — the status model already states it |
| "the user also asked this round for …" | request record | rewrite the affected boundary or problem in place |
| "a coarse deny gate matches user intent" · "`$HOME` is the normal case" | an option's rationale or risk | that ADR (Consequences / Risks) |
| "the figure is what production does" | a claim evidence can settle | a Gap in the evidence doc |

- **One section, re-derived** — a single `## Accepted assumptions` with stable `A<n>` IDs, rewritten or deleted in place; never a per-round block, a dated heading, or a second list. A set that only grows is a log, not a scope.
- **Removal test on every write** — deleting the line must change the split, a driver, or the done criteria; otherwise delete it. Prune assumptions the user settled, evidence verified, or no ADR relies on.
- Re-open an assumption only when evidence contradicts it; rewrite the line in place when the user decides.
- Never promote an assumption to fact without evidence — cite the evidence doc line instead.

## Next actions

A spike never implements. Record each discovered implementation need as one line under `## Next actions` — what must change and why. Never a plan, feature breakdown, or delivery status; `orchestrate-feature-delivery` turns a line into work when the user starts delivery.

## Validation (on save)

- A `done` problem has its ADR present.
- An area is never `done` with an open problem.
- The accepted request (goal, boundaries, constraints, done criteria) is recorded before any area; no gate state, restatement, inference list, question log, or per-round answer appears in `scope.md`.
- Every `## Accepted assumptions` line names the row it can move (split, driver, or done criteria), is not obtainable from code or artifacts, and survives the removal test; a line recording a step, a request, or one option's rationale is a defect.
- Every `## Next actions` line is one bounded implementation need — never a plan, feature breakdown, or status.

## In-flight units (recovery)

Statuses track **saved artifacts**, not in-flight dispatches. When a spike pauses mid-unit, record a one-line in-flight note in `scope.md` — unit (area / problem), stage (`investigating` / `verifying` / `re-investigating`), verification round, and open challenges. Clear it when the unit's artifact is saved. On resume, read it first so the verification loop continues instead of re-dispatching a completed unit.

## Usage

- **define-spike-scope**: record the accepted request (goal, boundaries, constraints, done criteria) and the scope-owned premises, then each area (no stored status — it derives `preparing` until its pair link exists) with its problems (`investigating`); start `## Next actions` empty.
- **continue-prior-spike**: read statuses to surface open problems; update problem statuses and re-derive the assumption set in place as each step completes.
- **sync-update-artifacts**: a changed decision reopens its problem to `deciding`.
