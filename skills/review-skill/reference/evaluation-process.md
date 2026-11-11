# Output Evaluation Process (review)

Scope: the reviewer's evaluation check; `create-skill` carries the requirement as an author-side standard.

## Two checks

| Check | Proves | Required for |
|---|---|---|
| **Gate** | The output broke no contract | Contractual capabilities: literals, schema, order, safety |
| **Grade** | The output is good, not merely valid | Judgment capabilities: design, review, writing, analysis |

A judgment capability with a gate only passes correct-but-mediocre output.

## Gate — accept any of

- A "Verify that [output] meets [criteria]" step.
- A dedicated validation capability with ordered checks.
- A reference checklist the capability loads and applies.

## Grade — require

- 3–5 criteria with ordinal levels, and an observable anchor per level.
- A stated pass bar, for example "≥8/10 and no criterion at 0".
- Criteria that some output can fail.
- A table (`Criterion | Levels | Anchor`), inline for ≤3 criteria, else in `reference/`.

## Severities

| Observation | Severity |
|---|---|
| No gate in a contractual capability that produces an artifact | 🟡 Minor (a silently wrong literal: 🔴 Major) |
| No grade in a judgment capability | 🟡 Minor (correct-but-mediocre is the common case) |
| A criterion no output can fail, or an anchor that is not observable | 🟡 Minor |
| A verify step that checks nothing the steps do not already guarantee | 🟢 Nit — recommend deletion |
| No evaluation step anywhere, and no example showing one | 🔴 Major |
