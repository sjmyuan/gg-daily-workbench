# Example: Rework That Risks Exceeding the Feature Scope

**Scenario**: A rework is requested for a delivered feature, but the rework would change behavior the original plan listed under **Must not change**. Demonstrates **define-scope-boundary** and the rework guard — refuse and ask, never write silently.

**Applies**: **define-scope-boundary**, **rework-plan-convention**

## User Request

"We found a defect in the delivered checkout rework: on partial payment failure the compensating rollback retries with wrong credentials. Investigate and fix it."

## Boundary Check

Original boundary (from the existing `plan.md`):

```
## Scope Boundary
**May change**: wallet-service `application/` + `test/` behavior; `adr-wallet-01-payment-failure-handling.md` payment-failure decision
**Expected files**: wallet application + tests (advisory)
**Must not change**: `payment-gateway/` client behavior; `adr-cutover-01-service-cutover.md` cutover; other modules
```

The rework request changes `payment-gateway/` credential-retry behavior — **Must not change**.

## Refusal + Decision Options

The rework is a material change to the original boundary, so the planner refuses to write silently and presents options:

> "This rework changes `payment-gateway/` credential-retry behavior, which is **Must not change** (original boundary). Options: (a) extend the boundary to include `payment-gateway/` credential handling, (b) keep it out and file a follow-up feature, (c) treat it as a new feature cell `F2-r2` instead of a rework."

**User decision**: (a) extend the boundary for this rework only.

## Rework File (Boundary Updated)

The rework is written as a new sibling `rework-2026-08-10.md`; the original `plan.md` is never modified. It inherits the original boundary, tightened and extended per the user decision:

```markdown
# Rework 2026-08-10 — compensating rollback credential retry
Mode: post-merge   ·   Cell: order-service/F2-r1   ·   ADR focus: adr-wallet-01-payment-failure-handling.md

## Scope Boundary
**May change**: original **May change** + `payment-gateway/` credential-retry behavior (user-approved extension)
**Expected files**: original **Expected files** + `payment-gateway/` client (advisory)
**Must not change**: original **Must not change** otherwise unchanged

## Done means
| Criterion | Verification | Pass rule |
|---|---|---|
| Correct credentials selected on retry | payment-gateway tests | all pass |
| No change outside the extended boundary | diff against `main` | no changes |

## Steps
- [ ] Fix credential retry selection in compensating rollback
- [ ] Update payment-gateway client tests for partial failures
- [ ] Validate linting, formatting, type checking
```

`context.md` gains a `## Reworks` manifest row for this file; the rework carries only the delta and inherits the charter by reference. Original `plan.md` steps 1–N remain byte-for-byte unchanged.
