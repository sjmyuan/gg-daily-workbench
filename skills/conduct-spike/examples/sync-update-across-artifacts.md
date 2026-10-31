# Example: Syncing All Artifacts After New Evidence Flips an ADR Decision

**Scenario**: A spike produced findings, `adr-communication-01-service-communication.md` (REST), and a solution doc. A follow-up prototype measures a 3K orders/sec REST throttle — below the 10K peak. The user asks to update the ADR. The assistant propagates the change through every downstream artifact so the whole bundle stays consistent.

**Applies**: `sync-update-artifacts`

**What makes this distinct**: Shows the full propagation — one change rippling through findings → ADR → solution doc — including the rewrite-in-place before/after shape (which the former `update-artifact-in-place.md` example showed in isolation).

---

## Context

Artifacts after the original spike:

- Findings doc: current state; peak load unmeasured (listed as an assumption)
- `adr-communication-01-service-communication.md`: "Synchronous REST" (chosen because it is the simplest option)
- Solution doc: target architecture with REST request/response contracts (communication decisions under the `Inter-service communication` area)

## The change (user request)

> "We measured the load in a prototype — REST throttles at 3K orders/sec, below the 10K peak. Update the ADR."

## Propagation trace (what the assistant determines)

| Origin | Affected downstream |
|---|---|
| Findings doc (new evidence: 3K/sec measured limit) | `adr-communication-01-service-communication.md` → solution doc §2 System Topology and §3 Interaction Details |

## What the assistant does, artifact by artifact

1. **Findings pair** (via `document-findings`): the evidence doc's ledger row for the peak-load claim moves from 💭 Assumption to ✅ Verified with `file:line`; the human doc's communication topic is revised to answer the measured question, and a new topic is added when no existing topic answers it.
2. **`adr-communication-01-service-communication.md`** (via `draft-adr`): decision changes to "Event-driven Kafka" — chosen option, justification, and consequences rewritten in place.

   **Before** (as drafted, abridged):
   ```markdown
   **Chosen:** "Synchronous REST" — the team is familiar with it and it is the simplest option.
   ```

   **After** (rewritten in place — old text deleted, not annotated):
   ```markdown
   **Chosen:** "Event-driven Kafka" — the measured 10K orders/sec peak exceeds REST's throttling limits, and Kafka provides the replay and redelivery semantics the audit path requires.
   ```
3. **Solution doc** (via `write-solution-doc`): §2 System Topology and §3 Interaction Details evolve from REST contracts to Kafka topics; C4/sequence diagrams updated; no "changed from REST" language.

## Consistency check

- [x] The communication ADR cites the measured 3K/sec fact from the evidence doc
- [x] Solution doc mirrors Kafka as the chosen option
- [x] No-note scan passes: no "changed from REST", "v2", or "Updated" in the ADR or solution doc

## What the assistant says (in conversation)

> "The prototype measured 3K/sec — below the 10K peak. I updated the findings pair with the measurement, flipped the communication ADR to Kafka in place, and refreshed the affected solution-doc sections and diagrams. All three artifacts now agree."

## What is deliberately absent from the artifacts

- No "Updated"/"v2"/"Previously" markers in the ADR or solution doc
- No change history inside the documents — git keeps it
- The delta exists only in conversation
