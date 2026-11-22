# Example: Performance Bug Fix — N+1 Query on Product Search

**Scenario**: The product search endpoint takes 8–12 seconds under normal load; profiling shows an N+1 query pattern.
**Applies**: **classify-change-type** → **define-scope** → **plan-bug-fix**

## Classification

**User reports:**
> "The `/products/search` endpoint is very slow — 8 to 12 seconds for a typical query. It gets worse as the catalog grows."

Keywords "slow", "performance degradation" → **Bug Fix** (performance). *User confirms: ✅*

## Scope

**Agent gathers evidence** — reads the controller, repository, and a query-count diagnostic. `ProductRepository.findByKeyword()` returns entities with lazy `category` and `tags` associations; serialization triggers one extra query per product (201 queries for 100 results).

**Agent asks:**
> 1. Are `category` and `tags` always needed in the search result?
> 2. Is there a latency target?

**User:** Always needed. Under 500 ms for a 100-product page.

**Root cause confirmed:** the search query lazily loads associations. *User confirms: ✅*

## Generated plan.md

```markdown
# Plan: fix-product-search-n-plus-one — 100-product search under 500 ms
**Type**: bug-fix
**Branch**: `fix-product-search-n-plus-one` off `main`
**Test strategy**: test-first, benchmarked — the proof is a failing timing and query-count assertion.
**Gate**: build=`mvn -q compile` · test=`mvn test` · lint-type=`mvn spotless:check checkstyle:check` — `pom.xml:88`

## Scope Boundary
**May change**: `ProductRepository` search-query behavior (query count, latency)
**Expected files**: `ProductRepository` + its tests (advisory)
**Must not change**: serializer behavior, controller behavior, other endpoints
**Protected zones**: none added

## Risk
- The slowdown is query count, not payload size → Step 2 measures both; fallback: re-plan against render time.
- **Expected to break first**: Step 2 — a timing assertion is the flakiest proof in the suite.

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch, a known gate baseline, and current latency.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green`.
**Status**: ⏳ Pending

### Step 2: Prove and fix the N+1 ⏳
**Objective**: Keep 1, 10, and 100 results at ≤3 queries and under 500 ms.
**Files**: `ProductRepositoryPerformanceTest.java`, `ProductRepository.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Parametrized benchmark plus a SQL counter interceptor (asserting returned data is unchanged), then rewrite the search query with `JOIN FETCH` for `category` and `tags`. One step because the proof and the change serve one verdict; the failing run is recorded in `Validation`.
**Validation**: Benchmark fails at ~201 queries before the change and passes at every size after — ≤3 queries, under 500 ms; repository suite green.
**Status**: ⏳ Pending

### Step 3: Remove the workarounds the fix makes obsolete ⏳
**Objective**: Drop caches and assertions that existed only to hide the N+1.
**Files**: `ProductRepository.java`, search tests
**Source**: edit · n/a · behavior-equal
**Implementation**: Delete the ad-hoc caching workaround and the tests asserting lazy loading.
**Validation**: Repository and search suites green; query counts unchanged from Step 2.
**Status**: ⏳ Pending

### Step 4: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `mvn -q compile` && `mvn test` && `mvn spotless:check checkstyle:check` — all exit 0, zero failures.
**Status**: ⏳ Pending
```

## Validation

- [x] The failing test asserts both latency and query count — a correctness-only test would pass today
- [x] Result-size variation is covered, so the fix cannot regress on larger pages
- [x] Steps are units: prove-and-fix, remove-what-it-obsoletes, gate
- [x] The failing run is evidence inside Step 2, not a step
