---
name: review-skill
description: Review SKILL.md files for content classification, structure, naming, duplication, script/CLI usage, and whether to refactor or add content. Use when reviewing, diagnosing, or checking a skill's content, structure, triggers, naming, tooling, or whether it needs refactoring or new content.
---

<when-to-use-this-skill>
- User asks to review a skill file (SKILL.md)
- User asks to diagnose or get feedback on a skill file before improving it (review-only — edits are applied via `create-skill`)
- User asks for feedback on content classification, section placement, or duplication in a skill file
- User asks whether a SKILL.md is correctly structured
- User asks whether a skill will trigger or activate correctly
- User asks whether an existing skill needs refactoring or new content
- User asks whether a skill's name or capability names follow naming conventions
- User asks whether a skill's scripts or CLI invocations are justified and safe
</when-to-use-this-skill>

<knowledge>

<named-standards>
Steps cite these standards by name; load the Details file when one is listed.

| Standard | Rule | Details |
|---|---|---|
| **content-model** | Fact → knowledge, procedure → capability, routing+guard → rule; decision order, adequacy severities, repair order. | [reference/content-model.md](reference/content-model.md) |
| **section-semantics** | Section order, directory layout, and common structural violations. | [reference/section-semantics.md](reference/section-semantics.md) |
| **trigger-correctness** | Description trigger clarity and when-to-use consistency. | [reference/trigger-correctness.md](reference/trigger-correctness.md) |
| **severity-levels** | Severity definitions and Blocker-vs-Major guidance. | [reference/severity-levels.md](reference/severity-levels.md) |
| **size-limits** | Char/line budgets per file type, line-length guard, gaming detection, measurement script. | [reference/size-limits.md](reference/size-limits.md) |
| **size-remediation** | Ordered remediation plus the structural-integrity gate (chars are the only gate; line/step-merging is 🔴). | [reference/size-remediation.md](reference/size-remediation.md) |
| **evaluation-process** | Output-evaluation patterns and severity when absent. | [reference/evaluation-process.md](reference/evaluation-process.md) |
| **naming-conventions** | Naming rules for the skill name, capability names, and knowledge names. | [reference/naming-conventions.md](reference/naming-conventions.md) |
| **conciseness-check** | Criteria for unnecessary content across SKILL.md, references, and examples. | [reference/conciseness-check.md](reference/conciseness-check.md) |
| **refactor-first** | Reshape before appending: reclassify, merge, split, rename, redistribute, or rewrite an existing element; add only when none can. | [reference/conciseness-check.md](reference/conciseness-check.md) |
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
| Before writing output — load first, every review | Canonical output format | [examples/skill-file-review.md](examples/skill-file-review.md) |
| The skill ships artifact templates, or 2+ examples emit one artifact | Template fidelity, identifier continuity, machine checker | [reference/artifact-consistency.md](reference/artifact-consistency.md) |
| The skill references another skill, or dispatches / is loaded by sub-agents | Integration checklist (skill-skill + skill-agent) | [reference/pipeline-integration.md](reference/pipeline-integration.md) |
| Capability tags are nouns, or examples sit inline in SKILL.md | Naming/inline model | [examples/noun-capabilities-and-inline-examples.md](examples/noun-capabilities-and-inline-examples.md) |
| The skill is near the char budget, or lines look dense | Size/gaming model | [examples/size-and-line-stuffing-review.md](examples/size-and-line-stuffing-review.md) |
| Prose is passive, verbose, or narrating | Style model | [examples/writing-style-review.md](examples/writing-style-review.md) |
| The description lacks a "Use when" clause, or contradicts a when-to-use bullet | Trigger-failure model | [examples/trigger-correctness-violation.md](examples/trigger-correctness-violation.md) |
| Step 7 runs, or the user asks whether the examples agree | Example-drift findings model | [examples/artifact-consistency-review.md](examples/artifact-consistency-review.md) |
| After the first pass — findings are only 🟡/🟢 or the request is a reshape | Near-passing / refactor model | [examples/clean-skill-review.md](examples/clean-skill-review.md) |
| After the first pass — the sub-agent axis produced findings | Agent-integration model | [examples/agent-integration-review.md](examples/agent-integration-review.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<review-skill-file>
**Objective**: Decide what each element *is* and whether it earns its place before judging how it is written; form is one mechanical pass.

**Note**: Do not modify the skill file during review; suggest changes as descriptions or patch snippets.

**Steps**:
1. **Check content classification** — apply **same-name-live-copy-ban**, read the full skill, load **reference/content-model.md**.
   a. Classify every element: a fact posing as a procedure, a procedure written as knowledge or inside a rule, a guard describing work.
   b. Report each duplicate owner — a fact held in two places, a template restated instead of extended.
   c. A claim fitting two classes → ⚠️ naming both candidate owners; never pick silently.
2. **Check content adequacy and justification** — the same standard, second pass.
   a. Adequacy: an unstated inferable fact, an objective no step produces, an undecidable step, a missing guard.
   b. Justification: an element whose removal breaks no step, objective, or trigger; a guard with no nameable failure; an unjustified example, reference, or script.
   c. Content outranks form — a content defect that makes the agent act wrongly is 🔴; a form defect is 🟡 or 🟢 unless it breaks loading.
   d. A capability that cannot be checked is inadequate: each ends with a validation step per **reference/evaluation-process.md**; absent → 🟡, absent with no validation example → 🔴.
3. **Check description and triggers** — load **reference/trigger-correctness.md**:
   a. Verify the two-part template via **reference/description-template.md**; missing trigger phrase → 🔴 Major.
   b. Score the five dimensions via **reference/description-scoring.md**; report x/10; ≤5 → 🔴 Major, 6–8 → 🟡 Minor.
   c. Verify trigger verbs and scenarios match the when-to-use bullets both ways; gap → 🟡 Minor.
   d. Missing when-to-use → 🔴 Major.
   e. Scope contradiction between `description` and when-to-use → 🔴 Major.
4. **Run the structural checklist** — one mechanical pass, every item delegating to its reference:
   a. Sections present and in order per **reference/section-semantics.md**; missing → 🔴, out of order → 🟡.
   b. Size per **reference/size-limits.md**, remedies per **reference/size-remediation.md**; line or step merging → 🔴 Blocker.
   c. `<rules>` present, rubrics extracted, on-demand context condition-first and file-linked — per **reference/section-semantics.md**.
   d. Skill and capability names take verbs, knowledge names take noun phrases — **reference/naming-conventions.md**.
   e. Measure with `python3 scripts/measure_sizes.py <skill-dir>` before judging size; `--diff` before and after a reduction.
5. **Check conciseness, style, and growth** — apply **reference/conciseness-check.md** and **reference/size-limits.md** to every file:
   a. Writing style — load **reference/writing-style.md**; flag per its severity table.
   b. Platform-agnostic writing — load **reference/platform-agnostic-writing.md**; tool names or context paths → 🟡, several across files → 🔴.
   c. Growth audit per **refactor-first** — count elements; report reshape candidates, superseded elements, and orphans; propose the reshape before adding.
6. Cross-reference each capability against its linked examples per **reference/example-coverage-criteria.md**.
7. **Review the example set** — load **reference/example-quality-criteria.md** and apply every criterion.
   a. Template fidelity and set-level continuity per **reference/artifact-consistency.md**; run `scripts/check_artifacts.py` when templates ship.
8. Surface inconsistencies — mixed styles or disagreeing artifact schemas. Present both variants, ask which is canonical, never pick silently.
9. Write the report from **examples/skill-file-review.md**, opening Overall Assessment with the verdict: "No change needed", "Refactor recommended", or "Changes recommended".
10. Format each finding with a severity per **reference/severity-levels.md**, a file anchor, and an actionable fix.
11. **Check integration** — when the skill references another skill or dispatches/loads sub-agents, load
    **reference/pipeline-integration.md** and verify the applicable axes from its own declarations, including
    callee-side caller-agnosticism; skip if neither applies.
    When it links another skill, run `python3 scripts/check_skill_links.py <skill-dir>` and report its findings per
    Axis 1 point 6; `--duplicates` lists same-name copies across skills.
12. **Check tooling** — when the skill ships `scripts/` or invokes a CLI, load **reference/script-and-cli-policy.md**:
    a. Each script passes the four justification tests; re-implementing a standard CLI → 🟡 Minor.
    b. Python 3 stdlib only or a stated exception; dependency, network call, or prompt → 🔴 Major.
    c. Contract met: path and name, shebang, usage docstring, exit codes, stable field-named output; gaps per its anti-pattern table.
    d. Each script named by a capability step and declared in the layout; orphan → 🔴 Major.
    e. CLI steps detect availability, state a fallback, and check the exit code.
13. Verify completeness: every finding carries a severity, and both **Positive Highlights** and **Risks & Assumptions** are present and specific.
</review-skill-file>

</capabilities>

<rules>
<rule>When reviewing a skill file, review only the user-provided file per **same-name-live-copy-ban** — never a same-named live copy in an installed skills folder.</rule>
<rule>When the user submits a SKILL.md file for review or asks to diagnose what to fix in it, use **review-skill-file** — suggest only, never edit.</rule>
<rule>When a request can be met by reshaping an element, recommend the refactor; add only when no reshape works.</rule>
<rule>When the user wants an existing skill file edited or improved (not just diagnosed), do not apply edits here — route to `create-skill`'s **edit-skill**.</rule>
<rule>When the user asks whether a skill will trigger or activate correctly, or whether its description matches its scenarios, use **review-skill-file** and focus on step 3.</rule>
</rules>
