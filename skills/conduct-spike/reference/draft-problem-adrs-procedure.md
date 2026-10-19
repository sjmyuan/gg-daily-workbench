# Draft-Problem-ADRs Procedure

Full procedure for the `draft-problem-adrs` capability — loaded on demand when the spike reaches ADR drafting, so the compile and investigation procedures are never pulled in. Dispatch briefs: **reference/adr-drafting-brief.md**; latest-state rules: **reference/artifact-maintenance-guide.md**.

1. Collect each problem's decision drivers from the user (the orchestrator owns the dialog). Dispatch ADR drafting for each **problem** to `adr-writer` per **multi-agent-orchestration**; batch a whole area's problems in one brief when they share its evidence (brief per **reference/adr-drafting-brief.md**). Each brief runs the `draft-adr` flow headlessly — drivers → options → evaluation → compilation — returning the ADR with a proposed chosen option.
2. Apply `question-everything`'s **verify-sub-agent-results** at the depth the decision warrants — full loop for a load-bearing ADR, single pass for new code claims.
3. Apply **sync-update-artifacts** when drafting surfaced new constraints, risks, or facts — write them back to the evidence doc before saving the ADR.
4. Save each ADR to `<spike-folder>/adrs/adr-<area>-<NN>-<problem>.md` per **spike-artifact-layout**, carrying its `Area:` tag from the scope map; mark the problem `deciding` in `scope.md` per **scope-map-status**.
5. Ask: "Would you like to adjust any ADR before compiling the solution document?" On uncertainty, apply **suggest-spike-on-adr-uncertainty** first. On user confirmation, mark each confirmed problem `done` in `scope.md` per **scope-map-status**.
6. Validate via `draft-adr`'s **compile-adr** checklist + spike-specific additions (each option's tech details carried into its evaluation section; the ADR stands alone without reading other ADRs; it cites the evidence doc for evidence); run the **no-note scan** per **artifact-maintenance-doctrine** until none remain.
