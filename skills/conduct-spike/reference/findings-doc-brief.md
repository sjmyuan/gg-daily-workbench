# Findings-Doc Brief

Ready-to-fill structured brief for `compile-findings-doc` → `findings-doc-writer` — loaded on demand when dispatching findings-doc compilation. Fills the **structured brief shape**; shared known-context + evidence-map contracts: **reference/dispatch-briefs.md**. Format rules: `document-findings`'s **reference/structure-and-template.md** (human doc) and **reference/evidence-and-ids.md** (evidence doc).

**Announce**: "Dispatching findings-doc compilation to a sub-agent."

## 1. Mission
You are the `findings-doc-writer`. Deliver the findings **doc pair** for **one investigation area**: the human doc `docs/findings-<area>.md` and the evidence doc `docs/evidence-<area>.md`. One pair per area, always.

## 2. Context
- Spike goal **(path)**: `scope.md`
- Area: **[area name]** — this brief compiles only this area's pair
- User's questions/notes **(inline)**: **[the questions and context the user already supplied]**
- Cross-area constraints **(path)**: sibling findings pairs `docs/findings-*.md` + `docs/evidence-*.md` — **[the constraints to cross-reference]**
- Investigation results **(inline)**: **[the area's summary + its evidence map]**

## 3. Inputs
- Investigation results **(inline)**: summaries + evidence maps — already verified; record faithfully, do not re-investigate.
- Sibling findings pairs **(path)**: **[...]** — for cross-references.
- Open verification challenges **(re-dispatch only, inline)**: **[challenged claims, verdicts, what the verifier disputed]** — resolve each; leave everything else settled.

## 4. Tasks
1. Load `document-findings` and produce the area's pair: **collect-area-questions** → **author-findings-doc** + **author-evidence-doc** → **validate-findings-doc**.
2. Seed the topic questions from the investigation's own questions and the area scope.

## 5. Output contract
- **Human doc** `docs/findings-<area>.md`: YAML frontmatter (title, area, status), Summary, Orientation resource index with a "Start here" pointer, Glossary, question-style topic blocks (TL;DR → diagram / comparison table / prose). No claims, confidence tags, ledger, or evidence-doc link.
- **Evidence doc** `docs/evidence-<area>.md`: metadata block, topic map, claim ledger (claim ID → claim → verdict → `Symbol#method (file:line)` → confidence), searched-negatives, coverage, cross-area references.

## 6. Constraints
- Write only `<spike-folder>/docs/findings-<area>.md` and `<spike-folder>/docs/evidence-<area>.md`; never modify code or any file outside the spike folder.
- Never add claims beyond the provided results.
- Never alter a **Verified** verdict or an evidence `file:line`.

## 7. Report back
- Flag evidence gaps and cross-area inconsistencies found in the source results.
