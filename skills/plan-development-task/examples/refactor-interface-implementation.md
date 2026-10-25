# Example: Refactor — Interface Extraction for Testability

**Scenario**: Extract an `EventPublisher` interface so `DataImportedHandler` can be tested with a fake.
**Applies**: **classify-change-type** → **define-scope** → **plan-refactor**

## Classification

**User request:**
> "Make `EventPublisherImpl` easier to mock in tests. Extract an interface and inject it via Spring."

Keywords "extract interface", "easier to mock" → **Refactor** (structural change, no behavior change). *User confirms: ✅*

## Scope

**Agent asks:**
> 1. Mirror all public methods or a subset?
> 2. Will other implementations exist?
> 3. Interface naming convention?

**User:** Mirror all public methods. A test fake will exist. Use `EventPublisher` with no prefix.

**Scope confirmed:** extract the interface, inject it into the handler, and add a fake for tests. Existing tests pass unchanged. *User confirms: ✅*

## Generated plan.md

```markdown
# Plan: extract-event-publisher-interface — handler depends on an abstraction
**Type**: refactor
**Branch**: `extract-event-publisher-interface` off `main`
**TDD variant**: Green-to-green — interface extraction changes no behavior; existing tests are the proof.
**Gate**: build=`mvn -q compile` · test=`mvn test` · lint-type=`mvn spotless:check checkstyle:check` — `pom.xml:88`

## Scope Boundary
**May change**: internal structure of event publishing (interface extraction, injection)
**Expected files**: `EventPublisher`, `EventPublisherImpl`, `DataImportedHandler`, Spring config, `FakeEventPublisher`, tests (advisory)
**Must not change**: observable publishing behavior, other modules
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch and a known gate baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 168 passed · lint=0).
**Status**: ⏳ Pending

### Step 2: Create the interface ⏳
**Objective**: Declare the publisher contract with all current public methods.
**Files**: `EventPublisher.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New interface — no prior source; signatures copied from the implementation.
**Validation**: Interface compiles; signatures match `EventPublisherImpl`.
**Status**: ⏳ Pending

### Step 3: Implement the interface ⏳
**Objective**: Make the existing publisher satisfy the contract.
**Files**: `EventPublisherImpl.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Add `implements EventPublisher`; no method changes.
**Validation**: Publisher tests stay green.
**Status**: ⏳ Pending

### Step 4: Inject the abstraction ⏳
**Objective**: Make the handler depend on the interface.
**Files**: `DataImportedHandler.java`, Spring configuration
**Source**: edit · n/a · behavior-equal
**Implementation**: Swap the concrete type for `EventPublisher` in the constructor and bean wiring.
**Validation**: Handler tests stay green.
**Status**: ⏳ Pending

### Step 5: Add the test fake ⏳
**Objective**: Provide a recording fake for handler tests.
**Files**: `FakeEventPublisher.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New test double that records published messages.
**Validation**: At least one handler test uses the fake and passes.
**Status**: ⏳ Pending

### Step 6: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green with no behavior drift.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command; grep production call sites for the implementation type.
**Validation**: All gate commands exit 0; no production call site references `EventPublisherImpl`.
**Status**: ⏳ Pending
```

## Validation

- [x] No failing test is introduced — the change is behavior-neutral
- [x] Every step is one six-field block with a `⏳` status
- [x] 6 steps — under the refactor cap of 20
- [x] The final gate proves no call site still depends on the implementation
