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
**Test strategy**: type/config-only — configuration-only change; the suite plus a startup check is the proof.
**Gate**: build=`./mvnw compile` · test=`./mvnw test` · lint-type=`./mvnw checkstyle:check` — `pom.xml:53`
**Autonomy**: auto — config-only; the startup check is cheap enough at every step.

## Scope Boundary
**May change**: retry configuration behavior (max count, delay)
**Expected files**: `application.yaml`, `RetryConfig`, `EventPublisherImpl`, their tests (advisory)
**Must not change**: message format, other Azure Service Bus settings
**Protected zones**: none added

## Risk
- The key is read in one place → Step 2 greps for other readers; fallback: add the second site to the same unit.
- **Expected to break first**: Step 2 — an existing default may mask the new value.

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch, toolchain, and a known gate baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 187 passed · lint=0).
**Status**: ⏳ Pending

### Step 2: Bind the retry settings and publish with them ⏳
**Objective**: Defaults load when the properties are absent, overrides apply, and publishing uses them.
**Files**: `application.yaml`, `RetryConfig.java`, `EventPublisherImpl.java`, `RetryConfigTest.java`, `EventPublisherImplTest.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Failing tests first (absent properties → 3 / 100 ms; explicit overrides); add a `@ConfigurationProperties` class under the existing `azure.servicebus` prefix; replace the hardcoded retry values and delete the constants they replace.
**Validation**: New tests fail on missing properties, then pass; publisher suite green.
**Status**: ⏳ Pending

### Step 3: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `./mvnw compile` && `./mvnw test` && `./mvnw checkstyle:check` — all exit 0, zero failures.
**Status**: ⏳ Pending
```

## Validation

- [x] Tests cover defaults and overrides — not just the happy path
- [x] `type/config-only` is the strategy, and the suite plus a startup check is the stated proof
- [x] Binding, consuming, and removing the constants share one verdict — so they share one step
- [x] The `Gate` line is evidence-backed and the Exit gate is the final step
