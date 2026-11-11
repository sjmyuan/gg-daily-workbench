# Scope-Map Status Guide

Full status model for `scope.md` — backs the **scope-map** / **scope-map-status** knowledge entries and the status updates in **define-spike-scope**, **continue-prior-spike**, and **sync-update-artifacts**.

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

## Accepted assumptions

`scope.md` owns the intake gate's outcome. Record the gate state, the restatement, and the inference list once, then one line per **admitted** default:

```
Gate: ACCEPTED-WITH-ASSUMPTIONS
Restatement: reduce first-token latency on web checkout
Inferred: metric = first-token p95 · surface = web only · no queue in the path

## Accepted assumptions
- A1 — Assumption (user-accepted, unverified): target is p95 first-token under 300ms — changes the success criteria
```

- The inference list is the gate's evidence: a `scope.md` with a gate state but no inferences did not run the gate.
- An assumption is admitted only per `clarify-request`'s **assumption-admission**: not obtainable from code or artifacts, decision-relevant, user-held or safely defaulted. A code fact is an investigation target — a Gap in the evidence doc, never a line here.
- One line per assumption: ID, the label, the assumed value, and the decision it can change.
- **Removal test on every write** — deleting the line must change an ADR, the split, or the done criteria; otherwise delete it. Prune assumptions the user settled, evidence verified, or no ADR cites.
- Re-open an assumption only when evidence contradicts it; rewrite the line in place when the user decides.
- Never promote an assumption to fact without evidence — cite the evidence doc line instead.

## Validation (on save)

- A `done` problem has its ADR present.
- An area is never `done` with an open problem.
- The gate state, restatement, and inference list are recorded before any area is recorded.
- Every `## Accepted assumptions` line names the decision it can change; none is obtainable from code or artifacts; no line survives the removal test.

## In-flight units (recovery)

Statuses track **saved artifacts**, not in-flight dispatches. When a spike pauses mid-unit, record a one-line in-flight note in `scope.md` — unit (area / problem), stage (`investigating` / `verifying` / `re-investigating`), verification round, and open challenges. Clear it when the unit's artifact is saved. On resume, read it first so the verification loop continues instead of re-dispatching a completed unit.

## Usage

- **define-spike-scope**: record the gate state and admission-passing assumptions, then the goal (1 sentence) and each area (`preparing`, empty findings-pair link) with its problems (`investigating`).
- **continue-prior-spike**: read statuses to surface open problems; update statuses as each step completes.
- **sync-update-artifacts**: a changed decision reopens its problem to `deciding`.
