# Example: Mechanical Restore — Revert Retry Changes in `OrderPoller`

**Scenario**: Polling retries caused double submits; the user asks to undo the change and keep `OrderPoller` exactly as the base branch has it.
**Applies**: **plan-mechanical-restore**

## User Request

"The retry changes in `OrderPoller` caused double submits. Revert them and keep it same as main."

## Classification

Mechanical, not a bug fix. The target state exists at `origin/main`, so no behavior needs deriving.
A bug-fix route would produce a failing test plus a hand-written fix — a third version of the file.
Main holds no other change to these paths since the retry commit, so `base` is safe; otherwise `port` the commit.

## Source Declaration

| Path | `Source` | `Ref` | `Equality` |
|---|---|---|---|
| `src/poller/order_poller.ts` | `base` | `origin/main@3f2a1c8` | `identical` |
| `src/poller/order_poller.test.ts` | `base` | `origin/main@3f2a1c8` | `identical` |

Ladder: rung 1 (`no-op`) fails — a retry block exists. Rung 2 (`base`) reaches the target. Stop.

## Generated plan.md

```markdown
# Plan: revert-order-poller-retries — OrderPoller matches origin/main
**Type**: restore
**Branch**: `revert-order-poller-retries` off `main`
**TDD variant**: None — non-behavioral restore; an equality proof replaces RED/GREEN.

## Scope Boundary
**May change**: `OrderPoller` retry behavior only
**Must match**: `src/poller/order_poller.ts` @ `origin/main@3f2a1c8`
**Must match**: `src/poller/order_poller.test.ts` @ `origin/main@3f2a1c8`
**Expected files**: `src/poller/order_poller.ts`, `src/poller/order_poller.test.ts` (advisory)
**Must not change**: order submission contract, public API signatures
**Protected zones**: none added

## Steps

### Step 1: Restore OrderPoller from base ⏳
**Objective**: Make both poller files identical to the base ref.
**Files**: `src/poller/order_poller.ts`, `src/poller/order_poller.test.ts`
**Source**: base · origin/main@3f2a1c8 · identical
**Implementation**: `git restore --source=origin/main@3f2a1c8 -- src/poller/order_poller.ts src/poller/order_poller.test.ts`
**Validation**: `git diff --exit-code origin/main@3f2a1c8 -- <both paths>` is empty.
**Status**: ⏳ Pending

### Step 2: Confirm nothing else moved ⏳
**Objective**: Prove the restore is the only change and the suite is green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Inspect working-tree status for the plan's paths only.
**Validation**: `git status --porcelain` shows no other plan-path change; affected-area suite passes.
**Status**: ⏳ Pending
```

Non-behavioral justification: restores pre-existing behavior; no new behavior is introduced (see **tdd-guardrails**).

## Rejected Alternatives

| Rejected | Reason |
|---|---|
| Rewrite `OrderPoller` without retry logic | Produces a third version; the diff no longer equals the ref |
| Revert then refactor the poller | Ships an unrequested change inside a revert |
| Add a test asserting the revert | Asserts a non-behavior; the diff proof covers it |

## Validation

- [x] `Source` declared per path; `Ref` pinned to a SHA, not a branch
- [x] Cheaper rung reached at 2 of 5, with the cheaper rung's failure stated
- [x] `Must match` listed for both restored paths; protected zones explicit
- [x] No RED/GREEN step; the non-behavioral justification is recorded
- [x] Final step proves the restore and runs the suite
- [x] 2 steps — under the restore cap of 5
