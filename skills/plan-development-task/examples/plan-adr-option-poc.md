# Example: Planning a POC as a Normal Feature for One ADR Option

**Scenario**: The payment-migration delivery can't pick a cache option from `adr-caching-01-cache-option.md`. The user says: "Plan a POC that builds the Redis option as a standalone feature; I'll review the MR and decide."

**Applies**: **plan-poc** → **export-plan**

## 1. Classify + clarify

- Classified: **POC** — an uncertain ADR option needs a working slice, not a decision document.
- Confirmed with the user: option = **Redis**; optional review checklist = p99 < 50ms @ 2k rps, ≤ 3 new ops dependencies; slice = a full caching layer behind the wallet-service read path.

## 2. Plan (normal feature steps, no measurement)

```markdown
## Scope Boundary
**May change**: wallet-service read path and caching-layer behavior (Redis option only)
**Expected files**: read path, cache layer, their tests (advisory)
**Must not change**: in-process option, other ADRs, unrelated modules

**Type**: poc · **ADR**: adr-caching-01-cache-option.md · **Option**: Redis

1. Prepare Environment — branch `poc-adr-caching-01-redis` per repo convention
2. Write focused tests for cache get/set/evict (Redis)
3. Confirm tests fail
4. Implement minimal Redis client + cache facade
5. Verify tests pass
6. Refactor, validate, clean up, quality gate
```

## 3. Export

- `plan.md` carries `type: poc`, the ADR, and the option; `context.md` records the optional review checklist and ADR references.
- Routes to **execute-plan** as a **normal plan**: implement, commit, offer to open an MR. The user evaluates the MR and records the decision; there is no measurement step and no report.
