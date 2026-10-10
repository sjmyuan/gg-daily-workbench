# Example: Validating a Findings Doc

**Scenario**: A drafted `findings-payment.md` is ready to save. Validate it against the quality checklist and report defects by severity.

**Applies**: **validate-findings-doc**

## Input / Context

Draft defects to catch: a topic claim missing `file:line`, one ledger claim absent from the ledger, and a sentence with a banned phrase.

## Output

| # | Check | Result | Severity |
|---|---|---|---|
| 1 | Metadata block present and first | Pass | — |
| 2 | Section order (Orientation → topics → Evidence) | Pass | — |
| 3 | Filename matches area slug | Pass | — |
| 4 | Every topic has a TL;DR (≤15 words) | Pass | — |
| 5 | Every claim has inline `file:line` | **Fail** — `payment/retry-config#c2` lacks a path | 🚫 Blocker |
| 6 | Every topic claim appears in the ledger | **Fail** — `payment/authorize-flow#c3` missing | 🔴 Major |
| 7 | IDs unique and unrenumbered | Pass | — |
| 8 | Searched-negatives and Coverage present | Pass | — |
| 9 | Current-state only, no version markers | Pass | — |
| 10 | No banned phrases | **Fail** — "It is important to note" in §3 | 🟢 Nit |
| 11 | Representation rule followed (diagram for flow; comparison rows = items) | Pass | — |

**Fixes applied**:
- Add `RetryConfig.java:14` to the missing claim.
- Add the `payment/authorize-flow#c3` ledger row.
- Delete the banned phrase.

**Result**: Re-run after fixes → all checks pass. Doc saved.
