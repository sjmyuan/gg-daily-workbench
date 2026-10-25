# Investigate-Per-Area Procedure

Full procedure for the `investigate-per-area` capability — loaded on demand when area investigation begins. Dispatch pattern: **reference/multi-agent-orchestration.md**; investigation brief: **reference/investigation-brief.md**.

1. Dispatch each area's investigation to `code-investigator` per **multi-agent-orchestration**.
2. Brief each investigation per **reference/investigation-brief.md**.
3. Apply `question-everything`'s **verify-sub-agent-results** at **single-pass** depth (default).
4. When an evidence map contradicts an accepted goal or constraint, re-challenge the affected claims via **challenge-the-ask** and rewrite `scope.md` before continuing.
5. Ask: "Is the investigation complete, or continue in a new direction?"
6. Loop to scope when a new direction is chosen.
7. Hand off to **compile-findings-doc** with the evidence maps.
