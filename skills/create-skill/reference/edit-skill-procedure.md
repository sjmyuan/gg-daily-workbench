# Editing an Existing Skill (edit-skill procedure)

Used by **edit-skill** (steps 2–8).

## Existing-file mode
The create-* capabilities author greenfield skills. **edit-skill** reuses them for an existing skill by applying these deltas:

| Reused capability | Greenfield step | Existing-file delta |
|---|---|---|
| **create-skill-file** | Create directory + write new SKILL.md | Locate the existing SKILL.md; skip directory creation; edit sections in place; preserve untouched meaning and retire superseded elements |
| **create-skill-examples** | Create example files | Adding an example is identical; editing one updates that file in place |
| **create-skill-references** | Create reference files | Adding a reference is identical; editing one updates that file in place |
| **create-skill-scripts** | Create `scripts/` + first script | Locate the existing `scripts/`; edit the script in place; keep its output fields and exit codes stable |
| **validate-created-skill** | Validate new files | Run unchanged on the edited files (it already accepts user-provided files) |

## Intent triage

| User wording | Mode |
|---|---|
| "check", "review", "see if", "diagnose" | **review-skill** only — report findings, never edit |
| "ensure", "fix", "make consistent", "update", "do it" | **edit-skill** — apply changes |
| "check ... and fix/update" | Review first, then edit the accepted findings |
| Open-ended "improve" | Run `review-skill` first, confirm findings, then edit |

When the user accepts a recommended variant without naming one ("do it"), apply the recommended
canonical variant, state it in the result, and record it in the owner template/reference.

## Change-type routing
Merge, demote, replace, and inline are first-class moves — not fallbacks taken after "add" fails a budget.

| Change | Route | Existing-file delta | Verify |
|---|---|---|---|
| Merge capabilities | **create-skill-file** | Fold the steps into the survivor; retire the losing tag, its rules, guide row, and example | every merged step lands; ripple |
| Demote | **create-skill-file** | Move capability → knowledge table → `reference/`; leave one route to it | **section-semantics** |
| Replace | **create-skill-file** | Write the new element and delete every element it supersedes, in the same edit | no duplicate claim |
| Inline | **create-skill-file** / references | Fold a single-use reference into its step; delete the file and its guide row | no dangling link |
| Retighten | **create-skill-file** | Rewrite the vague step that invited the addition; add nothing | step still unambiguous |
| Add capability or knowledge | **create-skill-file** | Pass the absorption test first; extend the owner before inserting a section; fund per the funding rule | example coverage + no dangling refs |
| Add example | **create-skill-examples** | Extend a scenario that shares the trigger; add a file only for a new trigger | **example-standards** |
| Add reference | **create-skill-references** | Only for a rubric no owner file can hold; self-link from knowledge | no orphaned ref |
| Add or change a script | **create-skill-scripts** | Re-run the justification tests before adding; keep exit codes and field names stable | **script-and-cli-policy** contract |
| Remove capability | **create-skill-file** | Delete the capability plus its rules, guide rows, examples | no dangling refs |
| Rename capability | **create-skill-file** | Rename the tag plus every mention in the skill | ripple propagation |
| Restructure | **create-skill-file** | Move content between knowledge, reference, and capabilities | **section-semantics** |
| Apply review findings | `review-skill` (diagnose), then **create-skill-file** / examples / references | Fix each accepted finding by its cheapest move — retighten, merge, or inline before adding; record the canonical variant in the owner template | re-validate |
| Make examples consistent | **create-skill-examples** / references | Reproduce the canonical template; fix identifiers/counts; update shared cross-skill examples | **example-standards** + checker |
| Size-reduce | **create-skill-file** / examples / references | Apply **size-remediation** lever order, then the funding rule | re-measure |

## Absorption test
Run before any addition, in order. Stop at the first yes.

1. Does an existing step already say this? → tighten that step; add nothing.
2. Does an existing capability cover most of it? → extend that capability; add no tag.
3. Is it a row in a table that already exists? → extend the table; add no section.
4. Is it a variant of an existing example scenario? → extend the example; add no file.
5. None apply, and it has its own trigger? → add exactly one element.

A vague step is the usual cause of an addition. Tighten the step instead of appending a rule that compensates for it.

## Funding rule
- Growth is paid in **elements**, not chars.
- Name the element a change supersedes, and retire it in the same edit.
- Trimming prose is not payment.
- Extracting into `reference/` is not payment — same content, one more file.
- An addition that retires nothing is valid only when it serves a trigger no existing element serves.
- State that new trigger in the result; otherwise the addition is unfunded and incomplete.
- Net element count per edit: flat or down, unless the user asked for new scope.

## Element delta ledger
Close every edit with the counts, taken at inventory and again after validation.

| Element | Before | After | Δ |
|---|---|---|---|
| capabilities | … | … | … |
| steps | … | … | … |
| chars | … | … | … |

One row per element type: capabilities, steps, knowledge rows, rules, guide rows, examples, references, chars.
Summarize in one line: `−1 capability, −1 rule, −2 examples, −840 chars`. Any positive Δ must be the funded one.

## Review-first composition
Open-ended "improve this skill" = diagnose then edit:
1. Run `review-skill`'s **review-skill-file** (read-only) on the existing files to get severity-labeled findings.
2. Confirm with the user which findings to apply — and which elements each fix will retire.
3. Fix each accepted finding by its cheapest move per the change-type table.
4. Re-run **validate-created-skill** to confirm resolution.
5. Report the element delta ledger; a fix that grows the skill without a funded element is incomplete.

## Ripple-propagation checklist
A rename or removal must update every mention in the edited skill and its declared links:
- capability tags in `<capabilities>` and any step that routes to them
- example `**Applies**` lines
- reference `Used by` headers and inline step routes
- `<context-loading-guide>` rows
- `<rules>` routing and `<knowledge>` self-links
- sibling files the skill itself declares (never fetch other skills)
- every skill or agent name in the edited skill — keep the ones it invokes, drop the ones that only load it
- shared examples another skill declares — update both sides in the same change
- the canonical artifact template when a field, zone, or status vocabulary changes

## Edit discipline
- Read and inventory the skill before editing — never edit blind.
- The inventory is the ledger's "before" column.
- Leave untouched text untouched — preserve its wording and meaning; rewrite only the sentences the change is about.
- Fund a budget overrun by deleting duplicated or superseded content, never by re-wording sentences the change does not touch.
- Retire every element the change supersedes.
- A superseded element left in place is a duplicate claim, not preserved content.
- Rewrite the smallest section that must change; never regenerate a passing file.
- Never add a second template to avoid editing the owner; extend the owner file.
- Separate introduced from pre-existing findings; report both, but do not let a pre-existing budget failure block a scoped consistency fix.
- Validate after each logical change; revert to the last valid state on a Blocker 🔴.
- Re-measure every changed file per **size-limits**; apply **size-remediation** (lever order + structural-integrity gate) when over budget.
- When size remediation is the goal, never let extraction raise the total element count.
