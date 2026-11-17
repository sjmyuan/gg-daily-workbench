# plan-refactor

Judgment capability: the seam and the order are yours; behavior preservation and the gate are not.

1. **Name the invariant** — the observable behavior that must survive, and how each unit proves it (`characterization-first` per **test-strategy**).
2. **Find the seam by reading the code.** A refactor planned against a guessed module boundary is a rewrite. Ratify the boundary per **define-scope-boundary**; behavior change stays **Must not change** and moves to a feature plan.
3. **Derive units as structural moves**, smallest reversible step each. Use the tooling's move/extract operation instead of retyping (see **change-provenance**).
4. **Never introduce a failing test.** A test that must fail is new behavior — that is a feature plan.
5. **Write the plan** per **reference/plan-file-format.md**, with `## Risk` naming the step most likely to change behavior undetected, then units, then the Exit gate.
6. **Self-check** against **plan-rubric**; present the risk route.

Existing coverage is the proof: name the tests that pin each moved unit, and add characterization tests only where coverage is missing.
