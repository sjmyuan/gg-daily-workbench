# Findings-Doc Compilation

Full procedure for the `compile-findings-doc` capability — the confirmation pass over each area's findings pair, loaded on demand when the spike reaches findings confirmation, so the solution-doc procedure is never pulled in. Brief: **reference/area-analyst-brief.md**; format and evidence rules: **reference/findings-document-guide.md**.

Findings docs are **one pair per area, always** — `docs/findings-<area>.md` (human) plus `docs/evidence-<area>.md` (evidence) for every area on the scope map, each from its area's verified investigation results. The scope gate covers the areas it accepted; notes the user supplies later are gated per **scope-acceptance-gate** before dispatch.

1. Take each area's pair returned and verified by **dispatch-area-session**. For an area seeded with pre-existing user findings, dispatch the same brief with phase 1 skipped — the analyst writes the pair and the ADRs from the supplied material; never re-investigate.
2. Verify a pair this step produced at **single pass + fidelity**, and its same-return ADRs at the **full loop** on each load-bearing decision. A pair already verified by **dispatch-area-session** needs no second evidence pass — validate it in step 3.
3. Validate each pair per **reference/findings-document-guide.md** §Validation (pair) — structure, ledger completeness, and cross-consistency; never vague references, never inference presented as evidence.
4. Cross-reference between areas (2+ areas) per the same validation list.
5. Ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"
6. When the answer changes a claim a returned ADR relies on, re-dispatch that area session to revise the ADR in place before the pair is confirmed.
7. Confirm each pair is written to `<spike-folder>/docs/findings-<area>.md` + `<spike-folder>/docs/evidence-<area>.md` per **spike-artifact-layout**, then set the area's pair link in `scope.md` — the area's derived status becomes `spiking` per **scope-map**. The evidence doc is the **current-state evidence home** — update the pair in place on new evidence, no round/version tracking.
