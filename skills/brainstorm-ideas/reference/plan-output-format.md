# Plan Output Format

Used by **compile-actionable-plan** to structure and verify the final plan.

## Skeleton

```markdown
## Plan
[One sentence stating what the plan delivers.]

## Why this plan
- [Goal it reaches]
- [Risk it removes]
- [What we deliberately left out]

## Goals
- **G1** [Goal] — success: [observable signal]

## Decisions
- **D1** Chose [idea] — [reason]
- **D2** Dropped [idea] — [reason]
- **D3** Open: [question]

## Risks
- **C1** [Challenge] — impact: [High/Med/Low] — mitigation: [action] — serves: G1

## Next steps
1. **S1** [Verb + object] → produces [output] — done when [check] — serves: G1, C1
```

## Guidance
- Number every goal, decision, risk, and step; cite the IDs in `serves` so a reader can trace each choice.
- Open `Plan` in plain language and define any term the user has not used.
- Give one line per reason in `Why this plan`: the goal, the risk, and any deliberate exclusion.
- Record every confirmed candidate that is not a next step in `Decisions`, with its reason.
- Order `Next steps` by execution; add a dependency note when order matters.
- Time-bound goals are allowed; never add a calendar schedule — dates in steps go stale.
- Keep one line per item so the plan reads without the session transcript.

## Quality bar

| Criterion | Pass |
|---|---|
| Every goal has an observable success signal | G1–Gn each carry `success:` |
| Every confirmed candidate appears in the plan or in `Decisions` with a reason | no silent drops |
| Every step names its output, its done-when, and the goal or risk it serves | S1–Sn complete |
| A reader who missed the session can act on it | no undefined term, no unexplained choice |

Pass bar: all four criteria. Fix any failure before presenting; never ask the user to confirm a plan that fails one.
