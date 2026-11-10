# Size Limits

Scope: the reviewer's size gate. The authoring side (create-skill) duplicates the numbers and the
lever order as a slice; neither copy may diverge in a budget or severity.

Sizes use **character count** (≈ tokens × 4) — the real context cost. Reformatting cannot change chars, so the budget cannot be gamed; line count is a secondary signal.

| File | Char budget | Line budget | Over-budget severity |
|---|---|---|---|
| SKILL.md | 12,000 | 150 | ≤2× 🟡 Minor · >2× 🔴 Major |
| Each `reference/` file | 12,000 | 150 | 🟡 Minor (on-demand; consider splitting) |
| Each `examples/` file | 9,000 | 150 | 🟡 Minor (on-demand; trim) |

- Line > 120 chars → 🟢 Nit; line > 200 chars → 🟡 Minor (multi-item stuffing). Exceptions: `description`, long URLs, Mermaid blocks, wide table cells.
- One line = one idea: a line bundling 2+ logical items is line-stuffing → 🟡 Minor even when short.
- Gaming: when the line budget passes but the char budget is exceeded, flag the char severity AND note the line count is misleading (line-merging).

## How to measure

Run the measurement script from the skill folder:
`python3 scripts/measure_sizes.py <skill-dir-or-file>` — reports chars, bytes,
lines, >120/>200 violations (excluding table rows, the frontmatter `description`,
and mermaid blocks), and budget status per file type.

Manual fallback (no script available) — state in the review that the machine measure did not run:
- **Character count** — use `wc -m` or python `len(open(f).read())`, NOT `wc -c`,
  which counts **bytes**; emoji and multi-byte chars inflate bytes above chars
  (a 6-char emoji sequence is 1 char and 4+ bytes), so a byte count misreports the budget.
- **Long-line scan** — exclude lines starting with `|` (table rows) and the
  frontmatter `description`; both are exempt per the rules above.
