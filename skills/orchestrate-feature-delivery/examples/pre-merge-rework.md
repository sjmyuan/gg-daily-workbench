# Example: Pre-Merge Rework — Sibling Rework File on an Unmerged Cell

**Scenario**: `order-service/F4` is **in-progress** — **execute-plan** finished the implementation and committed locally, but the branch is not yet pushed and no PR opened (per **branch-and-push-conventions**). Reviewing the unmerged diff, the team finds a defect: the checkout flow maps a payment-gateway timeout to the wrong error code — an implementation bug, not a flawed decision. The user says: "We found a bug in the unmerged checkout work — fix it before we push."

**Applies**: **handle-post-implementation-issue** → **update-delivery-index**

## 1. Identify scope + status

- Affected cell: `order-service/F4` — status **in-progress** (implemented, not pushed/merged)
- Governing decision: `adr-wallet-01-payment-failure-handling.md` (payment failure handling) — **not challenged**; only the timeout error mapping is wrong
- Mode: **pre-merge rework** (see **rework-modes**) — same append-only rule as post-merge, but the rework stays on this cell (no new feature/wave)

## 2. Write the sibling rework file (never modify the original)

`plan-development-task` writes a new sibling `deliveries/wallet-migration/order-service/order-wallet-integration/rework-2026-08-08.md` — `plan.md` is the frozen original and never gains a section:

```markdown
# Rework 2026-08-08 — checkout timeout error mapping
**Mode**: pre-merge · **Cell**: order-service/F4
**Branch**: `1234-f4` (existing cell branch)
**ADR focus**: `adr-wallet-01-payment-failure-handling.md`

## Scope Boundary
**May change**: checkout timeout → error-code mapping behavior in the unmerged F4 work
**Expected files**: checkout mapping + its tests (advisory)
**Must not change**: other ADR decisions, other modules
**Protected zones**: none added

## Done means
| Criterion | Verification | Pass rule |
|---|---|---|
| Timeout maps to the documented error code | checkout timeout test | pass |

## Steps

### Step 1: Write the failing timeout test ⏳
**Objective**: Reproduce the wrong error code for a payment-gateway timeout.
**Files**: `CheckoutIntegrationTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: New case asserts the documented timeout error code.
**Validation**: Test compiles and fails on the current mapping.
**Status**: ⏳ Pending

### Step 2: Fix the timeout mapping ⏳
**Objective**: Map gateway timeouts to the documented error code.
**Files**: `CheckoutErrorMapper.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: Replace the generic mapping branch for timeouts.
**Validation**: Step 1 test passes; checkout suite green.
**Status**: ⏳ Pending

### Step 3: Quality gate ⏳
**Objective**: Confirm the delta meets repo quality gates.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run linting, formatting, type checking, and the full suite.
**Validation**: All checks exit 0.
**Status**: ⏳ Pending
```

The rework file carries only the delta — trigger, Scope Boundary, Done means, changed steps. It inherits the cell's charter by reference and never creates a second `context.md`.

`context.md` gains a `## Reworks` manifest row:

```markdown
## Reworks
| Date | Mode | Cell | Trigger | File | Status |
|---|---|---|---|---|---|
| 2026-08-08 | pre-merge | F4 | checkout timeout error mapping | rework-2026-08-08.md | ⏳ |
```

Original `plan.md` steps 1–N remain byte-for-byte unchanged.

## 3. Execute the rework file

- Dispatch the **executor** (**execute-plan**) to run **only** `rework-2026-08-08.md` on the unmerged branch; original steps are never re-run or modified.
- No push/PR — the branch stays local until the user approves.

## 4. Update the index

| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| order-service/F4 | 1234-f4 | — | d4e5f6a | in-progress | executor | deliveries/wallet-migration/order-service/order-wallet-integration/ |

`F4` keeps its identity and **in-progress** status — no `F4-r1`, no new wave, and no index change; the sibling `rework-2026-08-08.md` (listed in the `context.md` manifest) is the only record of the rework.

## 5. Next actions

The executor asks before pushing and opens the PR (per **branch-and-push-conventions**); after the rework + original work merge, `F4` → **done** and its downstream cells unlock.
