# Example: Compiled ADR — Database Selection

**Scenario**: Output of **compile-adr** for the database-selection walkthrough: a complete template instance, one full option card and two abridged.

**Applies**: `compile-adr`; input walkthrough in [database-selection.md](database-selection.md).

```markdown
# 2026-07-04-Database-Selection-for-Order-Management-Service

* Status: draft
* Owners: Alice (Tech Lead)
* Date: 2026-07-04

## Context and Problem Statement

**Problem:** Which managed database serves order history and ACID payments within an early-stage budget?

The service handles ~10,000 orders/day on GCP and needs complex order-history queries with ACID payment writes. ACID writes, sub-100ms lookups, and a ≤$400/month budget rarely hold together on managed GCP services. Which managed database satisfies all constraints within an early-stage budget?

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

Greenfield: no service code exists, so each diff is added-only and every entry stays **unverified** until the first build.

**Code changes:**

1. **`C1` — `build.gradle` dependencies** (unverified)
   - Current: JPA and H2 declared, no PostgreSQL driver.
   - Diff:
     ```diff
     diff --git a/build.gradle b/build.gradle
     --- a/build.gradle
     +++ b/build.gradle
     @@ -18,3 +18,4 @@ dependencies {
          implementation 'org.springframework.boot:spring-boot-starter-web'
          implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
     +    implementation 'org.postgresql:postgresql:42.7.4'
          runtimeOnly 'com.h2database:h2'
     ```
   - How: add the PostgreSQL driver to `implementation`.
2. **`C2` — `application.yml` datasource block** (unverified)
   - Current: `spring` carries `application.name` only.
   - Diff:
     ```diff
     diff --git a/src/main/resources/application.yml b/src/main/resources/application.yml
     --- a/src/main/resources/application.yml
     +++ b/src/main/resources/application.yml
     @@ -1,3 +1,9 @@
      spring:
        application:
          name: order-service
     +  datasource:
     +    url: jdbc:postgresql://${DB_HOST}:5432/orders
     +    username: ${DB_USER}
     +    password: ${DB_PASSWORD}
     +    hikari:
     +      maximum-pool-size: 20
     ```
   - How: values from Secret Manager; pool at 20 until load data says otherwise.
3. **`C3` — `db/migration/V1__orders.sql`** (unverified, new file)
   - Diff:
     ```diff
     diff --git a/db/migration/V1__orders.sql b/db/migration/V1__orders.sql
     new file mode 100644
     --- /dev/null
     +++ b/db/migration/V1__orders.sql
     @@ -0,0 +1,12 @@
     +CREATE TABLE orders (
     +  id           BIGSERIAL PRIMARY KEY,
     +  customer_id  BIGINT NOT NULL,
     +  total_cents  BIGINT NOT NULL,
     +  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
     +);
     +CREATE TABLE payments (
     +  id        BIGSERIAL PRIMARY KEY,
     +  order_id  BIGINT NOT NULL REFERENCES orders(id),
     +  status    TEXT NOT NULL
     +);
     +CREATE INDEX orders_customer_created ON orders (customer_id, created_at);
     ```

**New files:** `V1__orders.sql` — initial schema, added-only diff under `C3`.
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

*(Options 2–3 abridged: Driver impact, Concerns, and Tech Details follow Option 1's shape.)*

## Implementation Plan

**Order:** `C1` → `C2` → `C3`; safe to stop after `C2` — schema lands with the first test run.
**Prerequisites:** Cloud SQL instance and replica provisioned, database created, Secret Manager entry for credentials, pooler sidecar added to the deployment.

| ID | Change | Location | Depends on | Verify | Rollback |
|---|---|---|---|---|---|
| `C1` | PostgreSQL driver | `build.gradle` | — | `./gradlew dependencies` resolves 42.7.4 | Revert commit |
| `C2` | Datasource config | `application.yml` | `C1` | `OrderRepositoryIT` connects | Revert commit |
| `C3` | Initial schema | `db/migration/V1__orders.sql` | `C2` | Flyway migrates on boot; `OrderRepositoryIT` passes | Drop schema |

**New files:** `V1__orders.sql` — initial schema.

```
