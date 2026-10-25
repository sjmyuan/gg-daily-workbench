# Rework Plan Convention

Used by **rework-plan-convention**, **export-plan**, and **amend-plan**.

A rework (triggered by **orchestrate-feature-delivery**'s **handle-post-implementation-issue**) is
a new sibling file `rework-<date>.md` in the feature folder — `plan.md` is the frozen original and
is never modified.

- Applies only when executed or delivered behavior must change; pending-step defects are amended
  in place via **amend-plan**.
- Opens with `# Rework <date> — <trigger>`, a `**Mode**`/`**Cell**` line, a `**Branch**` line, the
  ADR focus, and the inherited `**Gate**` line, then its own **Scope Boundary**, **Done means**,
  and six-field delta steps.
- Carries only the delta — never restates the original plan or the charter; inherits `context.md`
  **Must hold** / **Pointers** by reference and never creates a second `context.md`.
- Inherits and tightens the original **Scope Boundary** to the governing ADR decision.
- Refuses and asks only on a material change: original **Must not change** behavior, a protected
  zone, or reopening another ADR (likely a new feature cell).
- Runs on its own branch (see **plan-prerequisites**).
- Registers a row in the feature's `## Reworks` manifest in `context.md` (date, mode, cell,
  trigger, file, status) so resume finds the active file.

Worked example: [examples/rework-scope-boundary.md](../examples/rework-scope-boundary.md).
