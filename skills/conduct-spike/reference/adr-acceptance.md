# ADR Acceptance Gate

Loaded by **decide-spike-problems** step 4 and **accept-adrs** step 2. Run it on every ADR before the ADR is presented or adopted — including ADRs drafted headlessly inside an area session.

Pass every blocking check and report each failure by its ID. Fix the ADR, never relax a check.

## Blocking checks

| ID | Check | Passes when | Fails when |
|---|---|---|---|
| G1 | Section contract | Every required section appears once, in the order below | Any section missing, or an "abridged" ADR offered in its place |
| G2 | Takeaway first | Every section opens with a bolded one-line takeaway | Context opens with background; sections are prose walls |
| G3 | Problem statement | `**Decision:**` ≤15 words, then ≤3 sentences in SCQA order | The request pasted; no question; no outcome stated |
| G4 | Drivers measurable | Each driver tagged `HC n` / `SP n` with metric, threshold, and measurement | "Low cost", "good performance", untagged bullets |
| G5 | Options distinct | 2–4 distinct mechanisms, each `Option N: <name>`, label reused verbatim everywhere | One option; vendor twins; letters or bare names |
| G6 | Full evaluation | Every option carries Verdict, What it is, How it works, Driver impact, Concerns, Pros, Cons | A one-line option; an option with no Concerns |
| G7 | Driver coverage | Every driver appears for every option with mark, measured value, evidence, confidence | Only the winner is evaluated |
| G8 | Matrix agreement | Comparison-matrix marks equal each card's Driver impact marks | Matrix shows ✅ where the card shows ⚠️ |
| G9 | Evidence on the claim | Every decision-flipping claim carries `file:line`, or **unverified** plus what would settle it | Citations only in another document; inference stated as fact |
| G10 | Tech details | Chosen option has ordered `C1…Cn` changes with `file:line`, diff, confidence, verify, rollback; every option has its own target-state diagram | No change set; one diagram shared across options |
| G11 | Standalone | A reader with no session context can decide and start at `C1` | Understanding the ADR requires a notes doc or another ADR |
| G12 | Template checklist | `draft-adr`'s **adr-quality-checklist** run for prose, diagrams, and metadata | Checklist never run |

`G12` covers style and diagram mechanics that this gate does not restate. The other eleven are owned here.

## Required sections

Use the names and order from `draft-adr`'s **adr-template**:

1. Title, `Status`, `Area`, `Owners`, `Date`
2. `## Context and Problem Statement` — decision line, SCQA, context diagram
3. `## Decision Outcome` — `**Chosen:**` with justification naming the drivers, `**Start here:**`, target-state diagram
4. `## Consequences` — trade-off line plus Positive Consequences, Risks, Security
5. `## Decision Drivers` — `HC n` / `SP n`, metric, threshold, measurement
6. `## Considered Options` — the `Option N` list
7. Comparison matrix — table, plus a diagram only when it adds a view
8. `## Evaluation of the Options` — one card per option, template field order
9. `## Implementation Plan` — order, prerequisites, change table, new files
10. `## References` — evidence used, optional

`Area` is required on a spike ADR and must match `scope.md`.

## Verdict

Emit one line per ADR, then the failing checks:

```
adr-<area>-<NN>-<problem>.md — ACCEPT (12/12)
adr-<area>-<NN>-<problem>.md — REVISE: G4 (SP 2 has no threshold), G7 (Option 3 lacks Driver impact) — unverified: throughput at 2× peak
```

A `REVISE` verdict blocks presentation and adoption. Re-run the gate on the changed sections only.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| "Full record per the template" claimed, half the sections present | The gate ran after presentation, or not at all | Run the gate before the ADR leaves the session; never present an abridged ADR |
| Drivers read as a wish list | No metric, threshold, or measurement | Rewrite each driver as a testable statement or drop it |
| Comparison is a feature list | Driver-impact rows carry no measured value | Measure or mark **unverified** — never leave the cell empty |
| A confident decision with no citations | Evidence lived in a separate doc the ADR never cites | Cite `file:line` at the claim; re-read what the decision turns on |
| The ADR only makes sense after reading the notes doc | Investigation detail leaked into the decision | Move the narrative to notes; keep the decision and its citations |
| Twelve-page ADR for a reversible choice | Volume mistaken for rigor | Keep the evaluation; cut prose, not checks; prefer the cheaper option when drivers tie |

## Fast-path minimum

A single-decision spike passes the same gate. When the choice is reversible and cheap, the ADR may stop at 2 options.
It never drops below two distinct mechanisms, measured drivers, or the chosen option's change set when code is accessible.
