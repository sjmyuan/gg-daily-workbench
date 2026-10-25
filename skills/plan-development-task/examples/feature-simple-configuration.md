# Example: Simple Feature — Configurable Retry Settings

**Scenario**: Add configurable retry count and delay for Azure Service Bus publishing.
**Applies**: **classify-change-type** → **define-scope** → **plan-feature-implementation**

## Classification

**User request:**
> "Add configurable retry settings for our Azure Service Bus publishing — max retry count and retry delay."

Keywords "add", "configurable" → **Feature** (new configuration capability). *User confirms: ✅*

## Scope

**Agent asks:**
> 1. Defaults for retry count and delay?
> 2. Global or per message type?
> 3. Any existing configuration pattern to follow?

**User:** 3 retries, 100 ms delay. Global. Follow the existing `azure.servicebus` prefix.

**Requirement confirmed:** add `azure.servicebus.retry.max-retries` and `.delay-ms`, a `RetryConfig` class, and wire `EventPublisherImpl` to them. *User confirms: ✅*

## Generated plan.md

```markdown
# Plan: configurable-retry-settings — retry count and delay come from configuration
**Type**: feature
**Branch**: `configurable-retry-settings` off `main`
**TDD variant**: Streamlined — configuration-only change; test writing and wiring stay separate, cleanup folds into the exit gate.
**Gate**: build=`./mvnw compile` · test=`./mvnw test` · lint-type=`./mvnw checkstyle:check` — `pom.xml:53`

## Scope Boundary
**May change**: retry configuration behavior (max count, delay)
**Expected files**: `application.yaml`, `RetryConfig`, `EventPublisherImpl`, their tests (advisory)
**Must not change**: message format, other Azure Service Bus settings
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch, toolchain, and a known gate baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 187 passed · lint=0).
**Status**: ⏳ Pending

### Step 2: Write configuration tests ⏳
**Objective**: Assert defaults load and overrides apply to publishing retries.
**Files**: `RetryConfigTest.java`, `EventPublisherImplTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: Tests cover absent properties (3 / 100 ms) and explicit overrides.
**Validation**: Tests compile and join the suite.
**Status**: ⏳ Pending

### Step 3: Confirm test failure (RED) ⏳
**Objective**: Prove the tests fail because the properties are not consumed.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the new tests.
**Validation**: Fails on missing properties — not an error.
**Status**: ⏳ Pending

### Step 4: Add the properties and config class ⏳
**Objective**: Bind the retry settings with documented defaults.
**Files**: `application.yaml`, `RetryConfig.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New `@ConfigurationProperties` class under the existing `azure.servicebus` prefix.
**Validation**: Configuration-binding test passes.
**Status**: ⏳ Pending

### Step 5: Consume the settings ⏳
**Objective**: Publish with the configured retry count and delay.
**Files**: `EventPublisherImpl.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Replace hardcoded retry values with `RetryConfig` values.
**Validation**: Publisher tests pass.
**Status**: ⏳ Pending

### Step 6: Remove the hardcoded constants ⏳
**Objective**: Delete the retry constants now supplied by configuration.
**Files**: `EventPublisherImpl.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Remove the unused constants; no behavior change.
**Validation**: Publisher tests pass after the removal.
**Status**: ⏳ Pending

### Step 7: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `./mvnw compile` && `./mvnw test` && `./mvnw checkstyle:check` — all exit 0, zero failures.
**Status**: ⏳ Pending
```

## Validation

- [x] Tests cover defaults and overrides — not just the happy path
- [x] Streamlined keeps test-first; only cleanup is folded into the last code step
- [x] Every step is one six-field block with a `⏳` status
- [x] The `Gate` line is evidence-backed and the Exit gate is the final step
- [x] 7 steps — small enough for fast review
