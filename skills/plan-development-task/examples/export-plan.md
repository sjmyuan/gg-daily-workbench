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
**Test strategy**: test-first — a crash path needs a reproducing failing test.
**Gate**: build=`./mvnw compile` · test=`./mvnw test` · lint-type=`./mvnw checkstyle:check` — `pom.xml:41`
**Autonomy**: checkpoint — the suite is cheap at milestones; the build runs after each change.

## Scope Boundary
**May change**: `DataImportedHandler` null-guard behavior
**Expected files**: handler + its tests (advisory)
**Must not change**: transformer behavior, publisher behavior, other handlers
**Protected zones**: none added

## Risk
- The null payload arrives through a queue path the local suite cannot exercise → Step 2 uses the recorded fixture; fallback: log it in `## Open concerns`.
- **Expected to break first**: Step 2 — the reproduction may fail for a different reason.

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch, toolchain, and a known gate baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Create `fix-null-pointer` off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 214 passed · lint=0).
**Status**: ⏳ Pending

### Step 2: Reproduce and guard the null payload ⏳
**Objective**: A null transform result is skipped, not dereferenced.
**Files**: `DataImportedHandlerTest.java`, `DataImportedHandler.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Test first — a record whose transform result is null; then add the null guard before building the event and delete the dead defensive check and its fixture.
**Validation**: Test fails on the null dereference before the guard and passes after; handler suite green.
**Status**: ⏳ Pending

### Step 3: Exit gate ⏳
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
| Build, full suite, static checks green | `plan.md` Step 3 (Exit gate) | every gate command exit 0 |

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
| Range | — |
| PR | — |
| Gate receipt | — (not executed) |
| Self-check | — |

## Reworks

`## Reworks` and `## Amendments` start with their first row.
```

No branch metadata, strategy rationale, or decisions here — they live in `plan.md`. Charter ~50 lines.

## Save Location

Saved to `<repo-root>/feature-implementations/fix-null-pointer-in-transformer/`; the user can now invoke **execute-plan** to run it.

## Validation

- [x] Feature folder derived from the plan objective; repo-first layout applied
- [x] `plan.md` matches the template: title, metadata, zones in fixed order, `## Risk`, unit steps
- [x] The `Gate` line is evidence-backed; Step 1 records the baseline; Step 3 is the Exit gate
- [x] `context.md` `Done means` cites the Exit gate step for the build, suite, and static-check rows
- [x] Branch/base in `plan.md`; no branch metadata in `context.md`
- [x] `context.md` is 40–60 lines, passes the admission test, and duplicates no plan fact
