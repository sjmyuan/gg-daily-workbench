# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: A 4-area spike on migrating a legacy payment service; investigation and ADR drafting go to sub-agents in parallel.

**Applies**: `define-spike-scope` → `investigate-per-area` (parallel dispatch) → `compile-findings-doc` → `draft-problem-adrs` (parallel dispatch, evaluation via `draft-adr`) → `compile-solution-doc`

**What makes this distinct**: Parallel sub-agent orchestration — independent work units dispatched concurrently, then synthesized. Dispatch is the default for all spikes; parallel speed is secondary (see `reference/multi-agent-orchestration.md`).

## Define Spike Scope

*(As in `examples/end-to-end-spike.md` — the same payment migration problem with 4 areas.)*

| # | Area | Problem ("How to …?") |
|---|---|---|
| 1 | Service decomposition boundaries | How to split the monolith? |
| 2 | Inter-service communication | How to handle service-to-service communication? |
| 3 | Database decomposition strategy | How to break up the monolithic database? · How to migrate the schema safely? |
| 4 | Migration strategy | How to transition with zero downtime? |

> *User confirms. 4 areas → parallel dispatch for investigation (per area) and ADR drafting (per problem).*

---

## Investigate Per Area — PARALLEL DISPATCH

### Orchestrator: Prepare Briefs

4 self-contained briefs, one per area. The orchestrator first inventories its own context — scope dialog, `scope.md`, anything it already read or searched — then fills each brief with absolute paths, digests of what is already known, and the callee intake record. Every brief requires a per-area evidence map; no findings pair exists yet, so this round seeds it (see `reference/dispatch-briefs.md`).

**Brief 1 — Service decomposition** (excerpt of sections 2–3; full shape per `reference/investigation-brief.md`):
```
## 2. Context
- Spike goal (path + digest): /work/acme/spikes/payment-migration/scope.md
  — can the monolith be split without breaking settlement? Completion: a decision per area.
- Area: Service decomposition — bounded contexts, package deps, ownership
- Boundaries (inline): payment-service only; SOAP gateway and settlement batch are out of scope
- Accepted assumptions (digest): A1 → zero downtime is required for wallet traffic
- Mode: brownfield

## 3. Inputs
- Intake record (inline): system acme/payment-service · scope packages/payment/**,**/settlement
  · depth call chains to file:line · consumer this area's findings pair
- Known locations (digest): PaymentOrchestrator.java:1-1200, package-by-layer layout under
  packages/payment — located during scope dialog, not to be re-discovered
- Already searched (digest): "module" in packages/ → no Maven/Gradle modules; do not repeat
- First pass: no findings pair yet — build the evidence map from scratch
```
Four thin briefs would send each sub-agent hunting for its own scope, its own input files, and searches the orchestrator had already run.

### Orchestrator: Dispatch

> The orchestrator detects that code-exploration sub-agents are available and dispatches all 4 briefs concurrently.
> "Dispatching investigation of 4 areas to sub-agents in parallel for faster completion."

### Sub-Agents Return

| Agent | Current State | Constraints |
|---|---|---|
| A — Service decomposition | Package-by-layer; CreditCard 40% / BankTransfer 30% / Wallet 25%; `PaymentOrchestrator` (1200 lines) | Redeploy on any change; wallet can't scale; 3 teams contend |
| B — Inter-service communication | All in-process; external REST/gRPC/SOAP; no broker, no circuit breaker | No async experience; SOAP must stay |
| C — Database decomposition | Single PostgreSQL ~80 tables; `transactions`/`accounts`/`audit_log` shared; 12 settlement procs | Procs block migration; cross-type queries |
| D — Migration strategy | K8s (EKS) 3 replicas; Kong routes `/api/payments/*`; GH Actions canary CI/CD | No traffic splitting; canaries untested for routing |

### Orchestrator: Synthesize

> All 4 returned. Cross-area consistency: A + C both flagged tight coupling; B + D both noted missing migration infrastructure; no contradictions. Each area's verified evidence map is handed to `compile-findings-doc`.

---

## Compile Findings Documents

