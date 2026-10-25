# Repo Expertise

The target repo usually documents its own rules. Resolve them before judging the change — a repo
sentence outranks a reviewer preference, and a missing source is itself a finding about the review.

## Source priority

| Priority | Source | Settles |
|---|---|---|
| 1 | Repo-local skills and agents | Procedure, required sections, prohibitions |
| 2 | `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING*` | Commands, style, review rules, PR shape |
| 3 | ADRs and architecture docs | Placement, layering, naming, approved patterns |
| 4 | Codemaps, module READMEs, glossaries | Boundaries, ownership, domain language |
| 5 | Build, lint, test, and CI config | Commands and rules that are actually enforced |
| 6 | `CODEOWNERS`, runbooks, release docs | Approval path, deploy order, rollback |
| 7 | Recent practice — ≤10 commits, branches, PRs | Unwritten convention, only when 1–6 are silent |

- Read only the sources governing the changed area; a whole-repo doc sweep wastes the review budget.
- A hard prohibition in any source applies, even when a lower-priority source disagrees.
- Priority 7 is evidence of practice, not of intent — label it `observed in N of M`.

## Evidence card

One row per fact. A fact without a source does not enter the card.

| Field | Value | Evidence |
|---|---|---|
| Changed area | module or document under review | diff |
| Governing rules | one row per rule | `path:LINE` |
| Commands | build, test, lint, run | `path:LINE` |
| Placement convention | where this kind of code lives | `path:LINE` or `observed in N of M` |
| Known debt | documented workarounds and accepted gaps | `path:LINE` |
| Gaps | sources absent or silent on the changed area | search performed |

## How expertise changes the review

| Situation | Effect on the report |
|---|---|
| Change violates a documented rule | Finding at its severity, quoting the rule and its `path:LINE` |
| Change follows a rule the reviewer dislikes | Not a finding — record the rule in the card |
| Sources silent and modules disagree | ⚠️ Inconsistency with both variants, never a defect |
| Documented rule looks obsolete | Challenge, not a finding |
| Two sources conflict | Cite both and raise a challenge; never pick silently |
| Convention claim with no source | Drop it, or raise it as a challenge |

## Gaps are output

| Gap | Report as |
|---|---|
| No placement rule for the changed area | Challenge — the move may be unnecessary |
| No test or build command documented | Challenge — the review cannot confirm behavior |
| No ADR for a new pattern the change introduces | Challenge — pattern approval is missing |
| Docs contradict the code | ⚠️ Inconsistency, both sides anchored |

## Validation

- [ ] Every convention-based finding cites a source line
- [ ] No "project style" claim without a source
- [ ] Absent or silent sources appear as gaps or challenges
- [ ] Recent practice is used only where priorities 1–6 are silent
- [ ] The card fits in the report's Repo Expertise block without restating the docs
