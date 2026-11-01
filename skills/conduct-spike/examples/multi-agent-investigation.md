# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: A 4-area spike on migrating a legacy payment service; investigation and ADR drafting go to sub-agents in parallel.

**Applies**: `define-spike-scope` → `investigate-per-area` (parallel dispatch) → `compile-findings-doc` → `draft-problem-adrs` (parallel dispatch, evaluation via `draft-adr`) → `compile-solution-doc`

**What makes this distinct**: It shows only the **dispatch mechanics** — how an independent unit becomes a self-contained brief, and how returned units are synthesized. The areas, evidence, and ADRs are the payment-migration artifacts already walked through in `examples/end-to-end-spike.md`; they are not repeated here.

---

## Define Spike Scope

Same payment-migration problem and 4 areas as `examples/end-to-end-spike.md` (service decomposition · communication · database — 2 problems · migration). The user confirms → 4 areas mean parallel dispatch for investigation (per area) and ADR drafting (per problem).

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
A thin four-line brief would send each sub-agent hunting for its own scope, its own input files, and searches the orchestrator had already run.

### Orchestrator: Dispatch

> The orchestrator detects that code-investigation sub-agents are available and dispatches all 4 briefs concurrently, stating each brief's model.
> "Dispatching investigation of 4 areas to sub-agents in parallel."

### Sub-Agents Return

Four evidence maps (entry points, `file:line`, call chains, verdicts, searched-negatives) plus search logs. Cross-area consistency: A + C both flag tight coupling; B + D both note missing migration infrastructure; no contradictions. Each area's verified evidence map is handed to `compile-findings-doc`.

*(Returned current-state facts and constraints are the ones listed in `examples/end-to-end-spike.md`; the parallel path changes only how they are gathered.)*

---

## Compile Findings Documents

*(one findings pair per area, always — four pairs dispatched concurrently, each area's evidence map recorded in its evidence doc per `reference/findings-doc-compilation.md`.)*

Each pair follows the shape in `reference/findings-document-guide.md`. **Cross-area constraints**: `docs/evidence-service-decomposition.md` ↔ `docs/evidence-database.md` (shared `transactions`/`accounts`/`audit_log`); `docs/evidence-communication.md` ↔ `docs/evidence-migration.md` (no async/traffic-split infra → migration starts synchronous).

---

## Draft ADRs — PARALLEL DISPATCH

*(Each problem's ADR is drafted headlessly by an `adr-writer` sub-agent from the drivers and findings carried in the brief; a whole area's problems share one brief. The orchestrator confirms each proposed chosen option afterward. Chosen options: the five in `examples/end-to-end-spike.md`.)*

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

### Orchestrator: Synthesize

> All 5 returned ADRs reviewed: decomposition + database are consistent; communication + migration are complementary; migration cross-references decomposition correctly. No conflicts — presenting for review.

## Compile Solution Doc — SINGLE-TASK DISPATCH

*(One unit synthesizing all ADRs — single-task dispatch, for context preservation rather than parallelism. The brief carries the business context, the 4 findings pairs, and the decisions digest.)*

> "Dispatching solution-doc compilation to a sub-agent."

**Final bundle**: `scope.md` · 4 findings pairs · 5 ADRs · `solution.md` (decision-only).

**Takeaway**: the orchestrator's cost is the brief, the sub-agent's cost is the search — a complete brief (digests, known locations, intake record, absolute paths) is what keeps the second one from paying twice.
