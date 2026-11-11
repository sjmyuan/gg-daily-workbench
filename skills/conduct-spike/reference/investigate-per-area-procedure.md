# Investigate-Per-Area Procedure

Full procedure for the `investigate-per-area` capability — the area's single investigate-and-decide pass, loaded on demand when area investigation begins. One dispatch produces the findings pair and the ADRs; the session returns once, after the ADRs are written. Dispatch pattern: **reference/multi-agent-orchestration.md**; brief: **reference/area-analyst-brief.md**.

1. Collect each problem's decision drivers from the user before dispatching — the analyst drafts ADRs in the same session and never infers a driver.
2. Dispatch each area's full brief to `spike-area-analyst` per **multi-agent-orchestration** — one brief per area (2+ areas dispatch concurrently). The analyst investigates, writes `docs/findings-<area>.md` + `docs/evidence-<area>.md`, then drafts one ADR per problem, and returns once with both.
3. Brief each session per **reference/area-analyst-brief.md**.
4. Verify the single return: **single pass + fidelity** on the pair's material code claims, the **full loop** on load-bearing ADR decisions. Reuse one independent seat per returned unit.
5. On a `DISAGREE`, re-dispatch a NEW analyst with the verification result and the artifact paths: repair the affected claims in the pair via `document-findings`'s **update-findings-doc** and in the ADR, then confirm only the changed claims.
6. When an artifact contradicts an accepted goal or constraint, re-challenge the affected claims via `clarify-request`'s **re-challenge-the-ask** and rewrite `scope.md`; have the analyst update the pair and ADRs when the scope changes the area's questions.
7. Present the pair and ADRs; the user reviews them in the confirmation passes that follow — after the return, never between phases.
8. On feedback, re-dispatch the same session (or a new analyst with the artifacts) to revise in place, then re-verify only the changed claims.
9. Keep each area's pair, ADRs, receipt, and session through **compile-findings-doc** and **draft-problem-adrs** — never re-investigate to recover context.
