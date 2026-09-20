# Example: Database Selection for a New Microservice

**Scenario**: The user is choosing a database for a new order-management microservice and wants a structured walkthrough. Demonstrates all 5 capabilities in sequence (**define-problem** → **define-decision-drivers** → **define-considered-options** → **evaluate-options** → **compile-adr**).

---

## Capability: define-problem

**User input**:
> We're building a new order-management microservice handling ~10K orders/day. We need to pick a database. It needs complex queries on order history, ACID transactions for payment, and it'll run on GCP.

**Agent output**:
> **Problem Statement**: Select a database for a new order-management microservice on GCP supporting ~10,000 orders/day, complex order-history queries, and ACID payment transactions.
>
> Does this accurately capture the problem?

**User confirms**: Yes.

**Agent output**:
> Here's the system context so we're aligned:
>
> ```mermaid
> C4Context
>     title Order Management — System Context
>
>     Person(customer, "Customer", "Places orders and queries order history")
>     System(oms, "Order Management Service", "Handles ~10K orders/day, ACID payments, storage backend TBD")
>     System_Ext(ps, "Payment Processor", "Charges payments")
>     System_Ext(iam, "GCP IAM", "AuthN / authZ")
>
>     Rel(customer, oms, "places orders / queries")
>     Rel(oms, ps, "payment processing")
>     Rel(oms, iam, "authN / authZ")
> ```

---

## Capability: define-decision-drivers

**User input**:
> Team knows PostgreSQL well, infra costs must stay low, order lookups under 100ms, and we're on GCP so managed services are preferred.

**Agent output**:
> Decision drivers, split into hard constraints and soft preferences:
>
> **Hard constraints**: (1) ACID transactions for payments; (2) query latency < 100ms; (3) GCP integration.
> **Soft preferences**: (4) team expertise (PostgreSQL); (5) low infrastructure cost; (6) managed service.
>
> Would you like to reorder or adjust these?

**User confirms**: Looks good.

**Agent output**:
> Confirmed decision-driver map:
>
> ```mermaid
> flowchart TD
>     Root["Decision drivers"] --> Hard["Hard constraints"]
>     Root --> Soft["Soft preferences"]
>     Hard --> H1["ACID transactions"]
>     Hard --> H2["Query latency < 100ms"]
>     Hard --> H3["GCP integration"]
>     Soft --> S1["Team expertise: PostgreSQL"]
>     Soft --> S2["Low infrastructure cost"]
>     Soft --> S3["Managed service"]
> ```

---

## Capability: define-considered-options

**User input**:
> We're thinking Cloud SQL (PostgreSQL), but should we consider others?

**Agent output**:
> Brainstorming alternatives: **industry-standard** — Cloud Spanner (global scale, strong consistency), Firestore (serverless NoSQL); **build vs. buy** — all managed, no build option; **incremental vs. big-bang** — start simple, migrate later.
>
> Proposed options:
>
> - Option 1: Cloud SQL for PostgreSQL — managed relational DB, full SQL, ACID
> - Option 2: Cloud Spanner — globally distributed, strong consistency
> - Option 3: Firestore — serverless NoSQL document DB, real-time sync
>
> Do these three cover the viable options?

**User confirms**: These three are good.

---

## Capability: evaluate-options

**Evaluating Option 1: Cloud SQL for PostgreSQL**

**User input**:
> Pros: team knows it, full ACID, flexible queries. Cons: read replicas at scale, connection limits.

**Agent output**:
> | Driver | Impact |
> |---|---|
> | ACID transactions ✅ | Full support — HC1 |
> | Query latency ✅ | Indexed queries well under 100ms — HC2 |
> | GCP integration ✅ | Native managed service — HC3 |
> | Team expertise ✅ | Team knows PostgreSQL — SP4 |
> | Cost ⚠️ | Reasonable; read replicas add cost — partial SP5 |
> | Managed service ✅ | Automatic backups — SP6 |
>
> **Verdict:** Recommended — satisfies all three hard constraints. Full card rendered in the final ADR below.
>
> Does this evaluation look accurate?

**User confirms**: Yes.

**Options 2 and 3** use the same card pattern; key results:
- **Option 2: Cloud Spanner** — ACID ✅, GCP ✅, managed ✅; **fails** team experience and cost.
- **Option 3: Firestore** — latency ✅, cost ✅, managed ✅; **fails** the ACID hard constraint.

**User confirms**: Spanner and Firestore are out.

