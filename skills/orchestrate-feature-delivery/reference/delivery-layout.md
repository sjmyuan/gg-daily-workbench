# Delivery Layout

Artifact layout, base root, and branch/push conventions for `orchestrate-feature-delivery`.

## Layout

All delivery artifacts for one epic live under one top-level folder — one folder per epic (no `docs/` prefix), named after the spiked epic:

```
deliveries/<epic-name>/               # one folder per epic (epic-name = spike name)
├── <repo-name>/<feature-name>/       # one folder per repo per feature
│   ├── context.md                    # cell charter + latest handoff + pointers
│   └── plan.md                       # TDD plan from plan-development-task
└── index.md                          # delivery index (single source of truth)
```

- **Base root**: `deliveries/` is a sibling of the spike's `spikes/` under the artifact base the spike recorded (`scope.md` `Artifact root:`). Inherited, never re-resolved; only a missing record triggers `resolve-artifact-location`. The epic folder always carries a `deliveries/` path segment, anchoring the write boundary.
- **Feature folders** are named by the feature's kebab-case name (e.g. `wallet-contracts`), never its ID (`F1`).
- **context.md** carries the cell charter (why, must-hold, unknowns, done, pointers), the `## Reworks` manifest, and the latest handoff — never a copy of spike content.
- **plan.md** is the original plan; each rework is a sibling `rework-<date>.md` (see **reference/rework-modes.md**), implemented steps never modified.
- **index.md** lives at the epic folder root (see **reference/delivery-index-format.md**).
- **Handoff**: the verification gate reuses these docs — `plan.md` step statuses and `context.md` `## Execution`; the code-reviewer fetches the diff from git, and findings go to the planner as a `rework-<date>.md`.
- **Spike boundary**: spike artifacts stay under `spikes/<spike-name>/` and are referenced by path; delivery never copies them. Map: **[artifact-map.md](../../conduct-spike/reference/artifact-map.md)**.

## Branch and push conventions

Execution agents commit locally and small-step; they push and open the PR only after user confirmation.

- One branch per repo per cell, named per the **repo's branch convention** (detect from existing branches / git config / team docs — or ask; never assume a prefix like `feat/`); created during the execution agent's **Prepare Environment** step.
- The executor opens the PR after push approval, following the target repo's convention; the index records the returned reference.
- Pushing and PR creation are separate approvals.
- The index records the branch up front, the PR reference (number/URL) and **head commit** from the executor handoff — pointers only; work history stays in `plan.md` / git.
- Commit after each ✅ step, with no AI-related wording (see **execute-plan** commit-conventions).
- A cell is **done** only after its PR merges with the recorded head commit included, or the user records a gate waiver; pushing alone is not done.
