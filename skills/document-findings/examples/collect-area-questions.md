# Example: Sourcing Questions for a Payment Area

**Scenario**: A spike has verified investigation results for the `payment` area. The team needs the ordered question list before a findings doc is authored. No user-written questions exist yet.

**Applies**: **collect-area-questions**

## Input / Context

- Area scope: how card payments are authorized, captured, and refunded.
- Verified investigation summary: an HTTP authorize endpoint, a `ChargeService`, a ledger table, retry config, and a GitHub search that found no circuit breaker.

## Output

**Candidate questions by source**

| Source | Candidate |
|---|---|
| Investigation answered | Where does a payment get authorized? |
| Investigation answered | How does a charge flow from request to ledger? |
| Investigation answered | How is retry configured for the charge call? |
| Investigation found a gap | Is there a circuit breaker on the gateway call? |
| Starter set | What is this area responsible for? |
| Starter set | Where are the entry points? |

**Merged, ordered question list**

1. What is the payment area responsible for?
2. Where are the entry points?
3. Where does a payment get authorized?
4. How does a charge flow from request to ledger?
5. How is retry configured for the charge call?
6. Is there a circuit breaker on the gateway call?

**Result**: 6 topics, ordered orientation → depth, within the 3–7 cap. Confirmed with the user before authoring `findings-payment.md`.
