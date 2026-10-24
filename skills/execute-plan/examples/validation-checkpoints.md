# Plan Executor: Incremental Validation Checkpoints Example

**Scenario**: A 3-step feature plan executes with validation at each milestone, not only at the end — correctness tests after each code change, lint/type checks after wiring, and a full build gate at the final milestone. Demonstrates **run-validation-checkpoints** (with **execute-step**).

**Applies**: **run-validation-checkpoints**, **execute-step**

## User Request

"Execute the plan to add a `CustomerValidator`, validating after every change."

## Plan to Execute

1. Create CustomerValidator class
2. Wire validator into CustomerService
3. Run lint, formatting, type checks and build

```markdown
## Scope Boundary
**May change**: `CustomerService` validation behavior and its tests
**Expected files**: validator, service, tests (advisory)
**Must not change**: public API signatures, other services
**Protected zones**: none added
```

## Execution with Checkpoints

### Step 1: Create CustomerValidator Class ✅

**Objective**: Add a validator class for customer fields.
**Files**: `src/validation/CustomerValidator.java` (new)
**Source**: generate · n/a · behavior-equal
**Implementation**: validation rules for id, name, and email; no prior class.
**Validation**: `mvn test -Dtest=CustomerValidator` passes — correctness confirmed after the change.
**Status**: ✅ Completed · Steps 2–3 ⏳

### Step 2: Wire Validator into CustomerService ✅

**Objective**: Call the validator before persisting a customer.
**Files**: `src/service/CustomerService.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: inject `CustomerValidator`; validate at the service boundary.
**Validation**: full `mvn test` passes — no regressions; lint clean.
**Status**: ✅ Completed · Step 3 ⏳

### Step 3: Lint, Format, Type Check, Build ✅

**Objective**: Confirm the change passes the full quality gate.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: run the build gate; no edits.
**Validation**: `mvn verify` green — checkstyle, spotbugs, compile, all tests.
**Status**: ✅ Completed

**Checkpoint pattern**: correctness after each change (step 1), regressions + lint after wiring (step 2), full build/lint gate at the final milestone (step 3) — validation is incremental, never deferred to the end of the plan.
