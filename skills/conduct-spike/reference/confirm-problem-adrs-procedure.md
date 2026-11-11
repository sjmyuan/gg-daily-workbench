# Confirm-Problem-ADRs Procedure

Full procedure for the `confirm-problem-adrs` capability — the confirmation and revision pass over each area's returned ADRs, loaded on demand when the spike reaches decision review. Brief: **reference/area-analyst-brief.md**; latest-state rules: **reference/artifact-maintenance-guide.md**.

1. Take each ADR returned and verified with the area session's single return (on the pre-existing-findings path, the verification from **compile-findings-doc**). Re-verify only a claim a revision changed — full loop for a load-bearing decision. The analyst never prompts the user; the orchestrator owns the dialog.
2. Confirm each ADR is written to `<spike-folder>/adrs/adr-<area>-<NN>-<problem>.md` per **spike-artifact-layout**, carrying its `Area:` tag from the scope map; mark the problem `deciding` in `scope.md` per **scope-map**.
3. Ask: "Review the decisions; would you like any ADR adjusted before compiling the solution document?" On uncertainty, apply **suggest-spike-on-adr-uncertainty** first.
4. On feedback, re-dispatch the area session with the feedback and the artifact paths to revise the ADR in place, then re-verify only the changed claims. Apply **sync-update-artifacts** when the revision surfaces new constraints, risks, or facts — write them back to the evidence doc.
5. On user confirmation, set each ADR's `Status: adopt` via `draft-adr` and mark its problem `done` in `scope.md` per **scope-map**.
6. Validate via `draft-adr`'s **compile-adr** checklist + spike-specific additions (each option's tech details carried into its evaluation section; the ADR stands alone without reading other ADRs; it cites the evidence doc for evidence); run the **no-note scan** per **artifact-maintenance-doctrine** until none remain.
