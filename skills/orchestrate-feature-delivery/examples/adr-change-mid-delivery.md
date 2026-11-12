# Example: ADR Change Mid-Delivery

**Scenario**: The wallet-migration epic is mid-delivery — `order-service/F2` is **done**, `api-gateway/F3` is **planned**, `order-service/F4` is **in-progress**.
Integration testing of F2 reveals the payment gateway does not reject atomically; the team revises `adr-wallet-01-payment-failure-handling.md` (compensating transactions).
The user says: "The payment-failure decision changed — route what's affected."

**Applies**: **handle-adr-change** → **update-delivery-index**

## 1. Confirm the change + list governed cells

- Changed decision: `adr-wallet-01-payment-failure-handling.md` — revised to compensating transactions.
- Drift is signaled by the **adr-writer** agent's return; the ADR stays versionless, rewritten in place.
- Governed cells (index `ADRs:` per feature): F2 (done) · F3 (planned) · F4 (in-progress).

## 2. Route each cell by status

| Cell | Status | Route |
|---|---|---|
| order-service/F2 | done | post-merge rework — new `F2-r1` in a new wave (see **rework-modes**) |
| api-gateway/F3 | planned | re-plan in place — dispatch **plan-development-task** against the revised ADR (nothing implemented; no history to preserve) |
| order-service/F4 | in-progress | pre-merge rework — sibling `rework-<date>.md`, same cell, no new wave (see **rework-modes**) |

## 3. Dispatch

Rework mechanics — sibling file, append-only steps, execution — are walked through in `examples/post-implementation-rework.md` (post-merge) and `examples/pre-merge-rework.md` (pre-merge).

- **Planner A** → re-plan `api-gateway/F3` (plan-development-task) against the revised decision.
- **Planner B** → write the pre-merge rework for `order-service/F4` (plan-development-task), sibling `rework-2026-08-24.md`, original steps never modified.
- **Executor B** → execute only `rework-2026-08-24.md` (execute-plan) on the unmerged work.
- **F2-r1** (post-merge): the ADR + solution doc are already revised — a **planner** writes the rework file, then an **executor** runs it.
- No in-flight POC cells here — otherwise surface them to the user (the change may invalidate success criteria).

## 4. Update the index

| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| order-service/F2 | 1234-f2-wallet | #42 (merged) | e5f6a7b | done | — | deliveries/wallet-migration/order-service/wallet-service/ |
| order-service/F2-r1 | — | — | — | unplanned | — | deliveries/wallet-migration/order-service/wallet-service/rework-2026-08-24.md |
| api-gateway/F3 | 1234-f3-gateway | — | — | planned | planner-A | deliveries/wallet-migration/api-gateway/wallet-api-gateway/ |
| order-service/F4 | 1234-f4 | — | d4e5f6a | in-progress | executor-B | deliveries/wallet-migration/order-service/order-wallet-integration/ |

Recorded per **update-delivery-index**: F3 stays **planned** (re-planned against the revised ADR), F4 keeps **in-progress** (its rework file is the record), and `F2-r1` is added in a new wave.
The Features table records `Rework of: F2`.
Then run **Finalise**.

## 5. Next actions

No planned cell is dispatched on the stale decision. Re-plan F3, run F4's rework, and plan/execute F2-r1; all status changes land in the index before the next dispatch.
