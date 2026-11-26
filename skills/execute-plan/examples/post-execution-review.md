# Plan Executor: Post-Execution Review Example

**Scenario**: A 5-step refactoring plan finished standalone — **no independent gate follows** (not a delivery cell). Demonstrates **review-post-execution**: the full `review-code` pass, a fix inserted before the Exit gate, and a Minor logged. The plan file and context file remain the record.

## Context

A 5-step refactoring plan has just finished with all steps ✅. Step 5 is the Exit gate.

### Final Plan Status Before Review

```
### Step 1: Create DataValidator class ✅
### Step 2: Move validation logic to DataValidator ✅
### Step 3: Inject validator into DataImportedHandler ✅
### Step 4: Update handler tests ✅
### Step 5: Exit gate — lint, formatting, type check ✅
```

## Post-Execution Review

Applying **review-code** to all changed files:
- `domain/validation/DataValidator.java`
- `application/handler/DataImportedHandler.java`
- `test/DataValidatorTest.java`
- `test/DataImportedHandlerTest.java`

### Review Findings

**🔴 Major — Missing null-check in DataValidator**
- `DataValidator.java:L14` — `validateId(record.getId())` is called before `validateNotNull(record)` guards against a null record. If `record` is null, `record.getId()` throws a `NullPointerException` before the null-check runs.
- **Recommendation**: Move `validateNotNull(record)` to be the first call inside `validate()`.

**🟡 Minor — Test only covers the valid record**
- `DataValidatorTest.java` has one test for a valid record and none for a null record or an invalid ID.
- **Disposition**: logged — a 🟡 never opens a fix step. The plan's tests are its deliverable; a coverage gap the request does not name stays an accepted gap.

## Adding a Fix Step — before the Exit gate

The gate already ran, so its receipt is stale the moment anything changes. The fix goes in as `Step 4a`, ahead of Step 5, and the gate re-runs.

```
### Step 4a: Fix null-check ordering in DataValidator ⏳
**Objective**: Ensure `validateNotNull` runs before any field access.
**Files**: `domain/validation/DataValidator.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: `validate()` calls `validateNotNull` first, then the id, name, and value checks — the null guard no longer runs after `record.getId()`.
**Validation**: All existing tests still pass.
**Status**: ✅ Completed
```

### Plan Status After the Fix

```
### Step 1: Create DataValidator class ✅
### Step 2: Move validation logic to DataValidator ✅
### Step 3: Inject validator into DataImportedHandler ✅
### Step 4: Update handler tests ✅
### Step 4a: Fix null-check ordering in DataValidator ✅
### Step 5: Exit gate — lint, formatting, type check ✅  (re-run: build=0 · test=24/24 · lint=0)
```

## Re-Running the Exit Gate

The receipt must match the final tree, so Step 5 runs again after Step 4a. A green receipt from before the fix does not count.

**Result**: no 🚫 Blockers or 🔴 Majors remain; two 🟢 Nits (variable naming) noted, not blocking.

## Final Summary

All 6 steps completed ✅. Post-execution review resolved 1 🔴 Major (null-check ordering); the 🟡 coverage gap was logged, not stepped. Two 🟢 Nits noted.

## In a delivery cell

The independent gate replaces this pass. The executor sweeps only its own diff, reports `Self-check: clean | fixed:<n>`, and never runs `review-code` — `verify-cell` owns the review. A **mechanical** gate finding comes back as a gate repair fixed in place; a **design** finding goes to the planner as a rework.
