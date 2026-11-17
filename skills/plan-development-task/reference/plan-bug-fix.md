# plan-bug-fix

Judgment capability: diagnose before planning, then shape the plan yourself.
The diagnosis, the acceptance evidence, and the gate are not negotiable; the step list is.

1. **Diagnose from evidence.** Read the code on the symptom's path and state the root cause with the `file:line` proving it, plus the hypotheses ruled out. A symptom-only request has no root cause yet — ask what "correct" looks like before planning.
2. **Resolve the stated guarantee.** When the ask says never, always, exactly, or once, name the failure boundary that can break it — an ambiguous transport outcome, a retry after a partial write, a concurrent caller — and decide it: which side the plan takes, the test that proves it, and the fallback. Choosing "the library handles it" is a decision too; write it down. An open question on a stated guarantee is never an `Assumption` — it is a decision the plan makes or a question it asks before step 3 (see **plan-rubric** row 6).
3. **Choose the test strategy** per **test-strategy** — usually `test-first`; name the test that catches this exact break and the unit that owns it.
4. **Ratify the scope boundary** per **define-scope-boundary**. A fix needing an unrelated refactor first is two plans, not one.
5. **Derive units, not phases.** One unit per independent defect or observable outcome. "Confirm RED", "clean up", and "verify cleanup" are phases of a unit — fold each into that unit's `Validation` or the Exit gate. Keep only the order that matters: proof before fix.
6. **Write the plan** per **reference/plan-file-format.md** — header, ratified `## Scope Boundary`, `## Risk`, optional `## Decisions`, unit steps, Exit gate.
7. **Leave what the code decides open.** When the fix's shape depends on an unread module, write the step as a check with a fallback and say so in `## Risk` — never invent a diff. An unread seam is not an unresolved guarantee: that one is decided above.
8. **Self-check** against **plan-rubric**; the test and gate rows are pass/fail, the rest are graded.
9. **Present the risk route**, not the step list, per **plan-rubric**'s presentation row.

Worked miss to avoid: "retries must never double-notify" planned as a config change plus a dedupe step, with "the transport cannot deliver then fail" written as an assumption. The plan implements a guarantee it never decided — it passes every box and fails the one thing the user asked for.

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
