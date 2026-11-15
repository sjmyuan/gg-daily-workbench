# Example: Findings pair reaching confirmation when the reviewer is new to the area

**Scenario**: A `redis-cache-migration` spike returns the `auth-session` area's findings pair. The reviewer knows the product but has never read the auth module, and the pair's load-bearing claim is about where session state is read.
**Applies**: **brief-before-review**, **plan-orientation-route**

## Input / Context

The analyst's single return carries `spikes/redis-cache-migration/docs/findings-auth-session.md` + `docs/evidence-auth-session.md` and two ADRs. Three claims are load-bearing:

| Claim | Evidence |
|---|---|
| `E-AUTH-03` | The request guard reads the session cache synchronously on every request |
| `E-AUTH-07` | The cache is per-process — three workers hold three copies |
| `E-AUTH-11` | Two of five `sessionCache.invalidate` call sites are test-only |

Calibration signal from the session: the reviewer asked "what does the session module actually do?" and has accepted the first two ADRs without comment → **new area**, full sequence.

## Expected Output

```
**Decision**: Accept the current-state findings for `auth-session` so the two ADRs can be confirmed.

**Start here** — 3 stops, in order:
1. `src/auth/session.ts:12-84` — the session lifecycle: create, touch, invalidate — notice the store is a module-level `Map`, not a client
2. `src/auth/guard.ts:30-58` — every request passes here — notice `sessionCache.get()` is called on the synchronous path, before any await
3. `src/auth/session.test.ts:1-40` — the test-only invalidation callers — notice these are two of the five the ledger counts

**Predict first**: if the cache moves to Redis, which stop breaks first? — my read: only stop 2, because the guard holds a synchronous contract the other two never assume

**Check yourself** (<2 min): search `sessionCache.get(` under `src/auth` → expect exactly one non-test caller in `guard.ts`; wrong if a route handler calls it directly

**Then**: Does this accurately capture the current state? Anything to add, correct, or remove?

<spikes/redis-cache-migration/docs/findings-auth-session.md>
<spikes/redis-cache-migration/docs/evidence-auth-session.md>
```

## Why the route holds these stops

The two ADRs turn on a single mechanism: a synchronous read on the request path. Stop 1 shows where the state lives, stop 2 shows the contract that constrains any replacement, stop 3 shows the invalidate surface is smaller than the claim implies. Together they let the reviewer re-derive `E-AUTH-03` and `E-AUTH-07` without reading the pair first.

Rejected stops: `src/auth/index.ts` (a re-export barrel — resolves everywhere, establishes nothing) and every file the evidence ledger cites for `E-AUTH-11` (five stops, one mechanism).

The prediction is deliberately narrow. It is falsifiable by the reviewer's own reading of stop 2, and a wrong guess costs one sentence to correct — the point is that the reviewer commits before the read.
