# Example Quality Criteria

An example file is well-formed when it meets all of the following criteria:

| Criterion | What to check |
|---|---|
| Clear scenario heading | States the skill domain, the trigger condition, and what makes this case distinct from other examples |
| Realistic, non-trivial input | Representative of actual user requests — not a toy or hello-world scenario |
| Output matches capability steps | The structure and content of the output follow the steps of the capability it demonstrates |
| Template fidelity | Artifacts use the canonical template's headings, field labels, field order, and status vocabulary — no invented sections |
| Abridged labelling | Shortened output carries an explicit `(abridged)` / `(excerpt)` label naming the full schema |
| Set-level continuity | Examples sharing a scenario reuse the same epic, area, feature, folder, and file identifiers; counts and statuses agree |
| Narrative arithmetic | N problems → N ADRs, N features → N rows/cells, N waves → wave table; test order follows doctrine (e.g., RED before fix) |
| One home per fact | Branch, owner, status, and metadata appear in one canonical place; other examples point there |
| Cross-skill agreement | A shared example satisfies every declared schema and is updated in all owning skills together |
| Traceable to a named capability | A reader can identify which capability produced this output |
| No contradictions with the parent skill | The example output does not violate any rule or knowledge entry in the same skill |

**Common example quality violations**:
- Output structure does not match the steps in the corresponding capability (structural drift)
- Example restates a schema variant instead of instantiating the canonical template
- Abridged artifact presented as complete (no label, missing required fields)
- Same scenario uses different epic/area/feature/folder names across examples
- Counts disagree: four problems but five ADRs, four features but five cells
- One fact (branch, POC metadata) recorded in two documents with different values
- Shared example updated in one skill but not the other
- Scenario is trivially simple for a capability designed to handle complex cases
- Scenario description is missing or vague — the reader cannot tell which trigger condition is being demonstrated
- Example output contradicts a rule or knowledge constraint in the parent skill
- Example was written for an older version of the skill and references renamed or removed capabilities

## Machine assistance

Run `scripts/check_artifacts.py` for links, fences, step-field order, zone order, and duplicate
step numbers. Shape fidelity and set-level continuity still require the manual checks above.
