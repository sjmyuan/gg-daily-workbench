# Findings-Doc Brief

Ready-to-fill structured brief for `compile-findings-doc` → `findings-doc-writer` — loaded on demand when dispatching findings-doc compilation. Fills the **structured brief shape**; carries the shared context-inventory, fill-mode, intake-record, and evidence-map contracts: **reference/dispatch-briefs.md**. Format rules: `document-findings`'s **reference/structure-and-template.md** (human doc) and **reference/evidence-and-ids.md** (evidence doc).

**Announce**: "Dispatching findings-doc compilation to a sub-agent."

Every path is absolute.

## 1. Mission
You are the `findings-doc-writer`. Deliver the findings **doc pair** for **one investigation area**: the human doc `docs/findings-<area>.md` and the evidence doc `docs/evidence-<area>.md`. One pair per area, always.

## 2. Context
- Spike goal **(path + digest)**: `<artifact-root>/spikes/<spike-name>/scope.md` — **[1–3 lines: the question this area answers]**
- Area: **[area name]** — this brief compiles only this area's pair
- Accepted assumptions **(digest, from `scope.md#accepted-assumptions`)**: **[A<N> → assumed value]** — carry each into the ledger as 💭 Assumption
- User's questions/notes **(inline)**: **[the questions and context the user already supplied]** — each question becomes a topic block
- Cross-area constraints **(path + digest)**: sibling pairs `docs/findings-*.md` + `docs/evidence-*.md` — **[the constraints to cross-reference]**

## 3. Inputs
- Intake record **(inline)**: system **[...]** · scope **[...]** · depth **[...]** · consumer **[...]** — adopt it, do not re-derive it.
- Investigation results **(inline)**: **[the area's summary + its evidence map + its search log]** — already verified; record faithfully, do not re-investigate.
- Known locations **(digest)**: **[entry points and `file:line` that belong in the topic map]** — use these; never re-open the files to find them.
- Already searched **(digest)**: **[prior queries and "no matches" outcomes]** — carry into searched-negatives; never repeat the scan.
- Sibling findings pairs **(path)**: **[...]** — for cross-references.
- Open verification challenges **(re-dispatch only, inline)**: **[challenged claims, verdicts, what the verifier disputed]** — resolve each; leave everything else settled.

## 4. Tasks
1. Load `document-findings` and produce the area's pair: **collect-area-questions** → **author-findings-doc** + **author-evidence-doc** → **validate-findings-doc**.
2. Seed the topic questions from the investigation's own questions and the area scope.
3. Record the supplied evidence map as the claim ledger, preserving every verdict, `file:line`, and searched-negative exactly.

## 5. Output contract
- **Human doc** `docs/findings-<area>.md`: YAML frontmatter (title, area, status), Summary, Orientation resource index with a "Start here" pointer, Glossary, question-style topic blocks (TL;DR → diagram / comparison table / prose). No claims, confidence tags, ledger, or evidence-doc link.
- **Evidence doc** `docs/evidence-<area>.md`: metadata block, topic map, claim ledger (claim ID → claim → verdict → `Symbol#method (file:line)` → confidence), searched-negatives, coverage, cross-area references.

## 6. Constraints
- Write only `<spike-folder>/docs/findings-<area>.md` and `<spike-folder>/docs/evidence-<area>.md`; never modify code or any file outside the spike folder.
- Never re-investigate, re-read code to confirm a supplied location, or re-run a listed search — the results are settled input.
- Never add claims beyond the provided results.
- Never alter a **Verified** verdict or an evidence `file:line`.

## 7. Report back
- Flag evidence gaps and cross-area inconsistencies found in the source results.
- Flag every supplied claim that arrived without a location or verdict, so the orchestrator can re-brief that unit.
