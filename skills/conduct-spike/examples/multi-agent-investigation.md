# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: A 4-area spike on migrating a legacy payment service. Each area is one `spike-area-analyst` session running investigate → findings pair → ADRs; phases run in parallel across areas.

**Applies**: `define-spike-scope` → `investigate-per-area` (phase 1) → `compile-findings-doc` (phase 2) → `draft-problem-adrs` (phase 3) → `compile-solution-doc`

**What makes this distinct**: It shows only the **dispatch mechanics** — one brief per area, what each phase returns, and when the orchestrator resumes a session versus re-dispatches it. The areas, evidence, and ADRs are the payment-migration artifacts already walked through in `examples/end-to-end-spike.md`; they are not repeated here.

---

## Define Spike Scope

Same payment-migration problem and 4 areas as `examples/end-to-end-spike.md` (service decomposition · communication · database — 2 problems · migration). The user confirms → one area brief per area, dispatched concurrently.

---

## Phase 1 — INVESTIGATE (PARALLEL DISPATCH)

### Orchestrator: Prepare Briefs

4 self-contained briefs, one per area, each with `Phase stop: 1`. The orchestrator first inventories its own context — scope dialog, `scope.md`, anything it already read or searched — then fills each brief with absolute paths, digests of what is already known, and the callee intake record. No findings pair exists yet, so this phase seeds the evidence map (see `reference/area-analyst-brief.md`).

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
- Phase stop (inline): 1
- Intake record (inline): system acme/payment-service · scope packages/payment/**,**/settlement
  · depth call chains to file:line · consumer this area's findings pair
- Known locations (digest): PaymentOrchestrator.java:1-1200, package-by-layer layout under
  packages/payment — located during scope dialog, not to be re-discovered
- Already searched (digest): "module" in packages/ → no Maven/Gradle modules; do not repeat
- First pass: no findings pair yet — build the evidence map from scratch
```
A thin four-line brief would send each analyst hunting for its own scope, its own input files, and searches the orchestrator had already run.

### Orchestrator: Dispatch

> "Dispatching phase 1 of 4 area sessions to sub-agents in parallel."

### Analysts Return

Four receipts, each carrying an evidence map (entry points, `file:line`, call chains, verdicts, searched-negatives) and a search log. The orchestrator verifies each at **single-pass** depth on an independent seat.

Cross-area consistency: A + C both flag tight coupling; B + D both note missing migration infrastructure; no contradictions. Pause: "Is the investigation complete, or continue in a new direction?"

---

## Phase 2 — COMPILE THE PAIR (RESUME EACH SESSION)

> "Resuming all 4 area sessions for phase 2."

Each brief now carries `Phase stop: 2` plus the area's own phase-1 receipt. The analyst writes `docs/findings-<area>.md` then `docs/evidence-<area>.md` from the evidence it already holds — it does not re-read or re-investigate. Each returns the pair paths, the topic list, and the ledger count; the orchestrator verifies at **fidelity** depth and confirms the topic list at the pause.

**Cross-area constraints**: `docs/evidence-service-decomposition.md` ↔ `docs/evidence-database.md` (shared `transactions`/`accounts`/`audit_log`); `docs/evidence-communication.md` ↔ `docs/evidence-migration.md` (no async/traffic-split infra → migration starts synchronous).

> If a session cannot be resumed: re-dispatch the analyst with the written pair and the phase-2 receipt — never a blank brief.

---

## Phase 3 — DRAFT ADRs (RESUME EACH SESSION)

### Orchestrator: Collect Drivers

The orchestrator asks the user for each problem's decision drivers (99.9% SLA; no data loss; align with existing teams) — the analyst never prompts the user.

### Orchestrator: Dispatch

> "Resuming 4 area sessions for phase 3 — 5 ADRs."

**Brief 1 — Service decomposition, phase 3** (excerpt):
```
## 3. Inputs
- Phase stop (inline): 3
- Findings pair (path): docs/findings-service-decomposition.md + docs/evidence-service-decomposition.md
  — treat Verified claims as settled; dig only into Gap/Inconsistency/Inferred claims
- Decision drivers (inline): 99.9% SLA; no data loss; align with existing teams
- Candidate options (inline): payment-type services; domain-driven services; strangler extraction
- Cross-area constraints (path): docs/evidence-database.md; docs/evidence-communication.md
- Prior phase receipt (inline): pair written, 34 ledger claims, 0 open gaps

## 4. Tasks
- Load draft-adr; drivers → options → evaluation (detail-options-tech) → compile
- One ADR tagged Area: Service Decomposition
```

### Analysts Return

5 ADRs, one per problem (the database area batches its two problems in one session). Each receipt names the chosen option, the evidence IDs it rests on, and any assumption-dependent decision. The orchestrator verifies load-bearing decisions with the **full loop**, then pauses: "Would you like to adjust any ADR before compiling the solution document?"

---

## Compile Solution Doc — SINGLE-TASK DISPATCH

*(One unit synthesizing all ADRs — single-task dispatch, for context preservation rather than parallelism. The brief carries the business context, the 4 findings pairs, the decisions digest, and `Phase stop` is not used.)*

> "Dispatching solution-doc compilation to a sub-agent."

**Final bundle**: `scope.md` · 4 findings pairs · 5 ADRs · `solution.md` (decision-only).

**Takeaway**: the evidence map crosses **zero** agent boundaries — it becomes the pair and the ADRs inside one session. The orchestrator's cost is one brief per area plus a phase receipt; the saving is every re-read and re-search the old three-hop handoff paid for.
