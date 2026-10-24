# Example: Reworking a Delivered Feature After a Post-Implementation Issue

**Scenario**: `order-service/F2` is **done** (merged). Integration testing reveals a defect: the delivered checkout flow mishandles partial payment failures — the decision in `adr-wallet-01-payment-failure-handling.md` assumed the payment gateway rejects atomically, which is false. The user says: "We found an issue in the delivered checkout rework — investigate and fix it."

**Applies**: **handle-post-implementation-issue** → **update-delivery-index**

## 1. Identify scope + suggest skill routing

- Affected cell: `order-service/F2` (done) · governing decision: `adr-wallet-01-payment-failure-handling.md` (payment failure handling)
- **Triage (L3)**: the gateway assumption is invalid and compensating-failure **options must be compared** — one of the L3 triggers. A single decision tweak would be L2.
- Focused spike scope: `adr-wallet-01-payment-failure-handling.md` only — the rest of the epic is not re-opened.
- Skill-routing suggestion presented to the user before dispatch:

| Step | Agent | Skill |
|---|---|---|
| Triage | orchestrator (L3 by trigger) | **triage-issue** |
| Focused spike on `adr-wallet-01-payment-failure-handling.md` | **spike-conductor** | **conduct-spike** |
| ADR revision (decision changes) | **adr-writer** | **draft-adr** |
| Solution-doc refresh (target state changes) | **solution-doc-writer** | **write-solution-doc** |
| Write rework plan | **planner** | **plan-development-task** |
| Execute rework plan | **executor** | **execute-plan** |

## 2. Focused spike

- Dispatch **spike-conductor** scoped to `adr-wallet-01-payment-failure-handling.md`: validate the payment-gateway assumption and compare compensating-failure options.
- Result: `adr-wallet-01-payment-failure-handling.md` revised (decision changes to compensating transactions); the solution doc's §2 System Topology and §3 Interaction Details updated.

## 3. Update the delivery index

| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| order-service/F2 | 1234-f2-wallet | #42 (merged) | e5f6a7b | done | — | deliveries/wallet-migration/order-service/wallet-service/ |
| order-service/F2-r1 | — | — | — | unplanned | — | deliveries/wallet-migration/order-service/wallet-service/rework-2026-08-08.md |

The index records state + pointers — F2's status stays **done**, its branch + merged PR stay recorded; the Features table records `Rework of: F2` for `F2-r1`, and the rework's spike focus and steps live in the sibling rework file (see §4).

New **Wave 3**: `F2-r1` (after F2 merged). The rework traces to the revised `adr-wallet-01-payment-failure-handling.md`.

## 4. Write the rework plan (never modify the original)

`plan-development-task` writes a new sibling `deliveries/wallet-migration/order-service/wallet-service/rework-2026-08-08.md` — the existing `plan.md` is the frozen original and never gains a section:

```markdown
# Rework 2026-08-08 — compensating transactions on partial payment failure
**Mode**: post-merge · **Cell**: order-service/F2-r1
**Branch**: `rework-f2r1-compensating-transactions` off `main`
**ADR focus**: `adr-wallet-01-payment-failure-handling.md`

## Scope Boundary
**May change**: wallet-service `application/` + `test/` behavior; compensating-transaction rollback per the revised ADR decision
**Expected files**: wallet application + tests (advisory)
**Must not change**: other ADRs, other modules
**Protected zones**: none added

## Done means
| Criterion | Verification | Pass rule |
|---|---|---|
| Partial failure rolls back atomically | checkout integration test | pass |

## Steps

### Step 1: Write failing partial-failure tests ⏳
**Objective**: Reproduce a non-atomic rollback and misclassified gateway error.
**Files**: `CheckoutIntegrationTest.java`, `PaymentGatewayClientTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New tests assert atomic compensation and a compensable partial failure.
**Validation**: Tests compile and join the suite.
**Status**: ⏳ Pending

### Step 2: Confirm test failure (RED) ⏳
**Objective**: Prove both tests fail for the expected reasons.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run only the new tests.
**Validation**: Fail on partial-state and retry-classification assertions — not errors.
**Status**: ⏳ Pending

### Step 3: Add compensating rollback ⏳
**Objective**: Roll back atomically when a partial payment fails.
**Files**: `WalletApplicationService.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Replace the best-effort compensation with a compensating transaction.
**Validation**: Integration test passes; wallet suite green.
**Status**: ⏳ Pending

### Step 4: Update gateway error mapping ⏳
**Objective**: Map partial-failure gateway errors to the compensation path.
**Files**: `PaymentGatewayClient.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Classify partial failures as compensable instead of retryable.
**Validation**: Gateway test passes; existing gateway tests green.
**Status**: ⏳ Pending

### Step 5: Quality gate ⏳
**Objective**: Confirm the delta meets repo quality gates.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run linting, formatting, type checking, and the full suite.
**Validation**: All checks exit 0.
**Status**: ⏳ Pending
```

The rework file carries only the delta — trigger, Scope Boundary, Done means, changed steps. It inherits the cell's charter (`Why`, `Must hold`, `Pointers`) by reference and never creates a second `context.md`.

`context.md` gains a `## Reworks` manifest row:

```markdown
## Reworks
| Date | Mode | Cell | Trigger | File | Status |
|---|---|---|---|---|---|
| 2026-08-08 | post-merge | F2-r1 | partial-payment failure handling (ADR revised) | rework-2026-08-08.md | ⏳ |
```

Original `plan.md` steps 1–N remain byte-for-byte unchanged.

## 5. Execute the rework plan

- Dispatch **execute-plan** to run **only** `rework-2026-08-08.md`; completed original steps are never re-run.

## 6. Next actions

- After execution, update the index (`F2-r1` → in-progress → done after PR merge); the executor handles push approval and PR creation.
- Pre-merge variant: when the cell is implemented but not yet pushed/merged (status **in-progress**), the rework is still **append-only** (implemented steps never modified) but stays on the same cell — see **examples/pre-merge-rework.md**.
