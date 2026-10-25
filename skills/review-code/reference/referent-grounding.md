# Referent Grounding

Every path, package, symbol, flag, and config key the review names must be one the reviewer resolved
in the tree — or be labeled `unverified`. A plausible path is not evidence.

## The ledger

| Referent | Where it must come from |
|---|---|
| Path or file | `git diff --name-status`, `git ls-tree`, or a read of that path |
| Package or module | The manifest plus the directory listing — never pattern-completed |
| Symbol | Its definition site, read; a quoted name is located, not recalled |
| Config key, flag, env var | The config file or the parser that consumes it |
| Move or rename | Both sides from `git diff -M --summary` or `git log --follow` |
| Suggested destination | The convention, ADR, or sibling module that places code there |

- Never derive a path from a branch name, ticket title, PR title, or feature name.
- Never complete a path with a placeholder segment such as `<current-feature>`.
- A destination invented for the review is a challenge, not a recommendation — see **challenge-taxonomy**.

## Labels

| Label | Means | Use when |
|---|---|---|
| resolved | Read at `path:LINE` | Default for any referent inside a finding |
| `unverified` | Not located; search named | The tree does not contain the referent |
| `Suspected` | Inferred; evidence named | A move or rename git cannot prove |

`unverified` never stands alone. Name the failed search and raise the gap as a challenge:

```markdown
| Referent | Status | Evidence |
|---|---|---|
| `src/orders/order-discount/Pricing.java` | unverified | `git ls-files 'src/orders/*Pricing.java'` → 1 path, not this one |
```

## Restructure and placement claims

A move, extract, rename, or "should live in" claim needs one of these cited:

| Evidence | Example |
|---|---|
| Documented convention | `AGENTS.md:12` — feature code stays in its domain package |
| Architecture decision | `docs/adr/014-package-layout.md:9` |
| Observed structure | 11 of 12 sibling modules keep handlers beside their domain |
| Build constraint | Nested module would break the parent's package-private access |

Cite one or the claim is a challenge with `Blocking: yes`. Never present a preference as a finding.

## Prohibited

| Anti-pattern | Why it is a defect |
|---|---|
| `src/orders/<current-feature>/Pricing.java` | The feature name is not a directory; the path was invented |
| "moved to X" with one side only | The move is inferred from the diff's shape |
| "should live in X" with no cited rule | Placement preference dressed as a finding |
| `src/.../Pricing.java` | The elision hides which file was read |
| A path in a fix suggestion that no module contains | Sends the developer to a directory that does not exist |

## Referent check output

Add this block to the report whenever anything is unverified:

| Referent | Status | Evidence |
|---|---|---|
| `src/orders/do-something/Pricing.java` | resolved | `src/orders/do-something/Pricing.java:18` |
| `src/orders/order-discount/Pricing.java` | unverified | `git ls-files 'src/orders/*Pricing.java'` → 1 path |

## Validation

- [ ] Every referent is resolved, or `unverified` with a named search
- [ ] No path segment was derived from a branch, ticket, or feature name
- [ ] Every move or rename cites both sides
- [ ] Every placement or restructure recommendation cites a rule, ADR, observed structure, or constraint
- [ ] The referent check lists every unverified referent
