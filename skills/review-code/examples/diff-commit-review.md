````markdown
# Example: Diff/Commit Review (Bug Fix)

**Scenario**: Review of a bug fix commit for issue #234 — duplicate product events published to Azure Service Bus.

**Applies**: **gathering-review-context**, **conducting-code-review**

**Review Focus**: Correctness, blast radius, failure modes, regression prevention

## Code Review Summary

**Scope**: Fix for issue #234 — duplicate product events being published
**Focus Areas**: Correctness, idempotency, blast radius, regression prevention
**Reviewed**: 2 files, +38/-6 — `src/events/EventPublisherImpl.java` (+31/-4), `src/events/EventPublisherImplTest.java` (+7/-2)
**Overall Assessment**: Requires a bounded cache and a regression test before merge
**Ready to merge?**: With fixes — the dedup guard works for a single instance but leaks memory and drops duplicates without a trace

---

## Findings

> Severity legend: 🚫 Blocker = must fix before merge · 🔴 Major = should fix · 🟡 Minor = nice to fix · 🟢 Nit = polish · ⚠️ Inconsistency = decision required

### 🚫 Blockers (Must Fix)

#### Dedup Set grows for the lifetime of the process
- **File**: `src/events/EventPublisherImpl.java:27`
- **Confidence**: Confirmed
```java
27 │ private final Set<String> publishedMessageIds = new HashSet<>();
```
- **Issue**: `publishedMessageIds` has no size limit and no eviction, so every message ID ever published is retained. Nothing in the class removes an ID after the message is confirmed sent.
- **Impact**: Unbounded heap growth on a long-running instance — at 500 events/second the Set passes 20 million strings within 12 hours, raising GC pressure until the pod is OOM-killed and restarted.
- **Recommendation**: Replace with a bounded, expiring cache:
```java
private final Cache<String, Boolean> publishedMessageIds = Caffeine.newBuilder()
  .maximumSize(100_000)
  .expireAfterWrite(Duration.ofHours(1))
  .build();
```

### 🔴 Major Issues

#### Duplicates are dropped silently
- **File**: `src/events/EventPublisherImpl.java:71`
- **Confidence**: Confirmed
```java
71 │     if (publishedMessageIds.contains(messageId)) return;
```
- **Issue**: The duplicate path returns without logging or incrementing a metric. A producer that starts sending duplicate IDs is invisible to operators.
- **Impact**: A misbehaving publisher silently loses events until someone notices a downstream data gap — no signal exists to alert on.
- **Recommendation**:
```java
if (publishedMessageIds.contains(messageId)) {
  log.warn("Duplicate event skipped: messageId={}", messageId);
  meterRegistry.counter("event.publish", "result", "duplicate").increment();
  return;
}
```

#### No regression test for the duplicate path
- **File**: `src/events/EventPublisherImplTest.java:120 (after — insert the regression test here)`
- **Confidence**: Confirmed
- **Issue**: The fix adds a dedup guard, but no test publishes the same message ID twice. The existing test changes only update constructor arguments.
- **Impact**: A future refactor can remove or reorder the guard with a green build, reintroducing the original production bug.
- **Recommendation**: Add the failing-first regression test:
```java
@Test
void shouldNotPublishDuplicateEventsWithSameMessageId() {
  eventPublisher.publish(createTestMessage("test-message-123"));
  eventPublisher.publish(createTestMessage("test-message-123"));
  verify(serviceBusSender, times(1)).sendMessage(any());
}
```

### 🟡 Minor Issues

#### Guard is instance-local, so replicas still duplicate
- **File**: `src/events/EventPublisherImpl.java:27`
- **Related**: `src/events/EventRouter.java:58` (fan-out to both publisher instances)
- **Confidence**: Suspected
- **Issue**: The Set lives in the instance. With two replicas behind the router, each keeps its own Set and both publish the same message ID.
- **Impact**: The original bug reappears whenever the service runs more than one replica — the fix only holds for a single-instance deployment.
- **Recommendation**: Confirm the deployment topology, then move dedup to a shared store (Redis `SETNX` with TTL) or enforce idempotency on the consumer side.

---

## Positive Highlights
- Root cause correctly identified — the missing idempotency check, not the broker configuration
- Minimal, focused change with no unrelated refactoring
- `Set` lookup keeps the happy path at O(1)

---

## Failure Modes Checked

| Mode | Change under test | Result |
|---|---|---|
| Retry / duplicate | Same `messageId` published twice | verified — second publish skipped |
| Empty / null | `messageId` is null | not verified — `null` is added to the Set and skips every later null-ID message |
| Concurrency | Two threads publish the same ID | not verified — `contains` + `add` is not atomic; a check-then-act race can double-publish |
| Scale | Multi-replica deployment | not verified — guard is instance-local (see minor finding) |
| Rollback / undo | Revert the guard | verified — revert is code-only, no data migration |

---

## Risks & Assumptions
- Assumes `messageId` is always present and unique per logical event — confirm with the producer contract; the null case is unhandled
- Assumes the service runs as a single replica — the router fan-out at `EventRouter.java:58` contradicts this; verify the deployment manifest
- Memory-leak impact depends on event throughput — check the production publish rate before sizing the cache

---

## Recommended Next Steps
1. Replace the `HashSet` with a bounded cache (blocker — required before merge)
2. Add the regression test (major — required before merge)
3. Add duplicate logging and a metric (major — required for observability)
4. Confirm replica count and decide on shared idempotency (major — blocks the fix only in multi-replica deployments)

````
