# Example: Bug Fix — Wrong ID Passed to Publisher

**Scenario**: `DataImportedHandler` sends a transformed data ID to the message publisher instead of the original source ID.
**Applies**: **classify-change-type** → **define-scope** → **plan-bug-fix**

## Intake gate

**Restatement**: "In your words: the message publisher receives a transformed product ID where consumers expect the original source ID. Inferred: (i) the expected behavior is the original ID everywhere; (ii) this is a defect, not an intended format change."

**Q1 · Goal · non-blocking** — original ID everywhere or per message type.
  A) Every outgoing message carries the source ID
  B) Per message type — some legitimately carry the transformed ID
Recommendation: A — "instead of the original" reads as unconditional.
Default if unanswered: A.

User: "A — unconditional." → `ACCEPTED-WITH-ASSUMPTIONS`; A1 `Assumption (user-accepted, unverified)`: a defect, not an intended change.

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
**Test strategy**: test-first — a data-correctness bug needs proof of the break.
**Gate**: build=`mvn -q compile` · test=`mvn test` · lint-type=`mvn spotless:check checkstyle:check` — `pom.xml:88`

## Scope Boundary
**May change**: `DataImportedHandler` ID-passing behavior
**Expected files**: `DataImportedHandler.java` + its tests (advisory)
**Must not change**: transformer logic, publisher behavior, other handlers
**Protected zones**: none added

## Risk
- The transformer has one consumer → Step 2 greps for others; fallback: keep the old assertion with a recorded exception.
- **Expected to break first**: Step 2 — another handler may rely on the transformed ID.

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch and a known gate baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Create `fix-publisher-id` off `main`; no overlapping dirt; toolchain resolves; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 168 passed · lint=0).
**Status**: ⏳ Pending

### Step 2: Publish the source ID ⏳
**Objective**: Outgoing events carry the record's own ID.
**Files**: `DataImportedHandler.java`, `DataImportedHandlerTest.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Add the ID assertion to the existing handler test (it feeds a record whose transformation changes the ID and captures the payload); replace `transformedData.getId()` with `record.getId()` in the outgoing message; drop the now-unused ID-mapping helper.
**Validation**: New assertion fails on the source ID before the change and passes after; handler suite green.
**Status**: ⏳ Pending

### Step 3: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `mvn -q compile` && `mvn test` && `mvn spotless:check checkstyle:check` — all exit 0, zero failures.
**Status**: ⏳ Pending
```

## Validation

- [x] Type classified before planning; root cause confirmed by the user
- [x] Boundary names behavior, not just files; protected zones explicit
- [x] One unit (Step 2) carries the test, the fix, and the cleanup — one verdict, so one step
- [x] The failing run is recorded inside Step 2's `Validation`, not as a step of its own
- [x] 3 steps: prepare, unit, gate — nothing was added to meet a count
