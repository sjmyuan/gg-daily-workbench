# Investigate-Per-Area Procedure

Full procedure for the `investigate-per-area` capability — phase 1 of an area session, loaded on demand when area investigation begins. Dispatch pattern: **reference/multi-agent-orchestration.md**; brief: **reference/area-analyst-brief.md**.

1. Dispatch each area's **phase 1** to `spike-area-analyst` per **multi-agent-orchestration** — one brief per area with `Phase stop: 1` (2+ areas dispatch concurrently).
2. Brief each investigation per **reference/area-analyst-brief.md**.
3. Apply `question-everything`'s **verify-sub-agent-results** at **single-pass** depth (default).
4. When an evidence map contradicts an accepted goal or constraint, re-challenge the affected claims via `clarify-request`'s **re-challenge-the-ask** and rewrite `scope.md` before continuing.
5. Ask: "Is the investigation complete, or continue in a new direction?"
6. Loop to scope when a new direction is chosen.
7. Keep each accepted area's receipt and session for **compile-findings-doc** — do not discard the evidence map.
