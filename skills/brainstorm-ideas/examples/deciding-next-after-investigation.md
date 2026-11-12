# Example: Deciding What to Investigate Next

**Scenario**: A completed investigation narrowed slow checkout to three suspects.
The team can chase one next sprint; focused mode picks it and turns it into a plan.
**Applies**: **facilitate-session**
**Phases**: **clarify-idea**, **identify-goals**, **explore-challenges**, **generate-ideas**, **evaluate-ideas**, **challenge-ideas**, **refine-idea**, **compile-actionable-plan**

## Input / Context
User request: "We finished the checkout investigation: N+1 queries in the cart, payment p95, or the front-end bundle. One sprint, one suspect. What next?"

## Session Walkthrough

### clarify-idea (extract, don't re-ask)
Facilitator: "Restating the decision: pick one suspect to pursue next sprint, from a finished investigation. Correct?"
User: "Yes — we need a decision, not another full investigation."
Facilitator: "What is already ruled out?"
User: "The database host and the CDN; both measured clean."

**Confirmed idea**: Choose one of three checkout-latency suspects to pursue next sprint, using the completed investigation as evidence.

### identify-goals
Facilitator: "What must the next step achieve?"
User: "Cut p95 checkout latency by 30% before the quarter ends, and stop guessing."
Facilitator: "Which matters most?"
User: "The 30% cut; measured evidence is how we get there."

**Confirmed goals**: cut p95 by 30% this quarter; replace guesses with measured evidence.

### explore-challenges
Facilitator: "What could block the next step — for example, sprint capacity or staging data?"
User: "One sprint of capacity, staging traffic may not match production, and the payment provider is outside our control."

**Confirmed challenges**: one sprint; staging/production gap; third-party latency; wrong suspect.

### generate-ideas (focused set)
Facilitator: "Four next-step options, including one the investigation did not list:"

```
Next Checkout Step
├── Inversion — measure before optimizing
│   └── Add targeted span timing — name the dominant span before choosing a fix
├── Analogy — treat the cart like a query plan
│   └── Fix N+1 queries — the cheapest likely fix in the cart service
├── Constraint flip — test the boundary
│   └── Measure payment p95 in isolation — prove or exclude the third party
└── Elimination — remove the client from the path
    └── Profile the bundle on a cold cache — rule out the front end
```

User: "Full tracing is another investigation. Targeted span timing and the payment check are cheap."

### evaluate-ideas
Facilitator: "Scoring the four options:"

| Idea | Value | Feasibility | Differentiation | Scope | Impact | Why |
|---|---|---|---|---|---|---|
| Targeted span timing | 2 | 2 | 2 | 2 | 2 | Names the cause; fits two days |
| Fix N+1 queries | 1 | 2 | 1 | 2 | 1 | Cheap and likely; may fix the wrong thing |
| Measure payment p95 | 2 | 2 | 1 | 2 | 2 | Proves or excludes a third party quickly |
| Profile the bundle | 1 | 2 | 1 | 2 | 1 | Cheap; the evidence ranks it lowest |

Facilitator: "By effort vs impact, span timing and the payment check win. The N+1 fix follows the measurement; bundle profiling drops."

**Confirmed priorities**: targeted span timing, measure payment p95, fix N+1 if the cart query dominates.

### challenge-ideas
Facilitator: "What if the N+1 fix does not move p95 because the payment provider dominates?"
User: "Then we spend the sprint and learn little. The measurement gate prevents that."
Facilitator: "What if staging traffic hides the production p95?"
User: "Compare staging and production before trusting either number."
Facilitator: "Is full tracing worth the sprint?"
User: "No — two targeted spans answer the question."

**Stress-tested ideas**: two-day measurement gate; fix N+1 only if the cart query dominates; full tracing dropped.

### refine-idea
Facilitator: "What is essential versus nice-to-have?"
User: "Essential: the two-day measurement gate and the conditional N+1 fix. Nice-to-have: bundle profiling."
Facilitator: "Which remaining risk or gap does the idea still not cover?"
User: "A production check after the fix — otherwise we never prove the 30% cut."

**Refined idea**: Spend two days measuring the payment call and the cart query, commit the rest of the sprint to the dominant span, and verify the 30% cut on production.

### compile-actionable-plan
The facilitator compiles the plan per **plan-output-format**:

## Plan
Measure the payment call and the cart query for two days, commit the sprint to the dominant span, then verify the 30% cut on production.

## Why this plan
- Reaches G1 — the cut follows the measured cause, not the loudest suspect.
- Removes C1 and C2 — a two-day gate fits the sprint and closes the staging gap.
- Leaves out the front-end bundle and full tracing — the investigation ranks both lower.

## Goals
- **G1** Cut p95 checkout latency by 30% this quarter — success: p95 down 30% on production for two weeks.
- **G2** Replace guesses with measured evidence — success: the next step cites a span-level measurement, not a hypothesis.

## Decisions
- **D1** Chose a two-day measurement gate — prevents a sprint spent on the wrong suspect.
- **D2** Chose the N+1 fix only if the cart query dominates — the cheapest likely fix.
- **D3** Dropped full end-to-end tracing — costs most of the sprint; two targeted spans answer the question.
- **D4** Dropped front-end bundle profiling — the investigation ranks it below the other two.
- **D5** Open: whether staging traffic reproduces production p95.

## Risks
- **C1** One sprint of capacity — impact: High — mitigation: two-day gate, then one fix — serves: G1.
- **C2** Staging/production gap — impact: High — mitigation: compare both before trusting either — serves: G2.
- **C3** Payment provider outside our control — impact: High — mitigation: measure in isolation and escalate if it dominates — serves: G1.
- **C4** Wrong suspect — impact: High — mitigation: the gate chooses the fix from evidence — serves: G2.

## Next steps
1. **S1** Add span timing to the payment call and cart query → produces a latency dashboard — done when both spans report p50 and p95 — serves: G2.
2. **S2** Compare staging and production for one day → produces a gap note — done when the gap is quantified — serves: G2, C2.
3. **S3** Name the dominant span and pick the fix → produces a decision note — done when one span is shown to dominate — serves: G1, C4.
4. **S4** Fix the N+1 queries if the cart query dominates → produces a query plan and patch — done when the cart span drops below the payment span — serves: G1.
5. **S5** Escalate to the payment provider if their p95 dominates → produces a ticket with span evidence — done when the provider confirms the latency — serves: G1, C3.
6. **S6** Verify the cut on production → produces a before/after p95 report — done when p95 is 30% lower for two weeks — serves: G1.

Facilitator: "Here is the plan — it passes the four quality checks. Want to amend any section before we lock it?"
