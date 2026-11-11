# ADR Quality Checklist

Loaded by **compile-adr** step 7. Pass every item before presenting the ADR; fix the ADR, never the checklist.

## Decision

- [ ] Problem statement is clear, scoped, unambiguous, ≤3 sentences in SCQA order
- [ ] Every driver has a metric, a threshold, and a measurement, tagged `HC n` / `SP n`
- [ ] Hard constraints and soft preferences are separated
- [ ] The chosen option's justification names the drivers it wins on
- [ ] No chosen option rests on a driver that never received a measured value

## Options

- [ ] At least 2 distinct mechanisms were evaluated; near-duplicates merged or parked
- [ ] Every option reuses its `Option N: <name>` label in every section, table, and diagram
- [ ] Every option card has Verdict, What it is, How it works, Driver impact, Concerns, Pros, and Cons
- [ ] "How it works" is an ordered flow a reader can follow without reading the source code
- [ ] Every option card's Driver impact lists every driver, with the evidence and confidence
- [ ] Every quantitative claim carries a number and its evidence reference
- [ ] Every pro and con names the driver it moves
- [ ] Drivers knocked out by a hard constraint say which constraint, on the option's own row

## Diagrams

- [ ] Every option has its own target-state diagram; no two options share one
- [ ] The context diagram names volumes, protocols, and external systems
- [ ] Every diagram satisfies **reference/diagram-contract.md**
- [ ] No diagram only re-encodes a table or list already in the ADR
- [ ] Every Mermaid block validates with 0 errors via `draw-mermaid-diagrams`
- [ ] Every option's card marks agree with the comparison matrix
- [ ] No diagram contradicts a driver, a verdict, or the chosen option

## Implementability

- [ ] The chosen option has an ordered `## Implementation Plan` with change IDs
- [ ] Every change names `file:line` + symbol, its diff or exact config value, and its confidence
- [ ] Every change has a verification step and a rollback line
- [ ] New files, config keys, dependencies, and data migration are listed
- [ ] An engineer who did not join the session can start at `C1` without asking a question

## Prose

- [ ] A bolded one-line takeaway opens every section
- [ ] No sentence exceeds 20 words; no banned phrases
- [ ] Detail sits in carriers — tables, numbered flows, diagrams, diffs — not in prose
- [ ] Single source of truth: no fact restated across sections, tables, diagrams, or diffs
- [ ] Captions carry the takeaway; prose does not restate them
- [ ] Metadata (title, owners, status) is populated
- [ ] Delete-by-default pass run on prose only (~20% cut); carriers left intact
