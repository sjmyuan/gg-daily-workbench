# Rework Plan Convention

Used by **rework-plan-convention**, **export-plan**, and **amend-plan**.

A rework — an implemented or delivered cell needs a scoped change — is a sibling file in the feature folder; `plan.md` is the frozen original and is never modified.

| Mode | File | Lifecycle |
|---|---|---|
| **pre-merge** — cell **in-progress** | `rework.md` | One active file, overwritten when a new round starts; git keeps the previous round |
| **post-merge** — cell **done** | `rework-<date>.md` | One file per rework; same-day collision suffix `-2`, `-3` |

- Applies only when executed or delivered behavior must change; pending-step defects are amended
  in place via **amend-plan**.
- Opens with `# Rework <date> — <trigger>`, a `**Mode**`/`**Cell**` line, a `**Branch**` line, the
  inherited `**Test strategy**` line, the ADR focus, the inherited `**Gate**` line, and the inherited
  `**Autonomy**` line, then its own **Scope Boundary**, **Done means**, **Risk**, and six-field delta steps.
- Records `**Gate findings**:` as one line per unresolved finding with its `mechanical`/`design` label — the round's verdict must survive a session reset.
- Carries only the delta — never restates the original plan or the charter; inherits `context.md`
  **Must hold** / **Pointers** by reference and never creates a second `context.md`.
- Inherits and tightens the original **Scope Boundary** to the governing ADR decision.
- Refuses and asks only on a material change: original **Must not change** behavior, a protected
  zone, or reopening another ADR (likely a new feature cell).
- Runs on the cell's branch pre-merge; its own branch post-merge (see **plan-prerequisites**).
- Registers a row in the feature's `## Reworks` manifest in `context.md` (date, mode, cell,
  trigger, file, status) so resume finds the active file.

Worked example: [examples/rework-scope-boundary.md](../examples/rework-scope-boundary.md).
