# Define-Spike-Scope Procedure

Full procedure for the `define-spike-scope` capability — loaded on demand when scope definition begins. Backs **scope-acceptance-gate**; the model it records in is **reference/scope-map-guide.md**; the breakdown is validated against **reference/decomposition-rubric.md**.

1. Restate the goal in the user's words and itemize every inference it left open — ask nothing yet.
2. Clarify the goal — what question(s) to answer, what uncertainty to reduce.
3. Decompose into areas per **problem-decomposition-guide**; propose each area with a one-line description.
4. Enumerate each area's problems ("How to …?" — one ADR each) and propose them.
5. Apply `clarify-request`'s intake gate — at most 2 rounds: show the inference list with the proposed split, ask ≤3 material questions with options and a recommendation, and stop while the gate is `BLOCKED`.
6. Collect each problem's decision driver in the same confirmation — a required input, not a question against the cap. This one confirmation accepts or amends the decomposition.
7. Resolve the artifact base root via `resolve-artifact-location` when the user named no folder (spike folder = `<base>/spikes/<spike-name>/`).
8. Record `scope.md` per **reference/scope-map-guide.md**: `Artifact root:`, then the accepted request as facts — goal in one sentence, boundaries, binding constraints, done criteria — under one `## Accepted assumptions` only the premises that can move the split, a driver, or the done criteria, then each area (no stored status — it derives `preparing`) with its problems (`investigating`). The gate state, inference list, and each round's answers stay in the session.
9. Validate the breakdown and the goal per **reference/decomposition-rubric.md** — limits, decision independence, and a completion test the user can recognize — and apply the scope-map removal test to every `scope.md` line.
10. Note greenfield per **greenfield-scenarios**.
11. Validate the resolved spike folder carries a `spikes/` path segment (write-boundary anchor per **reference/write-boundary-guide.md**).
