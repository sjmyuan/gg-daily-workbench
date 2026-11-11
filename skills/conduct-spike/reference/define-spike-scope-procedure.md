# Define-Spike-Scope Procedure

Full procedure for the `define-spike-scope` capability — loaded on demand when scope definition begins. Backs **scope-acceptance-gate**; the model it records in is **reference/scope-map-guide.md**; the breakdown is validated against **reference/decomposition-rubric.md**.

1. Restate the goal in the user's words and itemize every inference it left open — ask nothing yet.
2. Clarify the goal — what question(s) to answer, what uncertainty to reduce.
3. Decompose into areas per **problem-decomposition-guide**; propose each area with a one-line description.
4. Enumerate each area's problems ("How to …?" — one ADR each) and propose them.
5. Apply `clarify-request`'s intake gate once: show the inference list together with the proposed split and problems, ask ≤3 material questions with options plus a recommendation, and stop while the gate is `BLOCKED`. This one confirmation accepts or amends the decomposition — never ask again.
6. Resolve the artifact base root via `resolve-artifact-location` when the user named no folder (spike folder = `<base>/spikes/<spike-name>/`).
7. Record `scope.md` per **reference/scope-map-guide.md**: `Artifact root:`, gate state, restatement, inference list, only admission-passing `## Accepted assumptions`, the goal in one sentence, and each area (`preparing`) with its problems (`investigating`).
8. Validate the breakdown and the goal per **reference/decomposition-rubric.md** — limits, decision independence, and a completion test the user can recognize — and apply the scope-map removal test to every `scope.md` line.
9. Note greenfield per **greenfield-scenarios**.
10. Validate the resolved spike folder carries a `spikes/` path segment (write-boundary anchor per **reference/write-boundary-guide.md**).
