# Example: Compiling the Evidence Ledger

**Scenario**: Topic blocks for the `payment` area are drafted, but the consolidated evidence layer and searched-negatives are missing. Build only the Evidence & Verification section.

**Applies**: **compile-evidence-ledger**

## Input / Context

- Topic claims (5): controller entry, gateway call, ledger write, retry count, no jitter.
- One dead-end search for a circuit breaker.

## Output

```markdown
## 4. Evidence & Verification

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|
| payment/authorize-flow#c1 | Authorize enters at the controller | Yes | `PaymentController.java:41` | ✅ Verified |
| payment/authorize-flow#c2 | Gateway called in `authorize()` | Yes | `ChargeService.java:88` | ✅ Verified |
| payment/authorize-flow#c3 | Ledger written after approval | Yes | `LedgerRepository.java:57` | ✅ Verified |
| payment/retry-config#c1 | Retry count is 3 | Yes | `RetryConfig.java:12` | ✅ Verified |
| payment/retry-config#c2 | No jitter configured | Yes | `RetryConfig.java:14` | ✅ Verified |
| payment/resilience#c1 | No circuit breaker on gateway | Gap | payment/** | ❓ Gap |

### Searched-negatives

| Search (pattern/query) | Result | Next step |
|---|---|---|
| `circuit.?breaker` in `payment/**` | No match | Investigate gateway client resilience |

### Coverage

| In-scope question | Investigated | Not investigated / Gaps |
|---|---|---|
| Card authorization path | Yes | — |
| Retry configuration | Yes | — |
| Circuit breaker on gateway | No | ❓ Not found |
```

**Result**: Every topic claim appears in the ledger with a stable `#cN` ID, and the gap is recorded honestly instead of omitted.
