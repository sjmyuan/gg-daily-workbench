---
name: create-skill
description: Author, edit, and validate skill files (SKILL.md), plus the examples, references, and scripts they ship. Use when creating, authoring, generating, building, extracting, editing, improving, revising, or validating a skill.
---

<when-to-use-this-skill>
- User asks to create or author a new skill (SKILL.md) from scratch
- User asks to generate examples or references for a skill
- User asks to build a complete skill with capabilities, knowledge, and rules
- User provides existing materials (agent prompts, docs, code) to extract into a skill
- User asks to edit, improve, or revise an existing skill
- User asks to validate a newly created or edited skill before delivery
- Do NOT load for a read-only review — use `review-skill` (its findings feed **edit-skill**)
</when-to-use-this-skill>

<knowledge>
<named-standards>
Capability steps cite these standards by name; load the Details file.

| Standard | Rule | Details |
|---|---|---|
| **section-semantics** | Distinct, non-overlapping sections in order: frontmatter → when-to-use → knowledge → capabilities → rules; violations and directory layout in file. | **reference/section-semantics.md** |
| **naming-conventions** | Skill and capability names use imperative verbs; knowledge names use noun phrases. | **reference/naming-conventions.md** |
| **description-quality** | Domain summary + "Use when…" trigger verbs, self-scored ≥9 on five dimensions. | **reference/description-quality.md** |
| **example-standards** | One linked example per capability: template fidelity, set-level continuity, no contradictions. | **reference/example-standards.md** |
| **platform-agnostic-writing** | No platform tool names or concrete context paths; abstract context descriptions; detect, don't assume. | **reference/platform-agnostic-writing.md** |
| **script-and-cli-policy** | CLI first, inline one-liner second, `scripts/` script last after four tests; Python 3 stdlib only; fixed output contract. | **reference/script-and-cli-policy.md** |
| **pipeline-integration** | 5 points: handoff, shared schema, one-way awareness (caller → callee), guard clauses, link self-containment. | **reference/pipeline-integration.md** |
| **writing-style** | Directive voice, BLUF, hard caps, atomic bullets, tables over prose, no banned phrases, no narration. | **reference/writing-style.md** |
| **size-limits** | SKILL.md and `reference/` ≤12,000 chars / 150 lines; `examples/` ≤9,000; >120-char lines flagged; measure with the reviewer's `measure_sizes.py`. | **reference/size-limits.md** |
| **size-remediation** | Re-encode → reuse → cut weight → redistribute → reduce → escalate; chars are the only gate, never merge steps or lines (🔴). | **reference/size-remediation.md** |
| **conciseness-check** | Every element justifies its existence; one line = one idea. | **reference/conciseness-check.md** |
| **evaluation-process** | Every capability ends with a validation or checklist step; absence severity in file. | **reference/evaluation-process.md** |
| **severity-levels** | Blocker 🚫 / Major 🔴 / Minor 🟡 / Nit 🟢 / Inconsistency ⚠️. | **reference/severity-levels.md** |
| **edit-existing-skill** | Existing-file mode: absorption test, merge/demote/replace, funding rule, element delta, re-validate. | **reference/edit-skill-procedure.md** |
| **same-name-live-copy-ban** | Never read, compare, or edit a live/loaded same-named skill; the user-provided files are the only subject. | — |
</named-standards>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Walking through a greenfield create flow | End-to-end create-skill-file walkthrough | [examples/create-skill-file.md](examples/create-skill-file.md) |
| Extracting an existing agent prompt or doc into a skill | Extraction walkthrough | [examples/extract-from-agent.md](examples/extract-from-agent.md) |
| Adding examples and references to a drafted skill | Examples + references walkthrough | [examples/create-examples-and-references.md](examples/create-examples-and-references.md) |
| Validating a newly created skill before delivery | Validation-report walkthrough | [examples/validate-new-skill.md](examples/validate-new-skill.md) |
| Editing an existing skill (merge, retire, rename ripple) | Edit walkthrough | [examples/editing-existing-skill.md](examples/editing-existing-skill.md) |
| A capability step needs automation (CLI vs script) | Automation-decision walkthrough | [examples/create-skill-scripts.md](examples/create-skill-scripts.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<collect-skill-requirements>
**Objective**: Gather what defines the new skill's purpose, scope, and capabilities.

1. Ask for: **skill name** (action verb), **description** (domain + trigger), **when-to-use bullets** (3–7), **capabilities** (action verbs), **knowledge** (tables, constraints), **rules** (routing), **examples** (≥1 per capability), **references** (large rubrics).
2. Present a summary of the collected information for confirmation.
3. If the user provides source materials (agent prompts, code, docs), extract knowledge from them instead of asking; never fetch a same-named live skill (per **same-name-live-copy-ban**).
</collect-skill-requirements>

<create-skill-file>
**Objective**: Generate a complete SKILL.md that meets reviewer quality requirements.

1. Create the target directory with `examples/`, `reference/`, and — only when justified — `scripts/`.
2. Write the frontmatter: action-verb `name`; `description` per the two-part template, self-scored ≥ 9 per **description-quality**.
3. Write `<when-to-use-this-skill>` as 3–7 bullet scenarios whose intent verbs appear in the `description` trigger phrase; phrase each as an input condition, never as a caller name.
4. Budget each section to ≤ **size-limits**.
5. Write knowledge as tables/lists; extract large rubrics to `reference/` and route them inline from the using step.
6. Write each capability with a unique action-verb name and numbered steps; no embedded reference tables or constraint bullets.
7. Write `<rules>` for every skill — required: one routing rule per capability ("When X → use capability Y"), plus a guard rule for each known misapplication ("Never …"); never restate a capability step.
8. Write all prose per **writing-style**.
9. Write prose per **platform-agnostic-writing**.
10. Validate the draft against **section-semantics** (violations, section order, naming).
11. If the skill is part of a multi-skill pipeline, verify the 5 integration points per **pipeline-integration**, keeping every dependency caller → callee.
12. Measure per **size-limits**; if over, apply **size-remediation**.
13. Write to the user-provided `<target>/SKILL.md` (per **same-name-live-copy-ban**).
</create-skill-file>

<create-skill-examples>
**Objective**: Create or update example files demonstrating each capability.

1. Determine one realistic scenario per capability per **example-standards**.
2. If the capability emits an artifact, load its canonical template; reproduce headings, field order, and statuses; label abridged output.
3. Create one `.md` per scenario under `examples/` with scenario heading, setup, `Applies **[capability]**`, input, and expected output.
4. Validate the set per **example-standards** — identifier/count continuity, no contradictions — then run `check_artifacts.py` from `review-skill` with the template's fields.
5. Write example prose per **writing-style**.
6. Measure per **size-limits**; if over, apply **size-remediation** (trim prose or low-value examples, never required fields).
7. Write each example to its file.
</create-skill-examples>

<create-skill-references>
**Objective**: Create or update reference files for large rubrics and detailed criteria.

1. Identify knowledge entries that are large rubrics, scoring matrices, criteria, or artifact schemas.
2. If a schema already exists, extend its owner file; never add a parallel template.
3. Create one `.md` per topic with a title, content, and a cross-reference to its capability.
4. Emit every template as a literal fenced skeleton with fixed field order and required labels.
5. Write per **writing-style**: title + rubric, no narrative intro, no restatement of SKILL.md.
6. Measure per **size-limits**; if over, apply **size-remediation** (split or condense).
7. Route each reference from its knowledge entry or a guide row; step-tied files also route inline.
</create-skill-references>

<create-skill-scripts>
**Objective**: Add the minimum automation a capability step needs — a CLI invocation, or a justified Python script.

1. Apply the preferred means in **script-and-cli-policy**: CLI, then inline one-liner, then `scripts/` only after all four justification tests.
2. Place an accepted script at `scripts/<verb>_<object>.py` and declare `scripts/` in the directory layout per **section-semantics**.
3. Write Python 3 stdlib only to the script contract: shebang, usage docstring, `main(argv) -> int`, exit 0/1/2, stable sorted output.
4. Name the script path and output fields in the step that runs it.
5. Validate: run with no arguments, a passing sample, and a failing sample; confirm exit codes and no dependency, network, or prompt.
6. Create the example per **example-standards**, then measure the script and changed skill files per **size-limits**.
</create-skill-scripts>

<validate-created-skill>
**Objective**: Validate the created or edited skill files before delivery.

1. Run the 16 checks in **reference/validate-skill-procedure.md**, in order, on every created file.
2. Report each finding with a severity label per **severity-levels** and an actionable fix; return to the failing capability and re-run step 1.
3. Re-measure changed files and confirm the structural-integrity gate passed — line or step merging is a 🔴 Blocker.
</validate-created-skill>

<edit-skill>
**Objective**: Edit an existing skill's files by reusing the create-* capabilities in existing-file mode.

1. Apply **same-name-live-copy-ban** — target only the user-provided existing files.
2. Inventory and count the skill: capabilities, steps, knowledge rows, rules, guide rows, examples, references, chars.
3. Triage intent per **reference/edit-skill-procedure.md**: "check / see if" = review only; "ensure / fix / do it" = edit; open-ended "improve" runs `review-skill` first.
4. Classify each change per the change-type, absorption, and funding rules in **reference/edit-skill-procedure.md**.
5. Route each change to the mapped create-* capability in existing-file mode.
6. Run the ripple checklist after renames, removals, merges, or inlining.
7. Run **validate-created-skill** after each change; revert on a Blocker 🔴 and redo.
8. Re-measure per **size-limits**, report the element delta ledger, and report findings per **severity-levels**.
</edit-skill>

</capabilities>

<rules>
<rule>When the user requests to create a new skill, use **collect-skill-requirements** to gather name, description, scenarios, capabilities, knowledge, and example needs.</rule>
<rule>After requirements are confirmed, use **create-skill-file** to generate SKILL.md, and **create-skill-examples** plus **create-skill-references** in parallel as needed.</rule>
<rule>After creating or editing all files, use **validate-created-skill** before presenting the result.</rule>
<rule>When creating or validating a skill, operate only on the user-provided files per **same-name-live-copy-ban** — never read, compare, or edit a live/loaded skill with the same name.</rule>
<rule>When the user asks to edit, improve, or revise an existing skill, use **edit-skill**; run an open-ended "improve" through `review-skill` first per **reference/edit-skill-procedure.md**.</rule>
<rule>When the user asks for a read-only review of an existing skill file, delegate to the `review-skill` skill instead.</rule>
<rule>When a capability step needs automation, use **create-skill-scripts** — pick an installed CLI before a script, and Python 3 stdlib before any other language.</rule>
</rules>
