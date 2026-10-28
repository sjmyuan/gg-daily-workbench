# Define-Spike-Scope Procedure

Full procedure for the `define-spike-scope` capability — loaded on demand when scope definition begins. Backs **scope-acceptance-gate**. Decomposition rubric: **reference/decomposition-rubric.md**; scope-map recording: **reference/scope-map-guide.md**.

1. Apply `grill-user`'s **grill-the-ask** to the request: restate the goal in the user's words, itemize every inference, show the list, then ask ≤3 material questions with options plus a recommendation, and stop while the gate is `BLOCKED`. Nothing inferred → accept on the restatement.
2. Clarify the goal — what question(s) to answer, what uncertainty to reduce.
3. Decompose into **investigation areas** per **problem-decomposition-guide** (target 2–5; a single area is valid).
4. Propose a breakdown with one-line descriptions for each area.
5. Confirm split, merge, add, or remove of areas.
6. Enumerate each area's **problems** ("How to …?" — one per ADR, target 1–3).
7. Propose the problems for each area.
8. Confirm split, merge, add, or remove of problems.
9. Resolve the artifact base root via `resolve-artifact-location` when the user named no folder (spike folder = `<base>/spikes/<spike-name>/`); record the scope map in `scope.md` — `Artifact root:` at the top — per the scope-map model (**reference/scope-map-guide.md**).
10. Record the goal (1 sentence) and each area (`preparing`, empty findings-pair link) with its problems (`investigating`).
11. Record the gate state and, when `ACCEPTED-WITH-ASSUMPTIONS`, one `## Accepted assumptions` line per default as `Assumption (user-accepted, unverified)` — with the restatement and inference list above it.
12. Validate each problem is independently decidable (areas are shared-subject groupings).
13. Validate the breakdown per **problem-decomposition-guide**: 2–5 areas is the target but a single area is valid; ~1–3 problems per area; >5 areas or >~8 total problems → narrow or split.
14. Validate the goal is clear enough to know completion.
15. Note greenfield per **greenfield-scenarios**.
16. Validate the resolved spike folder carries a `spikes/` path segment (required to anchor the write boundary per **reference/write-boundary-guide.md**).
