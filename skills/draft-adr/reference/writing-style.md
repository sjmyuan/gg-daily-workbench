# Concise Writing Style

Applies to all prose in ADRs and solution documents. Detail lives in **carriers** — tables, numbered flows, diagrams, and code diffs. Prose states takeaways. Every cap below applies to prose only; carriers are exempt and must carry the full detail.

## Core rule: BLUF (Bottom Line Up Front)
- Open every section with the conclusion in one line, then the why.
- Under each heading, the first line is a **bolded one-line takeaway** (e.g., `**Verdict:** …`, `**Trade-off:** …`).
- Never lead with evidence, background, or analysis.

## Detail carriers
- A cap is never a reason to omit a fact the reader needs to picture or implement the option.
- Move that fact to a carrier, then keep the prose to the takeaway: mechanism → numbered flow, concern → table row, comparison → matrix column, change → diff plus plan row.
- Every carrier row is one fact. A carrier that grows past ~10 rows splits by view or concern.
- If a carrier and the prose disagree, the carrier is authoritative; fix the prose.

## Hard caps

| Element | Cap |
|---|---|
| Section opening takeaway | 1 sentence (≤15 words) |
| Context / problem statement | ≤3 sentences |
| Decision justification | 1 sentence |
| "What it is" prose | 1–2 sentences; mechanism, concerns, and impact live in their tables |
| Decision drivers | ≤6 items (one fact each) |
| Consequences | ≤4 items per subsection |
| Consequence / risk item | ≤10 words |
| Pros / Cons bullet | 1 claim, no justification |
| Paragraph | ≤3 sentences |
| Sentence | ≤20 words, one clause |

## Atomic bullets
- Each bullet = one claim (fact or verdict), not a sentence with reasoning.
- Reasoning goes in the table or the section takeaway — never inside bullets.

## Diagrams & tables over prose
- Anything comparative (drivers × options, pros/cons, RAID, RACI) is a table.
- If a diagram or table can carry it, prose must not restate it — the caption or a one-line summary is the only prose allowed.
- A diagram is judged by the information it carries per **reference/diagram-contract.md**, never by how small it is.
- Prose's only job: one line summarizing the table or diagram.

## Single source of truth
- Every fact appears exactly once in the document; every other mention is a reference, never a restatement.
- Never repeat a fact already given in Context, a table, or a diagram elsewhere in the ADR.
- Change IDs are defined once in `## Implementation Plan`; the option's Tech Details reuses them without re-describing the order.

## Sentence surgery
- Active voice, subject–verb–object, one clause.
- Prefer a number to an adjective: "fast" → "2×", "significant" → "3 ms", "large" → "500 users".
- Banned phrases — delete or rewrite:
  - "It is important to note that…" / "It should be noted that…"
  - "In order to" → "To"
  - "As mentioned above / earlier"
  - "Generally speaking" / "In general"
  - "Please note"
  - "The diagram shows X, Y, Z" (the caption is the summary)
  - "This means that" / "What this means is"
- Never restate what a diagram or table already shows.

## The driver-anchored "So what?" test
- Every prose sentence must move a decision-driver score or add a fact a future reader needs to trust or redo the decision — otherwise delete it.
- Run the delete-by-default pass on prose before presenting: cut ~20% of prose sentences, then re-add only what is load-bearing.
- Never cut a carrier row to hit the prose budget.
