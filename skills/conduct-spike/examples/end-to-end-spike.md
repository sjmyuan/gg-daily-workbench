# Example: End-to-End Spike — Payment Service Migration

**Scenario**: The user wants to spike migrating a legacy payment processing service from a monolith to microservices, producing ADRs per decision problem and a consolidated solution document.

**Applies**: All capabilities in sequence — `define-spike-scope` → `investigate-per-area` → `compile-findings-doc` → `draft-problem-adrs` (option evaluation via `draft-adr`) → `compile-solution-doc`

**What makes this distinct**: Full multi-area brownfield spike, end to end (see `examples/multi-agent-investigation.md` for the parallel-dispatch variant).

---

## Define Spike Scope

### User Input
> "We need to spike migrating our payment processing service from the monolith to microservices. It handles credit card, bank transfer, and wallet payments. Currently it's a single Spring Boot app with ~200K LOC."

### Gate — clarify-the-ask, round 1

**Restatement**: "In your words: migrate the payment processing service from the monolith to microservices, and spike how. Inferred: (i) the goal is independent deployability, not a rewrite; (ii) all three payment types move; (iii) the spike decides architecture and migration, not a rollout date."

**Q1 · Scope · blocking** — "payment processing service" is one deployable or several.
  A) One service — a single boundary, one area
  B) Payment-type services — three boundaries, decomposition plus data split
Recommendation: B — the request names three payment types with different scaling needs.
Default if unanswered: none — blocking.

User: "Q1: B." → `ACCEPTED-WITH-ASSUMPTIONS`; A1 `Assumption (user-accepted, unverified)`: the spike ends at documents, not code — recorded in `scope.md` `## Accepted assumptions`.

### Assistant Output (after the gate)

**Spike Goal**: Determine the target architecture for decomposing the payment monolith into independently deployable services, selecting technologies, and defining a migration strategy.

**Areas and problems** (each problem → one ADR, recorded in `scope.md`):

| # | Area | Problems ("How to …?") |
|---|---|---|
| 1 | Service decomposition boundaries | How to split the monolith? |
| 2 | Inter-service communication | How to handle service-to-service communication? |
| 3 | Database decomposition strategy | How to break up the monolithic database? · How to migrate the schema safely? |
| 4 | Migration strategy | How to transition with zero downtime? |

---

## Investigate Per Area

*(investigate-code applied per area; evidence maps recorded)*

| Area | Current State | Key Constraint |
|---|---|---|
| 1. Service decomposition | Package-by-layer; CreditCard 40% / BankTransfer 30% / Wallet 25%; `PaymentOrchestrator` (1200 lines) couples all types | Redeploy on any change; wallet can't scale; 3 teams contend |
| 2. Inter-service communication | All in-process; external REST/gRPC/SOAP; no broker; no circuit breaker | No async experience; SOAP must stay |
| 3. Database decomposition | Single PostgreSQL ~80 tables; `transactions`/`accounts`/`audit_log` shared; 12 settlement stored procedures (2000+ lines) | No per-type access control; procs block decomposition |
| 4. Migration strategy | K8s (3 replicas); Kong routes `/api/payments/*`; GitHub Actions canary CI/CD | No feature flags or traffic splitting |

### Completion Checkpoint

> "Investigation complete — is this sufficient, or should we investigate further before formalizing?"
> User: "It's sufficient — let's formalize. We can dig into the orchestrator call graph after the first round of ADRs."

---

## Compile Findings Documents

*(one findings pair per area, always: `docs/findings-<area>.md` (human) + `docs/evidence-<area>.md` (evidence); four areas → four pairs, compiled concurrently.)*

| Findings human doc | Current-state orientation | Representative topic answers |
|---|---|---|
| `docs/findings-service-decomposition.md` | Monolithic Spring Boot app (~200K LOC), package-by-layer; `PaymentOrchestrator` (1200 lines) couples all types | Redeploy on any change; wallet can't scale; 3 teams contend |
| `docs/findings-communication.md` | All calls in-process; external REST/gRPC/SOAP; no broker; no circuit breaker | No async experience; SOAP must be maintained |
| `docs/findings-database.md` | Single PostgreSQL (~80 tables); `transactions`/`accounts`/`audit_log` shared; 12 settlement procedures | No per-type access control; procedures block decomposition |
| `docs/findings-migration.md` | K8s (3 replicas) behind Kong; GitHub Actions canary CI/CD; routes `/api/payments/*` | No feature flags or traffic splitting |

