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
**TDD variant**: Full cycle per component — transformer and resolver share fixtures, so one cycle covers both.

## Scope Boundary
**May change**: locale transformation and fallback-resolution behavior; handler integration
**Expected files**: `LocaleAttributeTransformer`, `FallbackLocaleResolver`, handler, their tests (advisory)
**Must not change**: product catalog, serialization, other locale logic
**Protected zones**: none added

## Decisions
- PD1 Transformer and resolver share one TDD cycle — shared fixtures; no separate resolver cycle.

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch and a green baseline for the attribute package.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch off `main`; no overlapping dirt; dependencies resolve.
**Validation**: Attribute-package tests, linting, and type checking pass.
**Status**: ⏳ Pending

### Step 2: Write transformation and fallback tests ⏳
**Objective**: Cover exact-locale hit, base-language fallback, default fallback, and total miss.
**Files**: `LocaleAttributeTransformerTest`, `FallbackLocaleResolverTest`
**Source**: generate · n/a · behavior-equal
**Implementation**: New tests; malformed BCP 47 codes expect a validation error.
**Validation**: Both test classes compile.
**Status**: ⏳ Pending

### Step 3: Confirm test failure (RED) ⏳
**Objective**: Prove the new tests fail because the behavior is absent.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the two new test classes.
**Validation**: Every test fails on missing symbols or missing behavior — not an error for the wrong reason.
**Status**: ⏳ Pending

### Step 4: Implement the resolver ⏳
**Objective**: Encapsulate the chain regional → base → default in one class.
**Files**: `FallbackLocaleResolver.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New class; no prior source — the chain does not exist in the repo.
**Validation**: Resolver tests pass for hit, fallback, and miss.
**Status**: ⏳ Pending

### Step 5: Implement the transformer ⏳
**Objective**: Resolve each attribute through the resolver and reject malformed locales.
**Files**: `LocaleAttributeTransformer.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: Null and empty values count as missing; return null when every level misses.
**Validation**: Transformer tests pass.
**Status**: ⏳ Pending

### Step 6: Verify both components ⏳
**Objective**: Confirm both classes pass together.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run the full attribute-package suite.
**Validation**: All tests pass.
**Status**: ⏳ Pending

### Step 7: Refactor both classes ⏳
**Objective**: Simplify the resolver API and align naming.
**Files**: `LocaleAttributeTransformer.java`, `FallbackLocaleResolver.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Extract the locale-parsing helper; keep behavior unchanged.
**Validation**: Suite stays green after the refactor.
**Status**: ⏳ Pending

### Step 8: Write handler integration tests ⏳
**Objective**: Assert the handler emits localized values end to end.
**Files**: `DataImportedHandlerLocalizationTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New test; fixtures cover a two-level fallback and a total miss.
**Validation**: Test compiles and joins the suite.
**Status**: ⏳ Pending

### Step 9: Confirm integration failure (RED) ⏳
**Objective**: Prove the handler does not yet localize values.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the integration test.
**Validation**: Fails on unlocalized output — not an error.
**Status**: ⏳ Pending

### Step 10: Integrate with the handler ⏳
**Objective**: Route handler attribute mapping through the transformer.
**Files**: `DataImportedHandler.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Replace direct attribute reads with transformer calls.
**Validation**: Integration test passes; handler suite green.
**Status**: ⏳ Pending

### Step 11: Clean up ⏳
**Objective**: Remove superseded mapping code and obsolete tests.
**Files**: handler, both test suites
**Source**: edit · n/a · behavior-equal
**Implementation**: Delete the old attribute lookup; drop tests asserting raw values.
**Validation**: Affected-area suite green.
**Status**: ⏳ Pending

### Step 12: Quality gate ⏳
**Objective**: Confirm linting, formatting, and type checking pass.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run the repo formatter, linter, and type checker.
**Validation**: All three exit 0.
**Status**: ⏳ Pending
```

## Validation

- [x] Every fallback level and the total-miss case has a test
- [x] Consolidation rationale lives in the TDD variant and `## Decisions`, not in prose
- [x] Every step is one six-field block with a `⏳` status
- [x] 12 steps — under the feature cap of 25
