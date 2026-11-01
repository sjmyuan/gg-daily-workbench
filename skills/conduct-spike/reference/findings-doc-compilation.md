# Findings-Doc Compilation

Full procedure for the `compile-findings-doc` capability — loaded on demand when the spike reaches findings-doc compilation, so the solution-doc procedure is never pulled in. Dispatch briefs: **reference/findings-doc-brief.md**; format and evidence rules: **reference/findings-document-guide.md**.

Findings docs are **one pair per area, always** — compile `docs/findings-<area>.md` (human) plus `docs/evidence-<area>.md` (evidence) for every area on the scope map, each from its area's verified investigation results.

1. For each area on the scope map, dispatch that area's findings-doc compilation to `findings-doc-writer` per **multi-agent-orchestration** — one brief per area per **reference/findings-doc-brief.md** (2+ areas dispatch concurrently).
2. Apply `question-everything`'s **verify-sub-agent-results** at **fidelity** depth — IDs, counts, and cross-references against the verified ledger; no evidence sweep.
3. Validate each pair per **reference/findings-document-guide.md** §Validation (pair) — structure, ledger completeness, and cross-consistency; never vague references, never inference presented as evidence.
4. Cross-reference between areas (2+ areas) per the same validation list.
5. Ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"
6. Save each pair to `<spike-folder>/docs/findings-<area>.md` + `<spike-folder>/docs/evidence-<area>.md` per **spike-artifact-layout**, then set the area's pair link and mark it `spiking` in `scope.md` per **scope-map-status**. The evidence doc is the **current-state evidence home** — update the pair in place on new evidence, no round/version tracking.
