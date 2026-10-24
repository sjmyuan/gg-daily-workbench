# Example: Exporting a Confirmed Plan to Files

**Scenario**: A confirmed bug-fix plan is persisted to a feature folder as `plan.md` + `context.md`.
**Applies**: **export-plan** · **doc-budgets** · **plan-file-format**

The single-repo workspace has no docs home or convention, so **resolve-artifact-location** asks and the user confirms the repo root as the base.

## Confirmed Input

- Change type **Bug Fix**; root cause confirmed; Scope Boundary ratified
- Branch/base recorded in the plan header: `fix-null-pointer` / `main`

## Feature Folder

`<repo-root>/feature-implementations/fix-null-pointer-in-transformer/`

## plan.md

```markdown
# Plan: fix-null-pointer-in-transformer — no crash when the transform result is null
**Type**: bug-fix
**Branch**: `fix-null-pointer` off `main`
**TDD variant**: Full cycle — a crash path needs a reproducing failing test.

## Scope Boundary
**May change**: `DataImportedHandler` null-guard behavior
**Expected files**: handler + its tests (advisory)
**Must not change**: transformer behavior, publisher behavior, other handlers
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch and a green handler baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Create `fix-null-pointer` off `main`; no overlapping dirt; dependencies resolve.
**Validation**: Handler suite, linting, and type checking pass.
**Status**: ⏳ Pending

### Step 2: Write the null-payload test ⏳
**Objective**: Reproduce the crash for a missing payload.
**Files**: `DataImportedHandlerTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New test feeds a record whose transform result is null.
**Validation**: Test compiles and joins the suite.
**Status**: ⏳ Pending

### Step 3: Confirm test failure (RED) ⏳
**Objective**: Prove the test fails with the observed null dereference.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the new test.
**Validation**: Fails on the null dereference — not an unrelated error.
**Status**: ⏳ Pending

### Step 4: Guard the null result ⏳
**Objective**: Skip publication when the transform result is null.
**Files**: `DataImportedHandler.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Add the null guard on the transform result before building the event.
**Validation**: Step 2 test passes; handler suite green.
**Status**: ⏳ Pending

### Step 5: Clean up and gate ⏳
**Objective**: Remove obsolete workaround code and confirm repo quality gates.
**Files**: handler, its tests
**Source**: edit · n/a · behavior-equal
**Implementation**: Delete the superseded defensive check; run formatting, linting, and type checking.
**Validation**: Affected-area suite green; all quality checks exit 0.
**Status**: ⏳ Pending
```

## context.md

The charter: unique facts only, 40–60 lines (ceiling 8,000 chars / 120 lines).

```markdown
# Context: fix-null-pointer-in-transformer — no crash on a null transform result

**Outcome:** `DataImportedHandler` no longer crashes when the transform result is null.

## Why

Outgoing events crash when the transform result is null on a missing payload.
Root cause confirmed in the handler; the transformer contract is correct.
Boundary: **plan.md** §Scope Boundary.

## Must hold

- No behavior change beyond the null guard.
- Existing tests stay green.

## Unknowns

- Other call sites may pass null → covered by Step 2's test matrix; no fallback needed.

## Done means

| Criterion | Verification | Pass rule |
|---|---|---|
| Missing payload no longer crashes | handler test suite | all pass |
| Transformer and publisher untouched | diff against `main` | no changes |

## Pointers

- `DataImportedHandler` — crash site
- `DataImportedHandlerTest` — suite extended in Step 2

## Open concerns

- — (none at planning time)

## State

| Field | Value |
|---|---|
| Active plan | `plan.md` |

## Execution

| Field | Value |
|---|---|
| Status | — (not executed) |
| Commits | — |
| PR | — |
| Test evidence | — |
| Review outcome | — |

## Reworks

| Date | Mode | Cell | Trigger | File | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

No `## Amendments` block yet — create it with the first amendment row.
```

No branch metadata, TDD rationale, or decisions here — they live in `plan.md`. Charter ~50 lines.

## Save Location

Saved to `<repo-root>/feature-implementations/fix-null-pointer-in-transformer/`; the user can now invoke **execute-plan** to run it.

## Validation

- [x] Feature folder derived from the plan objective; repo-first layout applied
- [x] `plan.md` matches the template: title, metadata, zones in fixed order, six-field steps
- [x] Branch/base in `plan.md`; no branch metadata in `context.md`
- [x] `context.md` is 40–60 lines, passes the admission test, and duplicates no plan fact
