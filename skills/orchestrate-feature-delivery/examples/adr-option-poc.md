# Example: Proving an ADR Option with Compare-POCs as MRs

**Scenario**: `adr-caching-01-cache-option.md` weighs two cache options — **Redis** vs **in-process**. The team can't decide on drivers alone; the user says: "Implement each option as a temporary slice and open an MR. I'll try both and pick."

**Applies**: **define-poc-scope** → **orchestrate-delivery** → **update-delivery-index**

## 1. Flag + sequence POC cells

Decomposition marks two POC cells (Wave 0, parallel) and one **poc-gated** implementation cell:

| Cell | Type | ADR / Option | Status |
|---|---|---|---|
| order-service/F5a | poc | adr-caching-01-cache-option.md · Redis | unplanned |
| order-service/F5b | poc | adr-caching-01-cache-option.md · in-process | unplanned |
| order-service/F5 | feature | — (poc-gated on F5a/F5b decision) | unplanned |

`success-criteria` is optional — the user may note "p99 < 50ms; ≤ 3 new ops deps" as a review checklist, but it is not a plan step or a gate.

## 2. Plan + execute as normal features

- **Planner A** → plan `F5a` with `plan-poc`: a normal feature plan carrying `type: poc`, the ADR, and the Redis option.
- **Executor A** → implement, commit, and open an MR after approval. No measurement step, no report.
- **Planner B / Executor B** → the same for `F5b` (in-process); serialize or split repos if they conflict.

## 3. Decision gate — the user reviews the MRs

Both cells reach **poc-ready**: implemented, gate passed, MR open. The orchestrator presents the MRs and waits. The user tests/reviews them and records the decision directly in the index:

| Cell | MR | Decision | Rationale (user) |
|---|---|---|---|
| F5a (Redis) | #51 | **adopted** | Meets the latency target; one dependency is acceptable |
| F5b (in-process) | #52 | **rejected** | Simpler, but the migration cost is not worth it |

The orchestrator never evaluates or decides.

## 4. Adopt + reject

- Dispatch **adr-writer** (draft-adr): `adr-caching-01-cache-option.md` records the Redis decision + the user's rationale.
- **F5a (POC-as-implementation)**: merge MR #51 → **done**. No `replaces` target, so nothing is **superseded**.
- **F5b**: close MR #52 → **rejected**; update index.
- **F5 (poc-gated)**: now dispatchable with the chosen option — if the POC slice already ships the full feature, F5 may be dropped or reduced to the remaining scope.

## 5. Next actions

Index shows F5a **done**, F5b **rejected**, F5 unblocked. All statuses landed in the index before the next dispatch.
