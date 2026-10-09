# Findings-Doc Brief

Ready-to-fill structured brief for `compile-findings-doc` → `findings-doc-writer` — loaded on demand when dispatching findings-doc compilation. Fills the **structured brief shape**; shared evidence-map contract: **reference/dispatch-briefs.md** (**Evidence map in every brief**); format rules: `document-findings`'s **reference/structure-and-template.md**.

**Announce**: "Dispatching findings-doc compilation to a sub-agent."

## 1. Mission
You are the `findings-doc-writer`. Deliver: the findings document for **one investigation area** — a question-style explanation of that area's existing code with its evidence ledger embedded. One findings doc per area, always (`docs/findings-<area>.md`).

## 2. Context
- Spike goal: **[goal]**
- Area: **[area name]** — this brief compiles only this area's findings doc
- Investigation results: **[the area's summary + its evidence map]**

## 3. Inputs
- Investigation results (summaries + evidence maps) — already verified; embed faithfully, do not re-investigate.

## 4. Tasks
1. Load `document-findings` and produce a findings doc for this area: **collect-area-questions** → **author-findings-doc** (which applies **compile-evidence-ledger**, then **validate-findings-doc**).
2. Seed the topic questions from the investigation's own questions and the area scope.

## 5. Output contract
- Findings doc: metadata block, Orientation resource index, question-style topic blocks (TL;DR → diagram/table → claims with `file:line` and confidence), and an Evidence & Verification section (ledger, searched-negatives, coverage); cross-area constraints as cross-references to the other area's findings doc.

## 6. Constraints
- Write only `<spike-folder>/docs/findings-<area>.md`; never modify code or any file outside the spike folder.
- Never add claims beyond the provided results.
- Never alter a **Verified** verdict or an evidence `file:line`.

## 7. Report back
- Flag evidence gaps and cross-area inconsistencies found in the source results.
