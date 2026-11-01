# Define-Spike-Scope Procedure

Full procedure for the `define-spike-scope` capability — loaded on demand when scope definition begins. Backs **scope-acceptance-gate**; the model it records in is **reference/scope-map-guide.md**; the breakdown is validated against **reference/decomposition-rubric.md**.

1. Restate the goal in the user's words and itemize every inference it left open — ask nothing yet.
2. Apply `clarify-request`'s intake gate: show the inference list, ask ≤3 material questions with options plus a recommendation, and stop while the gate is `BLOCKED`.
3. Clarify the goal — what question(s) to answer, what uncertainty to reduce.
4. Decompose into areas per **problem-decomposition-guide**; propose each area with a one-line description.
5. Enumerate each area's problems ("How to …?" — one ADR each) and propose them.
6. Confirm split, merge, add, or remove — areas first, then problems.
7. Resolve the artifact base root via `resolve-artifact-location` when the user named no folder (spike folder = `<base>/spikes/<spike-name>/`).
8. Record `scope.md` per **reference/scope-map-guide.md**: `Artifact root:`, gate state, restatement, inference list, `## Accepted assumptions`, the goal in one sentence, and each area (`preparing`) with its problems (`investigating`).
9. Validate the breakdown and the goal per **reference/decomposition-rubric.md** — limits, decision independence, and a completion test the user can recognize.
10. Note greenfield per **greenfield-scenarios**.
11. Validate the resolved spike folder carries a `spikes/` path segment (write-boundary anchor per **reference/write-boundary-guide.md**).
