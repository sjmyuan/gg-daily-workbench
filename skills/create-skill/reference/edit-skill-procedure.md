# Editing an Existing Skill (edit-skill procedure)

Used by **edit-skill** (steps 3, 4, 5, 6).

## Existing-file mode
The create-* capabilities author greenfield skills. **edit-skill** reuses them for an existing skill by applying these deltas:

| Reused capability | Greenfield step | Existing-file delta |
|---|---|---|
| **create-skill-file** | Create directory + write new SKILL.md | Locate the existing SKILL.md; skip directory creation; edit sections in place; preserve unrelated content byte-for-byte |
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
| Change | Route | Existing-file delta | Verify |
|---|---|---|---|
| Add capability or knowledge | **create-skill-file** | Insert the new section; add rule, guide row, and example as needed | example coverage + no dangling refs |
| Add example | **create-skill-examples** | None — same as greenfield | **example-standards** |
| Add reference | **create-skill-references** | Self-link from knowledge; route inline or add a guide row | no orphaned ref |
| Add or change a script | **create-skill-scripts** | Re-run the justification tests before adding; keep exit codes and field names stable | **script-and-cli-policy** contract |
| Remove capability | **create-skill-file** | Delete the capability plus its rules, guide rows, examples | no dangling refs |
| Rename capability | **create-skill-file** | Rename the tag plus every mention in the skill | ripple propagation |
| Restructure | **create-skill-file** | Move content between knowledge, reference, and capabilities | **section-semantics** |
| Apply review findings | `review-skill` (diagnose), then **create-skill-file** / examples / references | Fix each accepted finding by severity; record the canonical variant in the owner template | re-validate |
| Make examples consistent | **create-skill-examples** / references | Reproduce the canonical template; fix identifiers/counts; update shared cross-skill examples | **example-standards** + checker |
| Size-reduce | **create-skill-file** / examples / references | Apply **size-remediation** lever order | re-measure |

## Review-first composition
Open-ended "improve this skill" = diagnose then edit:
1. Run `review-skill`'s **review-skill-file** (read-only) on the existing files to get severity-labeled findings.
2. Confirm with the user which findings to apply.
3. Fix each accepted finding by severity per the change-type table.
4. Re-run **validate-created-skill** to confirm resolution.

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
- Read the full skill and inventory it before editing — never edit blind.
- Make targeted edits; preserve unrelated sections byte-for-byte.
- Never wholesale-rewrite a passing file while improving it.
- Never add a second template to avoid editing the owner; extend the owner file.
- Separate introduced from pre-existing findings; report both, but do not let a pre-existing budget failure block a scoped consistency fix.
- Validate after each logical change; revert to the last valid state on a Blocker 🔴.
- Re-measure every changed file per **size-limits**; apply **size-remediation** (lever order + structural-integrity gate) when over budget.
