# Example: Authoring the Evidence Doc

**Scenario**: The human `findings-payment.md` is authored. Build the matching machine `evidence-payment.md` with metadata, topic map, ledger, searched-negatives, and coverage.

**Applies**: **author-evidence-doc**

## Input / Context

- Human-doc topics: authorize-flow, authorize-failure, retry-config, resilience.
- Claims (5): controller entry, gateway call, ledger write, retry count, no jitter.
- One dead-end search for a circuit breaker.

## Output

````markdown
<!-- evidence-doc
area: payment
spike: checkout-reliability
status: complete
scope: card authorization, capture, and refund paths
related-areas: [orders]
human-doc: docs/findings-payment.md
-->

# Evidence: Payment

## 1. Topic map

| Topic slug | Human heading | Claim IDs |
|---|---|---|
| payment/authorize-flow | findings-payment.md#3-where-does-a-payment-get-authorized | #c1, #c2, #c3 |
| payment/authorize-failure | findings-payment.md#4-what-happens-when-the-gateway-fails | #c1, #c2 |
| payment/retry-config | findings-payment.md#5-how-is-retry-configured-for-the-charge-call | #c1, #c2 |
| payment/resilience | findings-payment.md#6-is-there-a-circuit-breaker-on-the-gateway-call | #c1 |

## 2. Claim ledger

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|
| payment/authorize-flow#c1 | Authorize enters at the controller | Yes | `PaymentController.java:41` | ✅ Verified |
| payment/authorize-flow#c2 | Gateway called in `authorize()` | Yes | `ChargeService.java:88` | ✅ Verified |
| payment/authorize-flow#c3 | Ledger row written after approval | Yes | `LedgerRepository.java:57` | ✅ Verified |
| payment/authorize-failure#c1 | Retries up to three times | Yes | `RetryConfig.java:12` | ✅ Verified |
| payment/authorize-failure#c2 | No ledger row written on failure | Yes | `ChargeService.java:96` | ✅ Verified |
| payment/retry-config#c1 | Retry count is 3 | Yes | `RetryConfig.java:12` | ✅ Verified |
| payment/retry-config#c2 | No jitter configured | Yes | `RetryConfig.java:14` | ✅ Verified |
| payment/resilience#c1 | No circuit breaker on gateway | Gap | payment/** | ❓ Gap |

## 3. Searched-negatives

| Search (pattern/query) | Result | Next step |
|---|---|---|
| `circuit.?breaker` in `payment/**` | No match | Investigate gateway client resilience |

## 4. Coverage

| In-scope question | Investigated | Not investigated / Gaps |
|---|---|---|
| Card authorization path | Yes | — |
| Retry configuration | Yes | — |
| Circuit breaker on gateway | No | ❓ Not found |

## 5. Cross-area references

| Constraint | This area | Related area | Evidence (file:line) |
|---|---|---|---|
| Ledger ownership | `payment` writes `ledger` | `orders` reads it | `LedgerRepository.java:57` |
````

**Result**: Every human-doc topic has a topic-map row linking its heading anchor, every claim carries a stable `#cN` ID and confidence, and the gap is recorded honestly instead of omitted.
