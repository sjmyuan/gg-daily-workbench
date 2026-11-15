# Example: Reviewer authored the area, so the route is dropped

**Scenario**: The `auth-session` findings pair reaches confirmation, but this reviewer wrote the session module. The case where the same artifact needs a different briefing, and a smaller one.
**Applies**: **brief-before-review**, **calibration**

## Input / Context

Same pair and same two ADRs as the findings-pair example. Calibration signal: the reviewer named `session.ts` and `guard.ts` unprompted, corrected the pair's wording on `E-AUTH-07` ("per-worker, not per-process — the Map is per isolate"), and asked why the invalidate surface was counted that way.

Four signal points, all upward → **authored area** row: no route.

## Expected Output

_(abridged — `Start here` omitted for an authored area; full schema: `reference/review-briefing-skeleton.md`)_

```
**Decision**: Accept the current-state findings for `auth-session` so the two ADRs can be confirmed.

**Predict first**: the guard's synchronous `get` is ADR-01's cost driver. Does the async adapter stop at the guard, or does it reach `touch` as well? — my read: `touch` too, which is the one place I think the pair understates the work

**Check yourself** (<2 min): search `sessionCache.touch(` under `src/auth` → expect a caller in the request pipeline as well as the guard; wrong if it is guard-only, in which case the pair's three-site estimate holds and ADR-01 is cheaper than written

**Then**: Does this accurately capture the current state? Anything to add, correct, or remove?

<spikes/redis-cache-migration/docs/findings-auth-session.md>
<spikes/redis-cache-migration/docs/evidence-auth-session.md>
```

## What the smaller briefing buys

The route is gone and nothing is explained: the reviewer wrote this code, and a tour of it would spend their attention on what they already hold. What survives is the part they cannot get from memory — the pair's *claims* about their own code, stated precisely enough to disagree with.

The prediction shifts accordingly. For a new reviewer it tested comprehension ("which stop breaks?"); here it tests the artifact, because the reviewer can already answer the comprehension question. The reviewer's correction of `E-AUTH-07` is folded into the check rather than argued with.

## The failure this avoids

Handing an authored-area reviewer the full briefing reads as condescension and trains them to skim — the habit that makes `waived` the default later. Calibration runs downward as well as upward: the next checkpoint for this reviewer starts at 2 stops unless a signal moves it back.
