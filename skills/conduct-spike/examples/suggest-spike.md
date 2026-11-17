# Example: Suggest a Spike From an Unsettled ADR

**Scenario**: The user is about to finalize an ADR choosing a feature-flag SDK. "The SDK evaluates locally, so p95 stays under 50 ms — let's adopt it."

**Applies**: `suggest-spike` → `define-spike-scope` (one problem) → `decide-spike-problems` → `accept-adrs`.

**What makes it distinct**: The ADR exists but its deciding claim is unmeasured. The skill offers a bounded spike instead of adopting on assertion — and the measurement reverses the choice.

---

## Detect and Offer

| Signal | Present? | Evidence |
|---|---|---|
| unverified assumption | **Yes** | "evaluates locally" is asserted, never measured on the edge runtime |
| missing measurement | **Yes** | `HC 1` p95 ≤ 50 ms has no measured value |
| unknown feasibility | No | The SDK exists and is supported |
| undecidable comparison | No | Only one option named so far |

The driver is hard: `HC 1` p95 flag evaluation ≤ 50 ms at the edge. The ADR's card shows `✅ 30 ms — vendor docs` — vendor documentation, not this runtime.

**Offer**: "This ADR's hard constraint rests on a vendor number, not a measurement on our edge runtime. A bounded spike — one problem, a measurement, one ADR — would settle it in about an hour and needs no code changes. Want it?"

**User**: "Yes, measure it before we adopt."

No spike starts without that confirmation; a declined offer leaves the claim tagged **unverified** and the risk surfaced at adoption.

---

## Define Spike Scope

Fast path, no `scope.md`:

| Field | Value |
|---|---|
| Question | How to meet p95 ≤ 50 ms for flag evaluation at the edge? |
| Driver | `HC 1` p95 ≤ 50 ms at 100 rps; `SP 1` no new 24/7 component |
| Options | Option 1: vendor local SDK · Option 2: edge-cached evaluation |
| Boundaries | Read the edge runtime and the vendor SDK only; no implementation |

One gate confirmation, one problem, no notes doc.

---

## Decide Spike Problems

Two reads and one measurement:

1. `edge/runtime.ts:22` — the edge handler runs in a V8 isolate with 128 MB; no background timers.
2. `edge/middleware/flags.ts:14` — a cached snapshot is already fetched per request; the SDK would sit in the same path.
3. Measurement — the SDK's cold evaluation on the isolate: p95 **180 ms**, because each isolate initializes its own store.

That single number fails `HC 1` and makes Option 1 unviable. Option 2 evaluates from the already-fetched snapshot: p95 **4 ms**, no new component.

**File**: `adrs/adr-flags-01-edge-evaluation.md` — full template, `Status: draft`.

**Decision spine**:

| Driver | Option 1: vendor local SDK | Option 2: edge-cached evaluation |
|---|---|---|
| `HC 1` p95 ≤ 50 ms | ❌ 180 ms measured — cold isolate init | ✅ 4 ms measured — snapshot already fetched |
| `SP 1` no new 24/7 component | ✅ managed | ✅ no new component |

**Gate result**: `ACCEPT (12/12)` | unverified: none — `HC 1` is now a measurement, not a vendor claim.

The old draft's `✅ 30 ms — vendor docs` row is deleted, not footnoted: the measurement replaced it.

---

## Accept ADRs

**Presented**: the vendor SDK fails the hard constraint by 3.6× on this runtime; cached evaluation clears it at 4 ms and adds no component. The cost is losing the vendor's targeting UI for this path, which the user accepts.

**User**: "Adopt Option 2, and record the 180 ms number — we'll re-evaluate the SDK if they ship a shared store."

`Status: adopt`; problem `decided`; the measurement and the re-evaluate condition go into Consequences and one handoff line.

**Why the spike paid**: one hour, two reads, one measurement — and it prevented an adopted decision that could not meet its own hard constraint.
