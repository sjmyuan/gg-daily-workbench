# Plan Prerequisites

Used by **plan-prerequisites**, **plan-feature-implementation**, **plan-bug-fix**,
**plan-refactor**, and **plan-poc**.

Every plan starts with a **Prepare Environment** step (Step 1) covering only the checks
execution needs.

| Check | Not ready → |
|---|---|
| Feature branch exists, based on the correct base, named per the **repo's branch convention** (detect from branches / git config / team docs, or ask — never assume a prefix) | Ask for the branch name and base; create the branch in Step 1 |
| No uncommitted changes overlapping the plan's work | Ask before proceeding; leave unrelated changes untouched |
| Dependencies and toolchain resolve for the plan's commands | Stop and raise: request install or confirmation |
| Gate commands identified from repo evidence (`build` / `test` / `lint-type`) | Ask; never invent or narrow a command |
| Those commands run on the base — `baseline: green`, or `red` with named failures | Stop: add a restore-baseline step or a ratified exclusion |

Unrelated dirt and unrelated failures are noted, not blocking; never stash, revert, or commit the
user's unrelated changes. An unnamed red baseline does not pass — it silently disables the gate
(see **exit-gate**).

The branch name, base, and gate commands live in the plan header so **export-plan** persists them
to `plan.md`; `index.md` mirrors the branch as cell state.
