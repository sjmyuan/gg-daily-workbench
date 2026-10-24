# Execution Modes

Conventions for plan variants. A normal plan runs steps 1–N to completion.

## POC — `type: poc`
A POC executes **exactly like a normal feature plan** — no special mode, no measurement step, no report. The only difference is organizational: the MR is the user's evaluation vehicle, and merging waits for the user's decision.

## Rework mode — sibling `rework-<date>.md`
A rework plan (triggered by **orchestrate-feature-delivery**'s **handle-post-implementation-issue**) is a sibling `rework-<date>.md` in the feature folder — `plan.md` is the frozen original:
- Execute **only** the rework file's steps — the original steps are all ✅ and are never re-run or modified.
- Treat the rework steps as a fresh step sequence with **step-status-definitions** statuses (⏳ → 🔄 → ✅).
- When resuming, find the active rework file via the `## Reworks` manifest in `context.md` (the latest file with incomplete steps).
- **verify-prerequisites** still applies — the rework runs on its own branch per the repo's branch convention (the original branch/PR may already be merged).
- Commit conventions, **request-push-approval**, and **review-post-execution** apply exactly as for a normal plan.

