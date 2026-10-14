# Example: Updating a Doc Pair on New Evidence

**Scenario**: A follow-up scan found the gateway client does have a timeout-based circuit breaker. Update the pair without renumbering IDs or adding version markers.

**Applies**: **update-findings-doc**

## Input / Context

- Affected claim: `payment/resilience#c1` — previously ❓ Gap ("No circuit breaker on gateway").
- New evidence: `GatewayClient.java:203` configures a timeout breaker.
- Downstream: `adr-payment-01-gateway-resilience.md` cites this claim.

## Output

**Changed evidence-doc rows** (topic map gains a row; ledger changes):

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|
| payment/resilience#c1 | Circuit breaker on gateway | Yes — timeout-based | `GatewayClient.java:203` | ✅ Verified |

**Changed human-doc topic** (only the affected topic; heading anchor stays stable):

```markdown
## 5. Is there a circuit breaker on the gateway call?

**TL;DR:** Yes, a timeout-based breaker on the gateway client.

> The breaker wraps the gateway call in `GatewayClient`.
```

**Changed tables**:
- Remove the `circuit.?breaker` row from Searched-negatives (no longer a dead end).
- Set the Coverage row to `Circuit breaker on gateway: Yes`.

**Result**:
- ID `payment/resilience#c1` is retained; its confidence moved ❓ Gap → ✅ Verified.
- The human topic keeps its heading anchor; no renumbering, no changelog.
- Flag: `adr-payment-01-gateway-resilience.md` cites this claim and should be re-synced.
