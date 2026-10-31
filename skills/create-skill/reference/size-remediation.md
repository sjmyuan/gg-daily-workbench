# Size Remediation

Scope: how to fix an over-budget file while authoring. The reviewer owns the severity and
gaming-detection rules; this copy carries the levers and the integrity gate.

Chars are the **only** size gate; line count is informational. Reformatting cannot reduce
chars, so the real levers are structural: re-encode, reuse, cut weight, redistribute, reduce.

## Structural-integrity gate

A reduction is valid only if it measurably cuts chars **and** keeps one line = one idea.

- Snapshot before: capability count, steps per capability, knowledge subsections, when-to-use bullets, rules, guide rows, chars, lines.
- **Revert and redo** when lines dropped but chars barely moved — that is line-merging.
- **Revert and redo** when a line now bundles 2+ former bullets.

## Levers, in order

Stop as soon as the char budget is met.

### Re-encode
1. Turn procedural steps into decision/state tables or option matrices.
2. Keep tables narrow so the wide-cell exemption is not abused.

### Reuse
3. Point at an existing **local** reference instead of re-describing it.
4. Need doctrine owned by another skill? Write a scoped local slice; never link across skill folders.

### Cut weight
5. Delete meta-narration, why-explanations, redundant preambles, low-value edge cases.
6. Never drop required artifact fields, status vocabulary, or schema labels to meet a budget.

### Redistribute
7. Extract large rubrics from `<knowledge>` or capability steps into `reference/`; leave a one-line pointer and a guide row.
8. Two-stage extraction when one file is still too big: capabilities → `<knowledge>` tables → `reference/`.
9. Lift a long capability step into its own procedure file with a pointer back.
10. Split into a new skill only when the chunk has its own triggers and knowledge — it adds cross-skill overhead.

### Reduce
11. Dedupe: rules restating capabilities, preambles re-describing delegated skills, when-to-use restating the description.
12. Merge 2–3 small capabilities only when real chars are cut.
13. Trim edge cases and "why" text from steps.
14. Convert repeated bullets into a table.
15. Drop duplicated or low-value examples.

### Escalate
16. Accept and flag: a hub-scope skill may legitimately stay over budget after dedupe.
17. Present split-vs-accept to the user as ⚠️ Inconsistency; never pick silently.

## Never

- Merge bullet steps into one sentence to pass the line budget.
- Re-word untouched sentences to reach the char budget — delete duplicated content instead.
- Cut `<when-to-use-this-skill>`, capabilities, or required sections.
- Trim steps until they are ambiguous.
- Strip an example's "Applies <capability>" line.

Still over **2×** the char budget after every lever → the skill needs a real split, not more trimming.
