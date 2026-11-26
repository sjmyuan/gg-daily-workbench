# Execution Modes

Conventions for plan variants. A normal plan runs steps 1–N to completion.

## POC — `**Type**: poc`
A POC executes **exactly like a normal feature plan** — no special mode, no measurement step, no report. The only difference is organizational: the MR is the user's evaluation vehicle, and merging waits for the user's decision.

## Rework mode — `rework.md` (pre-merge) · `rework-<date>.md` (post-merge)
A rework plan (an implemented or delivered cell needs a scoped change) is a sibling rework file in the feature folder — the pre-merge one is `rework.md`, overwritten when a new round starts (git keeps the previous round); post-merge files key by date. `plan.md` is the frozen original:
- Execute **only** the rework file's steps — the original steps are all ✅ and are never re-run or modified.
- Treat the rework steps as a fresh step sequence with the **step-tracking-format.md** statuses (⏳ → 🔄 → ✅) and the same six-field block.
- When resuming, find the active rework file via the `## Reworks` manifest in `context.md` (the latest file with incomplete steps).
- **verify-prerequisites** still applies — the rework runs on its own branch per the repo's branch convention (the original branch/PR may already be merged).
- Commit conventions, **request-push-approval**, and **review-post-execution** apply exactly as for a normal plan.

