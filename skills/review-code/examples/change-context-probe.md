````markdown
# Example: Change-Context Probe (Signature Change Across a Shared Library)

**Scenario**: Review of a change that widens `NotificationSender.send()` from two positional arguments to a single `NotificationRequest` object in a shared internal library.

**Applies**: **conducting-code-review** (steps 1-4 — adversarial stance, blast radius, failure modes, negative space)

**Review Focus**: Blast radius, behavior change, missed call sites

---

## Step 1 – Failure hypotheses stated before reading the fix

1. Some callers were not migrated, so a stale call site still sends the old payload.
2. The new request object defaults a field that the old signature always supplied.
3. An interface implementation or test mock still matches the old signature and silently stops being exercised.
4. A serialized payload or queued message in flight does not parse into the new shape.

## Step 2 – Blast radius

| Surface | Found | Evidence |
|---|---|---|
| Callers of `send()` | 12 | `rg "notificationSender.send" src` — 11 use the new request object, 1 does not |
| Interface implementations | 3 | `EmailSender`, `SmsSender`, `PushSender` — all updated |
| Mocks / test doubles | 4 | one `when(notificationSender.send(any(), any()))` still stubs the old signature |
| Serialized contracts | 1 | `NotificationCommand` written to the outbox queue before deploy |
| Parallel paths | 1 | `LegacyNotificationFacade` wraps `send()` and was not migrated |

## Step 3 – Behavior diff (not text diff)

| Aspect | Before | After |
|---|---|---|
| Template argument | Always supplied by the caller | Optional field on `NotificationRequest` |
| Default on absence | Not possible | Falls back to `"generic"` template |
| Missing recipient | Compile-time impossible | Runtime `NullPointerException` in `EmailSender` |

## Step 4 – Failure modes

| Mode | Change under test | Result |
|---|---|---|
| Empty / null | `request.getTemplate()` absent | not verified — silently defaults to `"generic"`, a behavior change |
| Boundary | Recipient list of 0 | not verified — `EmailSender` throws NPE instead of a domain error |
| Partial failure | SMS fails after email is sent | not verified — no compensations; caller sees one combined result |
| Retry / duplicate | Outbox redelivery after deploy | not verified — in-flight `NotificationCommand` predates the new shape |
| Concurrency | 12 call sites share one sender instance | verified — sender is stateless |
| Error path | `SendException` contract | verified — exception type unchanged |

## Step 5 – Negative space

| Artifact | Present? |
|---|---|
| Regression test for absent template | ✗ no test covers the new default `"generic"` |
| Migration note for in-flight outbox messages | ✗ nothing in the PR description or runbook |
| Contract test for `NotificationCommand` | ✗ serialization shape changed without one |
| Cleanup of `LegacyNotificationFacade` | ✗ unmigrated wrapper left in place |

## Step 6 – Red-team re-read

- **As an attacker**: `NotificationRequest` is deserialized from the outbox queue without a size check on `body` — a poisoned message can allocate an unbounded string.
- **As a careless maintainer**: `getTemplate()` returning `"generic"` looks intentional, so the next developer will not notice that the old signature could never omit a template.

## Resulting findings

#### One call site still uses the old signature
- **File**: `src/notify/LegacyNotificationFacade.java:44`
- **Confidence**: Confirmed
```java
44 │     notificationSender.send(userId, template);
```
- **Issue**: The facade was not migrated; the two-argument overload no longer exists, so this path fails at compile time in the module that consumes the facade.
- **Impact**: The notification path used by scheduled reports stops compiling — release blocked until fixed.
- **Recommendation**: Migrate the facade to the request object and delete it in the same change.

#### Absent template silently changes notification content
- **File**: `src/notify/NotificationRequest.java:31`
- **Confidence**: Suspected
```java
31 │     this.template = template == null ? "generic" : template;
```
- **Issue**: The old signature made a missing template impossible; the new request object substitutes `"generic"`. Callers that previously failed fast now send generic content.
- **Impact**: Users receive untargeted notifications — a silent content regression with no error to alert on.
- **Recommendation**: Reject a null template at construction, or log and meter the fallback if the default is intentional.

````
