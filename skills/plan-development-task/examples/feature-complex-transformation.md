# Example: Complex Feature — Multi-Locale Attribute Transformation

**Scenario**: Return product attribute values in the user's locale, with a fallback chain and locale validation.
**Applies**: **classify-change-type** → **define-scope** → **plan-feature-implementation**

## Classification

**User request:**
> "Transform product attribute values so each attribute is returned in the user's preferred locale, with a fallback to the default locale, and reject invalid locale codes."

Keywords "transform", "reject invalid" → **Feature** (new behavior). *User confirms: ✅*

## Scope

**Agent asks:**
> 1. BCP 47 (`en-US`) or ISO 639-1 (`en`)?
> 2. Does "missing" mean null, empty string, or both?
> 3. Is fallback one default locale or a priority chain?
> 4. If the fallback also misses — null or error?
> 5. Are values always strings?

**User:** BCP 47. Both null and empty string. Chain: regional → base language → configured default. Return null if all miss. Values are strings.

**Requirement confirmed:** `LocaleAttributeTransformer` resolves the value through the chain; `FallbackLocaleResolver` encapsulates it; malformed codes raise a validation error. *User confirms: ✅*

## Generated plan.md

```markdown
# Plan: localized-attributes — locale-aware values with a fallback chain
**Type**: feature
**Branch**: `localized-attributes` off `main`
**Test strategy**: test-first — transformer and resolver share fixtures, so one unit can cover both.
**Gate**: build=`mvn -q compile` · test=`mvn test` · lint-type=`mvn spotless:check checkstyle:check` — `pom.xml:88`
**Autonomy**: checkpoint — affected tests per step; the full suite at the exit gate.

## Scope Boundary
**May change**: locale transformation and fallback-resolution behavior; handler integration
**Expected files**: `LocaleAttributeTransformer`, `FallbackLocaleResolver`, handler, their tests (advisory)
**Must not change**: product catalog, serialization, other locale logic
**Protected zones**: none added

## Risk
- Fallback semantics come from the ADR, not the code → Step 3 tests the ADR's rule; fallback: ask before implementing.
- **Expected to break first**: Step 3 — fixtures may not cover the partial-apply case.

## Decisions
- PD1 Transformer and resolver share one TDD cycle — shared fixtures; no separate resolver cycle.

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch and a known gate baseline for the attribute package.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 241 passed · lint=0).
**Status**: ⏳ Pending

### Step 2: Resolve locales through one fallback chain ⏳
**Objective**: Regional → base language → default, with malformed BCP 47 codes rejected.
**Files**: `FallbackLocaleResolverTest`, `FallbackLocaleResolver.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: Tests first — exact-locale hit, base-language fallback, default fallback, total miss, malformed code. Then the resolver class; no prior source, the chain does not exist in the repo. The locale-parsing helper is extracted here rather than in a later step: it has no verdict of its own.
**Validation**: Every case fails on missing symbols before the class exists, and passes after; malformed codes raise the validation error.
**Status**: ⏳ Pending

### Step 3: Transform attributes through the resolver ⏳
**Objective**: Each attribute resolves through the chain; null and empty count as missing; a total miss returns null.
**Files**: `LocaleAttributeTransformerTest`, `LocaleAttributeTransformer.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: Tests first, then the transformer. Separate from Step 2 because missing-value semantics have their own verdict and can be reviewed alone.
**Validation**: Transformer tests fail on the absent transformer, then pass; naming aligned with the resolver from Step 2.
**Status**: ⏳ Pending

### Step 4: Localize the handler and drop the raw reads ⏳
**Objective**: The handler emits localized values end to end; the old attribute lookup is gone.
**Files**: `DataImportedHandlerLocalizationTest.java`, `DataImportedHandler.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Integration test first (two-level fallback and a total miss); route handler attribute mapping through the transformer; delete the superseded lookup and the tests asserting raw values.
**Validation**: Integration test fails on unlocalized output before the wiring, then passes; handler suite green.
**Status**: ⏳ Pending

### Step 5: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `mvn -q compile` && `mvn test` && `mvn spotless:check checkstyle:check` — all exit 0, zero failures.
**Status**: ⏳ Pending
```

## Validation

- [x] Every fallback level and the total-miss case has a test
- [x] Strategy rationale lives on the `Test strategy` line and in `## Decisions`, not in prose
- [x] Four units, not twelve phases: each step carries the tests, the code, and the cleanup that share one verdict
- [x] No step exists only to re-run the previous step's suite
