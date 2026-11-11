# Example: Compiled ADR — Database Selection

**Scenario**: The document produced by **compile-adr** at the end of the database-selection walkthrough. Shows a complete template instance: measured drivers, an evidence-backed matrix, a full option card, the chosen option's implementation plan, and the abridged sibling cards.

**Applies**: `compile-adr`; input walkthrough in [database-selection.md](database-selection.md).

```markdown
# 2026-07-04-Database-Selection-for-Order-Management-Service

* Status: draft
* Owners: Alice (Tech Lead)
* Date: 2026-07-04

## Context and Problem Statement

**Decision:** Cloud SQL for PostgreSQL — the only option meeting every hard constraint.

The service handles ~10,000 orders/day on GCP and must support complex order-history queries and ACID payment transactions. Which managed database satisfies all constraints within an early-stage budget?

![C4 context diagram: customer, order service, database candidate, payment processor, GCP IAM, with volumes and protocols](diagrams/context.png)

## Decision Outcome

**Chosen:** "Option 1: Cloud SQL for PostgreSQL" — passes all three hard constraints; $380/month and zero ramp-up.
**Start here:** `C1` — add the PostgreSQL driver, then `C2` datasource config.

![C4/flowchart: target state — order service on Cloud SQL PostgreSQL; PgBouncer NEW, read replica NEW](diagrams/solution.png)

## Consequences

**Trade-off:** manual scaling work at 10× growth for lower cost and zero ramp-up.

### Risks

* Connection pooling needed past ~50 concurrent writes
* Read replicas introduce lag on history reads
* Vertical ceiling forces migration at 10× growth

### Security

* Cloud SQL supports IAM, private IP, and encryption in transit and at rest
* Encrypt customer PII at the application layer before storage

## Decision Drivers

* `HC 1` ACID payment writes — 100% atomic rollback
* `HC 2` Lookup latency — p99 < 100ms at 10K orders/day
* `HC 3` GCP integration — managed, private-IP reachable
* `SP 1` PostgreSQL expertise — no training before launch
* `SP 2` Cost — ≤ $400/month invoiced
* `SP 3` Managed operations — GCP handles patching and backups

## Considered Options

* Option 1: Cloud SQL for PostgreSQL
* Option 2: Cloud Spanner
* Option 3: Firestore

| Driver | Option 1: Cloud SQL (PG) | Option 2: Cloud Spanner | Option 3: Firestore |
|---|---|---|---|
| `HC 1` ACID payment writes | ✅ full transactions | ✅ full transactions | ❌ no cross-collection txns |
| `HC 2` p99 < 100ms | ✅ 40ms | ✅ 38ms | ✅ 55ms |
| `HC 3` GCP integration | ✅ native | ✅ native | ✅ native |
| `SP 1` PostgreSQL expertise | ✅ 4 of 6 | ❌ none | ⚠️ partial |
| `SP 2` ≤ $400/month | ⚠️ $380 | ❌ $600+ | ✅ $120 |
| `SP 3` Managed operations | ✅ | ✅ | ✅ |

## Evaluation of the Options

### Option 1: Cloud SQL for PostgreSQL

#### Verdict

Recommended — passes `HC 1`–`HC 3`; cheapest zero-ramp-up fit.

#### What it is

A fully managed PostgreSQL instance on GCP, reached over private IP by a single Spring Boot service.

#### How it works

1. Service connects over JDBC through a sidecar connection pooler.
2. Payment writes run as one PostgreSQL transaction against the `payments` schema.
3. Order-history reads hit the primary; replica reads serve reporting.

#### Driver impact

| Driver | Mark | Measured value | Evidence | Confidence |
|---|---|---|---|---|
| `HC 1` ACID payment writes | ✅ | Full transaction support | PostgreSQL docs, rollback test | verified |
| `HC 2` p99 < 100ms | ✅ | p99 40ms on 1M seeded orders | Load test 2026-07-02 | verified |
| `HC 3` GCP integration | ✅ | Native private-IP managed service | GCP console | verified |
| `SP 1` PostgreSQL expertise | ✅ | 4 of 6 engineers use it daily | Team survey | verified |
| `SP 2` ≤ $400/month | ⚠️ | $380/month | GCP calculator | inferred |
| `SP 3` Managed operations | ✅ | Automated backups and patching | Provider feature list | verified |

#### Concerns

| Concern | This option |
|---|---|
| New infrastructure | 1 primary instance, 1 read replica, 1 pooler sidecar |
| Interfaces touched | JDBC datasource only; no API change |
| Data and consistency | Single-node ACID; replicas eventually consistent |
| Failure behaviour | Primary failover ~60s; writes rejected, reads fail over |
| Operational load | GCP patching; team owns connection-pool tuning |
| Cost model | $380/month now; +$240 per replica |
| Migration cost | Greenfield — schema created, no data to move |

#### Pros

* Moves `SP 1` — team has zero ramp-up
* Moves `HC 1` — full SQL transactions

#### Cons

* Moves `SP 2` negatively past ~50 concurrent writers
* Moves `HC 2` negatively once the single node saturates

#### Tech Details

No service code exists yet — every location below is **unverified**.

**Code changes:**

1. **`C1` — `build.gradle` dependencies** (unverified)
   - Current: no PostgreSQL driver declared.
   - How: add `org.postgresql:postgresql:42.7.4` to `implementation`.
2. **`C2` — `application.yml` datasource block** (unverified)
   - Current: no datasource block.
   - How: set `spring.datasource.url`, `username`, `password` from Secret Manager; `maximum-pool-size: 20`.
3. **`C3` — `db/migration/V1__orders.sql`** (unverified, new file)
   - How: create `orders` and `payments` tables with the FK and the `(customer_id, created_at)` index.

**New files:** `V1__orders.sql` — initial schema.
**Config / dependencies:** `spring.datasource.*`; PostgreSQL driver.
**Data changes:** schema creation only; no backfill.
**Tests affected:** add `OrderRepositoryIT` against a Testcontainers PostgreSQL.

### Option 2: Cloud Spanner

#### Verdict

Dropped — fails `SP 1` (no experience) and `SP 2` ($600+/month).

#### What it is

A globally distributed, strongly consistent relational database on GCP.

#### How it works

Shards data across regions and serves ACID transactions at horizontal scale.

#### Pros

* Moves `HC 2` — no sharding needed at any volume
* Moves `HC 1` — external consistency

#### Cons

* Moves `SP 2` negatively — $600+/month minimum
* Moves `SP 1` negatively — zero team experience

### Option 3: Firestore

#### Verdict

Dropped — fails `HC 1`: no cross-collection transactions.

#### What it is

A serverless NoSQL document database on GCP.

#### How it works

Stores JSON-like documents per collection and syncs clients in real time.

#### Pros

* Moves `SP 2` — $120/month at current volume
* Moves `SP 3` — fully serverless

#### Cons

* Moves `HC 1` negatively — no cross-collection transactions
* Moves `HC 2` negatively — no JOINs, application-side assembly

*(Options 2 and 3 abridged: Verdict, What it is, How it works, Pros, and Cons shown; Driver impact, Concerns, and Tech Details follow the Option 1 shape.)*

## Implementation Plan

**Order:** `C1` → `C2` → `C3`; safe to stop after `C2` — schema lands with the first test run.
**Prerequisites:** Cloud SQL instance and replica provisioned, database created, Secret Manager entry for credentials, pooler sidecar added to the deployment.

| ID | Change | Location | Depends on | Verify | Rollback |
|---|---|---|---|---|---|
| `C1` | PostgreSQL driver | `build.gradle` | — | `./gradlew dependencies` resolves 42.7.4 | Revert commit |
| `C2` | Datasource config | `application.yml` | `C1` | `OrderRepositoryIT` connects | Revert commit |
| `C3` | Initial schema | `db/migration/V1__orders.sql` | `C2` | Flyway migrates on boot; `OrderRepositoryIT` passes | Drop schema |

**New files:** `V1__orders.sql` — initial schema.

## References
```
