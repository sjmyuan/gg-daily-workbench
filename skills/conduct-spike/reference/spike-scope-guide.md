# Spike Scope Guide

Loaded by **define-spike-scope** and **continue-spike**. Owns when `scope.md` exists, its skeleton, the area/problem split, and status vocabulary.

## When scope.md exists

| Situation | Record |
|---|---|
| One problem, one ADR, reversible decision | Nothing — scope lives in the ADR's `Context and Problem Statement` |
| ≥2 problems, or a continuation is likely | `scope.md` |
| User supplied pre-existing notes | `scope.md` only if the notes cover ≥2 problems; otherwise the ADR |

A single-decision spike that writes `scope.md` has paid for a file it never reads.

## Skeleton

```markdown
# <Spike name>

**Artifact root:** <path>/spikes/<spike-name>/

## Question

<One sentence: what must be decided, and what completion looks like.>

## Boundaries

- In: <modules, systems, time range>
- Out: <what this spike will not decide>

## Drivers

| # | Problem | Drivers | Measurement |
|---|---|---|---|
| P1 | How to <…>? | <driver> | <metric + threshold> |
| P2 | How to <…>? | <driver> | <metric + threshold> |

## Problems

| ID | Area | Problem | Status | ADR |
|---|---|---|---|---|
| P1 | <area> | How to <…>? | open | `adrs/adr-<area>-01-<problem>.md` |
| P2 | <area> | How to <…>? | open | — |
```

- One row per problem; the ADR column fills when the ADR is written.
- No gate transcript, inference list, or round history — those stay in the session.
- No area status: derive `done` when every problem in the area is `decided`.
- Line budget: 2 pages. Longer means the split is wrong, not that the text is thin.

## Problem naming

A problem is a decision question a person could answer with "we will do X because Y":

- Good: "How to keep webhook delivery durable across pod restarts?"
- Bad: "Investigate the webhook dispatcher" (task, not decision)
- Bad: "Should we use Kafka?" (solution-shaped; hides the driver)
- Bad: "Improve reliability" (no decision surface)

One problem → one ADR. Two problems that share an ADR have not been separated; two ADRs that answer one problem should be merged.

## Area grouping

Group problems by shared subject — a subsystem, a migration stage, a shared data store. Rules:

- 3–7 problems per area: fewer means the area is a problem, more means the area is really two.
- Problems in one area share evidence, not necessarily a decision.
- A cross-area constraint is named in both areas' ADRs; it never becomes its own area.
- A spike above ~12 problems is an epic: split it, spike the first tranche, deliver, then continue.

## Drivers at scope time

Collect each problem's drivers at the gate, not during the investigation. The ADR needs them and the analyst must never invent them.

- Each driver: metric, threshold, measurement. "≤ $400/month, invoiced" beats "cheap".
- Mark each `HC` (knock-out) or `SP` (preference) once its threshold is known; the ADR does the tagging if it is unclear at scope time.
- A problem with no driver is not ready — ask, or park it.

## Status vocabulary

| Unit | Values | Notes |
|---|---|---|
| Problem | `open` → `decided` | `decided` requires an ADR with `Status: adopt` |
| Area | derived: `open` / `done` | Never stored in `scope.md` |

No `investigating` / `deciding` stages: they describe activity, not state, and every artifact already shows whether work happened.

## Greenfield

No code to trace: research approaches and comparable systems instead of `file:line`.
Drivers still need measurements — published benchmarks, vendor limits, or a stated assumption with its risk.
Every external claim is cited by source; anything unverifiable is tagged **unverified**.

## Continuation

Re-open the scope only when the question changes (a new constraint, a reversed goal). A continuation that adds problems:

1. Add rows to `## Problems` with `open` status.
2. Keep settled rows and their ADRs untouched.
3. Re-run the gate only for the new rows' drivers.

When a fact invalidates a `decided` problem, set it back to `open`, and let **continue-spike** rewrite its ADR.
