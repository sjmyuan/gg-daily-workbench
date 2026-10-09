# Findings Document Guide

A findings document explains **what exists in a code area today** — a question-style, resource-first artifact for both a human reader and a downstream agent. It is the spike's **evidence home**: the single place where code evidence lives.

## Producer

Findings documents are produced by the `document-findings` skill, compiled per area by the `findings-doc-writer` agent. That skill owns the structure, question style, evidence ledger, and stable IDs; this guide covers only the spike-specific handoff.

## One per area — always

Findings docs are always **one per investigation area** — `docs/findings-<area>.md` — for every spike. A single-area spike yields exactly one findings doc. Cross-area constraints travel as cross-references between the affected docs; there is no consolidated findings doc — areas come together only in the solution doc.

## Structure (owned by document-findings)

A metadata block → an Orientation resource index → question-style topic blocks (TL;DR → diagram/table → atomic claims with `file:line`) → an Evidence & Verification section (ledger, searched-negatives, coverage). Load `document-findings`'s **reference/structure-and-template.md** for the full template.

## Evidence the spike relies on

- **Entry points & key locations**: `file:line` beside the component or flow; never vague references like "the service layer".
- **Call chains**: topic sequence diagrams annotated with `file:line`.
- **Evidence ledger**: claim ID → claim → verdict → evidence → confidence (5-tag model: ✅ Verified, 🔶 Inferred, 💭 Assumption, ⚠️ Inconsistency, ❓ Gap).
- **Searched-negatives**: dead-end searches recorded so later sub-agents don't repeat them.
- **Stable IDs**: `<area>/<topic-slug>#cN`, cited by ADRs and the solution doc.

Details: `document-findings`'s **reference/evidence-and-ids.md**.

## Relationship to other artifacts

- **ADRs** cite the findings doc's stable IDs for evidence: "The current authorize path (`payment/authorize-flow#c2`, `ChargeService.java:88`) couples retries to the gateway call..."
- **The solution document** is produced by `write-solution-doc` (target-state, decision-only), seeded with the findings docs as the current-state evidence it references; it does not restate findings content.
- When findings change, update the affected findings doc via `document-findings`'s **update-findings-doc**, then the ADRs and solution doc that cite it.
- **ADRs and the solution document stay clean**: investigation detail and raw data live only in the findings doc.
