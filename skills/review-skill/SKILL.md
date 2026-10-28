---
name: review-skill
description: Review SKILL.md files for structure, section purpose, naming, duplication, and script/CLI usage. Use when reviewing, diagnosing, or checking a copilot skill's structure, triggers, naming, quality, or tooling.
---

<when-to-use-this-skill>
- User asks to review a skill file (SKILL.md)
- User asks to diagnose or get feedback on a skill file before improving it (review-only — edits are applied via `create-skill`)
- User asks whether a SKILL.md is correctly structured
- User asks for feedback on section placement, duplication, or capability format in a skill file
- User asks whether a skill will trigger or activate correctly
- User asks whether a skill's name or capability names follow naming conventions
- User asks whether a skill's scripts or CLI invocations are justified and safe
</when-to-use-this-skill>

<knowledge>

<named-standards>
Steps cite these standards by name; load the Details file.

| Standard | Rule | Details |
|---|---|---|
| **section-semantics** | Section-purpose table and common structural violations. | [reference/section-semantics.md](reference/section-semantics.md) |
| **trigger-correctness** | Description trigger clarity and when-to-use consistency. | [reference/trigger-correctness.md](reference/trigger-correctness.md) |
| **severity-levels** | Severity definitions and Blocker-vs-Major guidance. | [reference/severity-levels.md](reference/severity-levels.md) |
| **size-limits** | Char/line budgets per file type, line-length guard, gaming detection, measurement script. | [reference/size-limits.md](reference/size-limits.md) |
| **size-remediation** | Ordered remediation plus the structural-integrity gate (chars are the only gate; line/step-merging is 🔴). | [reference/size-remediation.md](reference/size-remediation.md) |
| **evaluation-process** | Output-evaluation patterns and severity when absent. | [reference/evaluation-process.md](reference/evaluation-process.md) |
| **naming-conventions** | Naming rules for the skill name, capability names, and knowledge names. | [reference/naming-conventions.md](reference/naming-conventions.md) |
| **conciseness-check** | Criteria for unnecessary content across SKILL.md, references, and examples. | [reference/conciseness-check.md](reference/conciseness-check.md) |
| **writing-style** | Directive voice, BLUF, hard caps, banned phrases, no narration. | [reference/writing-style.md](reference/writing-style.md) |
| **platform-agnostic-writing** | No platform tool names, no concrete context paths, detect-don't-assume. | [reference/platform-agnostic-writing.md](reference/platform-agnostic-writing.md) |
| **script-and-cli-policy** | Automation decision order, four script tests, Python-stdlib rule, contracts, anti-pattern severities. | [reference/script-and-cli-policy.md](reference/script-and-cli-policy.md) |
| **pipeline-integration** | Skill↔skill and skill↔sub-agent integration checklists. | [reference/pipeline-integration.md](reference/pipeline-integration.md) |
| **artifact-consistency** | One literal template per schema; examples reproduce its shape; identifiers/counts stay continuous; shared examples update together. | [reference/artifact-consistency.md](reference/artifact-consistency.md) |
| **same-name-live-copy-ban** | Review only the user-provided file; never a live same-named copy. An installed copy needs its exact path. | — |
</named-standards>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Before writing output — load first, every review | Output format | [examples/skill-file-review.md](examples/skill-file-review.md) |
| Noun-named capabilities or inline examples detected | Naming/inline model | [examples/noun-capabilities-and-inline-examples.md](examples/noun-capabilities-and-inline-examples.md) |
| Mostly well-structured skill (few or no major findings) | Near-passing model | [examples/clean-skill-review.md](examples/clean-skill-review.md) |
| Trigger failures dominant | Trigger-failure model | [examples/trigger-correctness-violation.md](examples/trigger-correctness-violation.md) |
| Size/density findings dominant | Size/gaming model | [examples/size-and-line-stuffing-review.md](examples/size-and-line-stuffing-review.md) |
| Writing-style findings dominant | Style model | [examples/writing-style-review.md](examples/writing-style-review.md) |
| Skill references another skill, or dispatches / is loaded by sub-agents | Integration checklist (skill-skill + skill-agent) | [reference/pipeline-integration.md](reference/pipeline-integration.md) |
| Sub-agent dispatch or embedded-execution findings dominant | Agent-integration model | [examples/agent-integration-review.md](examples/agent-integration-review.md) |
| Examples ship artifact templates, or several examples share one scenario | Template fidelity, identifier continuity, machine checker | [reference/artifact-consistency.md](reference/artifact-consistency.md) |
| Reviewing example consistency | Findings model: schema drift, identifier/count mismatch, shared-example gap | [examples/artifact-consistency-review.md](examples/artifact-consistency-review.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<review-skill-file>
**Objective**: Evaluate a SKILL.md file for correct section structure, separation of concerns, and absence of duplication.

**Note**: Do not modify the skill file during review; suggest changes as descriptions or patch snippets.

**Steps**:
1. Apply **same-name-live-copy-ban**; read the full skill and apply **reference/section-semantics.md** for purposes and violations.
   a. Verify frontmatter, when-to-use, knowledge, capabilities, and rules are present; missing → 🔴 Major.
   b. Verify order frontmatter → when-to-use → knowledge → capabilities → rules; out-of-order → 🟡 Minor.
   c. Measure size with `scripts/measure_sizes.py`, else chars and lines, per **reference/size-limits.md**.
      Over budget → recommend per **reference/size-remediation.md**; line/step-merging → 🔴 Blocker.
2. **Check description and triggers** — load **reference/trigger-correctness.md**:
   a. Verify the two-part template via **reference/description-template.md**; missing trigger phrase → 🔴 Major.
   b. Score the five dimensions via **reference/description-scoring.md**; report x/10; ≤5 → 🔴 Major, 6–8 → 🟡 Minor.
   c. Verify trigger verbs and scenarios match the when-to-use bullets both ways; gap → 🟡 Minor.
   d. Missing when-to-use → 🔴 Major.
   e. Scope contradiction between `description` and when-to-use → 🔴 Major.
3. Verify each capability is an ordered procedure — fact lists, reference tables, or constraint bullets drift into knowledge.
4. **Check output evaluation** — load **reference/evaluation-process.md**.
   Each capability needs a validation or checklist step; absent → 🟡 Minor; absent with no validation examples → 🔴 Major.
5. **Check conciseness, style, and growth** — load **reference/conciseness-check.md**; apply **reference/size-limits.md** to every file:
   a. Writing style — load **reference/writing-style.md**; flag per its severity table.
   b. Platform-agnostic writing — load **reference/platform-agnostic-writing.md**; tool names or context paths → 🟡 Minor.
   c. Growth audit — count the elements, then report merge candidates, superseded elements, and orphans per **reference/conciseness-check.md**.
6. Verify a `<rules>` section exists — missing → 🔴 Major. Each rule answers "when X → use capability Y" or states a guard ("never …"); restating capability content → 🟡 Minor.
7. Verify knowledge holds reference material; rubrics embedded in SKILL.md instead of `reference/` → 🔴 Major.
8. **Check naming** — load **reference/naming-conventions.md**:
   a. Frontmatter `name` uses an action verb (`edit-svg`, not `svg-editor`); noun phrase → 🔴 Major.
   b. Capability names use action verbs; noun-named → 🔴 Major.
   c. Knowledge subsections and named-standards rows use noun phrases; an action-verb name signals leaked procedure → 🟡 Minor.
9. Verify on-demand context sits in a condition-first `<context-loading-guide>` inside knowledge — not a standalone `<examples>`
   section, bullet list, or Scenario | Reference table → 🟡 Minor. Verify content is file-linked, not inline → 🔴 Major.
10. Cross-reference capabilities against linked examples; no-example → 🔴 Major; subset-only → 🟡 Minor. Load **reference/example-coverage-criteria.md**.
11. Review each linked example file (load **reference/example-quality-criteria.md**):
    a. Scenario heading names the trigger and the capability; missing or vague → 🟡 Minor.
    b. Output structure matches the capability's steps; drift → 🔴 Major.
    c. Scenario realistic and non-trivial; toy input for a complex capability → 🟡 Minor.
    d. No contradiction with a rule or knowledge entry; contradiction → 🔴 Major.
    e. Current capability name referenced; stale name → 🟢 Nit.
    f. Apply the example budget and line guard; overrun → 🟡 Minor, remediate per **reference/size-remediation.md**.
    g. Load **reference/artifact-consistency.md**; when the skill ships artifact templates, run
       `scripts/check_artifacts.py` with its field/zone lists and report each hit.
    h. Verify template fidelity: same headings, field labels, field order, statuses; abridged output labelled.
    i. Verify set-level continuity: shared identifiers, counts, statuses, and doctrine order across examples.
12. Surface inconsistencies — mixed styles, differing procedural detail, or artifact schemas that disagree
    across examples or skills. Present both variants and ask which is canonical; never pick silently.
13. Include **Positive Highlights** naming at least one well-structured aspect.
14. Include **Risks & Assumptions** stating format assumptions (e.g., four-section semantics) and that no runtime evaluation ran.
15. Format findings with severity per **reference/severity-levels.md**; load **examples/skill-file-review.md** for output structure.
16. **Check integration** — when the skill references another skill or dispatches/loads sub-agents, load
    **reference/pipeline-integration.md** and verify the applicable axes from its own declarations, including
    callee-side caller-agnosticism; skip if neither applies.
    When it links another skill, run `python3 scripts/check_skill_links.py <skill-dir>` and report its findings per
    Axis 1 point 6; `--duplicates` lists same-name copies across skills.
17. **Check tooling** — when the skill ships `scripts/` or invokes a CLI, load **reference/script-and-cli-policy.md**:
    a. Each script passes the four justification tests; re-implementing a standard CLI → 🟡 Minor.
    b. Python 3 stdlib only or a stated exception; dependency, network call, or prompt → 🔴 Major.
    c. Contract met: path and name, shebang, usage docstring, exit codes, stable field-named output; gaps per its anti-pattern table.
    d. Each script named by a capability step and declared in the layout; orphan → 🔴 Major.
    e. CLI steps detect availability, state a fallback, and check the exit code.
18. Verify completeness: every finding carries a severity, **Positive Highlights** and **Risks & Assumptions** exist, and every recommendation is actionable.
</review-skill-file>

</capabilities>

<rules>
<rule>When reviewing a skill file, review only the user-provided file per **same-name-live-copy-ban** — never a same-named live copy in claude/opencode/copilot dirs.</rule>
<rule>When the user submits a SKILL.md file for review or asks to diagnose what to fix in it, use **review-skill-file** — review and suggest only, never edit the file.</rule>
<rule>When the user wants an existing skill file edited or improved (not just diagnosed), do not apply edits here — route to `create-skill`'s **edit-skill**.</rule>
<rule>When the user asks whether a skill will trigger or activate correctly, or whether its description matches its scenarios, use **review-skill-file** and focus on step 2.</rule>
</rules>
