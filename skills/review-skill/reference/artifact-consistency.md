# Artifact Consistency

Used by **review-skill-file** (step 11) and `create-skill`'s **example-standards**.
Applies when a skill ships artifact templates (plan, ADR, index, context, findings, report, schema)
and examples that instantiate them — in one skill or across a pipeline.

## Rule 1 — One canonical template

- A schema lives in exactly one reference file as a **literal fenced skeleton** with fixed field order.
- Examples instantiate that skeleton; they never restate a variant.
- When two skills disagree, the **consumer's** schema wins (see **pipeline-integration**), and the
  producer's examples must reproduce it.
- Never add a second template file to avoid editing the owner; extend the owner.

## Rule 2 — Example shape fidelity

- Same headings, field labels, field order, and status vocabulary as the template.
- **Abridged** output is allowed only when labelled: `(abridged)`, `(excerpt)`, or
  `excerpt — full schema in <file>`.
- No invented sections: a section absent from the template (`Key Characteristics`, `Root Cause`,
  `Notes` outside the schema) is structural drift, not enrichment.

## Rule 3 — Set-level continuity

- Examples that share one scenario reuse the same identifiers: epic, area slugs, feature IDs,
  folder names, ADR/findings filenames, branch names.
- Counts agree: N problems → N ADRs; N features → N feature rows and cells; N waves → wave table.
- Status terms agree with the status model and with the example's own headings.
- Test/implementation order agrees with the skill's doctrine (e.g., RED before the fix).

## Rule 4 — One home per fact

- Schema facts (branch/base, POC metadata, owner, status, path) have one canonical home; other
  documents link to it.
- A fact repeated in `plan.md`, `context.md`, and `index.md` with different values is a finding,
  not redundancy.

## Rule 5 — Cross-skill examples

- An example declared as shared by two skills must satisfy both schemas; update both in one change.
- A consumer example shows the producer's current template or is labelled as a summary.
- A renamed epic, area, feature, or ADR must not silently break the other skill's continuity.

## Severity

| Finding | Severity |
|---|---|
| Template missing, prose-only, or duplicated in two files | 🔴 Major |
| Example heading/field/order drift from the template | 🔴 Major |
| Abridged artifact without a label | 🟡 Minor |
| Identifier or count mismatch across examples | 🟡 Minor (🔴 when it invalidates the artifact) |
| Duplicate fact home with conflicting values | ⚠️ Inconsistency |
| Broken relative link or unbalanced fence | 🟡 Minor |
| Shared example updated in one skill only | 🔴 Major |

## Machine checks

Run `scripts/check_artifacts.py` (links, fences, step-block fields, Scope Boundary zones,
duplicate step numbers). Then apply Rules 1–5 manually — shape fidelity and set-level continuity
are not fully mechanizable.

```bash
python3 scripts/check_artifacts.py <skill-dir> \
  --step-fields Objective,Files,Source,Implementation,Validation,Status \
  --zones "May change,Must match,Expected files,Must not change,Protected zones"
```

Exit `0` clean, `1` findings, `2` usage error; output is stable and sorted.
