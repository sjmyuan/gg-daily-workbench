# Example: Bug Fix — Wrong ID Passed to Publisher

**Scenario**: `DataImportedHandler` sends a transformed data ID to the message publisher instead of the original source ID.
**Applies**: **classify-change-type** → **define-scope** → **plan-bug-fix**

## Classification

**User reports:**
> "The message publisher is receiving the wrong product ID — downstream consumers see a transformed ID in the outgoing event instead of the original source ID."

Keywords "wrong", "incorrect", "instead of original" → **Bug Fix**. *User confirms: ✅*

## Scope

**Agent gathers evidence** — reads `DataImportedHandler.java` and the publishing tests. The handler calls `dataTransformer.transform(record)` and passes `transformedData.getId()` instead of `record.getId()`.

**Agent asks:**
> 1. Should the outgoing message always carry the original source ID, or the transformed ID in some scenarios?
> 2. Do existing tests cover the ID field in the published message?

**User:** Always the original source ID. Existing tests check the message type but not the ID field.

**Root cause confirmed:** the handler publishes the transformed ID; the transformation changes the ID format. *User confirms: ✅*

## Generated plan.md

```markdown
# Plan: fix-publisher-id — outgoing events carry the original source ID
**Type**: bug-fix
**Branch**: `fix-publisher-id` off `main`
**TDD variant**: Full cycle — a data-correctness bug needs test-first proof.

## Scope Boundary
**May change**: `DataImportedHandler` ID-passing behavior
**Expected files**: `DataImportedHandler.java` + its tests (advisory)
**Must not change**: transformer logic, publisher behavior, other handlers
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch and a green handler baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Create `fix-publisher-id` off `main`; no overlapping dirt; toolchain resolves.
**Validation**: `mvn test -Dtest=DataImportedHandlerTest` passes before changes.
**Status**: ⏳ Pending

### Step 2: Write the ID assertion ⏳
**Objective**: Assert the published message carries the original source ID.
**Files**: `DataImportedHandlerTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New test feeds a record whose transformation changes the ID and captures the outgoing payload.
**Validation**: Test compiles and joins the suite.
**Status**: ⏳ Pending

### Step 3: Confirm test failure (RED) ⏳
**Objective**: Prove the new test fails for the wrong-ID reason.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the new test.
**Validation**: Fails asserting the source ID — not an error.
**Status**: ⏳ Pending

### Step 4: Pass the original ID ⏳
**Objective**: Publish the source ID instead of the transformed ID.
**Files**: `DataImportedHandler.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Replace `transformedData.getId()` with `record.getId()` in the outgoing message.
**Validation**: Step 2 test passes; handler suite green.
**Status**: ⏳ Pending

### Step 5: Clean up ⏳
**Objective**: Remove the obsolete ID-mapping helper and stale assertions.
**Files**: `DataImportedHandler.java`, `DataImportedHandlerTest.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Delete the unused helper; drop assertions on the old transformed ID.
**Validation**: Affected-area suite green after cleanup.
**Status**: ⏳ Pending

### Step 6: Quality gate ⏳
**Objective**: Confirm the change meets repo quality gates.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run Spotless and Checkstyle.
**Validation**: `mvn spotless:check checkstyle:check` exits 0.
**Status**: ⏳ Pending
```

## Validation

- [x] Type classified before planning; root cause confirmed by the user
- [x] Boundary names behavior, not just files; protected zones explicit
- [x] Every step is one six-field block with a `⏳` status
- [x] RED precedes the fix; cleanup and quality gate precede hand-off
- [x] 6 steps — consolidated from the 9-step full cycle, under the bug-fix cap of 20
