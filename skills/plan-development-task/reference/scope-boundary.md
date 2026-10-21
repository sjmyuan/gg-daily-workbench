# Scope Boundary

Used by **define-scope-boundary**, **plan-file-format**, and **plan-quality-checklist**.

## Purpose
The boundary gates on **behavior**, not on file paths. A diff that touches an unlisted file but changes no behavior is not a breach.

## Three zones

| Zone | Holds | Executor action |
|---|---|---|
| **Behavior gate** | **May change** / **Must not change** behaviors, contracts, and ADR decisions | Change outside **May change** → stop and ask |
| **Protected zones** | Schema and migrations, infrastructure, secrets and credentials, public API, other ADRs | Any touch → stop and ask; material unless **May change** names it |
| **Expected files** | Files likely to change — advisory only | Unlisted file that changes no behavior → proceed and log |

Default protected zones apply to every plan unless **May change** names them; list additions only.

## Materiality test
Stop and ask only when a change answers **yes** to any question:

1. Alters observable behavior outside **May change**?
2. Touches a protected zone?
3. Leaves the step's objective unverified after two attempts?
4. Requires an irreversible or destructive action?
5. Changes *what* is built rather than *how*?

All **no** → proceed; add a one-line note when the change was unplanned.

## Incidental changes — proceed, no ask
Formatting, whitespace, indentation, import order, line endings, lockfiles, generated output, comments and docs, this plan's own tests.

Never incidental: a behavior change, a protected-zone edit, a deleted test, a dependency swap with runtime effect.

## Writing the block

```markdown
## Scope Boundary
**May change**: <behaviors and contracts the plan may alter>
**Expected files**: <likely files> (advisory)
**Must not change**: <behaviors and contracts that must be preserved>
**Protected zones**: <additions to the default set, if any>
```

Rules:
- One behavior per line; name the observable effect, not just the path.
- **Expected files** never gates; it sets reviewer expectations.
- Rework files inherit the original three zones and tighten them to the governing ADR.

## Validation criteria
Every step validates behavior: tests pass, output matches, latency within budget.
Never "diff matches the plan", "same commit", or byte-identical files — hashes and messages are illustrative.

## Rationalizations to reject

| Excuse | Reality |
|---|---|
| "The file is out of scope, so stop" | Scope is behavior; check whether behavior changed |
| "Whitespace differs, so the step failed" | Cosmetic; normalize the diff and proceed |
| "The commit message differs from the plan" | Messages are illustrative; follow repo convention |
| "Ask just in case" | Ask only on material changes; log the rest |
| "It is only a small behavior change" | Behavior changes are material at any size |
