# Example: Updating a Findings Doc on New Evidence

**Scenario**: A follow-up scan found the gateway client does have a timeout-based circuit breaker. Update `findings-payment.md` in place without renumbering IDs or adding version markers.

**Applies**: **update-findings-doc**

## Input / Context

- Affected claim: `payment/resilience#c1` — previously ❓ Gap ("No circuit breaker on gateway").
- New evidence: `GatewayClient.java:203` configures a timeout breaker.
- Downstream: `adr-payment-01-gateway-resilience.md` cites this claim.

## Output

**Changed topic block** (only the resilience topic touched):

```markdown
## 5. Is there a circuit breaker on the gateway call?

**TL;DR:** Yes, a timeout-based breaker on the gateway client.

**Key claims**
- A timeout-based circuit breaker is configured — `GatewayClient.java:203` ✅ Verified
```

**Changed ledger rows**:

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|
| payment/resilience#c1 | Circuit breaker on gateway | Yes — timeout-based | `GatewayClient.java:203` | ✅ Verified |

**Changed tables**:
- Remove the `circuit.?breaker` row from Searched-negatives (no longer a dead end).
- Set the Coverage row to `Circuit breaker on gateway: Yes`.

**Result**:
- ID `payment/resilience#c1` is retained; its confidence moved ❓ Gap → ✅ Verified.
- No renumbering, no changelog.
- Flag: `adr-payment-01-gateway-resilience.md` cites this claim and should be re-synced.
