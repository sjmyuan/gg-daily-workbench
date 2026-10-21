# Plan File Format

Layout for the files **export-plan** writes into a feature folder.

## plan.md

1. Start with the ratified `## Scope Boundary` block (see **scope-boundary**): **May change**, **Expected files**, **Must not change**, **Protected zones**.
2. Follow with the complete numbered step list; each step states one objective in one sentence. Abandoned steps keep their number and carry `⏭` with a reason.
3. A rework is a **new sibling file** `rework-<date>.md` (per **rework-plan-convention**): `# Rework <date>` + one-line trigger, its own **Scope Boundary**, and numbered steps — `plan.md` is the frozen original and is never modified.
4. An amendment adjusts the same `plan.md` in place (per **plan-amendment**): add steps by next number or letter suffix, mark obsolete pending steps `⏭ abandoned — <reason>`, never renumber.

## context.md

Concise (see **concise-writing**): one bolded takeaway per section, tables for requirements/constraints, compact bullet lists for references.

- Original request, change type, root cause/requirement summary
- TDD rationale; boundary rationale (see **scope-boundary**); branch + base (see **plan-prerequisites**)
- Constraints, assumptions, codebase references
- `## Reworks` manifest: one table row per rework (date, mode, cell, trigger, file, status) so resume finds the active file
- `## Amendments`: one row per in-place plan change (date, trigger, added, abandoned, boundary, reason)
- For an **orchestrate-feature-delivery** cell: the agent brief's spike references (ADR files, solution-doc sections)
