# Findings-Doc Compilation

Full procedure for the `compile-findings-doc` capability — loaded on demand when the spike reaches findings-doc compilation, so the solution-doc procedure is never pulled in. Dispatch briefs: **reference/findings-doc-brief.md**; format and evidence rules: **reference/findings-document-guide.md**.

Findings docs are **one pair per area, always** — compile `docs/findings-<area>.md` (human) plus `docs/evidence-<area>.md` (evidence) for every area on the scope map, each from its area's verified investigation results.

1. For each area on the scope map, dispatch that area's findings-doc compilation to `findings-doc-writer` per **multi-agent-orchestration** — one brief per area per **reference/findings-doc-brief.md** (2+ areas dispatch concurrently).
2. Verify each compiled pair via `question-everything`'s **verify-sub-agent-results**.
3. Validate per `document-findings`'s **reference/quality-checklist.md**:
   - **Human doc** `docs/findings-<area>.md`: frontmatter → Summary → Orientation → topic blocks; no claims, confidence tags, ledger, or evidence-doc link.
   - **Evidence doc** `docs/evidence-<area>.md`: metadata → topic map → claim ledger → searched-negatives → coverage → cross-area references; every claim with inline `file:line` and a confidence tag; the ledger complete; stable IDs unrenumbered.
   - **Cross-consistency**: every human-doc topic claim appears in the ledger; every ledger row links back to a topic.
   Never vague references; never present inference as evidence.
4. Cross-reference between areas (2+ areas): each affected area's evidence doc records cross-area constraints and points to the other area's evidence doc.
5. Ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"
6. Save each pair to `<spike-folder>/docs/findings-<area>.md` + `<spike-folder>/docs/evidence-<area>.md` per **spike-artifact-layout**, then set the area's pair link and mark it `spiking` in `scope.md` per **scope-map-status**. The evidence doc is the **current-state evidence home** — update the pair in place on new evidence, no round/version tracking.
