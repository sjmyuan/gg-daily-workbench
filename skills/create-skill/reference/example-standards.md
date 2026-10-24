# Example Coverage and Quality Standards

Used by **create-skill-examples** and **validate-created-skill** (checks 9, 15, 16).
Mirrors **../review-skill/reference/artifact-consistency.md** for cross-skill pipelines.

## Coverage requirements
- Every distinct capability must have at least one linked example
- Examples should cover key scenarios, not just happy-path inputs
- Example labels must reference current capability names (no stale/renamed references)

## Template fidelity
When the skill ships an artifact schema (plan, ADR, index, context, findings, report, config):
- The schema lives in **one** reference file as a literal fenced skeleton with fixed field order.
- Every example reproduces the skeleton's headings, field labels, field order, and status vocabulary.
- Never restate a variant; edit the owner template and let examples follow.
- An abbreviated artifact is allowed only with an explicit `(abridged)` / `(excerpt)` label naming
  the full schema.
- No invented sections: anything the template does not define is structural drift.

## Set-level continuity
Examples are validated as a set, not one by one:
- Examples sharing a scenario reuse the same epic, area, feature, folder, and file identifiers.
- Counts agree — N problems → N ADRs, N features → N rows/cells, N waves → wave table.
- Statuses agree with the status model and with each example's own headings.
- Test/implementation order follows the skill's doctrine (e.g., RED before the fix).
- One home per fact: branch, owner, POC metadata, and paths appear once; other docs point.
- An example declared as shared by another skill is updated in both in the same change.

## Quality requirements
Each example file must meet:
- **Clear scenario heading**: states the skill domain, the trigger condition, and what makes this case distinct
- **Realistic, non-trivial input**: representative of actual user requests — not a toy or hello-world scenario
- **Output matches capability steps**: structure and content follow the capability's steps
- **Traceable to a named capability**: a reader can identify which capability produced this output
- **No contradictions with the parent skill**: the output does not violate any rule or knowledge entry in the same skill

## Machine check
If the skill ships artifact templates, run
`../review-skill/scripts/check_artifacts.py` with the template's field and zone lists.
It covers links, fences, step fields, zone order, and duplicate step numbers; template fidelity
and set-level continuity remain manual.
