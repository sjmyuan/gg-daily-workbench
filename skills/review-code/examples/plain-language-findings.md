# Example: Plain-Language Findings (Before → After)

## User Request
"Review this change: a bug fix for duplicate product events."

**Applies**: **conducting-code-review**

## Before — vague, unactionable

### 🟡 Minor Issues

#### Consider improving the idempotency approach
- **File**: [EventPublisherImpl.java](EventPublisherImpl.java#L28-L30)
- **Issue**: The idempotency implementation could be better.
- **Impact**: Potential issues over time.
- **Recommendation**: Consider a more robust approach.

No exact behavior, no specific consequence, no concrete fix, and the anchor is a range the reader must search — the developer cannot act on it.

## After — anchored, concrete, actionable

> Severity legend: 🚫 Blocker = must fix before merge · 🔴 Major = should fix · 🟡 Minor = nice to fix · 🟢 Nit = polish · ⚠️ Inconsistency = decision required

### 🔴 Major Issues

#### Unbounded in-memory Set grows for the lifetime of the process
- **File**: `src/events/EventPublisherImpl.java:27`
- **Confidence**: Confirmed
```java
27 │ private final Set<String> publishedMessageIds = new HashSet<>();
```
- **Issue**: `publishedMessageIds` is a `HashSet<String>` with no size limit and no eviction. Every message ID ever published stays in memory for the lifetime of the process.
- **Impact**: At 500 events/second the Set passes 20 million strings within 12 hours, raising GC pressure and heap usage until the instance is OOM-killed and restarted.
- **Recommendation**: Use a bounded cache with expiration:
```java
private final Cache<String, Boolean> publishedMessageIds = Caffeine.newBuilder()
  .maximumSize(100_000)
  .expireAfterWrite(Duration.ofHours(1))
  .build();
```

## What changed

| Before | After |
|---|---|
| Range `#L28-L30` the reader must search | One line `EventPublisherImpl.java:27` plus the quoted line |
| Vague "could be better" | Names the exact code and behavior (`HashSet`, no eviction) |
| "Potential issues over time" | Specific consequence (unbounded growth → heap/GC pressure) |
| "Consider a more robust approach" | Concrete fix with code snippet |
| No confidence, no severity legend | `Confirmed` label plus one-line severity legend at first use |
