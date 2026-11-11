# Run-Spike-Workflow Procedure

Full procedure for the `run-spike-workflow` capability — loaded on demand when a spike investigation starts from scratch. Pause for user confirmation after each capability; skip a pause only if the user requests it. Run the own-writes write-boundary check after every write capability per **reference/write-boundary-guide.md**; stop and report on newly written out-of-folder paths.

1. Apply **define-spike-scope**.
2. Do not proceed until the intake gate is `ACCEPTED` or `ACCEPTED-WITH-ASSUMPTIONS` and the scope is confirmed.
3. Collect each problem's decision drivers from the user, then apply **investigate-per-area** — each area returns its written pair and ADRs in one return, verified on an independent seat. Skip the investigation when the user supplied pre-existing findings and apply **compile-findings-doc** directly.
4. Loop to step 1 when a new investigation direction emerges.
5. Apply **compile-findings-doc** to validate and confirm each returned pair, then mark each area `spiking`; run the write-boundary check.
6. Apply **draft-problem-adrs** to confirm each returned ADR, take the user's review feedback, and mark each confirmed problem `done`; run the write-boundary check.
7. Apply **compile-solution-doc** to consolidate ADRs into the solution document; run the write-boundary check.
8. Run the **final consistency review** — cross-check findings → ADRs → solution doc and cross-area constraints; confirm each `done` problem has its ADR and each area's decisions are mirrored in the solution doc; surface inconsistencies before concluding.
9. Record any implementation need as an out-of-scope note in `scope.md` / `solution.md`; never implement — the user runs `orchestrate-feature-delivery`.
