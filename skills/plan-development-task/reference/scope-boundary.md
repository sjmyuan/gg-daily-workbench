# Scope Boundary

Used by **define-scope-boundary**, **plan-file-format**, and **plan-rubric**.

## Purpose
The boundary gates on **behavior**, not on file paths. A diff that touches an unlisted file but changes no behavior is not a breach.
An opt-in **Must match** zone adds reference equality for paths that must be restored or ported verbatim.

## Zones

| Zone | Holds | Executor action |
|---|---|---|
| **Behavior gate** | **May change** / **Must not change** behaviors, contracts, and ADR decisions | Change outside **May change** → stop and ask |
| **Must match** (opt-in) | Paths that must equal a pinned ref — `Must match: <path> @ <ref>` | Diff against the ref non-empty → stop and ask |
| **Protected zones** | Schema and migrations, infrastructure, secrets and credentials, public API, other ADRs | Any touch → stop and ask; material unless **May change** names it |
| **Expected files** | Files likely to change — advisory only | Unlisted file that changes no behavior → proceed and log |

Default protected zones apply to every plan unless **May change** names them; list additions only.
**Must match** is the only zone that permits byte-equality validation; omit it unless the request is a revert, restore, or port.
Zone order in a plan: **May change** · **Must match** · **Expected files** · **Must not change** · **Protected zones**.

## Materiality test
Stop and ask only when a change answers **yes** to any question:

1. Alters observable behavior outside **May change**?
2. Touches a protected zone?
3. Leaves a **Must match** path unequal to its ref?
4. Leaves the step's objective unverified after two attempts?
5. Requires an irreversible or destructive action?
6. Changes *what* is built rather than *how*?

All **no** → proceed; add a one-line note when the change was unplanned.

## Incidental changes — proceed, no ask
Formatting, whitespace, indentation, import order, line endings, lockfiles, generated output, comments and docs, this plan's own tests.

Never incidental: a behavior change, a protected-zone edit, a deleted test, a dependency swap with runtime effect.

## Defensive changes
A guard, validation, retry, timeout, or fallback is a behavior change: it makes something fail, block, or retry that previously did not. It sits under **May change** like any other change.

- **Baseline = the surrounding code's rigor.** Raise it only when the request names the case.
- **Name the trigger.** Each new branch names the production input or event that reaches it. No reachable trigger → no branch, no test.
- **Inherited gaps stay open.** A case the current code never handled and the request does not name is one line under `## Risk` as an accepted gap — never a step.

## Writing the block

```markdown
## Scope Boundary
**May change**: <behaviors and contracts the plan may alter>
**Must match**: <path> @ <ref> (optional; omit unless restoring or porting)
**Expected files**: <likely files> (advisory)
**Must not change**: <behaviors and contracts that must be preserved>
**Protected zones**: <additions to the default set, if any>
```

Rules:
- One behavior per line; name the observable effect, not just the path.
- **Expected files** never gates; it sets reviewer expectations.
- Rework files inherit the original zones and tighten them to the governing ADR.

## Validation criteria
Every step validates behavior: tests pass, output matches, latency within budget.
Byte equality applies only where **Must match** names a path and ref.
Never assert an unstated diff, a commit hash, or an unstated byte-identical file — hashes and messages are illustrative.

## Rationalizations to reject

| Excuse | Reality |
|---|---|
| "The file is out of scope, so stop" | Scope is behavior; check whether behavior changed |
| "Whitespace differs, so the step failed" | Cosmetic; normalize the diff and proceed |
| "The commit message differs from the plan" | Messages are illustrative; follow repo convention |
| "Ask just in case" | Ask only on material changes; log the rest |
| "It is only a small behavior change" | Behavior changes are material at any size |
| "The code could crash on a null or empty input" | Only if a caller, the request, or an existing test can supply it |
| "The refactor is equivalent, so it matches" | Only a `Must match` path is checked for equality; equivalence is `behavior-equal` |
