# Example: ADR batch confirmed without a read, and the skip recorded as waived

**Scenario**: The same `auth-session` area now presents two ADRs for confirmation. The reviewer replies "just proceed, I trust the analysis" — the case where acceptance and comprehension diverge.
**Applies**: **design-self-check**, **record-review-state**

## Input / Context

Two ADRs returned with the verified pair: `adr-auth-session-01-session-store.md` (choose the cache backend) and `adr-auth-session-02-invalidation.md` (choose the invalidation strategy). ADR-01's recommendation is Redis behind an async adapter, which forces the guard off its synchronous path.

The reviewer's message: "Both look fine, just proceed — I don't need the tour, the previous pair was solid."

## Expected Output

_(abridged — `Start here` omitted because the reviewer waived the route; full schema: `reference/review-briefing-skeleton.md`)_

```
**Decision**: Adopt both auth-session decisions, or hold ADR-01 for a feasibility spike.

**Check yourself** (<2 min): search `sessionCache.get(` and `sessionCache.set(` under `src` excluding tests → expect 1 and 3 callers; wrong if the set has more than 3, because ADR-01's cost estimate counts the adapter change at three sites

**Then**: Confirm or adjust either ADR before the solution document is compiled.

---

Recorded: `waived` — reviewer declined the tour for both units.
Trusted unread: ADR-01's estimate that migrating the guard to an async adapter touches three call sites.
```

## Why the briefing collapses

The reviewer explicitly declined the route, so **plan-orientation-route** does not run and the prediction is dropped: there is no live hypothesis once the reviewer has already decided. Two elements survive because they do not depend on the reviewer's cooperation:

- The self-check stays, because it is one search and it can still be run later — it is the reviewer's cheapest route back into the decision.
- The question stays, because the checkpoint had one and the skill never replaces it.

## Why the state is `waived`

`reviewed` would be a false record: the reviewer said so in their own words. `waived` is recorded against both units, in the same status field that tracks the unit — never in conversation only, or the rubber stamp disappears at the next resume.

The unread claim is named exactly once, with no pressure and no repeat. Naming it converts a silent risk into a tracked one; arguing about it would make the state adversarial, and the reviewer owns the risk. If ADR-01's cost estimate later proves wrong, the `waived` record is what tells the next session that nobody checked it.
