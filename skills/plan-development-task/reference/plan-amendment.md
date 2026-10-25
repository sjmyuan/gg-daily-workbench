# Plan Amendment

Used by **amend-plan**, **plan-file-format**, and **plan-quality-checklist**.

## Rule
Change what has **not run** → amend the plan. Change what **has run** → sibling rework file.

## Amend vs rework

| Trigger | Action | Artifact |
|---|---|---|
| Defect in a pending, failed, or blocked step | Amend in place | Same `plan.md` + `## Amendments` row |
| New step discovered before it runs | Amend in place | Same |
| Boundary needs tightening | Amend in place | Same |
| Executed ✅ behavior must change | Rework | `rework-<date>.md` |
| Post-merge issue | Rework as a new cell | `rework-<date>.md` |

## Step status: ⏭ Abandoned
A step that is deliberately not executed:

- Reason required; the step stays visible with its number.
- Excluded from completion: every step must be ✅ **or** ⏭.
- Never has a commit; if the work is needed later, append a new step.
- Never abandon a step that already has commits — that is executed work; use a rework instead.
- Never abandon, reorder, or defer the **Exit gate** step — only a user-ratified waiver removes it (see **exit-gate**).
- Set only by the planner during an approved amendment, or by explicit user instruction.
- Distinct from 🚫 blocked — blocked may still run; abandoned will not.

## Procedure

1. Read the active plan, its statuses, and `context.md` `## Amendments`.
2. Freeze every ✅ step and its notes byte-for-byte.
3. Append new steps with the next number, or insert with a letter suffix (`3a`, `3b`) when the work must run before an existing pending step; file order is execution order; never renumber. New steps use the full six-field block from **plan-file-format**.
4. Mark obsolete pending steps `⏭ abandoned — <reason>`; keep the step's other fields and change only `Status`; never delete.
5. Tighten the boundary freely; widen only with user ratification.
6. Add one `## Amendments` row to `context.md`.
7. Re-run the plan-quality checklist and show the step diff.

## `## Amendments` row

| Date | Trigger | Added | Abandoned | Boundary | Reason |
|---|---|---|---|---|---|
| 2026-10-21 | Step 3 blocked: token store absent | Steps 8–9 | Step 4 | none | Plan assumed an existing store |

One row per amendment; newest last.

## Resume
Resume at the first ⏳ or 🚫 step; skip ✅ and ⏭. Remaining count includes only pending and blocked steps.

## Abandoned step format

```markdown
### Step 4: Migrate legacy tokens ⏭
**Objective**: Backfill legacy tokens into the shared store.
**Status**: ⏭ Abandoned — superseded by Step 8; token store removed
```

## Rationalizations to reject

| Excuse | Reality |
|---|---|
| "Start a fresh plan to keep history clean" | A second file loses the in-flight record; amend |
| "Delete the obsolete step" | Deletion breaks numbering and traceability; mark ⏭ |
| "Make a rework file for it" | Rework is for delivered behavior; pending defects are amendments |
| "Let the executor tweak the steps" | Only the planner amends; the executor returns an amendment request |
| "Renumber so it looks tidy" | Renumbering breaks step and commit references |
