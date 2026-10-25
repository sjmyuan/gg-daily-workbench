# Example: Challenging a Vague Request Before Accepting a Spike

**Scenario**: A user opens a spike with one sentence and expects investigation to start. The choice of metric changes the area split, so the gate runs before `scope.md` exists.

Applies **challenge-the-ask**.

## Input / Context
- **Request**: "Our checkout is slow, spike what we should do."
- **Stakes**: the spike's area split depends on which latency the user means.
- **Known**: three open tickets mention waiting on the first token; none mention query time.

## Restatement
"In your words: checkout is slow and you want a spike on options. Inferred: the goal is user-perceived speed, not infrastructure cost."

## Findings before filtering
| # | Dimension | Finding | Material? |
|---|---|---|---|
| 1 | Ambiguity | "slow" — first byte, query, or paint? | Yes — changes the split |
| 2 | Scope | Web checkout, mobile, or both? | Yes — changes the repos |
| 3 | Goal | Driver is user complaints or infrastructure cost? | Yes — changes the options |
| 4 | Constraints | Is adding a cache or queue allowed? | No — the repo answers it |
| 5 | Success criteria | No target latency stated | Yes — changes the done criteria |

Finding 4 is a note, not a question: the acceptance criteria in the repo already settle it.

## Output — batched gate, round 1

**Q1 · Ambiguity · blocking** — "slow" names three different measurements.
  A) First-token latency — the spike covers streaming and buffering
  B) Query latency at p95 — the spike covers indexing and caching
  C) Time to interactive — the spike covers bundle and render path
Recommendation: A — all three open tickets mention waiting on the first token; none mention query time.
Default if unanswered: none — blocking.

**Q2 · Scope · non-blocking** — "checkout" is one surface or three.
  A) Web checkout only — one repo, one area
  B) Web plus mobile — two repos, contract-first edge
  C) All checkout surfaces including POS — three areas
Recommendation: A — every ticket is web; expand later if mobile reports appear.
Default if unanswered: A.

**Q3 · Success criteria · non-blocking** — no target is stated.
  A) p95 first-token under 300ms — measurable now
  B) Any improvement users notice — measure, no target
Recommendation: A — a decision ADR needs a falsifiable target.
Default if unanswered: A.

## User response
"Q1: A. Q2: just web for now. Take the defaults on the rest."

## Result

| Item | Value |
|---|---|
| Gate state | `ACCEPTED-WITH-ASSUMPTIONS` |
| Handed to the calling skill | goal = reduce first-token latency on web checkout; scope = one repo, one area |
| Assumption A1 | `Assumption (user-accepted, unverified)` — target is p95 first-token under 300ms, per the Q3 default |
| Recorded in | `scope.md` → `## Accepted assumptions` |
| Round 2 | Not due — no re-challenge trigger |

Validation: three questions, each with options, a recommendation, and a default; every surviving finding passed the materiality test; one blocking question held the gate until answered.
