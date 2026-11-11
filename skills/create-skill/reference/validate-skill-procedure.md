# Validate-Skill Procedure

Used by **validate-created-skill** (step 1). Run the checks in order and report each finding with a severity label. Content checks 1–2 run first: a passing structure never offsets a failed content gate.

| # | Check | Fail severity |
|---|---|---|
| 1 | Every element classifies per **content-model**: no fact carrying an order, no procedure that only forbids, no guard describing work. | 🔴 Major |
| 2 | Adequacy and justification gates per **content-model**: an unstated inferable fact, an objective no step produces, a missing guard, and any element whose removal breaks nothing. | 🟡 Minor (missing guard for a known misapplication: 🔴 Major) |
| 3 | Sections present and in order: frontmatter, when-to-use, knowledge, capabilities, rules. | 🔴 Major (order: 🟡 Minor) |
| 4 | Each element sits in its class section; knowledge holds facts and judgment, rubrics extracted, context-loading-guide condition-first; a reference earns existence by size or load timing, never tidiness. | 🔴 Major |
| 5 | Skill and capability names use action verbs; capabilities hold ordered steps, or judgment content under a judgment regime; no embedded reference data or constraint bullets. | 🔴 Major |
| 6 | `description` scores ≥9 per **description-quality** and covers every when-to-use scenario both ways. | 🟡 Minor for 6–8 · 🔴 Major for ≤5 |
| 7 | Prose follows **writing-style**. | 🟡 Minor when systematic in one file · 🔴 Major when pervasive across files |
| 8 | Prose is platform-agnostic per **platform-agnostic-writing**. | 🟡 Minor for one reference · 🔴 Major for several across files |
| 9 | Every file is within **size-limits**; over-budget files remediated per **size-remediation**. | 🟡 Minor / 🔴 if >2× |
| 10 | One line = one idea; nothing fails the conciseness test per **conciseness-check**. | 🟡 Minor |
| 11 | Every capability has a linked example; examples meet **example-standards**, stay traceable, and contradict no rule. | 🔴 Major (subset-only: 🟡 Minor) |
| 12 | Rules route "when → capability" and carry one guard per known misapplication, without restating capability content. | 🟡 Minor |
| 13 | Each capability ends with a gate or grade per **evaluation-process**. | 🟡 Minor (with no validation example: 🔴 Major) |
| 14 | Declared pipeline and sub-agent integration points hold per **pipeline-integration**; check only relationships the files declare themselves. A callee naming the skill or agent that loads it → 🟡 Minor. | 🟡 Minor |
| 15 | Scripts and CLI steps meet **script-and-cli-policy**: justified, Python stdlib only or stated exception, fields documented, named by a step, no dependencies/network/prompts. | 🔴 Major (orphan script) / 🟡 Minor |
| 16 | Findings reported with **severity-levels**; each has an actionable fix. | — |
| 17 | Artifact templates are literal, single-owner skeletons; examples reproduce headings, field labels, order, and statuses; abridged output is labelled. | 🔴 Major (label-only: 🟡 Minor) |
| 18 | The example set is continuous: identifiers, counts, statuses, and doctrine order agree; a shared cross-skill example is updated in both. | 🟡 Minor (invalidating: 🔴 Major) |
| 19 | Prescriptiveness matches each capability's regime per **empowerment-model**: no step a capable model would take unaided; a judgment capability states outcome, tradeoffs, failure modes, and an exemplar. | 🟡 Minor (judgment capability holding steps only: 🔴 Major) |
| 20 | Non-obvious constraints keep one reason; delegation boundaries appear where the agent makes judgment calls. | 🟡 Minor |
| 21 | A judgment skill with sample tasks runs the behavioral test per **reference/behavioral-acceptance.md**; every skipped run is reported with its reason. | 🟡 Minor (flat delta left in place: 🔴 Major) |

## Order of operations

1. Snapshot the structure before judging size: capability count, step count, knowledge rows, rule count, guide rows.
2. Fall back to checks 1–2 when a structural fix changed meaning — a tidier section is not a corrected class.
3. Re-measure after every fix; compare with `--diff` to confirm chars dropped without step or line merging.
4. Revert to the last valid state on a 🔴 Blocker and redo with a real lever.
5. Stop when the gates pass; do not keep trimming a passing file.
6. Separate **introduced** from **pre-existing** findings; report both, but never block a scoped fix on a pre-existing budget failure.
7. When artifact templates exist, run `review-skill`'s `check_artifacts.py` with the template's field and zone lists before the manual checks; if the tool is absent, say so in the report.
8. Run the behavioral test once at delivery, never after each edit; it grades the shipped skill, not the draft.

## Structural-integrity gate

- Chars are the only size gate; a passing reduction also keeps one line = one idea.
- Lines dropped while chars barely moved (line-merging) → 🔴 Blocker: restore the structure and redo.
- Any line bundling 2+ former steps → 🔴 Blocker: split back to one line per step.
