# plan-bug-fix

Judgment capability: diagnose before planning, then shape the plan yourself.
The diagnosis, the acceptance evidence, and the gate are not negotiable; the step list is.

1. **Diagnose from evidence.** Read the code on the symptom's path and state the root cause with the `file:line` proving it, plus the hypotheses ruled out. A symptom-only request has no root cause yet — ask what "correct" looks like before planning.
2. **Choose the test strategy** per **test-strategy** — usually `test-first`; name the test that catches this exact break and the unit that owns it.
3. **Ratify the scope boundary** per **define-scope-boundary**. A fix needing an unrelated refactor first is two plans, not one.
4. **Derive units, not phases.** One unit per independent defect or observable outcome. "Confirm RED", "clean up", and "verify cleanup" are phases of a unit — fold each into that unit's `Validation` or the Exit gate. Keep only the order that matters: proof before fix.
5. **Write the plan** per **reference/plan-file-format.md** — header, ratified `## Scope Boundary`, `## Risk`, optional `## Decisions`, unit steps, Exit gate.
6. **Leave what the code decides open.** When the fix's shape depends on an unread module, write the step as a check with a fallback and say so in `## Risk` — never invent a diff.
7. **Self-check** against **plan-rubric**; the test and gate rows are pass/fail, the rest are graded.
8. **Present the risk route**, not the step list, per **plan-rubric**'s presentation row.

```markdown
### Step 2: Publish the source ID ⏳
**Objective**: Outgoing events carry the record's own ID.
**Files**: `DataImportedHandler.java`, `DataImportedHandlerTest.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Test asserts the captured payload's ID equals the record ID; replace `transformedData.getId()` with `record.getId()`.
**Validation**: New test fails on the source ID before the change, passes after; handler suite green.
**Status**: ⏳ Pending
```

One step, because test and fix share one verdict. A unit whose proof and change are separable stays two.
