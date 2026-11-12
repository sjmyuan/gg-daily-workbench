# Example: One Orchestration Round with Parallel Agents

**Scenario**: The delivery index from **multi-repo-feature-decomposition** exists — 4 features, 3 waves, 5 cells, all **unplanned**. The user says: "Start delivering — dispatch agents."

**Applies**: **orchestrate-delivery** → **update-delivery-index**

## 1. Assess state

- **Wave 0**: `shared-contracts/F1` — ready (no deps, unplanned)
- **Wave 1**: `order-service/F2`, `api-gateway/F3` — wait for F1 (not yet ready)
- **Wave 2**: `order-service/F4`, `api-gateway/F4` — wait for F2 + F3

## 2. Dispatch — Phase 1 (planners only)

- **Planner A** → plan `shared-contracts/F1` (plan-development-task)
  - Inventory first: the ask and its gate record, the F1 index row, the ADR already read at decompose time, the branch convention detected in `shared-contracts`, and the absolute epic path.
  - Brief (excerpts; contract in `reference/dispatch-briefs.md`):
    ```
    Cell: shared-contracts/F1 — wallet-contracts · repo shared-contracts · wave 0
    Plan location (path): /work/acme/deliveries/wallet-migration/shared-contracts/wallet-contracts/
    Governing ADR (path + digest): /work/acme/spikes/wallet-migration/adrs/adr-wallet-01-payment-failure-handling.md
      — decided: retries + idempotency keys at the client; contract-first, no server change
    Solution doc (path): /work/acme/spikes/wallet-migration/solution.md §2 System Topology · §3 Interaction Details (wallet slice)
    Spike evidence (digest): evidence-wallet#c1 failure paths (PaymentOrchestrator.java:88),
      #c4 no circuit breaker — settled, do not re-investigate
    Intake record: type feature · expected behavior: shared DTOs + envelope · triggering input:
      consumer call sites in order-service · done criteria: solution §3 contract satisfied
    Branch convention (inline): <ticket>-<slug> in this repo · base: main
    Gating (inline): wave 1 cells wait on F1's contract; no conflict constraint
    ```
  - The planner starts from the decided contract instead of re-reading the ADR, the evidence doc, and the repo.

> **Plan-first gate**: no executor may touch `F1` until Planner A's `plan.md` exists on disk. The gate forbids the reverse order — never implement first and back-fill a plan.

## 3. Verify the gate + update index

- Planner A returns: `deliveries/wallet-migration/shared-contracts/wallet-contracts/plan.md` exists (verified on disk) → `F1` may advance.

| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| shared-contracts/F1 | 1234-f1-contracts | — | — | **planned** | planner-A | deliveries/wallet-migration/shared-contracts/wallet-contracts/ |

F2 and F3 become develop-ready (F1 planned; contract-first allows planning in parallel).

## 4. Dispatch — Phase 2 (executors + planners, gated)

- **Executor A** → execute `shared-contracts/F1` (execute-plan) — plan file verified
- **Planner B** → plan `order-service/F2`
- **Planner C** → plan `api-gateway/F3`

> **Delegation rule in action**: when any agent's plan or execution surfaces a solution-doc or ADR change, the orchestrator dispatches a **solution-doc-writer** / **adr-writer** agent.
> It never edits artifacts itself.

## 5. Verify the gate

F1's execution completes → the orchestrator applies **verify-cell**: a fresh **code-reviewer** gets the recorded range, `plan.md`, `context.md`, the governing ADR, and the cell digest.
It returns spec-compliance and trust verdicts.
F1 advances to **verified** (see **examples/cell-verification-gate.md**). Never mark a cell **done** without this gate.

## 6. Push approval + merge + update index

Per **delivery-layout**'s branch conventions, the executor pushes and opens the PR after user approval — F1 becomes **done** only after the PR merges with the recorded head commit.

| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| shared-contracts/F1 | 1234-f1-contracts | #1 | a1b2c3d | **done** | code-reviewer-A | deliveries/wallet-migration/shared-contracts/wallet-contracts/ |
| order-service/F2 | 1234-f2-wallet | — | — | **planned** | planner-B | deliveries/wallet-migration/order-service/wallet-service/ |
| api-gateway/F3 | 1234-f3-gateway | — | — | **planned** | planner-C | deliveries/wallet-migration/api-gateway/wallet-api-gateway/ |
| order-service/F4 | — | — | — | unplanned | — | — |
| api-gateway/F4 | — | — | — | unplanned | — | — |

## 7. Next actions

Verify F2 + F3 plan files, then execute both in parallel (develop-ready, no conflict); apply **verify-cell** to each on completion. With F1 **done**, F2 and F3 are now merge-ready.
F4 cells remain wave-2 until F2 + F3 merge. All status changes landed in the index before the next round was dispatched.
