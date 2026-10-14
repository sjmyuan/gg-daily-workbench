# Pipeline Integration

The findings doc pair sits upstream of ADRs and the solution doc, and is seeded by investigation.

## Position

`investigate-code` (evidence) → **findings doc pair** → `draft-adr` (decisions) → `write-solution-doc` (target state)

## Handoff

| Point | Rule |
|---|---|
| Upstream input | Verified investigation results for one area, with an evidence map (`file:line`, call chains, confidence). |
| Embedding agent | `findings-doc-writer` loads this skill to author a per-area pair. |
| Seed (spike) | `conduct-spike`'s `compile-findings-doc` seeds one pair per area; this skill owns the format and IDs. |
| Output path | `<spike-folder>/docs/findings-<area>.md` plus `<spike-folder>/docs/evidence-<area>.md` inside a spike; a user-provided path otherwise. |
| Downstream | `draft-adr` grounds options in the evidence doc; `write-solution-doc` cites IDs for the current-state baseline. |

## Return contract

When seeded by an orchestrator, return:
- The saved paths `docs/findings-<area>.md` and `docs/evidence-<area>.md`.
- Evidence gaps (❓) and any ⚠️ inconsistencies found in the source results.
- Cross-area constraints that reference the other area's pair.

## Shared schema

Consumers rely on five stable elements:
- Fixed human-doc section order
- Evidence-doc section order
- Scope-slug IDs
- `file:line` evidence
- 5-tag confidence model

## Publishing

The human doc is self-contained — no claim IDs, confidence tags, ledger, or evidence-doc link — so it publishes to any external system unchanged. The evidence doc stays repo-only.

## Guard

| Do not load for | Route to |
|---|---|
| Target-state architecture, solution docs, decision records | `write-solution-doc`, `draft-adr` |
| Unverified investigation output | `investigate-code` first |
