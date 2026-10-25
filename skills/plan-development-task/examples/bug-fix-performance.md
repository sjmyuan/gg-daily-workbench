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
**TDD variant**: Full cycle with benchmarks — a performance bug needs a failing timing and query-count assertion.
**Gate**: build=`mvn -q compile` · test=`mvn test` · lint-type=`mvn spotless:check checkstyle:check` — `pom.xml:88`

## Scope Boundary
**May change**: `ProductRepository` search-query behavior (query count, latency)
**Expected files**: `ProductRepository` + its tests (advisory)
**Must not change**: serializer behavior, controller behavior, other endpoints
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the branch, a known gate baseline, and current latency.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch off `main`; no overlapping dirt; dependencies resolve; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green`; baseline p99 recorded in the step note.
**Status**: ⏳ Pending

### Step 2: Write the performance test ⏳
**Objective**: Assert 500 ms and ≤3 queries for 1, 10, and 100 results.
**Files**: `ProductRepositoryPerformanceTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: Parametrized benchmark plus a SQL counter interceptor; assert returned data is unchanged.
**Validation**: Test compiles and joins the suite.
**Status**: ⏳ Pending

### Step 3: Confirm test failure (RED) ⏳
**Objective**: Prove the test fails on query count and latency.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the new benchmark under the current implementation.
**Validation**: Fails at ~201 queries, above the 3-query assertion — not an error.
**Status**: ⏳ Pending

### Step 4: Eager-load the associations ⏳
**Objective**: Fetch products, categories, and tags in one query.
**Files**: `ProductRepository.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Rewrite the search query with `JOIN FETCH` for `category` and `tags`.
**Validation**: Step 2 test passes; repository suite green.
**Status**: ⏳ Pending

### Step 5: Verify result-size scaling ⏳
**Objective**: Prove the query count no longer grows with result size.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run the parametrized benchmark at 1, 10, and 100 results.
**Validation**: Every size stays at ≤3 queries and under 500 ms.
**Status**: ⏳ Pending

### Step 6: Clean up ⏳
**Objective**: Remove caches that masked the N+1 pattern.
**Files**: `ProductRepository.java`, search tests
**Source**: edit · n/a · behavior-equal
**Implementation**: Delete the ad-hoc caching workaround and tests asserting lazy loading.
**Validation**: Repository and search suites green.
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

- [x] The failing test asserts both latency and query count — a correctness-only test would pass today
- [x] Result-size variation is covered, so the fix cannot regress on larger pages
- [x] Every step is one six-field block with a `⏳` status
- [x] 7 steps — under the bug-fix cap of 20
