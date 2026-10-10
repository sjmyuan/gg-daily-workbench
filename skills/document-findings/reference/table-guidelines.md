# Table Guidelines

Backs the topic-block table guidance; used by **author-findings-doc**. Use a table only for a cross-flow comparison or a list of homogeneous facts. Any flow, structure, or branch is a diagram.

## When a table is allowed

| Data | Use |
|---|---|
| Comparison — the same thing across flows/variants | Table, rows = the compared items |
| Homogeneous facts — configuration, data stores, dependencies, failure modes | Table |
| A single flow, structure, sequence, or state | **Diagram**, not a table |
| Dimensions × flows (rows = dimensions, columns = flows) | **Diagram**, not a table |
| Branch / decision logic | **Diagram** (flowchart), not a table |

## Principles

- Self-describing headers — full words, no abbreviations.
- One idea per cell — values, not sentences.
- Units stated — `Base amount (USD)`, `Timeout (s)`.
- Define terms — a Meaning column or the doc's Glossary.
- No ambiguous cells — write the value; no bare `Yes`, `—`, or `maybe` without a defined legend.
- Keep it narrow — ≤6–7 columns; split by aspect when wider.
- Consistent value formats across cells.
- If a header needs a paragraph to explain, it is not tabular — use a diagram or prose.

## Required columns

| Required column | Present when |
|---|---|
| Evidence (file:line) | The table asserts anything about the code |
| Confidence | Not every cell is ✅ Verified (mixed reliability) |
| Meaning / Description | Rows are terms, config keys, or stores |

Domain columns (Trigger, Base amount, Rounding, …) are free, but must obey the principles.

## Comparison-table pattern

Rows = the compared items; columns = the aspects that answer the question; end with `Evidence` and `Confidence`.

```markdown
**Fee charge across flows**

| Flow | When charged | Base amount | Rounding | Ledger entry | Evidence | Confidence |
|---|---|---|---|---|---|---|
| Checkout | On capture | Order subtotal | Half-up, 2 dp | `fee` debit | `FeeService.java:44` | ✅ Verified |
| Refund | On refund | Refunded subtotal | Half-up, 2 dp | `fee_reversal` credit | `RefundService.java:71` | ✅ Verified |
| Subscription | On renewal | Plan price | Floor, 2 dp | `fee` debit | `SubscriptionFee.java:33` | 🔶 Inferred |
```

When each flow's **shape** also matters, pair the table with one compact diagram per flow (multiple diagrams are allowed).

## Anti-patterns

- **Table-washing** — a single flow or structure forced into rows → use a diagram.
- **Dimensions × flows matrix** — rows = dimensions, columns = flows → use a diagram.
- **Decision table** — branch logic → use a flowchart.
- **Cryptic columns** — invented or abbreviated headers.
- **Ambiguous cells** — `Yes`/`—`/`maybe` without a defined legend.
- **Over-wide tables** — more than ~7 columns → split by aspect.
