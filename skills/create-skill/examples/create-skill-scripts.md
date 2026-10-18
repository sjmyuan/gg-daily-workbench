# Example: Choose Automation for a Capability Step

**Scenario**: A drafted skill must list every Markdown table in a document and flag wide cells; the user asks
whether to add a script. Demonstrates the CLI-first decision and, where no CLI fits, a justified Python script.

**Applies**: **create-skill-scripts**

## Input / Context

`skills/doc-auditor/SKILL.md` capability `<check-tables>` step 2 reads: "List all tables and flag rows over 200
characters." The skill folder has `SKILL.md`, `examples/`, and no `scripts/`.

## Decision (create-skill-scripts step 1)

| Test | Result |
|---|---|
| No installed CLI produces the result | Pass — `awk`/`grep` cannot split table blocks by header and exemption |
| A capability step runs it every time | Pass — step 2 runs on every audit |
| Output must be deterministic and machine-checkable | Pass — the step prints a per-table row count |
| Would need >5 inline commands | Pass — block detection, exemption, and counting |

Verdict: script justified. A one-off "count lines in a file" would have failed tests 2 and 4 — that is `wc -l`.

## Created Script (create-skill-scripts steps 2–4)

`scripts/audit_tables.py` — Python 3 stdlib only, 84 lines:

```python
#!/usr/bin/env python3
"""List Markdown tables and wide rows.

Usage: python3 scripts/audit_tables.py <file.md>
Exit:  0 no findings, 1 findings, 2 usage error
"""
import sys


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    ...
    print(f"tables={tables} wide_rows={wide}")
    return 1 if wide else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

Capability step 2 now reads: "Run `python3 scripts/audit_tables.py <file.md>`; `tables=` and `wide_rows=` are the
counts. Exit `1` means findings exist; exit `2` means fix the arguments."

Directory layout gains `scripts/` and `examples/audit-markdown-tables.md` is added for this capability.

## Validation (create-skill-scripts step 5)

| Run | Command | Expected |
|---|---|---|
| Usage | `python3 scripts/audit_tables.py` | Prints usage, exit `2` |
| Passing sample | `python3 scripts/audit_tables.py docs/clean.md` | `wide_rows=0`, exit `0` |
| Failing sample | `python3 scripts/audit_tables.py docs/wide.md` | `wide_rows=3`, exit `1` |

Rejected during validation: an earlier draft imported `yaml` for frontmatter skipping. It became a stdlib `---`
scan, because a third-party dependency is a 🔴 Major finding.

## Considered and Rejected

| Request | Outcome |
|---|---|
| Shell script piping `grep -n '^|' \| awk …` | Fails portability and the >5-commands test; a one-off `grep -c` would have passed |
| Node script | No npm package involved; the Python exception list does not apply |
