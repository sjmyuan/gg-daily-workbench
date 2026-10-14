# Example: Validating a Findings Doc Pair

**Scenario**: A drafted `findings-payment.md` and its `evidence-payment.md` are ready to save. Validate both against the quality checklist and report defects by severity.

**Applies**: **validate-findings-doc**

## Input / Context

Draft defects to catch: a ledger claim missing `file:line`, one human-doc claim absent from the ledger, and a sentence with a banned phrase.

## Output

| # | Check | Result | Severity |
|---|---|---|---|
| 1 | Human doc frontmatter and Summary present | Pass | — |
| 2 | Human doc section order (Summary → Orientation → topics) | Pass | — |
| 3 | Human doc free of claim IDs, confidence tags, ledger, and evidence-doc references | Pass | — |
| 4 | Every human topic has a TL;DR (≤15 words) | Pass | — |
| 5 | Every human-doc topic claim appears in the ledger | **Fail** — `payment/authorize-flow#c3` missing | 🔴 Major |
| 6 | Evidence doc metadata and topic map present | Pass | — |
| 7 | Every ✅/🔶 ledger claim has inline `file:line` | **Fail** — `payment/retry-config#c2` lacks a path | 🚫 Blocker |
| 8 | IDs unique and unrenumbered | Pass | — |
| 9 | Searched-negatives and Coverage present | Pass | — |
| 10 | Current-state only, no version markers | Pass | — |
| 11 | No banned phrases | **Fail** — "It is important to note" in §3 | 🟢 Nit |
| 12 | Representation rule followed (diagram for flow; comparison rows = items) | Pass | — |

**Fixes applied**:
- Add the `payment/authorize-flow#c3` ledger row.
- Add `RetryConfig.java:14` to the missing claim.
- Delete the banned phrase.

**Result**: Re-run after fixes → all checks pass. Pair saved.
