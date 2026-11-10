---
name: create-skill
description: Author, edit, and validate skill files (SKILL.md), plus the examples, references, and scripts they ship. Use when creating, authoring, generating, building, extracting, editing, improving, revising, or validating a skill.
---

<when-to-use-this-skill>
- User asks to create, author, or build a new skill (SKILL.md) from scratch
- User asks to generate examples or references for a skill
- User provides existing materials (agent prompts, docs, code) to extract into a skill
- User asks to edit, improve, or revise an existing skill
- User asks to validate a created or edited skill before delivery (read-only diagnosis → `review-skill`)
</when-to-use-this-skill>

<knowledge>
<named-standards>
Steps cite these standards by name; load the Details file.

| Standard | Rule | Details |
|---|---|---|
| **content-model** | Fact → knowledge, procedure → capability, routing+guard → rule; decision order, adequacy and justification gates. | **reference/content-model.md** |
| **section-semantics** | Sections in order: frontmatter → when-to-use → knowledge → capabilities → rules; violations, layout in file. | **reference/section-semantics.md** |
| **naming-conventions** | Skill and capability names take imperative verbs; knowledge names take noun phrases. | **reference/naming-conventions.md** |
| **description-quality** | Domain summary + "Use when…" triggers, self-scored ≥9 on five dimensions. | **reference/description-quality.md** |
| **example-standards** | One linked example per capability: template fidelity, set continuity, no contradictions. | **reference/example-standards.md** |
| **platform-agnostic-writing** | No platform tool names or concrete context paths; abstract the context, detect don't assume. | **reference/platform-agnostic-writing.md** |
| **script-and-cli-policy** | CLI first, inline one-liner second, `scripts/` last after four tests; Python 3 stdlib; fixed output contract. | **reference/script-and-cli-policy.md** |
| **pipeline-integration** | 5 points: handoff, shared schema, one-way awareness (caller → callee), guard clauses, link self-containment. | **reference/pipeline-integration.md** |
| **writing-style** | Directive voice, BLUF, hard caps, atomic bullets, tables over prose, no banned phrases, no narration. | **reference/writing-style.md** |
| **size-limits** | SKILL.md and `reference/` ≤12,000 chars / 150 lines; `examples/` ≤9,000; >120-char lines flagged. | **reference/size-limits.md** |
| **size-remediation** | Re-encode → reuse → cut weight → redistribute → reduce → escalate; chars are the only gate, never merge steps or lines. | **reference/size-remediation.md** |
| **conciseness-check** | Every element justifies its existence; one line = one idea. | **reference/conciseness-check.md** |
| **evaluation-process** | Every capability ends with a validation or checklist step; absence severity in file. | **reference/evaluation-process.md** |
| **severity-levels** | Blocker 🚫 / Major 🔴 / Minor 🟡 / Nit 🟢 / Inconsistency ⚠️. | **reference/severity-levels.md** |
| **edit-existing-skill** | Existing-file mode: absorption test, merge/demote/replace, funding rule, element delta, re-validate. | **reference/edit-skill-procedure.md** |
| **same-name-live-copy-ban** | Never read, compare, or edit a live/loaded same-named skill; the user-provided files are the only subject. | — |
</named-standards>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Greenfield create flow | End-to-end walkthrough | [examples/create-skill-file.md](examples/create-skill-file.md) |
| Mixed facts, steps, and prohibitions | Classification walkthrough | [examples/classify-skill-content.md](examples/classify-skill-content.md) |
| Extracting an agent prompt or doc into a skill | Extraction walkthrough | [examples/extract-from-agent.md](examples/extract-from-agent.md) |
| Validating before delivery | Validation-report walkthrough | [examples/validate-new-skill.md](examples/validate-new-skill.md) |
| Editing an existing skill (merge, retire, rename) | Edit walkthrough | [examples/editing-existing-skill.md](examples/editing-existing-skill.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<collect-skill-requirements>
**Objective**: Gather what defines the new skill's purpose, scope, and capabilities.

1. Run `clarify-request`'s intake gate on the ask; its acceptance record replaces the question list.
2. Fill that record with **name** (action verb), **description**, **when-to-use**, **capabilities**, **knowledge**, **rules**, **examples**, **references** — from supplied materials first.
3. Set the gate state and one `Assumption (user-accepted, unverified)` per default; `BLOCKED` → write no SKILL.md.
4. Validate: every inference is a field or a labeled assumption; name, description, and triggers agree both ways.
</collect-skill-requirements>

<classify-skill-content>
**Objective**: Assign every requirement and claim exactly one content class before any section is written.

1. Harvest the claims as one statement per line, unclassified, in the source's own words.
2. Apply the **content-model** decision order to each claim; record its class.
3. Split any claim carrying two classes; apply the one-step versus many-step tie-breaks.
4. Route each claim to its section — knowledge, capability steps, or rules.
5. Run the **content-model** gates in order — adequacy adds, justification deletes what breaks nothing.
6. Validate: one owner per claim, no class in another class's section, one route and one guard per known misapplication.
</classify-skill-content>

<create-skill-file>
**Objective**: Generate a complete SKILL.md whose content is classified before it is shaped.

1. Create the target directory; add `examples/`, `reference/`, or `scripts/` only as content needs them.
2. Run **classify-skill-content** on the requirements record.
3. Write knowledge as facts under noun-phrase subsections per **section-semantics**.
4. Extract rubrics and lookup tables to `reference/` and route each from its step.
5. Write each capability as ordered steps under an action-verb name, facts and guards excluded, ending with a validation step.
6. Write `<rules>`: one routing rule per capability, one guard per known misapplication.
7. Re-run the **content-model** gates on the written sections; delete what breaks nothing.
8. Write the frontmatter: `name` per **naming-conventions**; `description` per **description-quality**.
9. Write `<when-to-use-this-skill>` per **description-quality**; every verb mirrors the trigger phrase.
10. Write all prose per **writing-style**.
11. Write all prose per **platform-agnostic-writing**.
12. Check the draft: **content-model** gates hold and every file is within **size-limits**; over → **size-remediation**.
13. In a multi-skill pipeline, verify the 5 integration points per **pipeline-integration**.
14. Write to the user-provided `<target>/SKILL.md` per **same-name-live-copy-ban**.
</create-skill-file>

<create-skill-examples>
**Objective**: Create or update example files demonstrating each capability.

1. Pick one realistic scenario per capability per **example-standards**; drop an example another teaches. Walkthrough: [create-examples-and-references.md](examples/create-examples-and-references.md).
2. Reproduce the artifact template's headings, field order, and statuses; label abridged output per **example-standards**.
3. Create one `.md` per scenario under `examples/`, reproducing the file skeleton in **example-standards**.
4. Validate the set per **example-standards**, then run `check_artifacts.py` from `review-skill` with the template's fields.
5. Measure per **size-limits**; if over, apply **size-remediation** (trim prose or low-value examples, never required fields).
</create-skill-examples>

<create-skill-references>
**Objective**: Create or update reference files for large rubrics and detailed criteria.

1. Identify knowledge too large for its step: rubrics, matrices, criteria, or artifact schemas that must load on demand.
2. If a schema already exists, extend its owner file; never add a parallel template.
3. Create one `.md` per topic with a title, the rubric, and a cross-reference to its capability.
4. Emit every template as a literal fenced skeleton with fixed field order and required labels.
5. Check each file: skeletons literal, within **size-limits**; over → **size-remediation** (split or condense).
6. Route each reference from its knowledge entry or a guide row; step-tied files also route inline.
</create-skill-references>

<create-skill-scripts>
**Objective**: Add the minimum automation a capability step needs — a CLI invocation, or a justified Python script.

1. Apply **script-and-cli-policy** — CLI, then one-liner, then `scripts/` after the four tests; walkthrough: [examples/create-skill-scripts.md](examples/create-skill-scripts.md).
2. Place an accepted script at `scripts/<verb>_<object>.py` and declare `scripts/` in the directory layout per **section-semantics**.
3. Write Python 3 stdlib only to the script contract: shebang, usage docstring, `main(argv) -> int`, exit 0/1/2, stable sorted output.
4. Name the script path and output fields in the step that runs it.
5. Validate with no arguments, then a passing and a failing sample; confirm exit codes and no dependency.
</create-skill-scripts>

<validate-created-skill>
**Objective**: Validate the created or edited skill files before delivery.

1. Run the checks in **reference/validate-skill-procedure.md** in order; content checks precede structural ones.
2. Report each finding with a severity label per **severity-levels** and an actionable fix; re-run step 1 after the fix.
3. Re-measure changed files and confirm the structural-integrity gate passed — line or step merging is a 🔴 Blocker.
</validate-created-skill>

<edit-skill>
**Objective**: Edit an existing skill's files by reusing the create-* capabilities in existing-file mode.

1. Inventory and count the skill: capabilities, steps, knowledge rows, rules, guide rows, examples, references, chars.
2. Triage intent per **reference/edit-skill-procedure.md**: "check" = review only; "ensure / fix / do it" = edit; open-ended "improve" runs `review-skill` first.
3. Categorize each change per the change-type, absorption, funding, and edit-discipline rules in **reference/edit-skill-procedure.md**.
4. Route each change to the mapped create-* capability in existing-file mode.
5. Run the ripple checklist after renames, removals, merges, or inlining.
6. Run **validate-created-skill** after each change; revert on a Blocker 🔴 and redo.
7. Re-measure per **size-limits**, report the element delta ledger, and report findings per **severity-levels**.
</edit-skill>

</capabilities>

<rules>
<rule>When the user requests a new skill, use **collect-skill-requirements** — it owns the intake gate and the requirements record.</rule>
<rule>When deciding what a skill must know, do, or forbid, use **classify-skill-content** — the class decides the section, never the reverse.</rule>
<rule>After requirements are confirmed, use **create-skill-file** to generate SKILL.md, and **create-skill-examples** plus **create-skill-references** in parallel as needed.</rule>
<rule>After creating or editing all files, use **validate-created-skill** before presenting the result.</rule>
<rule>When creating or validating a skill, operate only on the user-provided files per **same-name-live-copy-ban**.</rule>
<rule>When the user asks to edit, improve, or revise an existing skill, use **edit-skill**; run an open-ended "improve" through `review-skill` first per **reference/edit-skill-procedure.md**.</rule>
<rule>When the user asks for a read-only review of an existing skill file, delegate to the `review-skill` skill instead.</rule>
<rule>When a capability step needs automation, use **create-skill-scripts** — pick an installed CLI before a script, and Python 3 stdlib before any other language.</rule>
</rules>
