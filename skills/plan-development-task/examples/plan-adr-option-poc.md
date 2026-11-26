# Example: Planning a POC as a Normal Feature for One ADR Option

**Scenario**: The payment-migration delivery cannot pick a cache option from `adr-caching-01-cache-option.md`.
**Applies**: **plan-poc** → **export-plan**

## 1. Classify + Clarify

**User request:**
> "Plan a POC that builds the Redis option as a standalone feature; I'll review the MR and decide."

- Classified **POC** — an uncertain ADR option needs a working slice, not a decision document.
- Confirmed with the user: option **Redis**; optional review checklist p99 < 50 ms at 2k rps and ≤3 new ops dependencies; slice = the full caching layer behind the wallet-service read path.
- Success criteria are the user's review checklist — never a plan step or a gate.

## 2. Generated plan.md

```markdown
# Plan: poc-redis-cache-option — Redis caching layer behind the wallet read path
**Type**: poc
**Branch**: `poc-adr-caching-01-redis` off `main`
**Test strategy**: test-first — the slice must behave like production code for the MR to be evaluable.
**Gate**: build=`./mvnw -q compile` · test=`./mvnw test` · lint-type=`./mvnw spotless:check` — `pom.xml:112`
**Autonomy**: checkpoint — affected tests per step; the full suite before the MR.
**ADR**: `adr-caching-01-cache-option.md` · **Option**: Redis
**Success criteria**: p99 < 50 ms at 2k rps; ≤3 new ops dependencies

## Scope Boundary
**May change**: wallet-service read path and caching-layer behavior (Redis option only)
**Expected files**: read path, cache layer, their tests (advisory)
**Must not change**: in-process option, other ADRs, unrelated modules
**Protected zones**: none added

## Risk
- The cache abstraction is shared with the other option → Step 2 tests only this option's contract; fallback: narrow the slice.
- **Expected to break first**: Step 2 — the option may need a surface the slice does not expose.

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the POC branch and a known gate baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch `poc-adr-caching-01-redis` off `main`; no overlapping dirt; gate commands confirmed against `pom.xml`.
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 96 passed · lint=0).
**Status**: ⏳ Pending

### Step 2: Implement the cache facade behind its tests ⏳
**Objective**: Get, set, and evict work through a Redis-backed facade with the ADR's TTL and key prefix.
**Files**: `RedisCacheFacadeTest.java`, `RedisCacheFacade.java`, cache configuration
**Source**: generate · n/a · behavior-equal
**Implementation**: Tests first against a containerized Redis (they fail on the missing facade), then the minimal client and facade. No prior source; TTL and prefix come from the ADR option.
**Validation**: Tests fail on the absent facade, then pass; no other suite moves.
**Status**: ⏳ Pending

### Step 3: Wire the read path ⏳
**Objective**: Wallet reads serve through the cache and fall back to the repository.
**Files**: `WalletQueryService.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Read-through cache with fallback to the existing repository; add the hit/miss assertion to the existing service test.
**Validation**: Cache tests pass; wallet-service suite green; a cold read still returns repository data.
**Status**: ⏳ Pending

### Step 4: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green for the slice.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `./mvnw -q compile` && `./mvnw test` && `./mvnw spotless:check` — all exit 0.
**Status**: ⏳ Pending
```

## 3. Export

- `plan.md` carries `**Type**: poc`, the ADR, the option, and the optional success criteria; `context.md` holds the ADR/solution pointers.
- Routes to **execute-plan** as a **normal plan**: implement, commit, offer to open an MR.
- The user evaluates the MR and records the decision; the plan has no measurement step and no report.

## Validation

- [x] POC is planned as a feature, not a probe harness
- [x] Success criteria stay out of the step list
- [x] Units, not phases: the facade and its wiring each carry their own proof
- [x] The slice is reviewable on its own — the user's MR review is the evaluation
