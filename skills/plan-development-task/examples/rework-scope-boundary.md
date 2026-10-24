# Example: Rework That Risks Exceeding the Feature Scope

**Scenario**: A rework would change behavior the original plan lists under **Must not change**.
**Applies**: **define-scope-boundary** · **rework-plan-convention**

Demonstrates the rework guard: refuse and ask, never write silently.

## User Request

"We found a defect in the delivered checkout rework: on partial payment failure the compensating rollback retries with wrong credentials. Investigate and fix it."

## Boundary Check

Original boundary (from the existing `plan.md`):

```markdown
## Scope Boundary
**May change**: wallet-service `application/` + `test/` behavior; `adr-wallet-01-payment-failure-handling.md` payment-failure decision
**Expected files**: wallet application + tests (advisory)
**Must not change**: `payment-gateway/` client behavior; `adr-cutover-01-service-cutover.md` cutover; other modules
**Protected zones**: none added
```

The request changes `payment-gateway/` credential-retry behavior — **Must not change**.

## Refusal + Decision Options

The planner refuses to write silently and presents options:

> "This rework changes `payment-gateway/` credential-retry behavior, which is **Must not change**. Options: (a) extend the boundary to include `payment-gateway/` credential handling, (b) keep it out and file a follow-up feature, (c) treat it as a new feature cell `F2-r2` instead of a rework."

**User decision**: (a) extend the boundary for this rework only.

## Generated rework-2026-08-10.md

The original `plan.md` is never modified; the rework inherits the original boundary and tightens or extends it per the user decision.

```markdown
# Rework 2026-08-10 — compensating rollback credential retry
**Mode**: post-merge · **Cell**: order-service/F2-r1
**Branch**: `rework-f2r1-rollback-credentials` off `main`
**ADR focus**: `adr-wallet-01-payment-failure-handling.md`

## Scope Boundary
**May change**: original **May change** + `payment-gateway/` credential-retry behavior (user-approved extension)
**Expected files**: original **Expected files** + `payment-gateway/` client (advisory)
**Must not change**: original **Must not change**, otherwise unchanged
**Protected zones**: none added

## Done means
| Criterion | Verification | Pass rule |
|---|---|---|
| Correct credentials selected on retry | payment-gateway tests | all pass |
| No change outside the extended boundary | diff against `main` | no changes |

## Steps

### Step 1: Write the failing retry test ⏳
**Objective**: Reproduce the wrong-credential retry on a partial payment failure.
**Files**: `CompensatingRollbackClientTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New test asserts the retry uses the failing payment's credentials.
**Validation**: Test compiles and joins the suite.
**Status**: ⏳ Pending

### Step 2: Confirm test failure (RED) ⏳
**Objective**: Prove the retry test fails for the wrong-credential reason.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the new test.
**Validation**: Fails on the credential assertion — not an error.
**Status**: ⏳ Pending

### Step 3: Fix credential selection on retry ⏳
**Objective**: Select the rollback credentials from the failing payment, not the default client.
**Files**: `payment-gateway/CompensatingRollbackClient.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Resolve credentials per transaction; keep the retry policy unchanged.
**Validation**: Step 1 test passes; gateway suite green.
**Status**: ⏳ Pending

### Step 4: Cover credential rotation ⏳
**Objective**: Pin credential selection across rotation and repeated failures.
**Files**: `CompensatingRollbackClientTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: Add cases for rotated credentials and a second failed attempt.
**Validation**: All new cases pass against the fix.
**Status**: ⏳ Pending

### Step 5: Quality gate ⏳
**Objective**: Confirm the delta meets repo quality gates.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run linting, formatting, type checking, and the full suite.
**Validation**: All checks exit 0.
**Status**: ⏳ Pending
```

`context.md` gains a `## Reworks` manifest row for this file; the rework carries only the delta and inherits the charter by reference. Original `plan.md` steps 1–N remain byte-for-byte unchanged.

## Validation

- [x] Material change detected against the original **Must not change**
- [x] User ratified the boundary extension before the file was written
- [x] Rework uses the same step block as a plan, numbered from 1
- [x] `plan.md` untouched; one manifest row added
