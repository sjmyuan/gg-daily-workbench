# Example: Single-Decision Spike (Fast Path)

**Scenario**: "We're losing webhook deliveries when a pod restarts. Decide how to make delivery durable — settled this week."

**Applies**: `define-spike-scope` (fast path) → `decide-spike-problems` → `accept-adrs`. No notes doc, no architecture overview, no `scope.md`.

**What makes it distinct**: One problem, one ADR, one review.
The ADR is a full `draft-adr` template file — the complete instance and skeleton live in `draft-adr`'s **adr-template** and `examples/database-selection-adr.md`.
This page shows the decision spine and the gate result, not a second copy of the template.

---

## Define Spike Scope

**Restatement**: one decision — how to make merchant webhook delivery survive a pod restart. Inferred: (i) at-least-once is acceptable if effects are idempotent; (ii) no new broker this quarter — platform review is booked out; (iii) ordering is per merchant, not global.

**Q1 · Durability target · blocking** — zero lost deliveries, or best-effort with alerting?
A) Zero lost across restart · B) Alert on loss. Recommendation: A — a lost settlement notice is a support ticket every time.
User: "A."

**Drivers accepted**:

| Tag | Driver | Metric | Threshold | Measurement |
|---|---|---|---|---|
| `HC 1` | Survive pod restart | Lost deliveries | 0 | Kill the pod mid-batch |
| `HC 2` | Order per merchant | Out-of-order deliveries | 0 | Replay 10k events per merchant |
| `SP 1` | Dispatch latency | p95 commit → POST | ≤ 2 s at 100 rps | Load test |
| `SP 2` | No new on-call surface | New 24/7 components | 0 | Ops review |
| `SP 3` | Incremental cost | Invoice delta at 4M events/mo | ≤ $150 | Cost model |

One problem, so no `scope.md`: the scope is recorded in the ADR's Context.

---

## Decide Spike Problems

**Sufficiency reads** — four locations, each because an option needed it:

| Read | Why | Feeds |
|---|---|---|
| `src/payments/webhook/dispatch.ts:41` | The retry scheduler is the loss mechanism | `HC 1`, both options |
| `dispatch.ts:88` | The attempt map is in-process, not shared | `HC 1` |
| `db/migrations/` + schema | Postgres 14, no broker, no outbox table | `SP 2`, `SP 3`, `C1` |
| Platform new-component policy | Broker review booked past the quarter | `SP 2` |

**File**: `adrs/adr-webhook-01-durable-delivery.md` — full template, `Status: draft`, `Area: Webhook delivery`.

**Decision spine** — the rows the gate inspects:

**Chosen:** "Option 1: Postgres outbox + worker" — passes both hard constraints with no new component and no new cost.
**Start here:** `C1` — create the outbox table before touching the dispatcher.
**Trade-off:** one extra table and a polling loop, for durability with zero new infrastructure.

| Driver | Option 1: Postgres outbox | Option 2: SQS FIFO |
|---|---|---|
| `HC 1` 0 lost | ✅ row survives restart — `dispatch.ts:41` | ✅ broker durability |
| `HC 2` 0 out-of-order | ✅ ordered by id per merchant | ❌ ordering needs a group per merchant |
| `SP 1` p95 ≤ 2 s | ✅ 1.2 s — 500 ms poll | ✅ 0.3 s |
| `SP 2` no new component | ✅ same database | ❌ new 24/7 component |
| `SP 3` ≤ $150/mo | ✅ $0 incremental | ❌ ~$2,000/mo FIFO |

Winner's driver-impact rows — the evidence and confidence the matrix abbreviates:

| Driver | Mark | Measured value | Evidence | Confidence |
|---|---|---|---|---|
| `HC 1` | ✅ | 0 lost, 20 restarts | restart test | verified |
| `HC 2` | ✅ | 0 out-of-order, 10k replay | replay test | verified |
| `SP 1` | ✅ | 1.2 s p95 | load test | verified |
| `SP 2` | ✅ | 0 new components | ops review | verified |
| `SP 3` | ✅ | $0 incremental | cost model | inferred |

Change set: `C1` outbox table (`0042_webhook_outbox.sql`, new, verified) → `C2` insert in the event transaction (`dispatch.ts:41`, verified) → `C3` drain worker (`worker.ts`, new, inferred). Each carries verify and rollback rows in the Implementation Plan.

**Gate result**:

```
adr-webhook-01-durable-delivery.md — ACCEPT (12/12)
inferred: SP 3 cost model (no invoice yet). unverified: none.
```

What the gate caught before presentation: `SP 3` had no threshold until the driver was rewritten as an invoice delta, and Option 2's first draft was a *standard* SQS queue — G5 rejected it as a near-duplicate that silently failed `HC 2`.

---

## Accept ADRs

**Presented**: Option 1 survives a restart with zero new infrastructure and no new cost; the accepted cost is write amplification and a 1.2 s latency floor. Option 2 is faster but needs a message group per merchant — ~$2,000/month plus a new on-call surface. One claim stays inferred: the cost delta.

**User**: "Adopt Option 1. Fine on the cost estimate."

`Status: adopt`; problem `decided`. Handoff line: "Implementation need: outbox migration + worker — run `orchestrate-feature-delivery`."

No `solution.md`, no `scope.md` — neither had a consumer.