Each area's `evidence-<area>.md` holds the claim ledger (IDs, `file:line`, confidence) and searched-negatives.

**Cross-area constraints**: `docs/evidence-database.md` ↔ `docs/evidence-service-decomposition.md` (shared tables); `docs/evidence-communication.md` ↔ `docs/evidence-migration.md` (no async/traffic-split infra → migration starts synchronous).

> *Findings = a human explanation + an evidence doc per area; ADRs cite the evidence doc's stable IDs; the solution doc is authored target-state and references the evidence docs for evidence.*

---

## Draft Problem ADRs — Evaluate + Draft

*(Per problem, an `adr-writer` sub-agent runs the `draft-adr` flow headlessly from the drivers and findings carried in the brief; the orchestrator confirms each proposed chosen option. A whole area's problems share one brief when evidence is shared.)*

| Area → Problem | Options evaluated | Chosen Option |
|---|---|---|
| Service decomposition → split the monolith | A payment-type services · B domain-driven services · C strangler extraction | A — payment-type services + shared lib |
| Communication → service communication | A synchronous REST · B async events (Kafka) · C hybrid | C — REST for queries, Kafka for commands |
| Database → break up the database | A DB per service · B shared DB + views · C event-driven sync | A — DB per service, phased from Wallet |
| Database → migrate the schema safely | A expand-contract · B central tool · C shared DB + views | A — expand-contract migrations |
| Migration → zero-downtime migration | A strangler fig · B parallel run · C big-bang | A — strangler fig, Wallet first |

**ADR output** (`adrs/`, each tagged with its `Area:`): `adr-service-decomposition-01-split-monolith.md`, `adr-communication-01-service-communication.md`, `adr-database-01-break-up-database.md`, `adr-database-02-schema-migration.md`, `adr-migration-01-zero-downtime-migration.md`.

Example — `adr-service-decomposition-01-split-monolith.md` (abridged; full record per `draft-adr`'s template):

```markdown
# 2026-10-24-Decompose Payment Monolith into Payment-Type Microservices

* Status: draft
* Area: Service decomposition
* Owners: adr-writer · reviewed by the payment team
* Date: 2026-10-24

## Context and Problem Statement

**Decision:** Split the monolith into Wallet, Bank Transfer, and Credit Card services?

The monolith couples three independent payment domains, preventing independent deployment and scaling.

## Decision Outcome

**Chosen:** "Option A: payment-type services" — independent deploy/scale with a shared utility library.

## Consequences

**Trade-off:** independent delivery for shared-lib coupling.

### Risks

* Shared library becomes a coordination point

## Decision Drivers

* Maintain 99.9% SLA
* No payment-data loss
* Align with existing teams
* Prefer incremental migration
```

---

## Compile Solution Doc

*(write-solution-doc applied — target-state, decision-only; each ADR decision mirrored into the canonical sections.)*

**Solution Document**: `solution.md`
- §2 System Topology (C4 Model): C2 — API Gateway → Wallet, Bank Transfer, Credit Card services, each with its own DB; Kafka event bus; C3 per service
- §3 Interaction Details: payment initiation, settlement, and migration sequences
- §4 API / Event Schema: REST contracts for queries, Kafka topic schemas for events
- §8 RAID Analysis: risks (data consistency), assumptions (Kafka adoption), issues (SOAP legacy); §9 RACI per service

**Final bundle**: `scope.md` · `adrs/` (5 area-prefixed ADRs) · `solution.md` · `docs/findings-<area>.md` + `docs/evidence-<area>.md` (4 pairs).

### Wrap-Up (conversation level — not written into any artifact)

> All five chosen options are adopted into the solution doc, each mirrored in the canonical section it governs. `scope.md` remains the only area-grouped view. If an ADR decision changes during review, the affected solution-doc section is rewritten in place. Artifacts version together in `spikes/payment-migration/` (see `examples/spike-artifact-layout.md`).
