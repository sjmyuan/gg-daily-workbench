# Scope Boundary Check

Used by **check-scope-boundary** and **verify-prerequisites**.

## Zones

| Zone | Holds | Action |
|---|---|---|
| **May change / Must not change** | Behaviors, contracts, ADR decisions | Outside **May change** → material |
| **Must match** (opt-in) | Paths declared equal to a pinned ref | Diff against the ref non-empty → material |
| **Protected zones** | Schema/migrations, infrastructure, secrets, public API, other ADRs | Material unless **May change** names them |
| **Expected files** | Likely files (advisory) | Unlisted and behavior-neutral → proceed |

## Classify a change

1. List the changed paths and the behavior each edit alters.
2. Normalize cosmetics: `git diff -w --ignore-blank-lines --stat <base>`. An empty normalized diff is cosmetic.
3. Compare commit content, not identity: `git diff <base>..HEAD -- <expected paths>`. Hashes, messages, and commit counts are not contractual.
4. Check every `Must match` path: `git diff --exit-code <ref> -- <path>` exits non-zero → residual hunks.
5. Apply the materiality test — behavior outside **May change**, protected-zone touch, `Must match` drift, objective still unverified after two attempts, irreversible action, or a change to *what* is built.
6. Any hit → hold and ask. No hit → proceed; add a one-line note when the change was unplanned.

## Closed stop list

Stop and ask only for:

- material behavior change outside **May change**
- protected-zone touch
- `Must match` drift on a declared path
- necessary environment blocker (branch, dependency, affected-area baseline)
- objective unverified after two attempts
- irreversible or destructive command
- ambiguity that changes *what* is built

Never stop for: cosmetic diffs, commit identity drift, unrelated pre-existing changes, unrelated test failures, plan wording drift, or an unlisted file that changes no behavior.

## Proceed and log

Incidental: formatting, whitespace, indentation, import order, line endings, lockfiles, generated output, comments/docs, this plan's own tests.
Also incidental: extra fixup commits, a commit message or hash that differs from the plan.

Note format in the step: `Deviation: <what> — cosmetic, no behavior change`.

## Asking

- One ask per blocking event: state the changed behavior, why it is material, and the options — extend the boundary, file a follow-up, proceed with a recorded deviation.
- Ambiguous but non-blocking: finish the step, then batch every pending question into one ask at the step boundary.
- Never ask twice about the same class of change in one plan.

## Environment

- Required: correct branch, dependencies resolve for the plan's commands, affected-area baseline green.
- Not required: pristine tree, green full suite, an identical commit graph.
- Leave the user's unrelated changes untouched; never stash, revert, or commit them.

## Rationalizations to reject

| Excuse | Reality |
|---|---|
| "An out-of-scope path changed, so stop" | Check behavior first; expected files are advisory |
| "The commit hash differs" | Compare content, never identity |
| "Ask to be safe" | The stop list is closed; log the rest |
| "Ignore it, it is small" | Cosmetic is ignorable; a behavior change is not |
| "The hand-written version behaves the same" | Behavior equality is not `Must match`; diff against the pinned ref |
