# Example: Multi-Area Spike With Dispatch

**Scenario**: "Decide how to take payment processing out of the monolith — settlement, wallet, and reconciliation are the pain points."

**Applies**: `define-spike-scope` → `decide-spike-problems` (3 area sessions dispatched concurrently) → `accept-adrs` → `produce-optional-artifact` (architecture overview, consumer named).

**What makes it distinct**: ≥2 areas cross the dispatch threshold. The ADR set is reviewed once; notes are declined; the overview is produced because delivery starts next.

---

## Define Spike Scope

The request names three pain points, so the fast path does not apply. One gate confirmation carries the proposed split and each problem's drivers.

**`scope.md`** (abridged to its tables):

| ID | Area | Problem | Status | ADR |
|---|---|---|---|---|
| P1 | Settlement | How to isolate settlement processing from the monolith? | open | — |
| P2 | Settlement | How to preserve settlement ordering during the move? | open | — |
| P3 | Wallet | How to split wallet balance ownership from the shared ledger? | open | — |
| P4 | Reconciliation | How to keep reconciliation correct across two systems? | open | — |

Drivers: `HC 1` no double-settle (0 duplicates in a replay); `HC 2` settlement order preserved (0 inversions); `SP 1` zero downtime for the cutover; `SP 2` reconciliation within 5 minutes. User accepted with one assumption: the ledger stays in the monolith for year one.

**Dispatch decision**: 3 areas, each with code spanning 2 subsystems → one area session each, dispatched concurrently. Scope stays in the orchestrator.

**Roles resolved once**: no project agent is scoped to these areas, so each area session runs on `code-analyst` with `investigate-code` + `draft-adr`, writing only under `adrs/`; a project agent that matched an area would take that seat instead.

---

## Decide Spike Problems

Each area session gets the brief from **scale-and-dispatch** (drivers inline, known locations, rejected options) and returns once, after its ADRs pass the gate.

**Area: Settlement** — returned `adr-settlement-01-isolate-processing.md` and `adr-settlement-02-preserve-ordering.md`; one claim left **unverified** (queue throughput at 2× peak) with the load test named as what would settle it.

**Area: Wallet** — `adr-wallet-01-balance-ownership.md`. Returned `REVISE` on the first gate run: `SP 1` had no threshold, and the cards evaluated only the winner. The re-dispatch carried the two failing IDs and the ADR path; the second return passed 12/12.

**Area: Reconciliation** — `adr-reconciliation-01-cross-system-correctness.md`.
Cross-area conflict flagged: the chosen sync reconciliation reads the wallet ledger directly, contradicting Wallet's decision to move ownership out.
The orchestrator verifies both sides in-session — two reads, no new session — and sends the constraint back to Reconciliation.

**Cross-area conflict** surfaced to the user before review: "Reconciliation assumed a shared ledger; Wallet is splitting it. Reconciliation will be rewritten to consume wallet events. That adds ~2 weeks to the reconciliation change set. Continue?"

| ADR | Chosen option | Gate |
|---|---|---|
| `adrs/adr-settlement-01-isolate-processing.md` | Option 2: strangler extraction, settlement first | ACCEPT |
| `adrs/adr-settlement-02-preserve-ordering.md` | Option 1: outbox with per-account ordering | ACCEPT, 1 unverified (throughput) |
| `adrs/adr-wallet-01-balance-ownership.md` | Option 1: ledger-per-wallet with dual-write window | ACCEPT |
| `adrs/adr-reconciliation-01-cross-system-correctness.md` | Option 3: event-sourced reconciliation | ACCEPT after rewrite |

Four ADRs, four problems, no findings pair. Evidence lives in each ADR's citations — the settlement ADRs cite `settlement/SettlementBatch.java:112` and `settlement/OrderKey.java:34`; nothing required a separate document.

---

## Accept ADRs

**Presented once, decisions first**:

- Settlement goes first via strangler — slowest option, but the only one that keeps `HC 1` provable at each step.
- Ordering is preserved by a per-account outbox; throughput at 2× peak stays unverified — the user accepted it, with the load test scheduled before the cutover.
- Wallet takes ledger ownership with a dual-write window; the accepted cost is a temporary consistency gap, bounded to 6 hours.
- Reconciliation moves to events, which adds ~2 weeks but removes the shared-ledger assumption.

**User**: "Adopt all four. Schedule the load test before cutover."

All four `Status: adopt`; P1–P4 `decided`; area status derived `done`. Unverified throughput recorded in the handoff line for delivery.

---

## Produce Optional Artifact

**Request**: "Delivery kicks off Monday — I need the target-state picture, not another decision doc."

Consumer named (delivery planning), so:

1. Dispatch `solution-doc-writer` with the four ADR paths, their cited evidence, and the audience.
2. Instruct it to reference each ADR for the decision and restate none — the overview carries topology, interaction sequences, and RAID only.
3. Verify fidelity: no changed chosen option, no invented component; one correction (the overview drew a shared ledger, contradicting Wallet's ADR).
4. Save as `solution.md`; link it in the handoff.

**Declined**: no separate current-state doc — each ADR already cites what it needs. Saying so took one line.

**Handoff**: ADR paths → feature rows; `solution.md` → `## Spike References`; P2's unverified throughput and the cutover load test → the delivery cell's context.
