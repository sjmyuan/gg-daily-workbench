# Example: Spike from Existing Investigation Findings

**Scenario**: The user has already done informal investigation on a caching strategy problem and has notes. They want to formalize the findings into ADRs and a solution document without re-doing the investigation.

**Applies**: `define-spike-scope` → `compile-findings-doc` → `draft-problem-adrs` (option evaluation via `draft-adr`) → `compile-solution-doc` (skipping `investigate-per-area`; compile-findings-doc formalizes the provided findings)

## Define Spike Scope

### User Input
> "I've already looked into our caching problem. Here's what I found: [pastes notes]. Can you help me turn this into proper ADRs and a solution doc?"

### Assistant Output

*(Reviews the provided notes, then works through scope definition)*

**Spike Goal**: Define a caching strategy for the product catalog service to reduce database load and improve response times.

**Areas and problems** (derived from the user's notes, recorded in `scope.md`):

| # | Area | Problem ("How to …?") |
|---|---|---|
| 1 | Cache topology | How to position caches in the architecture? (application-level, distributed, CDN) |
| 2 | Cache invalidation strategy | How to keep cached data consistent with the source of truth? |

## Compile Findings Documents

*(compile-findings-doc applied to the user's pre-existing notes — one findings pair per area, always: `docs/findings-<area>.md` (human) + `docs/evidence-<area>.md` (evidence). Two areas → two pairs, compiled via `document-findings`.)*

### Cache topology — human doc `docs/findings-cache-topology.md` (excerpt)

```markdown
---
title: Findings: Cache topology
area: cache-topology
status: investigating
---

# Findings: Cache topology

**Summary:** The product catalog read path queries PostgreSQL directly; no cache exists at any tier.

## 3. Is there a caching layer today?
**TL;DR:** No — the read path queries PostgreSQL directly.
```

### Cache topology — evidence doc `docs/evidence-cache-topology.md` (excerpt — full schema per `document-findings`)

```markdown
<!-- evidence-doc
area: cache-topology
spike: caching-strategy
status: investigating
scope: current caching state of the product catalog service
related-areas: [cache-invalidation]
human-doc: docs/findings-cache-topology.md
-->
```

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|
| cache-topology/present#c1 | No cache exists at any tier | Yes | `ProductCatalogService.java:64` | ✅ Verified |
| cache-topology/present#c2 | Reads query PostgreSQL directly | Yes | `ProductRepository.java:112` | ✅ Verified |
| cache-topology/load#c1 | 200:1 read-to-write ratio; DB CPU >80% at peak; P99 450ms | Unverified | user notes | 💭 Assumption |
| cache-topology/infra#c1 | No Redis/ElastiCache infrastructure exists | Unverified | user notes | 💭 Assumption |

Coverage: caching tier, load profile, cache infrastructure. Searched-negatives: none (notes only).

### Cache invalidation — human doc `docs/findings-cache-invalidation.md` (excerpt)

**Is there any invalidation mechanism today?**
**TL;DR:** No caching tier exists, so no invalidation mechanism is present.

### Cache invalidation — evidence doc `docs/evidence-cache-invalidation.md` (excerpt)

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|
| cache-invalidation/present#c1 | No TTL, write-through, or event invalidation exists | No | `ProductCatalogService.java:64` | ✅ Verified |
| cache-invalidation/writes#c1 | All writes go to the single source of truth | Yes | `ProductRepository.java:130` | ✅ Verified |
| cache-invalidation/latency#c1 | Invalidation must not add write latency | Assumed | user notes | 💭 Assumption |

Coverage: invalidation mechanisms, write path. Cross-area reference: `docs/evidence-cache-topology.md`.

> *Findings formalized from your pre-existing notes: code-verifiable facts are ✅ Verified, note-only metrics remain 💭 Assumption. Evaluation will compare options against each area's constraints. No re-investigation was needed.*

## Draft Problem ADRs — Evaluate + Draft

*(Per problem, an ADR-writer sub-agent runs the full `draft-adr` flow — drivers → options → **evaluate-options** → compile-adr — interactively with the user, seeded from the provided notes. The evaluation tables below are the evaluate stage of each drafting session.)*

### Area 1: Cache Topology

| Option | Pros | Cons |
|---|---|---|
| **A: In-memory (Caffeine/Guava)** | Simplest; no network latency; no new infra | Per-instance; cold starts; memory contention with app |
| **B: Redis (ElastiCache)** | Shared cache; persistence; rich data structures | Network hop; new infra cost; operational overhead |
| **C: Two-tier (in-memory + Redis)** | Best latency for hot keys; resilience | Complexity; two sources of staleness; harder to debug |

**Chosen Option**: Option C (Two-tier) — in-memory Caffeine cache with 30s TTL for ultra-hot keys, backed by Redis cluster for shared cache with 5min TTL.

### Area 2: Cache Invalidation Strategy

| Option | Pros | Cons |
|---|---|---|
| **A: TTL-only** | Simplest; no coordination needed | Stale data window; wasted cache space |
| **B: Write-through** | Always consistent; good for read-heavy workloads | Write latency penalty; cache must be available for writes |
| **C: Cache-aside with CDC invalidation** | Eventual consistency; decoupled; no write penalty | Eventual consistency window; CDC pipeline complexity |

**Chosen Option**: Option C (Cache-aside with CDC) — services write to DB only; Debezium CDC captures changes and publishes invalidation events to Kafka; cache consumers listen and invalidate affected keys.

### ADR: Cache topology — position caches

*(draft-adr applied — full ADR produced; saved as `adr-cache-topology-01-position-caches.md`. Summary below; the full record follows `draft-adr`'s template with `Area: Cache topology` and `Status: draft`.)*

**Title**: Adopt Two-Tier Caching (In-Memory + Redis) for Product Catalog

**Status**: draft

**Problem**: The product catalog service experiences 10K reads/second with only 50 writes/second. Database CPU regularly exceeds 80% during peak traffic. A caching layer is needed to reduce database load and improve P99 latency (currently 450ms).

**Decision Drivers**:
- Hard: Must reduce DB CPU below 50%; Must maintain < 100ms P99 for cache hits
- Soft: Prefer solutions that don't require application restarts for cache changes

**Chosen:** Two-tier cache: application-level Caffeine (30s TTL) + Redis cluster (5min TTL)

The second ADR is saved as `adr-cache-invalidation-01-invalidate-cached-data.md` with the same template and `Area: Cache invalidation`.

## Compile Solution Doc

*(write-solution-doc applied)*

### Final Output Bundle

**Solution Document**: `solution.md`
- §2 System Topology: Product Catalog Service with Caffeine + Redis; CDC pipeline for invalidation
- §3 Interaction Details: read path (cache hit/miss) and write path (DB write → CDC → invalidation) sequences
- §4 API / Event Schema: API contracts unaffected (caching is transparent to callers)
- §8 RAID Analysis: risk of Redis outage, assumption about CDC pipeline reliability

**ADRs** (one per problem, area-prefixed in `adrs/`, each mirrored into the solution doc's canonical sections):
- `adr-cache-topology-01-position-caches.md` — Two-tier (Caffeine + Redis)
- `adr-cache-invalidation-01-invalidate-cached-data.md` — CDC-based

> *Wrap-up (conversation only): if ADR review exposes an investigation gap, re-run that area's investigation.*
