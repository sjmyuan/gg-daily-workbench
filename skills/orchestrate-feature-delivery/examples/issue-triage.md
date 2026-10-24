# Example: Triage an Issue Before Dispatching

**Scenario**: Epic `wallet-migration` is in delivery. Cell `order-service/F2` is **done** and merged. The user raises four issues in sequence, each one rung higher than the last.

**Applies**: **triage-issue** → **handle-post-implementation-issue**

## Issue 1 — "Why does the wallet retry three times?"

**Rung L0 — Answer from the record.**

The orchestrator checks the index, `context.md`, the governing ADR, and `plan.md`:

| Source | Fact |
|---|---|
| `adr-wallet-01-payment-failure-handling.md` | Retry up to 3 times, exponential backoff |
| `context.md` §Open concerns | Retry cap hard-coded during F2; flagged Minor |
| `plan.md` step 4 | Implemented retry policy |

**Answer**: "Three attempts was the ADR decision; F2 hard-coded the cap and flagged configurability as a deferred Minor. No dispatch, no artifacts."

## Issue 2 — "Is the cap actually three in production config?"

**Rung L1 — One evidence check.**

A code fact is missing, so the orchestrator dispatches one read-only **code-investigator** with `context.md` and the ADR by path.

**Answer**: "`wallet-service/retry.ts:41` uses `maxAttempts = 3`; the Helm value is ignored. The record was stale — L0 could not settle this."

No spike artifacts; the delivery index is unchanged.

## Issue 3 — "The ADR says the cap must be configurable, so the decision is wrong"

**Rung L2 — Direct ADR revision.**

The finding contradicts exactly one decision. The orchestrator dispatches **adr-writer** to revise the ADR in place; no scope map, findings pair, or solution rebuild. The target state does not change, so **solution-doc-writer** is not dispatched.

**Answer**: ADR revised: the cap is configured per environment with a 3-attempt default. One independent pass verifies the new `file:line` claim. A sibling `rework-<date>.md` is planned and executed by the normal planner/executor flow.

## Issue 4 — "Maybe our whole failure-handling approach is wrong across payment and wallet"

**Rung L3 — Spike, with a stated trigger.**

Trigger: the issue spans **two decisions/areas** (payment failure handling and wallet retry) and needs option evaluation. The orchestrator dispatches **spike-conductor** with a delta brief — original `scope.md`, both evidence docs, and the governing ADRs by path.

**Answer**: The spike investigates only the delta and updates the affected ADR and solution section; unaffected findings are reused, not rebuilt.

## Rung summary

| Issue | Rung | Dispatches | Artifacts |
|---|---|---|---|
| 1 | L0 Answer | 0 | none |
| 2 | L1 Evidence | 1 | none |
| 3 | L2 Decision | 2 | ADR update + rework file |
| 4 | L3 Spike | ≥3 | delta spike artifacts |

**Checks**: every rung was stated with its justification; L3 named its trigger; no artifact was written at L0/L1.
