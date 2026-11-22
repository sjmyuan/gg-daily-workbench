# plan-feature-implementation

Judgment capability: decompose the requirement, then shape the plan yourself.
The acceptance evidence and the gate are not negotiable; the step list is.

1. **Decompose the requirement** into independently observable behaviors. Every term the user left silent becomes a question or a labeled assumption (see **define-scope**).
2. **Resolve the stated guarantee.** When the ask says never, always, exactly, or once, name the failure boundary that can break it — an ambiguous transport outcome, a retry after a partial write, a concurrent caller — and decide it: which side the plan takes, the test that proves it, and the fallback. Choosing "the library handles it" is a decision too; write it down. An open question on a stated guarantee is never an `Assumption` — it is a decision the plan makes or a question it asks before step 4 (see **plan-rubric** row 6).
3. **Choose the test strategy** per **test-strategy** — prefer one across the plan, and name each unit's proof.
4. **Ratify the scope boundary** per **define-scope-boundary**.
5. **Derive units, not phases.** One unit per observable outcome. A small unit carries its test and its implementation in one step; a complex one may need several. Never emit "confirm RED", "refactor", "clean up", or "verify cleanup" as standalone steps — they are phases, not units.
6. **Order by dependency.** Each step's precondition is the base or an earlier step; contract before consumer.
7. **Write the plan** per **reference/plan-file-format.md** — header, `## Scope Boundary`, `## Risk`, optional `## Decisions`, unit steps, Exit gate.
8. **Leave what the code decides open.** Name the check that closes the step, not a guessed change. An unread seam is not an unresolved guarantee: that one was decided in step 2.
9. **Self-check** against **plan-rubric**; present the risk route per its presentation row.

Worked miss to avoid: "retries must never double-notify" planned as a config change plus a dedupe step, with "the transport cannot deliver then fail" written as an assumption. The plan implements a guarantee it never decided — it passes every box and fails the one thing the user asked for.

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
