# Orchestrator Handoff and Charter Scope

Used by **orchestrator-handoff** and the `context.md` writes in **track-plan** and **commit-step**.

## Which sections this skill owns

`context.md` is the cell's charter. The planner owns Why, Must hold, Unknowns, Done means, and Pointers; execution owns three sections only:

| Section | Rule |
|---|---|
| `## Execution` | Latest round only — overwritten, never appended |
| `## Open concerns` | Persistent, ≤5, deleted when resolved |
| `## State` | Current position, rewritten in place |

Never edit a planner-owned section; report a needed change instead. Never write a log — git and the PR are the history. Target 40–60 lines, ceiling 8,000 chars / 120 lines.

**One writer at a time**: the planner never amends a plan while its executor runs — amendments happen at a dispatch boundary; the executor never edits a planner-owned section, including `## Reworks`.

## Execution handoff

Written into `## Execution` when the plan runs inside a dispatched agent:

```
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Range:  <base7>..<head7>   (base = branch point on first run, previous head for a rework)
PR:     <reference | none>
Gate:   build=0 · test=<N> passed · lint=0   (or the ratified waiver)
Self-check: clean | fixed:<n>   (never a review-code pass when a gate follows)
Needs:  <amendment request, only when NEEDS_CONTEXT>
```

- Record the actual range; drift from the plan is not a failure.
- Deferred concerns belong in `## Open concerns`, never in the handoff.
- A POC's MR is the user's evaluation vehicle; merging waits for their decision.
- Never restate the charter, the plan's steps, or the execution log.
