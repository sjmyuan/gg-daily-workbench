# Size Limits

Scope: authoring budgets for the files this skill creates. The reviewer owns the full
severity model; this copy carries the numbers and how to measure.

Sizes use **character count** (≈ tokens × 4) — the real context cost. Reformatting cannot
change chars; line count is a secondary scanability signal.

| File | Char budget | Line budget |
|---|---|---|
| SKILL.md | 12,000 | 150 |
| Each `reference/` file | 12,000 | 150 |
| Each `examples/` file | 9,000 | 150 |

- Line > 120 chars → tighten. Line > 200 chars → multi-item stuffing; split it.
- Exceptions: `description`, long URLs, Mermaid blocks, wide table cells.
- One line = one idea; a line bundling 2+ items is a violation even when short.

## Measure

```sh
python3 ../review-skill/scripts/measure_sizes.py <skill-dir-or-file>
```

Reports chars, bytes, lines, long-line hits, and budget status per file type.

Manual fallback — `wc -m` counts chars, `wc -c` counts **bytes** (never use it);
exclude table rows and the frontmatter `description` from the long-line scan.
