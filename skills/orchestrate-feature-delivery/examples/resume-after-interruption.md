# Example: Resuming an Interrupted Epic

**Scenario**: Delivery of the payment-migration epic was interrupted (context reset / new session). The delivery index shows mixed statuses. The user says: "Continue where we left off."

**Applies**: **resume-delivery** → **orchestrate-delivery** → **update-delivery-index**

## 1. Load and assess (current index state)

- `shared-contracts/F1` — **done** (merged)
- `order-service/F2` — **in-progress** (plan.md steps 1–3 ✅, step 4 🔄)
- `api-gateway/F3` — **failed** (compile errors; reason recorded)
- `order-service/F4` — **unplanned** (wave 2, waits F2 + F3)
- `api-gateway/F4` — **unplanned** (wave 2, waits F2 + F3)
- **ADR currency**: confirmed with the user — no governing ADR changed since the last run.

## 2. Resume decisions

| Cell | Decision | Rationale |
|---|---|---|
| shared-contracts/F1 | **skip** | done |
| order-service/F2 | **resume** | continue execution from step 4 in plan.md, skipping ✅ and ⏭ |
| api-gateway/F3 | **amend** | failed — compile errors from a missing planned step; planner amends the same plan, no new folder |
| order-service/F4 | **wait** | blocked-by F2 + F3 |
| api-gateway/F4 | **wait** | blocked-by F2 + F3 |

## 3. Dispatch

- **Executor A** → resume `order-service/F2` from step 4 (execute-plan) — works from plan.md + context.md (spike references embedded); reloads `adr-wallet-01-payment-failure-handling.md` / solution-doc from the index's Spike References if a step needs more detail
- **Planner B** → amend `api-gateway/F3`'s existing `plan.md` (insert the missing step, mark obsolete pending steps ⏭) — same path, no second plan
- **Executor B** → resume F3 at the first ⏳ step after the amendment (execute-plan), same cell
- **Agent C** (solution-doc-writer / adr-writer) → update solution-doc §Wallet and `adr-wallet-01-payment-failure-handling.md` if F2's execution surfaces artifact changes — the orchestrator never edits them itself
- Both F4 cells wait

## 4. Update index

| Cell | Branch | PR | Commit | Status | Agent | Location |
|---|---|---|---|---|---|---|
| shared-contracts/F1 | 1234-f1-contracts | #1 | a1b2c3d | done | executor-A | deliveries/payment-migration/shared-contracts/wallet-contracts/ |
| order-service/F2 | 1234-f2-wallet | — | d4e5f6a | in-progress (step 4 🔄) | executor-A | deliveries/payment-migration/order-service/wallet-service/ |
| api-gateway/F3 | 1234-f3-gateway | — | — | in-progress (amended; same plan) | planner-B → executor-B | deliveries/payment-migration/api-gateway/gateway-service/ |
| order-service/F4 | — | — | — | unplanned (blocked-by F2/F3) | — | — |
| api-gateway/F4 | — | — | — | unplanned (blocked-by F2/F3) | — | — |

## 5. Reported to the user

Resumed F2 from step 4 · skipped F1 (done) · amended F3's existing plan in place (no new plan file) · both F4 cells wait for F2 + F3. Completed work was never redone.
