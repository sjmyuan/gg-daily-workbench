# Plan File Format

Layout for the files **export-plan** writes into a feature folder.

One artifact, one job: `index.md` = state · `context.md` = charter · `plan.md` = execution ·
`rework-<date>.md` = delta · git/PR/CI = record. Boundaries and budgets: **doc-budgets**.

## plan.md

1. Start with the ratified `## Scope Boundary` block (see **scope-boundary**): **May change**, **Expected files**, **Must not change**, **Protected zones**.
2. Follow with the complete numbered step list; each step states one objective in one sentence. Abandoned steps keep their number and carry `⏭` with a reason.
3. Each step that touches existing code declares `Source`, `Ref`, and `Equality` per **change-provenance**; `generate` carries its justification.
4. A rework is a **new sibling file** `rework-<date>.md` (per **rework-plan-convention**):
   `# Rework <date>` + one-line trigger, its own **Scope Boundary**, **Done means**, and numbered delta steps.
   `plan.md` is the frozen original and is never modified.
5. An amendment adjusts the same `plan.md` in place (per **plan-amendment**): add steps by next number or letter suffix, mark obsolete pending steps `⏭ abandoned — <reason>`, never renumber.

## context.md

The cell's **charter** — why it exists, what must hold, what is unknown, how done is judged.
Target **40–60 lines**; hard cap **8,000 chars / 120 lines** (see **doc-budgets**).

- **Outcome** + **Why** (≤3 lines): problem, decision served, ADR link, adopted/do-not-re-litigate status
- **Must hold** (≤6): user-ratified constraints + operational invariants not already in `plan.md`
- **Unknowns** (≤5): unknown — resolving step — fallback; delete when resolved
- **Done means** (≤5 rows): criterion, verification, pass rule
- **Pointers** (≤6): cell-specific ADR, solution-doc section, findings, evidence — paths only, never copies
- **Open concerns** (≤5): deferred Minor/risk — owner or next action; delete when resolved
- **State**: active plan/rework file
- **Execution**: latest handoff only — status, `base7..head7`, PR, 1-line evidence, 1-line review outcome
- **Reworks** manifest (≤8 rows; drop oldest done rows — files remain): date, mode, cell, trigger, file, status
- **Amendments** (≤8 rows; ⏭ markers are the record): date, trigger, added, abandoned, boundary, reason

Not here: Scope Boundary, steps, TDD rationale, and plan decisions (`plan.md`); feature status,
wave, branch, and PR (`index.md`); pre-flight evidence (synthesize into a decision or an Unknown);
commit tables, test matrices, deviations, incidents — do not write them; git/PR are the history.

`## Execution` is written by **execute-plan**, latest round only — never appended.
Template and admission test: **[doc-budgets.md](doc-budgets.md)**.
