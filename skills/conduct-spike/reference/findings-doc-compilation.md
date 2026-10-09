# Findings-Doc Compilation

Full procedure for the `compile-findings-doc` capability — loaded on demand when the spike reaches findings-doc compilation, so the solution-doc procedure is never pulled in. Dispatch briefs: **reference/findings-doc-brief.md**; format and evidence rules: **reference/findings-document-guide.md**. Findings docs are **one per area, always** — compile one `docs/findings-<area>.md` for every area on the scope map, each from its area's verified investigation results.

1. For each area on the scope map, dispatch that area's findings-doc compilation to `findings-doc-writer` per **multi-agent-orchestration** — one brief per area per **reference/findings-doc-brief.md** (2+ areas dispatch concurrently).
2. Verify each compiled doc via `question-everything`'s **verify-sub-agent-results**.
3. Validate per `document-findings`'s **reference/quality-checklist.md**: fixed structure (metadata → Orientation → topic blocks → Evidence & Verification); every claim with inline `file:line` and a confidence tag; the ledger complete; searched-negatives and coverage present; stable IDs unrenumbered. Never vague references; never present inference as evidence.
4. Cross-reference between findings docs (2+ areas): each affected doc notes cross-area constraints and points to the other area's doc.
5. Ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"
6. Save each to `<spike-folder>/docs/findings-<area>.md` per **spike-artifact-layout**, then set the area's findings link and mark it `spiking` in `scope.md` per **scope-map-status**; findings docs are the **current-state evidence home** — update in place on new evidence, no round/version tracking.
