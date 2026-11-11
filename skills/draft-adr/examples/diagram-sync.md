# Example: Keeping ADR Diagrams Current After Mid-Session Corrections

**Scenario**: In an ADR session about choosing a message queue, the user corrects a decision driver and introduces a new option after evaluation has started, then reveals a new dead-letter/replay flow. This example shows how **sync-diagrams** updates the affected artifacts (driver table, option comparison matrix, elimination tree) and adds a new diagram for the newly revealed context, so the record never goes stale.

**Applies**: `sync-diagrams` — triggered whenever the user corrects previously confirmed content or reveals new context mid-session. It runs on top of whatever capability handled the change (here **evaluate-options**), not as part of the linear define-problem → compile-adr sequence.

---

## Starting state (already confirmed)

- **Problem**: Choose a message queue for an order-events pipeline (~50K msgs/day).
- **Drivers (confirmed)**:
  - Hard: at-least-once delivery, GCP integration, team familiarity with Kafka
  - Soft: low cost, managed service
- **Options (confirmed)**: Option 1: Apache Kafka (self-hosted); Option 2: Pub/Sub (GCP); Option 3: RabbitMQ
- **Evaluation so far**: Pub/Sub recommended; Kafka self-hosted dropped on operational cost; RabbitMQ dropped on throughput ceiling.

**Diagrams already in the session**:
1. C4 context diagram of the pipeline
2. Option comparison matrix + elimination tree

---

## Correction 1: New hard constraint + new option

**User input**:
> One correction — we missed a hard constraint: all message data must stay within EU data centers. And please also consider Redpanda, which the team has been prototyping.

**Agent response (applies evaluate-options + sync-diagrams)**:
> Noted — adding "EU data residency" as a hard constraint and Redpanda as Option 4. Let me re-evaluate Redpanda against the drivers, then sync the affected diagrams.

**Evaluation summary for Redpanda**:

| Driver | Option 4: Redpanda |
|---|---|
| At-least-once delivery | ✅ |
| GCP integration | ⚠️ (runs on GCP VMs, but not a managed GCP service) |
| EU data residency | ✅ (self-hosted in EU) |
| Team familiarity | ✅ (team has been prototyping) |
| Low cost | ⚠️ (infra cost, no license fee) |
| Managed service | ❌ (self-hosted) |

**Agent output — updated driver table**:
> Updated: added the "EU data residency" hard constraint. It enters the matrix below rather than a diagram of its own — a driver map would only re-encode this table.

| Tag | Driver | Threshold | Measured by |
|---|---|---|---|
| `HC 1` | At-least-once delivery | No lost message in the replay test | Consumer replay test |
| `HC 2` | GCP integration | Managed service reachable from the VPC | Private-IP connect |
| `HC 3` | EU data residency | 100% of message data stored in EU regions | Region config audit |
| `SP 1` | Team familiarity | No training before launch | Team survey |
| `SP 2` | Low cost | ≤ €300/month | Provider invoice |
| `SP 3` | Managed operations | Patching handled by the provider | Provider feature list |

**Agent output — updated comparison matrix + elimination tree**:
> Updated: Redpanda added to the matrix; Pub/Sub now fails the EU data residency hard constraint and is eliminated.

| Driver | Option 1: Kafka (self-hosted) | Option 2: Pub/Sub | Option 3: RabbitMQ | Option 4: Redpanda |
|---|---|---|---|---|
| At-least-once delivery | ✅ | ✅ | ✅ | ✅ |
| GCP integration | ✅ | ✅ | ✅ | ⚠️ |
| EU data residency | ✅ | ❌ (knock-out) | ✅ | ✅ |
| Team familiarity | ✅ | ✅ | ✅ | ✅ |
| Low cost | ⚠️ | ✅ | ✅ | ⚠️ |
| Managed service | ❌ | ✅ | ✅ | ❌ |

```mermaid
flowchart TD
    All["All options"] --> A["Option 1: Kafka (self-hosted)"]
    All --> B["Option 2: Pub/Sub"]
    All --> C["Option 3: RabbitMQ"]
    All --> D["Option 4: Redpanda"]
    B -->|"fails EU data residency"| X["Eliminated"]
    C -->|"throughput ceiling"| X
    D -->|"no managed service, partial GCP"| X
    A -->|"passes all hard constraints"| W["Chosen: Option 1"]
```

> The corrected picture now points to Kafka (self-hosted) as the recommendation, since it is the only option satisfying the new EU residency hard constraint — the recommendation flipped from Pub/Sub.

---

## New finding: dead-letter / replay flow

**User input**:
> Also worth noting: when a consumer fails repeatedly, messages should go to a dead-letter topic and be replayed later. Can we show that?

**Agent response (applies sync-diagrams — new context, no existing diagram covers it)**:
> This is new context not covered by the existing diagrams, so I'll add a new diagram for it:

```mermaid
flowchart TD
    A([Start]) --> B[Consumer processes message]
    B --> C{Process succeeds?}
    C -->|yes| D[Acknowledge message]
    D --> E([End])
    C -->|no| F{Retry budget exhausted?}
    F -->|yes| G[Route to dead-letter topic]
    G --> H[Alert on-call]
    H --> E
    F -->|no| I[Retry with backoff]
    I --> J[Requeue message]
    J --> E
```

> This dead-letter flowchart will be embedded in the ADR's Context section alongside the other diagrams.

---

## Final check (sync-diagrams step 4)

**Agent output**:
> Cross-check of the full artifact set:
> - C4 context diagram — unchanged, pipeline topology is unaffected ✅
> - Driver table — updated with the EU residency constraint ✅
> - Comparison matrix + elimination tree — updated with Redpanda and the flipped recommendation ✅
> - Dead-letter flow — new diagram covering the newly revealed context ✅
>
> Every confirmed fact now appears in a table or diagram, and no diagram contradicts the latest state.
