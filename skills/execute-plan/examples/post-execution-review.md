# Plan Executor: Post-Execution Review Example

**Scenario**: All plan steps are ✅ complete. Demonstrates **review-post-execution** (applying review-code, adding a fix step for a Major finding, logging a Minor). The plan file and context file are kept as a permanent record.

## Context

A 5-step refactoring plan has just finished with all steps ✅. The executor now runs the post-execution review.

### Final Plan Status Before Review

```
### Step 1: Create DataValidator class ✅
### Step 2: Move validation logic to DataValidator ✅
### Step 3: Inject validator into DataImportedHandler ✅
### Step 4: Update handler tests ✅
### Step 5: Validate linting, formatting and type checking ✅
```

## Post-Execution Review

Applying **review-code** skill on all changed files:
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

## Adding a Fix Step

```
### Step 6: Fix null-check ordering in DataValidator ⏳
```

### Step 6: Fix Null-Check Ordering ✅

**Objective**: Ensure `validateNotNull` runs before any field access.
**Files**: `domain/validation/DataValidator.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: `validate()` calls `validateNotNull` first, then the id, name, and value checks — the null guard no longer runs after `record.getId()`.
**Validation**: All existing tests still pass.
**Status**: ✅ Completed

#### Plan Status After Step 6
```
### Step 1: Create DataValidator class ✅
### Step 2: Move validation logic to DataValidator ✅
### Step 3: Inject validator into DataImportedHandler ✅
### Step 4: Update handler tests ✅
### Step 5: Validate linting, formatting and type checking ✅
### Step 6: Fix null-check ordering in DataValidator ✅
```

## Re-Running Code Reviewer

Applying **review-code** on `DataValidator.java` and `DataValidatorTest.java` again.

**Result**: No 🚫 Blockers or 🔴 Major issues remain. Two 🟢 Nits (variable naming preferences) — documented in final summary, not blocking.

## Final Summary

All 6 steps completed ✅. Post-execution review resolved 1 🔴 Major issue (null-check ordering); the 🟡 coverage gap was logged, not stepped. Two 🟢 Nits noted for future consideration.

The plan file and context file are kept as a permanent record of this implementation.
