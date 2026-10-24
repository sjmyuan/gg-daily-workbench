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
**TDD variant**: Full cycle — the slice must behave like production code for the MR to be evaluable.
**ADR**: `adr-caching-01-cache-option.md` · **Option**: Redis
**Success criteria**: p99 < 50 ms at 2k rps; ≤3 new ops dependencies

## Scope Boundary
**May change**: wallet-service read path and caching-layer behavior (Redis option only)
**Expected files**: read path, cache layer, their tests (advisory)
**Must not change**: in-process option, other ADRs, unrelated modules
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
**Objective**: Confirm the POC branch and a green wallet-service baseline.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Branch `poc-adr-caching-01-redis` off `main`; no overlapping dirt.
**Validation**: Wallet-service tests and build pass.
**Status**: ⏳ Pending

### Step 2: Write cache behavior tests ⏳
**Objective**: Assert get, set, and evict through the cache facade.
**Files**: `RedisCacheFacadeTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New tests against a containerized Redis; no production facade exists yet.
**Validation**: Tests compile and join the suite.
**Status**: ⏳ Pending

### Step 3: Confirm test failure (RED) ⏳
**Objective**: Prove the facade behavior is missing.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the new tests.
**Validation**: Fails on missing facade — not an error.
**Status**: ⏳ Pending

### Step 4: Implement the cache layer ⏳
**Objective**: Add the minimal Redis client and cache facade.
**Files**: `RedisCacheFacade.java`, cache configuration
**Source**: generate · n/a · behavior-equal
**Implementation**: New code — no prior source; TTL and key prefix come from the ADR option.
**Validation**: Step 2 tests pass.
**Status**: ⏳ Pending

### Step 5: Wire the read path ⏳
**Objective**: Serve wallet reads through the cache.
**Files**: `WalletQueryService.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Read-through cache with fallback to the existing repository.
**Validation**: Wallet-service suite green; cache tests pass.
**Status**: ⏳ Pending

### Step 6: Quality gate ⏳
**Objective**: Confirm the slice is reviewable.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run linting, formatting, type checking, and the full suite.
**Validation**: All checks exit 0; MR ready for the user's evaluation.
**Status**: ⏳ Pending
```

## 3. Export

- `plan.md` carries `**Type**: poc`, the ADR, the option, and the optional success criteria; `context.md` holds the ADR/solution pointers.
- Routes to **execute-plan** as a **normal plan**: implement, commit, offer to open an MR.
- The user evaluates the MR and records the decision; the plan has no measurement step and no report.

## Validation

- [x] POC is planned as a feature, not a probe harness
- [x] Success criteria stay out of the step list
- [x] Every step is one six-field block with a `⏳` status
- [x] 6 steps — under the feature/POC cap of 25
