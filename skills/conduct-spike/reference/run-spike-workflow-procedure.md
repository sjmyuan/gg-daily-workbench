# Run-Spike-Workflow Procedure

Full procedure for the `run-spike-workflow` capability — loaded on demand when a spike investigation starts from scratch. User checkpoints: the scope gate, the findings confirmation, the ADR review, and the solution-doc approval; never add a pause between an area session's internal phases. Run the own-writes write-boundary check after every write capability per **reference/write-boundary-guide.md**; stop and report on newly written out-of-folder paths.

1. Apply **define-spike-scope** — its single gate confirmation also accepts or amends the proposed areas, problems, and drivers.
2. Do not proceed until the gate is `ACCEPTED` or `ACCEPTED-WITH-ASSUMPTIONS` and `scope.md` records the scope.
3. Apply **dispatch-area-session** with the drivers accepted at the gate — each area returns its written pair and ADRs in one return, verified on an independent seat. Skip it when the user supplied pre-existing findings and go to step 5: the phase-1-skipped area session writes both the pair and the ADRs.
4. When a new investigation direction adds an area or problem, return to step 3; when the scope map changes, apply **continue-prior-spike**; re-open the intake gate only on a `clarify-request` **re-challenge-trigger**.
5. Apply **compile-findings-doc** — dispatch the phase-1-skipped session when findings were pre-existing, else validate and confirm each pair returned by **dispatch-area-session** — then link each pair in `scope.md`; the area's derived status becomes `spiking`; run the write-boundary check.
6. Apply **confirm-problem-adrs** to confirm each returned ADR (setting `Status: adopt`), take the user's review feedback, and mark each confirmed problem `done`; run the write-boundary check.
7. Apply **compile-solution-doc** to consolidate ADRs into the solution document; run the write-boundary check.
8. Record any implementation need as one line under `scope.md` `## Next actions`; never implement — the user runs `orchestrate-feature-delivery`.
9. Run the **final consistency review** — cross-check findings → ADRs → solution doc and cross-area constraints; confirm each `done` problem has its ADR and each area's decisions are mirrored in the solution doc; surface inconsistencies before concluding.
