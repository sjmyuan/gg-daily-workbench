# Example: Resolve Pull-Request Conventions

**Scenario**: A delivery cell is ready for review in `acme/order-service`. Demonstrates **resolve-conventions** for the `pull-request` domain when sources conflict.

**Applies**: **resolve-conventions**

## Input / Context
Repo `acme/order-service`, remote `git@github.com:acme/order-service.git`, domain `pull-request`.

Evidence found:
- `.github/skills/contribution-flow/SKILL.md` — "Open PRs against `develop`; include a Risk section."
- `.github/PULL_REQUEST_TEMPLATE.md` — Problem, Change, Tests, Rollback, Checklist.
- `AGENTS.md:30` — "Disclose the agent, model, and harness."
- Recent merged requests: 7 target `develop`, 2 older ones target `main`.
- No label or reviewer rule found.

## Output

```
## Convention Card — acme/order-service · pull-request
| Field | Value | Evidence |
|---|---|---|
| Base branch | develop | .github/skills/contribution-flow/SKILL.md |
| Title format | type(scope): summary | recent: 9/10 merged |
| Body structure | Problem, Change, Tests, Rollback, Checklist + Risk | template + contribution skill |
| Labels | unknown | no rule; recent requests inconsistent |
| Reviewers | unknown | no CODEOWNERS; no stable practice |
| Draft flag | ready | recent: 10/10 non-draft |
| Linked issue | not required | template + recent requests |
| Disclosure | agent, model, harness | AGENTS.md:30 |
| Forbidden content | unrelated bundled changes | contribution skill |
| Duplicate search | required, open and closed | contribution skill |

Conflicts: recent requests split 7 develop / 2 main. The contribution skill and
template both require develop, so the two main requests are legacy.
Unknowns: labels, reviewers.
```

Asked the user:

> "Base is `develop` per the contribution skill. Labels and reviewers have no
> rule. Which should this PR carry, or should I open it without them?"

## Validation
- Every decided field cites evidence.
- Hard prohibitions are recorded.
- Labels and reviewers remain `unknown` until answered.
