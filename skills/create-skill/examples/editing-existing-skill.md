# Example: Edit an Existing Skill — Merge, Retire, and Rename

**Scenario**: A skill grew to four capabilities where three would do. An open-ended "improve" request must
leave it **smaller**. Demonstrates **edit-skill**: absorption test, funding rule, ripple, ledger.

**Applies**: **edit-skill** (routes to **create-skill-file**, **validate-created-skill**)

## Input / Context

`skills/draft-release-notes/SKILL.md`:

- capabilities `<collect-release-items>`, `<write-release-notes>`, `<format-release-note>` (noun-named), `<check-release-notes>`
- 5 rules, 12 knowledge rows, 4 guide rows
- 4 examples; references `release-note-template.md`, `formatting-rules.md`

User: "Improve this skill — writing and formatting feel like one job, and reviewers keep asking for the same thing."

## Walkthrough (edit-skill steps)

1. **Scope** — target only the user-provided files; never a same-named live copy.
2. **Inventory and count** — 4 capabilities, 21 steps, 12 knowledge rows, 5 rules, 4 guide rows, 4 examples,
   2 references, 9,240 chars. These are the ledger's "before" column.
3. **Triage intent** — open-ended "improve" → run `review-skill`'s **review-skill-file** first.
   - 🔴 `<write-release-notes>` and `<format-release-note>` share one trigger with 60% step overlap: merge candidate.
   - 🟡 rule 4 restates `<check-release-notes>` step 3.
   - 🟡 `formatting-rules.md` is routed from one step only.
4. **Classify, absorb, fund** — classification and payment happen together:
   - **Absorption test** — "formatting" fails question 2: `<write-release-notes>` covers most of it → extend, add no tag.
   - **Absorption test, question 4** — it is a variant of an existing scenario, not a new trigger → add no file.
   - **Merge** — fold the 2 unique steps into `<write-release-notes>`; drop its 3 duplicate steps.
   - **Merge, retirements** — the tag, rule 3, its guide row, and its example all go with it.
   - **Inline** — `formatting-rules.md` has one consumer → fold its table into the survivor's steps. Delete the file and its guide row.
   - **Rename** — `<format-release-note>` is noun-named, but the merge deletes it, so no rename is needed.
   - **Funded** — 2 folded steps and 1 `Applies` line land against 9 retirements.
5. **Route (existing-file mode)** — **create-skill-file** edits both capabilities and the knowledge table,
   cuts rules 5 → 4, drops two guide rows. **create-skill-examples** folds the formatting scenario into
   `write-release-notes.md`. **create-skill-references** deletes `formatting-rules.md`.
6. **Ripple** — remove the `<format-release-note>` tag from rules, guide rows, and the example `**Applies**` line.
   Drop the `formatting-rules.md` route from knowledge and from the step that inlined it.
   Keep `release-note-template.md` as the single template.
7. **Validate after each change** — **validate-created-skill**: 16 checks pass, no 🔴; every merged step lands;
   no dangling link to the deleted reference.
8. **Re-measure and report** — re-count, then close with the ledger.

## Expected Output

| Element | Before | After | Δ |
|---|---|---|---|
| Capabilities | 4 | 3 | −1 |
| Steps | 21 | 18 | −3 |
| Knowledge rows | 12 | 12 | 0 |
| Rules | 5 | 4 | −1 |
| Guide rows | 4 | 2 | −2 |
| Examples | 4 | 3 | −1 |
| References | 2 | 1 | −1 |
| Chars | 9,240 | 8,410 | −830 |

- `−1 capability, −3 steps, −1 rule, −2 guide rows, −1 example, −1 reference, −830 chars` — every addition funded.
- Knowledge rows held flat: the inlined table replaced a row rather than adding one.
- The reviewer's 🔴 and both 🟡 findings resolve through retirements, not new text.
- The tempting fifth capability ("check tone") was rejected: `<check-release-notes>` already hosts it.
