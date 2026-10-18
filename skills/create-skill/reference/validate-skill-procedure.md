# Validate-Skill Procedure

Used by **validate-created-skill** (step 2). Run the checks in order and report each finding with a severity label.

| # | Check | Fail severity |
|---|---|---|
| 1 | Required sections present and in order: frontmatter, when-to-use, knowledge, capabilities, optional rules. | 🔴 Major (order: 🟡 Minor) |
| 2 | `description` scores ≥9 per **description-quality** and covers every when-to-use scenario both ways. | 🟡 Minor |
| 3 | Capabilities use action-verb names, ordered steps, and carry no embedded reference data. | 🔴 Major |
| 4 | Knowledge holds reference material; large rubrics extracted; context-loading-guide is condition-first. | 🔴 Major |
| 5 | Prose follows **writing-style**. | Per its severity table |
| 6 | Prose is platform-agnostic per **platform-agnostic-writing**. | 🟡 Minor per reference |
| 7 | Every file is within **size-limits**; over-budget files remediated per **size-remediation**. | 🟡 Minor / 🔴 if >2× |
| 8 | One line = one idea; nothing fails the conciseness test per **conciseness-check**. | 🟡 Minor |
| 9 | Every capability has a linked example; examples meet **example-standards**, stay traceable, and contradict no rule. | 🔴 Major (subset-only: 🟡 Minor) |
| 10 | Rules route "when → capability" without restating capability content. | 🟡 Minor |
| 11 | Each capability ends with a validation or checklist step per **evaluation-process**. | 🟡 Minor (with no validation example: 🔴 Major) |
| 12 | Declared pipeline and sub-agent integration points hold per **pipeline-integration**; check only relationships the files declare themselves. | 🟡 Minor |
| 13 | Scripts and CLI steps meet **script-and-cli-policy**: justified, Python stdlib only or stated exception, fields documented, named by a step, no dependencies/network/prompts. | 🔴 Major (orphan script) / 🟡 Minor |
| 14 | Findings reported with **severity-levels**; each has an actionable fix. | — |

## Order of operations

1. Snapshot the structure before judging size: capability count, step count, knowledge rows, rule count, guide rows.
2. Re-measure after every fix; compare with `--diff` to confirm chars dropped without step or line merging.
3. Revert to the last valid state on a 🔴 Blocker and redo with a real lever.
4. Stop when the gates pass; do not keep trimming a passing file.

## Structural-integrity gate

- Chars are the only size gate; a passing reduction also keeps one line = one idea.
- Lines dropped while chars barely moved (line-merging) → 🔴 Blocker: restore the structure and redo.
- Any line bundling 2+ former steps → 🔴 Blocker: split back to one line per step.
