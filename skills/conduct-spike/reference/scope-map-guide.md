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

`scope.md` owns the intake gate's outcome. Record the gate state once, then one line per accepted default:

```
Gate: ACCEPTED-WITH-ASSUMPTIONS

## Accepted assumptions
- A1 — Assumption (user-accepted, unverified): target is p95 first-token under 300ms
```

- One line per assumption: ID, the label, the assumed value.
- Re-open an assumption only when evidence contradicts it; rewrite the line in place when the user decides.
- Never promote an assumption to fact without evidence — cite the evidence doc line instead.

## Validation (on save)

- A `done` problem has its ADR present.
- An area is never `done` with an open problem.
- The gate state is recorded before any area is recorded.

## In-flight units (recovery)

Statuses track **saved artifacts**, not in-flight dispatches. When a spike pauses mid-unit, record a one-line in-flight note in `scope.md` — unit (area / problem), stage (`investigating` / `verifying` / `re-investigating`), verification round, and open challenges. Clear it when the unit's artifact is saved. On resume, read it first so the verification loop continues instead of re-dispatching a completed unit.

## Usage

- **define-spike-scope**: record the gate state and accepted assumptions, then the goal (1 sentence) and each area (`preparing`, empty findings-pair link) with its problems (`investigating`).
- **continue-prior-spike**: read statuses to surface open problems; update statuses as each step completes.
- **sync-update-artifacts**: a changed decision reopens its problem to `deciding`.
