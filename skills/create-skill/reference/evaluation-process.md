# Output Evaluation

Scope: every authored capability must let the agent check its own output.

Used by **create-skill-file** (step 5) and **validate-created-skill** (check 13).

## Two checks

| Check | Answers | Required for |
|---|---|---|
| **Gate** | Did the output break a contract? | Contractual capabilities: literals, schema, order, safety |
| **Grade** | How good is the output? | Judgment capabilities: design, review, writing, analysis |

A judgment capability needs a grade; a gate alone passes correct-but-mediocre output.

## Gates

End the capability with a validation or checklist step, or name the observable signal.
Use whichever fits:

- A "Verify that <output> meets <criteria>" step.
- A pointer to a quality checklist: "Load **reference/quality-checklist.md** and apply each criterion."
- A dedicated validation capability with ordered checks.

A capability whose output has no check leaves correctness to agent discretion.

## Grades

- Use 3–5 criteria; each scores 0–2, or 1–4 when the levels need nuance.
- Give every level an observable anchor: `0 = no reason given`, `2 = reason names the tradeoff`.
- State the pass bar, for example "≥8/10 and no criterion at 0".
- Score the artifact, never the intent; a criterion that no output can fail is deleted.
- Keep ≤3 criteria inline at the final step; put larger rubrics in `reference/`.
- Emit the rubric as a table: `Criterion | Levels | Anchor`.

A grade is falsifiable too: two readers must reach the same band from the same output.

## Checklist

- [ ] Every artifact-producing capability has a gate, a grade, or both.
- [ ] Gate criteria are falsifiable; grade anchors are observable.
- [ ] At least one example demonstrates the check in action.
