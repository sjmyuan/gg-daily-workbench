# Pipeline Integration

Backs the `<pipeline-integration>` knowledge entry. The findings doc sits upstream of ADRs and the solution doc, and is seeded by investigation.

## Position

`investigate-code` (evidence) → **findings doc** → `draft-adr` (decisions) → `write-solution-doc` (target state)

## Handoff

| Point | Rule |
|---|---|
| Upstream input | Verified investigation results for one area, with an evidence map (`file:line`, call chains, confidence). |
| Seed (spike) | `conduct-spike`'s `compile-findings-doc` seeds one doc per area; this skill owns the format and IDs. |
| Output path | `<spike-folder>/docs/findings-<area>.md` inside a spike; a user-provided path otherwise. |
| Downstream | `draft-adr` grounds options in the doc's evidence; `write-solution-doc` cites IDs for the current-state baseline. |

## Return contract

When seeded by an orchestrator, return:
- The saved `docs/findings-<area>.md` path.
- Evidence gaps (❓) and any ⚠️ inconsistencies found in the source results.
- Cross-area constraints that reference the other area's findings doc.

## Shared schema

Consumers rely on four stable elements:
- Fixed section order
- Scope-slug IDs
- `file:line` evidence
- 5-tag confidence model

## Guard

| Do not load for | Route to |
|---|---|
| Target-state architecture, solution docs, decision records | `write-solution-doc`, `draft-adr` |
| Unverified investigation output | `investigate-code` first |
