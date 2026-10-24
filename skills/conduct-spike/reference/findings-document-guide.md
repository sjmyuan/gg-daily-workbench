# Findings Document Guide

The spike's findings docs explain **what exists in a code area today**: a **human doc** for readers and an **evidence doc** holding the claim ledger for machine consumption and downstream citations. The evidence doc is the spike's **evidence home** — the single place where code evidence, claim IDs, and confidence live.

## Producer

Findings docs are produced by the `document-findings` skill, compiled per area by the `findings-doc-writer` agent. That skill owns the structure, question style, evidence ledger, and stable IDs; this guide covers only the spike-specific handoff.

## One pair per area — always

Findings docs are always **one pair per investigation area** — `docs/findings-<area>.md` (human) + `docs/evidence-<area>.md` (evidence) — for every spike. A single-area spike yields exactly one pair. Cross-area constraints travel as cross-references between evidence docs; there is no consolidated findings doc — areas come together only in the solution doc.

## Structure (owned by document-findings)

- **Human doc** `docs/findings-<area>.md`: YAML frontmatter (title, area, status) → a Summary → an Orientation resource index with a "Start here" pointer → a Glossary (optional) → question-style topic blocks (TL;DR → diagram / comparison table / prose). No claims, confidence tags, ledger, or evidence-doc link — it stays publishable.
- **Evidence doc** `docs/evidence-<area>.md`: a metadata block → a topic map → a claim ledger → searched-negatives → coverage → cross-area references.

Load `document-findings`'s **reference/structure-and-template.md** (human doc) and **reference/evidence-and-ids.md** (evidence doc) for the full templates.

## Evidence the spike relies on

All of the following live in the **evidence doc**, not the human doc:

- **Entry points & key locations**: `Symbol (file:line)` beside the component or flow; never vague references like "the service layer".
- **Call chains**: topic sequence diagrams annotated with `file:line`.
- **Evidence ledger**: claim ID → claim → verdict → evidence → confidence (5-tag model: ✅ Verified, 🔶 Inferred, 💭 Assumption, ⚠️ Inconsistency, ❓ Gap).
- **Searched-negatives**: dead-end searches recorded so later sub-agents don't repeat them.
- **Stable IDs**: `<area>/<topic-slug>#cN`, cited by ADRs and the solution doc.

Details: `document-findings`'s **reference/evidence-and-ids.md**.

## Relationship to other artifacts

- **ADRs** cite the evidence doc's stable IDs for evidence: "The current authorize path (`payment/authorize-flow#c2`, `ChargeService.java:88`) couples retries to the gateway call..."
- **The solution document** is produced by `write-solution-doc` (target-state, decision-only), seeded with the evidence docs as the current-state evidence it references; it does not restate findings content.
- When findings change, update the pair via `document-findings`'s **update-findings-doc**, then the ADRs and solution doc that cite it.
- **ADRs and the solution document stay clean**: investigation detail and raw data live only in the evidence doc.

## Delivery handoff

The pair is the **current-state knowledge plane**. Delivery references it from the index `## Spike References` and `context.md` `## Pointers` — never copies it.

A fact discovered during delivery that changes a decision re-enters here via `update-findings-doc`, then propagates to the ADR and solution doc. Delivery agents never edit the pair. Two-plane map: **[artifact-map.md](artifact-map.md)**.
