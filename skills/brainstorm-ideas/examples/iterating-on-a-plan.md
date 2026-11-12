# Example: Iterating on a Code-Review Plan

**Scenario**: Process topic — a focused round 1 improves a clear idea, then **iterate-session** deepens one direction. Shows **adaptive-pacing**, **iterate-session**, and the upgraded plan output.

**Applies**: **facilitate-session**, **iterate-session**
**Phases**: **clarify-idea**, **identify-goals**, **explore-challenges**, **generate-ideas**, **evaluate-ideas**, **challenge-ideas**, **refine-idea**, **compile-actionable-plan**

## Input / Context
User request: "My team's code reviews take days. The problem is clear — waiting and nitpicking — but I don't know the fix."

## Round 1 — focused mode
Facilitator: "The idea is clear, so I'll run focused mode — only the gaps, one checkpoint."

### clarify-idea (extract, don't re-ask)
Facilitator: "Captured: reviews take days because of waiting and nitpicking. What would faster mean in practice?"
User: "A non-trivial PR reviewed within one working day."

**Confirmed idea**: Get non-trivial PRs reviewed within one working day by cutting waiting and nitpicking.

### identify-goals
Facilitator: "What would success look like?"
User: "Median review time under 24 hours, and reviewers stop leaving nitpick comments."

**Confirmed goals**: median review under 24h; fewer nitpick comments.

### explore-challenges
Facilitator: "What could stop this — for example, reviewers being busy or PRs too big?"
User: "Reviewers are on other work, and PRs get too large before review."

**Confirmed challenges**: reviewer availability; oversized PRs.

### generate-ideas (focused set)
Facilitator: "Four candidates, quick pass:"

```
Faster Reviews
├── Inversion — smaller PRs
│   └── Enforce PR size limits — large PRs wait longer, so cap the size
├── Combination — scheduled review slots
│   └── Shared review calendar — reviewers reserve a review slot
├── Elimination — no full re-review
│   └── One-pass approval, fix later — skip the second pass
└── Analogy — like a queue
    └── Reviewer rotation queue — every PR gets an owner
```

User: "PR size limits and the rotation queue feel strongest."

### evaluate + challenge (merged checkpoint)
Facilitator: "Scoring and stress-testing in one pass since these are few:"

| Idea | Value | Feasibility | Scope | Challenge result |
|---|---|---|---|---|
| PR size limits | 2 | 2 | 2 | Allow exceptions for big refactors |
| Reviewer rotation | 2 | 2 | 2 | One reviewer per PR, less context — acceptable |
| Review calendar | 1 | 1 | 2 | Dropped — coordination overhead |
| One-pass + fix later | 1 | 0 | 2 | Dropped — quality risk |

**Refined idea**: Speed up reviews with PR size limits and a reviewer rotation queue.

### compile-actionable-plan (round 1)
Facilitator: "Here is the round-1 plan:"

## Plan
Get non-trivial PRs reviewed within one working day using PR size limits and a reviewer rotation queue.

## Why this plan
- Reaches G1 — size limits shrink the queue and rotation assigns an owner.
- Removes C1 and C2 — no PR waits for a volunteer, and no PR grows before review.
- Leaves out the review calendar and one-pass approval — coordination cost and quality risk.

## Goals
- **G1** Median review time under 24 hours — success: median under 24h for four weeks.
- **G2** Reviewer nitpick comments near zero — success: nitpick comments under 10% of review comments.

## Decisions
- **D1** Chose PR size limits — smaller PRs are faster to review.
- **D2** Chose a reviewer rotation queue — assigns an owner before review starts.
- **D3** Dropped the review calendar — coordination overhead for little gain.
- **D4** Dropped one-pass + fix later — quality risk.
- **D5** Open: how to enforce size limits without blocking large refactors.

## Risks
- **C1** Reviewer availability — impact: High — mitigation: rotation queue assigns up front — serves: G1.
- **C2** Oversized PRs — impact: High — mitigation: size limit with a refactor exception — serves: G1.

## Next steps
1. **S1** Define the PR size limit → produces a size rule — done when the team agrees on a line count — serves: G1, C2.
2. **S2** Set up the rotation queue → produces a queue and owner rule — done when every new PR gets an owner — serves: G1, C1.
3. **S3** Pilot on one team and measure median review time → produces a four-week measurement — done when the median is under 24h — serves: G1.

Facilitator: "Round 1 done. Want to go further — deepen a direction, combine, or pivot?"

## Round 2 — iterate-session
User: "Deepen the rotation queue — how should the rotation actually work?"

### Re-apply generate-ideas (deepen one direction)
Facilitator: "Three sub-ideas for the rotation:"

```
Rotation Queue
├── By expertise
│   └── Route to the owner of the touched area — fastest, most accurate review
├── By availability
│   └── Pick from reviewers free today — no waiting on a busy owner
└── By fairness
    └── Round-robin across the team — nobody is skipped
```

User: "Expertise routing, with a round-robin fallback so nobody is skipped."

### Re-apply refine-idea
Facilitator: "So the queue routes by expertise first, falls back to round-robin. Does that hold against the availability challenge?"
User: "Yes — the fallback keeps it fair and unblocked."

**Refined addition**: rotation routes by expertise, falling back to round-robin.

### Update the plan
Facilitator: "Round-2 plan, updated with the queue decision:"

## Plan
Speed up code reviews with PR size limits and a rotation queue that routes by expertise, falling back to round-robin.

## Why this plan
- Reaches G1 — expertise routing removes the "who reviews?" wait.
- Keeps C1 low — the round-robin fallback prevents stalls.
- Leaves out the review calendar and one-pass approval — unchanged from round 1.

## Goals
- **G1** Median review time under 24 hours — success: median under 24h for four weeks.
- **G2** Reviewer nitpick comments near zero — success: under 10% of review comments.

## Decisions
- **D1** Chose PR size limits — unchanged from round 1.
- **D2** Chose expertise-first rotation — routes to the owner of the touched area.
- **D3** Chose a round-robin fallback — no reviewer is skipped when no expert is free.
- **D4** Dropped availability routing — the fallback already prevents stalls.
- **D5** Open: size-limit enforcement mechanics.

## Risks
- **C1** Reviewer availability — impact: High — mitigation: rotation queue assigns up front — serves: G1.
- **C2** Oversized PRs — impact: High — mitigation: size limit with a refactor exception — serves: G1.

## Next steps
1. **S1** Define the PR size limit → produces a size rule — done when the team agrees on a line count — serves: G1, C2.
2. **S2** Map reviewers to expertise areas → produces an expertise map — done when every area has an owner — serves: G1.
3. **S3** Build the queue: expertise match, then round-robin fallback → produces the queue — done when a PR is assigned within one hour — serves: G1, C1.
4. **S4** Pilot on one team and measure median review time → produces a four-week measurement — done when the median is under 24h — serves: G1.

Facilitator: "Round 2 captured. Anything else to deepen, or is this the plan we lock in?"
