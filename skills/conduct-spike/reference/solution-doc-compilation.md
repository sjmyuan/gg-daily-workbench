# Solution-Doc Compilation

Full procedure for the `compile-solution-doc` capability — loaded on demand when the spike reaches solution-doc compilation, so the findings-doc procedure is never pulled in. Dispatch briefs: **reference/solution-doc-brief.md**; latest-state rules: **reference/artifact-maintenance-guide.md**.

1. Dispatch solution-doc compilation to `solution-doc-writer` per **multi-agent-orchestration**; brief per **reference/solution-doc-brief.md**.
2. Apply `question-everything`'s **verify-sub-agent-results** at **fidelity** depth — fidelity to verified ADRs and evidence; no evidence sweep.
3. Save per **spike-artifact-layout** (scope map → `scope.md`, findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`); keep at the latest state (see **artifact-maintenance-doctrine**); recompute each area's derived status per **scope-map**.
4. Validate: the solution doc mirrors every ADR's chosen option in its canonical sections (per `write-solution-doc` structure), cross-references consistent, diagrams match; run the **no-note scan** until clean.
5. Brief per **review-pacing**, reusing each area's returned route for the decisions it carries and adding one self-check on a target-state claim — findings = current-state record, ADRs = decision records, solution doc = target-state architecture. Then present the bundle for review/approve and record `reviewed` or `waived` in `scope.md` per **scope-map**; version-control together.
