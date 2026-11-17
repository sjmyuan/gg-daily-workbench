# plan-feature-implementation

Judgment capability: decompose the requirement, then shape the plan yourself.
The acceptance evidence and the gate are not negotiable; the step list is.

1. **Decompose the requirement** into independently observable behaviors. Every term the user left silent becomes a question or a labeled assumption (see **define-scope**).
2. **Choose the test strategy** per **test-strategy** — prefer one across the plan, and name each unit's proof.
3. **Ratify the scope boundary** per **define-scope-boundary**.
4. **Derive units, not phases.** One unit per observable outcome. A small unit carries its test and its implementation in one step; a complex one may need several. Never emit "confirm RED", "refactor", "clean up", or "verify cleanup" as standalone steps — they are phases, not units.
5. **Order by dependency.** Each step's precondition is the base or an earlier step; contract before consumer.
6. **Write the plan** per **reference/plan-file-format.md** — header, `## Scope Boundary`, `## Risk`, optional `## Decisions`, unit steps, Exit gate.
7. **Leave what the code decides open.** Name the check that closes the step, not a guessed diff.
8. **Self-check** against **plan-rubric**; present the risk route per its presentation row.

```markdown
### Step 3: Apply tiered pricing ⏳
**Objective**: Orders over the threshold receive the tier discount, exactly once per order.
**Files**: `pricing/TierRule.java`, `pricing/TierRuleTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: Rule reads the tier from config; apply at the single pricing entry point. Generated because no existing rule composes two thresholds — rationale ratified with this plan.
**Validation**: Table test covers below, at, and above the threshold, and a double-application guard; pricing suite green.
**Status**: ⏳ Pending
```

One step, because it has one verdict: the table proves the behavior. Splitting it into RED / implement / refactor would buy the executor nothing.