**Agent output (after all options evaluated)**:
> Summary across all three options:
>
> | Driver | Option 1: Cloud SQL (PG) | Option 2: Cloud Spanner | Option 3: Firestore |
> |---|---|---|---|
> | ACID transactions | ✅ | ✅ | ❌ (knock-out) |
> | Query latency < 100ms | ✅ | ✅ | ✅ |
> | GCP integration | ✅ | ✅ | ✅ |
> | Team expertise | ✅ | ❌ | ⚠️ |
> | Low cost | ⚠️ | ❌ | ✅ |
> | Managed service | ✅ | ✅ | ✅ |
>
> Option 3 is eliminated by the ACID hard constraint; Option 2 fails cost and team expertise. Option 1 satisfies all hard constraints and 3/3 soft preferences.
>
> ```mermaid
> flowchart TD
>     All["All options"] --> A["Option 1: Cloud SQL for PostgreSQL"]
>     All --> B["Option 2: Cloud Spanner"]
>     All --> C["Option 3: Firestore"]
>     C -->|"fails ACID knock-out"| X1["Eliminated"]
>     B -->|"fails low cost + team expertise"| X2["Eliminated"]
>     A -->|"passes all hard constraints + 3/3 soft"| W["Chosen: Option 1"]
> ```
>
> **Given the evaluations, which option best satisfies the decision drivers?**

**User confirms**: Option 1.

---

## Capability: compile-adr

**Agent output**:
> Metadata: title, owners, and status?

**User input**:
> "Database Selection for Order-Management Service"; Alice (Tech Lead); draft.

**Agent loads reference/adr-template.md and produces**:

```markdown
# 2026-07-04-Database-Selection-for-Order-Management-Service

* Status: draft
* Owners: Alice (Tech Lead)
* Date: 2026-07-04

## Context and Problem Statement

**Decision:** Cloud SQL for PostgreSQL — the only option meeting all hard constraints.

The service handles ~10,000 orders/day on GCP and must support complex order-history queries and ACID payment transactions. Which managed database satisfies all constraints within an early-stage budget?

![C4 context diagram: customer, order management service, payment processor, GCP IAM](diagrams/context.png)

## Decision Outcome

**Chosen:** "Option 1: Cloud SQL for PostgreSQL" — the only option satisfying all three hard constraints (ACID, <100ms lookups, GCP) while meeting every soft preference.

![C4/flowchart: target state — order management service with Cloud SQL for PostgreSQL, PgBouncer, and read replica](diagrams/solution.png)

## Consequences

**Trade-off:** manual scaling work at 10× growth for lower cost and zero ramp-up.

### Risks

* Connection pooling needed if order volume grows significantly
* Read replicas introduce eventual consistency for reads
* Outgrowing Cloud SQL's vertical ceiling may force migration

### Security

* Cloud SQL supports IAM, private IP, and encryption in transit and at rest
* Encrypt customer PII at the application layer before storage

## Decision Drivers

* ACID transactions (hard constraint — payments)
* Query latency < 100ms (hard constraint)
* GCP integration (hard constraint)
* Team expertise in PostgreSQL (soft preference)
* Low infrastructure cost (soft preference)
* Managed service (soft preference)

## Considered Options

* Option 1: Cloud SQL for PostgreSQL
* Option 2: Cloud Spanner
* Option 3: Firestore

## Evaluation of the Options

### Option 1: Cloud SQL for PostgreSQL

#### Verdict

Recommended — satisfies all three hard constraints.

#### What it is

A fully managed PostgreSQL database on GCP.

#### How it works

Standard PostgreSQL with automated backups and replication; the service connects over JDBC.

#### Pros

* Team already knows PostgreSQL — zero ramp-up
* Full SQL + extensions cover all query patterns

#### Cons

* Connection pooling needed at scale
* Vertical scaling has an upper bound

### Option 2: Cloud Spanner

#### Verdict

Dropped — fails the cost and team-expertise drivers.

#### What it is

A globally distributed, strongly consistent relational database on GCP.

#### How it works

Shards data across regions and serves ACID transactions at horizontal scale.

#### Pros

* Unlimited horizontal scaling with no sharding
* 99.999% SLA for critical workloads

#### Cons

* Minimum cost prohibitive for early-stage ($600+/month)
* Team has zero experience; significant ramp-up

### Option 3: Firestore

#### Verdict

Dropped — fails the ACID hard constraint.

#### What it is

A serverless NoSQL document database on GCP.

#### How it works

Stores JSON-like documents per collection and syncs clients in real time; transactions cannot span collections.

#### Pros

* Serverless pricing ideal for early-stage
* Real-time sync enables live order-tracking features

#### Cons

* Fails ACID hard constraint — no cross-collection transactions
* No JOINs — application-level data assembly
```

**Agent output**:
> Here's the completed ADR. Would you like to adjust any section before saving?
