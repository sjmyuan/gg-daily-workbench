# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: A 4-area spike on migrating a legacy payment service. Each area is one `spike-area-analyst` session that investigates, writes its findings pair, drafts its ADRs, and returns once; the areas run concurrently.

**Applies**: `define-spike-scope` → `investigate-per-area` (single return: pair + ADRs) → `compile-findings-doc` (confirm) → `draft-problem-adrs` (review) → `compile-solution-doc`

**What makes this distinct**: It shows only the **dispatch mechanics** — one brief per area, what the single return carries, and how feedback re-dispatches a session. The areas, evidence, and ADRs are the payment-migration artifacts already walked through in `examples/end-to-end-spike.md`; they are not repeated here.

---

## Define Spike Scope

Same payment-migration problem and 4 areas as `examples/end-to-end-spike.md` (service decomposition · communication · database — 2 problems · migration). The user confirms → one area brief per area, dispatched concurrently.

---

## Collect Drivers

Before dispatching, the orchestrator asks the user for each problem's decision drivers (99.9% SLA; no data loss; align with existing teams) and the candidate options already considered. The analyst drafts ADRs in the same session and never infers a driver; a missing driver blocks the dispatch.

---

## Dispatch — INVESTIGATE + PAIR + ADRs (PARALLEL, SINGLE RETURN)

### Orchestrator: Prepare Briefs

4 self-contained briefs, one per area. The orchestrator first inventories its own context — scope dialog, `scope.md`, anything it already read or searched — then fills each brief with absolute paths, digests of what is already known, the drivers, and the callee intake record. No findings pair exists yet, so each analyst investigates from scratch, writes the pair, drafts the ADRs, and returns once — no intermediate return (see `reference/area-analyst-brief.md`).

**Brief 1 — Service decomposition** (excerpt of sections 2–3):
```
## 2. Context
- Spike goal (path + digest): /work/acme/spikes/payment-migration/scope.md
  — can the monolith be split without breaking settlement? Completion: a decision per area.
- Area: Service decomposition — bounded contexts, package deps, ownership
- Boundaries (inline): payment-service only; SOAP gateway and settlement batch are out of scope
- Accepted assumptions (digest): A1 → zero downtime is required for wallet traffic
- Mode: brownfield

## 3. Inputs
- Return (inline): once, after the ADRs — the written pair and the ADRs together
- Intake record (inline): system acme/payment-service · scope packages/payment/**,**/settlement
  · depth call chains to file:line · consumer this area's pair and ADRs
- Known locations (digest): PaymentOrchestrator.java:1-1200, package-by-layer layout under
  packages/payment — located during scope dialog, not to be re-discovered
- Already searched (digest): "module" in packages/ → no Maven/Gradle modules; do not repeat
- Decision drivers (inline): 99.9% SLA; no data loss; align with existing teams
- Candidate options (inline): payment-type services; domain-driven services; strangler extraction
```
A thin four-line brief would send each analyst hunting for its own scope, its own input files, and searches the orchestrator had already run.

### Orchestrator: Dispatch

> "Dispatching 4 area sessions to sub-agents in parallel — one return each."

### Analysts Return

Four written pairs (`docs/findings-<area>.md` + `docs/evidence-<area>.md`) and 5 ADRs, one per problem (the database area batches its two problems in one session). Each receipt carries the pair paths, topic list, ledger count, ADR paths, and the chosen option per problem with its evidence IDs.

### Orchestrator: Verify

One independent seat per returned unit: the pair at **single pass + fidelity** — material code claims against primary sources, IDs, counts, and `file:line` consistent with the ledger; each load-bearing ADR at the **full loop** — chosen-option fit plus any new code claims.

Cross-area consistency: A + C both flag tight coupling; B + D both note missing migration infrastructure; no contradictions.

---

## Confirm and Review (NO NEW DISPATCH)

Each pair is structurally validated and cross-referenced per `reference/findings-document-guide.md`, then confirmed with the user: "Does this accurately capture the current state?"

**Cross-area constraints**: `docs/evidence-service-decomposition.md` ↔ `docs/evidence-database.md` (shared `transactions`/`accounts`/`audit_log`); `docs/evidence-communication.md` ↔ `docs/evidence-migration.md` (no async/traffic-split infra → migration starts synchronous).

The user reviews the ADRs after delivery: "Review the decisions; would you like any adjusted before compiling the solution document?" Feedback re-dispatches the affected area session with the artifacts — it revises in place, and the orchestrator re-verifies only the changed claims.

> If a session fails before writing its artifacts: re-dispatch it with the same brief and its search log — a written pair and ADRs are the only acceptable return.

---

## Compile Solution Doc — SINGLE-TASK DISPATCH

*(One unit synthesizing all ADRs — single-task dispatch, for context preservation rather than parallelism. The brief carries the business context, the 4 findings pairs, and the decisions digest.)*

> "Dispatching solution-doc compilation to a sub-agent."

**Final bundle**: `scope.md` · 4 findings pairs · 5 ADRs · `solution.md` (decision-only).

**Takeaway**: the evidence map never crosses an agent boundary unpersisted — the pair and ADRs are written inside the session that built the evidence and leave in one return. The orchestrator's cost is one brief per area; the saving is every re-read and re-search the old four-hop handoff paid for.
