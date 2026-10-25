# Example: Refactor — Split a Large Handler into Focused Services

**Scenario**: Split `DataImportedHandler` into category-mapping and price-transformation services.
**Applies**: **classify-change-type** → **define-scope** → **plan-refactor**

## Classification

**User request:**
> "`DataImportedHandler` handles category mapping, price transformation, and localization in one class. Split it up."

Keywords "split", "too big" → **Refactor** (internal restructuring, no new behavior). *User confirms: ✅*

## Scope

**Agent asks:**
> 1. Stateless utilities or injected beans?
> 2. Should the handler become a pure orchestrator?
> 3. Must existing handler tests stay green?
> 4. Any service naming convention?

**User:** Spring beans, injected. Pure orchestrator. Existing tests stay green. `<Domain>Service` naming.

**Scope confirmed:** extract `CategoryMappingService` and `PriceTransformationService`; the handler delegates to both; observable behavior is unchanged. *User confirms: ✅*

## Generated plan.md

```markdown
# Plan: split-data-imported-handler — one service per transformation concern
**Type**: refactor
**Branch**: `split-data-imported-handler` off `main`
**TDD variant**: Green-to-green — existing tests prove behavior is preserved; characterization tests only where coverage is missing.
**Gate**: build=`mvn -q compile` · test=`mvn test` · lint-type=`mvn spotless:check checkstyle:check` — `pom.xml:88`

## Scope Boundary
**May change**: internal structure of `DataImportedHandler` (decomposition into two services)
**Expected files**: `DataImportedHandler`, `CategoryMappingService`, `PriceTransformationService`, tests (advisory)
**Must not change**: observable behavior, other handlers
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch and a known gate baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (compile=0 · 168 passed · static=0).
**Status**: ⏳ Pending

### Step 2: Confirm coverage for category mapping ⏳
**Objective**: Prove category-mapping behavior is pinned by tests.
**Files**: `DataImportedHandlerTest.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Add characterization tests only for uncovered category-mapping cases; they pass immediately.
**Validation**: Suite green; every mapping branch asserted.
**Status**: ⏳ Pending

### Step 3: Extract CategoryMappingService ⏳
**Objective**: Move category mapping into an injected service.
**Files**: `CategoryMappingService.java`, `DataImportedHandler.java`
**Source**: copy · `DataImportedHandler.java:48-71` · ast-equal
**Implementation**: Move the block with the IDE extract operation; record the adaptation list (constructor injection only).
**Validation**: All handler tests stay green.
**Status**: ⏳ Pending

### Step 4: Confirm coverage for price transformation ⏳
**Objective**: Prove price-transformation behavior is pinned by tests.
**Files**: `DataImportedHandlerTest.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Add characterization tests only for uncovered price cases.
**Validation**: Suite green; rounding and currency branches asserted.
**Status**: ⏳ Pending

### Step 5: Extract PriceTransformationService ⏳
**Objective**: Move price transformation into an injected service.
**Files**: `PriceTransformationService.java`, `DataImportedHandler.java`
**Source**: copy · `DataImportedHandler.java:73-96` · ast-equal
**Implementation**: Move the block with the IDE extract operation; keep the handler as orchestrator.
**Validation**: All handler tests stay green.
**Status**: ⏳ Pending

### Step 6: Clean up ⏳
**Objective**: Remove code and tests left obsolete by the extraction.
**Files**: `DataImportedHandler.java`, test suites
**Source**: edit · n/a · behavior-equal
**Implementation**: Delete the leftover private helpers and tests that asserted the pre-split structure.
**Validation**: Affected-area suite green.
**Status**: ⏳ Pending

### Step 7: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `mvn -q compile` && `mvn test` && `mvn spotless:check checkstyle:check` — all exit 0, zero failures.
**Status**: ⏳ Pending
```

## Validation

- [x] No step introduces a failing test — behavior stays unchanged
- [x] Extraction uses `copy` with an origin and adaptation list, not retyping from memory
- [x] Every step is one six-field block with a `⏳` status
- [x] 7 steps — under the refactor cap of 20
