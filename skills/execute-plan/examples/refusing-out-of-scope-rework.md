# Example: Refusing a Recovery Fix That Exceeds the Plan Boundary

**Scenario**: Executing a rework plan; a step fails and the only viable fix requires changing behavior that the plan lists under **Must not change**. Demonstrates **check-scope-boundary** inside **handle-errors** — hold and ask, never silently change it.

**Applies**: **check-scope-boundary**, **handle-errors**

## Plan in Execution

Excerpt of the active `rework-<date>.md`; header and `## Steps` heading are unchanged.

```markdown
## Scope Boundary
**May change**: `application/` behavior + `test/`
**Expected files**: `application/`, `test/` (advisory)
**Must not change**: `infrastructure/` behavior (DB schema, external client calls)
**Protected zones**: none added
```

### Step 2: Update Compensating Rollback Tests 🚫

**Objective**: Cover the compensating-rollback retry path.
**Files**: `test/CompensatingRollbackTest.java` (new)
**Source**: generate · n/a · behavior-equal
**Implementation**: new test for partial-failure retries.
**Validation**: blocked — the test cannot compile against current client behavior.
**Status**: 🚫 Blocked — the only viable fix crosses **Must not change**

**Error**: `infrastructure/PaymentGatewayClient.java` throws on partial failure; the new test cannot compile without handling it.

**Recovery analysis**: the only viable fix is to add retry behavior in `infrastructure/PaymentGatewayClient.java` — **Must not change**.

## Refusal + Decision Options

Applying **check-scope-boundary**: the fix is material, so the executor holds the step and asks:

> "Recovering Step 2 requires changing `infrastructure/PaymentGatewayClient.java` retry behavior, which is **Must not change**. Options: (a) extend the boundary to include it, (b) stay in scope and record a follow-up, (c) proceed anyway with a recorded deviation."

**User decision**: (a) extend the boundary.

The executor returns `NEEDS_CONTEXT`; the **planner** rewrites the boundary in the active `rework-<date>.md` (planner-owned) and records the extension. The executor then resumes Step 2 — it never edits the boundary itself.
