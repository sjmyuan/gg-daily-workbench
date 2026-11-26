# Example: Verifying a Completed Cell (Independent Gate)

**Scenario**: `order-service/F2` finished execution. The executor reported `DONE_WITH_CONCERNS` with commit range `a1b2c3d..d4e5f6a`.
The orchestrator must verify spec compliance, report trust, and judge quality before F2 advances to **verified**.

**Applies**: **verify-cell** → **update-delivery-index**

## 1. Require the executor handoff

- `deliveries/wallet-migration/order-service/wallet-service/plan.md` — every step ✅ or ⏭.
- `context.md` `## Execution` — latest round only:

  | Field | Value |
  |---|---|
  | Status | `DONE_WITH_CONCERNS` |
  | Range | `a1b2c3d..d4e5f6a` |
  | PR | — (not opened) |
  | Gate receipt | `build=0 · test=18/18 passed · lint=0` |
  | Self-check | `fixed:2` — two Blockers fixed before hand-off |

- `context.md` `## Open concerns` — "retry cap hard-coded" (deferred Minor).

## 2. Dispatch a fresh code-reviewer

- **Tier**: **Full** — F2 changes the wallet service's retry contract, which F4 consumes.
- **code-reviewer A** (**review-code**) — inputs: the cell brief, the range `a1b2c3d..d4e5f6a`, the plan/context/ADR paths, the decision digest, the **cell digest**, and the tier. Global constraints only when they change the verdict.
  It gates the diff against the stated decision instead of re-deriving it.
- code-reviewer A fetches the diff from git over the range — no diff file, and the output never enters the orchestrator's context.
- Not executor-B, the agent that produced the work.

## 3. Verdicts

**Spec compliance** (brief + governing ADR):

- Missing: none.
- Extra: none.
- Misunderstood: none.
- ⚠️ Cannot verify from diff: retry-cap value lives in unchanged config — orchestrator confirmed it matches the ADR.

**Trust check**:

- Executor claimed a Blocker fix ("unbounded retry") — confirmed resolved in the diff (`wallet-service/retry.ts:41`).
- Gate receipt `build=0 · test=18/18 · lint=0` matches `d4e5f6a`; no re-run needed.

**Quality** (graded, one call):

- Blocker: none.
- Major: none. The retry loop's backoff is extracted and tested; the hard-coded cap is the only smell and it is Minor.
- Minor: retry cap hard-coded; envelope construction repeats a literal key.
- **Merge recommendation**: merge.

**Verdict**: spec compliant, report trustworthy, quality acceptable — merge.

## 4. Handle the open concern

- The hard-coded retry cap is a Minor, outside spec scope and not load-bearing.
- No index record; it stays in `## Open concerns` and rolls into the epic integration review.

## 5. Update the index

| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| order-service/F2 | 1234-f2-wallet | — | d4e5f6a | **verified** | code-reviewer-A | deliveries/wallet-migration/order-service/wallet-service/ |

- F2 awaits merge; with F1 **done**, F2 is now merge-ready.
- The executor returns the branch and commits under `Push: batched`; the orchestrator asks once for the wave per **delivery-layout**'s branch conventions and records the returned reference.

## 6. Fix-round variant

Had the code-reviewer returned findings, the label routes the round:

- **All mechanical** → one **executor** dispatch with the findings inline and `Fix class: mechanical`; it repairs in place and records a `Gate repair:` line per finding in `## Execution`, then a scoped re-review.
- **Any design** → the **planner** writes `rework.md` with a `**Gate findings**:` line (mechanical ones ride along), then the **executor**, then a scoped re-review.
The loop is capped at 2 rounds (see **reference/verification-gate.md**).

- Findings travel **inline** in the fix-round brief; the scoped re-review receives them plus the rework file's **path** (or the `Gate repair:` lines).
- The cell stays **in-progress**; the rework file records a design fix, `## Execution` a gate repair.
- A cell never reaches **verified** with an unresolved spec gap.
- A recurring or unresolved finding escalates to the user immediately.
