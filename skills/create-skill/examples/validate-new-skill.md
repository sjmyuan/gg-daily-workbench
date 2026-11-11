# Example: Validate a Newly Created Skill Before Delivery

**Scenario**: The first draft of a skill exists and the user wants a quality check before presenting it. The input is the pre-fix state; `create-skill-file` produces the corrected one. Demonstrates **validate-created-skill**.

**Applies**: **validate-created-skill**

## Input / Context
First draft of `skills/write-commit-message/SKILL.md` — one capability, no example, footer format written as prose.

## Expected Output — validation report
| Check | Result |
|---|---|
| Content classification | 🟡 `<write-commit-message>` step 2 restates the 72-char limit already held in knowledge |
| Content adequacy | 🔴 "when needed" is not a decidable condition |
| Structure & order | ✅ sections present in order |
| Description score | ✅ 9/10, trigger covers all scenarios |
| Capability naming | ✅ `<write-commit-message>` action verb |
| Knowledge placement | ✅ facts only, guide condition-first |
| Prescriptiveness | ✅ contractual: micro-steps are correct for a fixed footer format |
| Rationale | 🟡 the 72-char limit states no reason in its knowledge entry |
| Writing style | ✅ directive voice, BLUF, no banned phrases |
| Size | 🟡 SKILL.md 12,400/12,000 chars — over char budget |
| Conciseness | ✅ one line = one idea |
| Evaluation process | ✅ `<write-commit-message>` ends with a verify step |
| Behavioral | ➖ not run — contractual capability; its gates prove the output |
| Example coverage | 🔴 `<write-commit-message>` has no linked example |
| Template fidelity | 🔴 the BREAKING CHANGE footer is described in prose; no literal skeleton |
| Rules routing | ✅ "when → capability", no content restated |

## Issues Found & Fix
- Duplicate fact (🟡 Minor) → justification deletes the step's copy and leaves the step citing knowledge; rewording would keep two owners.
- Undecidable step (🔴 Major) → replace "when needed" with the change condition; content fixes precede style fixes.
- Size overrun (🟡 Minor) → apply **size-remediation**: extract the footer-format table to `reference/commit-format.md`, re-measure, then re-validate.
- Missing example (🔴 Major) → return to **create-skill-examples**, add `examples/write-commit-message.md`, then re-validate.
- Prose-only template (🔴 Major) → emit the footer as a fenced skeleton in `reference/commit-format.md` — the same extraction the size fix performs.
- Missing constraint reason (🟡 Minor) → add the reason once to the knowledge entry that owns the 72-char limit; do not repeat it in each step.

## Final
Validation passes after the fixes; report the final file tree to the user.
