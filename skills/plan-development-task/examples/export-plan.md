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
**Gate**: build=`./mvnw compile` · test=`./mvnw test` · lint-type=`./mvnw checkstyle:check` — `pom.xml:41`

## Scope Boundary
**May change**: `DataImportedHandler` null-guard behavior
**Expected files**: handler + its tests (advisory)
**Must not change**: transformer behavior, publisher behavior, other handlers
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch, toolchain, and a known gate baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Create `fix-null-pointer` off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 214 passed · lint=0).
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
**Objective**: Skip publication on a null result and drop the superseded workaround.
**Files**: `DataImportedHandler.java`, `DataImportedHandlerTest.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Add the null guard before building the event; delete the dead defensive check and its fixture.
**Validation**: Step 2 test passes; handler suite green after the removal.
**Status**: ⏳ Pending

### Step 5: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `./mvnw compile` && `./mvnw test` && `./mvnw checkstyle:check` — all exit 0, zero failures.
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
| Build, full suite, static checks green | `plan.md` Step 5 (Exit gate) | every gate command exit 0 |

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
| Gate receipt | — (not executed) |
| Review outcome | — |

## Reworks

`## Reworks` and `## Amendments` start with their first row.
```

No branch metadata, TDD rationale, or decisions here — they live in `plan.md`. Charter ~50 lines.

## Save Location

Saved to `<repo-root>/feature-implementations/fix-null-pointer-in-transformer/`; the user can now invoke **execute-plan** to run it.

## Validation

- [x] Feature folder derived from the plan objective; repo-first layout applied
- [x] `plan.md` matches the template: title, metadata, zones in fixed order, six-field steps
- [x] The `Gate` line is evidence-backed; Step 1 records the baseline; Step 5 is the Exit gate
- [x] `context.md` `Done means` cites the Exit gate step for the build, suite, and static-check rows
- [x] Branch/base in `plan.md`; no branch metadata in `context.md`
- [x] `context.md` is 40–60 lines, passes the admission test, and duplicates no plan fact
