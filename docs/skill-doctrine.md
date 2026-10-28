# Skill Doctrine Registry

Each skill is self-contained: every reference path resolves inside its own folder, and
another skill is named, never deep-linked. Doctrine that several skills need is
**duplicated as a scoped slice**, not shared by path — a skill may be installed alone.

This file is the drift map. It lives outside `skills/` so the skills stay clean.

## Rule

- Change a doctrine → update the owning copy **and** every mirror in the table below.
- Need a doctrine in a new skill → write a local slice with a `Scope:` header; never a `../` link.
- A slice may be narrower than its owner; it may never contradict it.

## Doctrines and their slices

| Doctrine | Owning copy | Mirrors (scoped slices) |
|---|---|---|
| Two-plane artifact map | `conduct-spike/reference/artifact-map.md` | `orchestrate-feature-delivery/reference/artifact-map.md` (delivery side only) |
| Document budgets | `plan-development-task/reference/doc-budgets.md` | `orchestrate-feature-delivery/reference/delivery-index-format.md` (index caps) · `execute-plan/reference/feature-folder-structure.md` (charter caps) |
| Change provenance | `plan-development-task/reference/provenance-first.md` | `orchestrate-feature-delivery/reference/mechanical-restore.md` (routing) · `execute-plan/reference/provenance-proof.md` (proof commands) |
| Sub-agent verification | `question-everything/reference/verification-protocol.md` | `conduct-spike/reference/multi-agent-orchestration.md` (spike verification) |
| Request intake gate | `grill-user/reference/user-challenge-protocol.md` | inline `request-intake` knowledge in `conduct-spike`, `orchestrate-feature-delivery`, `plan-development-task`, `execute-plan`, `investigate-code` |
| Concise writing style | `plan-development-task/reference/writing-style.md` | `orchestrate-feature-delivery`, `execute-plan`, `draft-adr` `reference/writing-style.md` |
| Review/authoring standards (severity, conciseness, evaluation, size, scripts, style) | `review-skill/reference/*` | `create-skill/reference/*` — same seven names, authoring-scoped |
| Write boundary | `conduct-spike/reference/write-boundary-guide.md` | `orchestrate-feature-delivery/reference/write-boundary-guide.md` |
| Rework file shape | `plan-development-task/reference/plan-file-format.md` | `orchestrate-feature-delivery/examples/post-implementation-rework.md` |
| POC round | `orchestrate-feature-delivery/examples/adr-option-poc.md` | `plan-development-task/examples/plan-adr-option-poc.md` |

## Check

```sh
# no link may leave its skill folder
python3 skills/review-skill/scripts/check_skill_links.py skills

# same basename in several skills — review each `differ` row against this table
python3 skills/review-skill/scripts/check_skill_links.py --duplicates skills
```

A new `differ` row is either a missing entry in this table or accidental drift.
Run the first check before shipping a skill change; the reviewer runs both when it
reviews a skill.