*(one findings pair per area, always; four pairs dispatched concurrently, each area's evidence map recorded in its evidence doc.)*

### `docs/evidence-communication.md` (excerpt — full schema per `document-findings`)

**Current State**: all calls in-process; external REST/gRPC/SOAP; no message broker; no circuit breaker.
**Constraints**: no async experience on team; SOAP contract must stay.

**Claim ledger**:

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|
| communication/present#c1 | Circuit breaker around external calls? | No | `grep "CircuitBreaker\|Resilience4j\|fallback"` across `payment-service` — no matches | ❓ Gap |
| communication/present#c2 | All internal calls in-process? | Yes | `PaymentOrchestrator.java:88` | ✅ Verified |

**Searched-negatives**: `grep -ri "kafka\|rabbit\|mq"` in `payment-service` — no broker usage.

*(The other three pairs follow the same shape.)*

**Cross-area constraints**: `docs/evidence-service-decomposition.md` ↔ `docs/evidence-database.md` (shared `transactions`/`accounts`/`audit_log`); `docs/evidence-communication.md` ↔ `docs/evidence-migration.md` (no async/traffic-split infra → migration starts synchronous).

---

## Draft ADRs — PARALLEL DISPATCH

*(Each problem's ADR is drafted headlessly by an `adr-writer` sub-agent from the drivers and findings carried in the brief; a whole area's problems share one brief. The orchestrator confirms each proposed chosen option afterward.)*

**Chosen Options Summary**:

| Area → Problem | Chosen Option |
|---|---|
| Service decomposition → split the monolith | Payment-type services (Wallet, Bank Transfer, Credit Card) |
| Inter-service communication → service communication | Hybrid: REST for queries, Kafka events for commands |
| Database decomposition → break up the database | Database per service, phased by payment type |
| Database decomposition → migrate the schema safely | Expand-contract migrations |
| Migration strategy → zero-downtime migration | Strangler Fig, starting with Wallet payments |

### Orchestrator: Prepare Briefs

4 briefs — one per problem, except the database area batches both of its problems into one brief since they share evidence:

**Brief 1 — ADR for Service Decomposition (problem: split the monolith)**:
```
Produce ADR for problem: How to split the monolith? (Area: Service Decomposition)  [path: /work/acme/spikes/payment-migration/scope.md]
Intake record (inline): system acme/payment-service · scope packages/payment/** · depth file:line · consumer this ADR
Decision drivers (inline): 99.9% SLA; no data loss; align with existing teams
Candidate options (inline): A) Payment-type services — clear ownership, independent scaling; shared-lib coupling. B) Domain-driven services — cleaner dependencies; team restructuring. C) Strangler extraction — lowest risk; temporary hybrid complexity.
User context (inline): each team owns a payment type; wallet scaling is the pain
Cross-area constraints (path): docs/evidence-database.md (shared transactions/accounts/audit_log); docs/evidence-communication.md (SOAP must stay)
Evidence doc (path): docs/evidence-service-decomposition.md — claim ledger; cite locations, never re-read code
Known locations (digest): PaymentOrchestrator.java:88 routes by payment type; coupling in packages/payment/shared
Load draft-adr; produce the ADR tagged Area: Service Decomposition.
```

### Orchestrator: Dispatch

> "Dispatching ADR drafting for 4 areas to sub-agents in parallel."

### Sub-Agent Results

**`adr-service-decomposition-01-split-monolith.md`**: Payment-type services
**`adr-communication-01-service-communication.md`**: Hybrid sync/async
**`adr-database-01-break-up-database.md`**: Database per service
**`adr-database-02-schema-migration.md`**: Expand-contract
**`adr-migration-01-zero-downtime-migration.md`**: Strangler Fig

### Orchestrator: Synthesize

> All 5 ADRs reviewed: decomposition + database are consistent; communication + migration are complementary; migration cross-references decomposition correctly. No conflicts — presenting for review.

## Compile Solution Doc — SINGLE-TASK DISPATCH

*(One unit synthesizing all ADRs — single-task dispatch, for context preservation rather than parallelism. The brief carries the business context, the 4 findings pairs, and the decisions digest.)*

> "Dispatching solution-doc compilation to a sub-agent."

**Final bundle**: `scope.md` · 4 findings pairs · 5 ADRs · `solution.md` (decision-only).

**Takeaway**: the orchestrator's cost is the brief, the sub-agent's cost is the search — a complete brief (digests, known locations, intake record, absolute paths) is what keeps the second one from paying twice.
