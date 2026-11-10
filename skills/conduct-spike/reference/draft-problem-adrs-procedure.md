# Draft-Problem-ADRs Procedure

Full procedure for the `draft-problem-adrs` capability — phase 3 of an area session, loaded on demand when the spike reaches ADR drafting, so the compile and investigation procedures are never pulled in. Brief: **reference/area-analyst-brief.md**; latest-state rules: **reference/artifact-maintenance-guide.md**.

1. Collect each problem's decision drivers from the user (the orchestrator owns the dialog). Resume each area's session for **phase 3** per **multi-agent-orchestration** — one brief per area with `Phase stop: 3`, batching the area's problems. When the session cannot be resumed, re-dispatch the analyst with the verified pair and the phase-2 receipt; never re-investigate. The brief runs the `draft-adr` flow headlessly — drivers → options → evaluation → compilation — returning the ADR with a proposed chosen option.
2. Apply `question-everything`'s **verify-sub-agent-results** at the depth the decision warrants — full loop for a load-bearing ADR, single pass for new code claims.
3. Apply **sync-update-artifacts** when drafting surfaced new constraints, risks, or facts — write them back to the evidence doc before confirming the ADR.
4. Confirm each ADR is written to `<spike-folder>/adrs/adr-<area>-<NN>-<problem>.md` per **spike-artifact-layout**, carrying its `Area:` tag from the scope map; mark the problem `deciding` in `scope.md` per **scope-map-status**.
5. Ask: "Would you like to adjust any ADR before compiling the solution document?" On uncertainty, apply **suggest-spike-on-adr-uncertainty** first. On user confirmation, mark each confirmed problem `done` in `scope.md` per **scope-map-status**.
6. Validate via `draft-adr`'s **compile-adr** checklist + spike-specific additions (each option's tech details carried into its evaluation section; the ADR stands alone without reading other ADRs; it cites the evidence doc for evidence); run the **no-note scan** per **artifact-maintenance-doctrine** until none remain.
