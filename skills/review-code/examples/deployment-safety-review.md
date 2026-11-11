````markdown
# Example: Observability & Deployment Safety Review (New Service Endpoint + DB Migration)

**Scenario**: Review of a PR that adds a new `/api/v1/orders/summary` endpoint backed by a new `order_summary` table, a Flyway migration, and a Redis cache layer.

**Applies**: **conducting-code-review**

## Code Review Summary

**Scope**: `feature/order-summary-endpoint` — new REST endpoint, DB migration, and Redis caching
**Focus Areas**: Observability, deployment safety, correctness, security
**Reviewed**: 4 files, +161/-4 — `OrderSummaryService.java` (+96/-4), `OrderSummaryController.java` (+41), `V20_create_order_summary.sql` (+18), `application.yaml` (+6)
**Overall Assessment**: Requires two blockers to be addressed before merge; deployment sequence must be documented
**Ready to merge?**: No — the migration is not backward-compatible and the cache has no eviction path
**Repo expertise**: `AGENTS.md`, `docs/adr/`, `.github/workflows/`
**Open challenges**: 0 open, 0 blocking · **Unverified referents**: 0

---

## Findings

> Severity legend: 🚫 Blocker = must fix before merge · 🔴 Major = should fix · 🟡 Minor = nice to fix · 🟢 Nit = polish · ⚠️ Inconsistency = decision required

### 🚫 Blockers (Must Fix)

#### DB Migration Is Not Backward-Compatible
- **File**: `db/migration/V20_create_order_summary.sql:7`
- **Confidence**: Confirmed
```sql
7 │ ALTER TABLE orders ADD COLUMN summary_status VARCHAR(32) NOT NULL;
```
- **Issue**: The migration adds a `NOT NULL` column to `orders` with no default value.
  Old code still running during a rolling deploy inserts rows without `summary_status`, so every such `INSERT` fails.
- **Impact**: 500 errors and lost writes for the whole deployment window under any rolling or blue/green strategy.
- **Recommendation**: Add a default value, or split into two migrations — add nullable, backfill, then enforce `NOT NULL` in a later release.

#### Cache Has No Invalidation on Order Update
- **File**: `src/main/java/com/shop/order/OrderSummaryService.java:72`
- **Confidence**: Confirmed
```java
72 │ cache.put("orderSummary::" + orderId, summary, Duration.ofHours(1));
```
- **Issue**: Summaries are cached for an hour with no `@CacheEvict` on `updateOrder()` or `cancelOrder()`; a cancelled order stays active in the summary for up to 60 minutes.
- **Impact**: Users see stale financial data; regulatory and support risk depending on the domain.
- **Recommendation**:
```java
@CacheEvict(value = "orderSummaries", key = "#orderId")
public void updateOrder(String orderId, OrderUpdate update) { ... }

@CacheEvict(value = "orderSummaries", key = "#orderId")
public void cancelOrder(String orderId) { ... }
```

### 🔴 Major Issues

#### No Logging on Cache Miss or Slow Query Path
- **File**: `src/main/java/com/shop/order/OrderSummaryService.java:57`
- **Confidence**: Confirmed
- **Issue**: A cache miss runs the DB query with no log line and no counter, so production cannot tell a working cache from one that always misses.
- **Impact**: The performance improvement cannot be validated post-deployment; latency regressions will be invisible.
- **Recommendation**:
```java
UserSummary summary = cache.get(orderId);
if (summary == null) {
    log.debug("Cache miss for orderId={}, fetching from DB", orderId);
    meterRegistry.counter("order.summary.cache", "result", "miss").increment();
    summary = repository.findSummaryById(orderId);
    cache.put(orderId, summary);
}
```

#### New Endpoint Has No Authorization Check
- **File**: `src/main/java/com/shop/order/OrderSummaryController.java:31`
- **Confidence**: Confirmed
- **Issue**: `GET /api/v1/orders/summary` has no `@PreAuthorize` and is absent from the restricted paths; any authenticated user can read another user's summary by changing `orderId`.
- **Impact**: Horizontal privilege escalation — OWASP A01:2021 Broken Access Control.
- **Recommendation**: Add ownership check:
```java
@PreAuthorize("@orderSecurityService.isOwner(#orderId, authentication)")
@GetMapping("/{orderId}/summary")
public ResponseEntity<OrderSummary> getSummary(@PathVariable String orderId) { ... }
```

#### No Deployment Runbook
- **File**: `docs/deploy-runbook.md (file absent — create here)`
- **Confidence**: Confirmed
- **Issue**: The migration must run before the new code deploys, yet there is no runbook, checklist item, or README note stating that order.
- **Impact**: If a developer deploys app code before running the migration, the new endpoint will throw on every request.
- **Recommendation**: Add a deployment notes section to the PR and to the service README:
```markdown
## Deployment Notes — v2.4.0
1. Run `flyway migrate` against production DB **before** deploying the new application image.
2. Verify `order_summary` table exists and `summary_status` column is populated before routing traffic.
3. Monitor `order.summary.cache` hit/miss counters for the first 30 minutes post-deploy.
```

---

### 🟡 Minor Issues

#### Redis TTL Is Hardcoded
- **File**: `src/main/java/com/shop/order/OrderSummaryService.java:72`
- **Confidence**: Confirmed
- **Issue**: `Duration.ofHours(1)` is hardcoded. Cannot be tuned for different environments without a code change.
- **Recommendation**: Externalize to configuration:
```yaml
# application.yaml
cache:
  order-summary:
    ttl: 1h
```

#### No Test Verifies Migration Is Backward-Compatible
- **File**: `db/migration/V20_create_order_summary.sql:1 (after — add the backward-compatibility test here)`
- **Confidence**: Confirmed
- **Issue**: No integration test runs the migration against an empty database and then exercises `INSERT` via the old schema to confirm compatibility.
- **Recommendation**: Add a `@MigrationTest` that verifies the old `INSERT` path succeeds after migration runs.

---

## Positive Highlights
- Flyway versioning is correctly sequenced; no gaps in version numbers.
- The new endpoint follows the existing REST naming and response conventions consistently.

---

## Failure Modes Checked

| Mode | Change under test | Result |
|---|---|---|
| Empty / null | Order with no summary row | not verified — the miss path returns an empty object rather than 404 |
| Partial failure | Migration runs, app deploy fails | not verified — no documented rollback for the new table |
| Concurrency | Two copies warm one cache key | not verified — no stampede guard |
| Rollback / undo | Revert after the migration ran | not verified — no down-migration, old code ignores the new column |

## Risks & Assumptions
- Review covered source only; rolling-deploy behavior depends on the orchestrator — verify it handles the migration window.
- Redis failure mode was not verified in code; if Redis is unavailable the cache miss path will fall through to the DB (acceptable), but this was not explicitly tested.

---

## Recommended Next Steps
1. Fix migration backward-compatibility (blocker — prevents safe rolling deploy)
2. Add cache invalidation on order mutations (blocker — stale data risk)
3. Add authorization check to the new endpoint (major — access control gap)
4. Add deployment runbook to the PR and README (major — operational safety)
5. Externalize Redis TTL to configuration (minor — defer if time-constrained)
````
