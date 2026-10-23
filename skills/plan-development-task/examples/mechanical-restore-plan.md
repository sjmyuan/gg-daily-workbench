# Example: Mechanical Restore Plan

**Scenario**: A user asks to undo a delivered change and keep the file exactly as the base branch has it, after polling retries caused double submits.

**Applies**: **plan-mechanical-restore**

## User Request

"The retry changes in `OrderPoller` caused double submits. Revert them and keep it same as main."

## Classify

Mechanical, not a bug fix. The target state exists at `origin/main`, so no behavior needs deriving.
Bug-fix routing would have produced a failing test plus a hand-written fix — a third version of the file.
Main holds no other change to these paths since the retry commit, so `base` is safe; otherwise `port` the commit.

## Source declaration

| Path | `Source` | `Ref` | `Equality` |
|---|---|---|---|
| `src/poller/order_poller.ts` | `base` | `origin/main@3f2a1c8` | `identical` |
| `src/poller/order_poller.test.ts` | `base` | `origin/main@3f2a1c8` | `identical` |

Ladder: rung 1 (`no-op`) fails — a retry block exists. Rung 2 (`base`) reaches the target. Stop.

## Output plan

```markdown
# Revert retry changes in OrderPoller

## Scope Boundary
**May change**: `OrderPoller` retry behavior only
**Must match**: src/poller/order_poller.ts @ origin/main@3f2a1c8
**Must match**: src/poller/order_poller.test.ts @ origin/main@3f2a1c8
**Expected files**: src/poller/order_poller.ts, src/poller/order_poller.test.ts (advisory)
**Must not change**: order submission contract, public API signatures
**Protected zones**: none added

Non-behavioral justification: restores pre-existing behavior; no new behavior is introduced (see tdd-guardrails).

### Step 1: Restore OrderPoller from base
**Files**: src/poller/order_poller.ts, src/poller/order_poller.test.ts
**Source**: base · origin/main@3f2a1c8 · identical
**Implementation**: `git restore --source=origin/main@3f2a1c8 -- <both paths>`
**Validation**: `git diff --exit-code origin/main@3f2a1c8 -- <both paths>` empty
**Status**: ⏳ Pending

### Step 2: Confirm nothing else moved
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: no edit — run `git status --porcelain` for the plan's paths
**Validation**: empty output; affected-area suite green
**Status**: ⏳ Pending
```

## Rejected alternative

| Rejected | Reason |
|---|---|
| Rewrite `OrderPoller` without retry logic | Produces a third version; the diff no longer equals the ref |
| Revert then refactor the poller | Ships an unrequested change inside a revert |
| Add a test asserting the revert | Asserts a non-behavior; the diff proof covers it |

## Validation

- `Source` declared per path; `Ref` pinned to a SHA, not `main`
- Cheap rung reached at 2 of 5, with the cheaper rung's failure stated
- `Must match` listed for both restored paths
- No RED/GREEN step; justification recorded for the non-behavioral change
- Final step proves the restore and runs the suite
