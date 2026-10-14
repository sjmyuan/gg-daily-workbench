# Example: Comparing Fee Logic Across Flows

**Scenario**: The `payment` area charges a fee in three flows — checkout, refund, subscription. The reader needs to see how the logic differs. Author one comparison topic in the human doc.

**Applies**: **author-findings-doc**

## Input / Context

- Confirmed question: "How does fee charging differ across flows?"
- Verified evidence: `FeeService.java:44`, `RefundService.java:71`, `SubscriptionFee.java:33` (the last inferred from config).

## Output

```markdown
## 3. How does fee charging differ across flows?

**TL;DR:** Checkout and refund round half-up; subscription floors.

| Flow | When charged | Base amount | Rounding | Ledger entry | Evidence |
|---|---|---|---|---|---|
| Checkout | On capture | Order subtotal | Half-up, 2 dp | `fee` debit | `FeeService.java:44` |
| Refund | On refund | Refunded subtotal | Half-up, 2 dp | `fee_reversal` credit | `RefundService.java:71` |
| Subscription | On renewal | Plan price | Floor, 2 dp | `fee` debit | `SubscriptionFee.java:33` |
```

*Each flow's shape is not diagrammed because the question is a diff; when the flow shape also matters, add one compact diagram per flow.*

**Result**: One comparison topic — rows are the compared flows, closing with an `Evidence` column. Confidence for the inferred subscription rounding lives in `evidence-payment.md`, not here.
