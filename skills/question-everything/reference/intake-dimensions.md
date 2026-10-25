# Intake Dimensions Rubric

Use with **challenge-the-ask** to probe a user-supplied request. A request has no primary source: the closer is the user's decision, never a verdict.

## Dimensions

| Dimension | What it probes | Sample question |
|---|---|---|
| **Goal** | The problem behind the ask | Is the real driver latency, cost, or a deadline? |
| **Ambiguity** | Overloaded or vague terms | "Faster" means first byte, query time, or paint? |
| **Scope** | Surface inside and outside | Which repos, modules, or teams are in? |
| **Success criteria** | How completion is judged | What must be true for you to call this done? |
| **Constraints** | Limits the user already holds | Which are fixed: deadline, budget, no new infrastructure? |
| **Conflict** | Contradiction with repo state or prior decisions | The ADR chose polling; this asks for events — which wins? |
| **Feasibility** | Whether the ask is possible as written | Is the data available to measure that? |
| **Consumer** | Who uses the output | Who signs off: you, a team, a reviewer? |

## Materiality test

A finding becomes a question only when a different answer changes one of:

| Lever | Example |
|---|---|
| The area/problem split | "Checkout" is one area or three |
| Which options are compared | Caching versus streaming |
| The done criteria | p95 versus first-token latency |
| The investigation budget | One area versus a five-area spike |

Everything else is a note, never a question.

## Clarify versus push back

| | **Clarify** | **Push back** |
|---|---|---|
| Situation | The user was unclear | The user is clear, the evidence disagrees |
| Evidence | Their own words, in conflict | Repo, prior ADRs, investigation |
| Opening phrase | "I read this two ways" | "The evidence says otherwise" |

Never present a push-back as a clarification — the user must know which one they are answering.

## Question format

```
Q<N> · <Dimension> · <blocking | non-blocking>
"<the user's own words>" — <the ambiguity in one line>
  A) <option> — <what the work becomes>
  B) <option> — <what the work becomes>
  C) Something else — describe it
Recommendation: <A | B> — <the evidence behind it>.
Default if unanswered: <A | B>.
```

## Option rules

- 2–3 options, mutually exclusive, each changing the work concretely.
- An option restating the question is not an option.
- The recommendation names its evidence — never "it depends" or "both are valid".
- The default must be safe: it may not lock an irreversible decision.
- A contradicted user constraint is always blocking — never reinterpret it silently.
- A blocking question carries no default; the gate stays `BLOCKED` until it is answered.

## Checklist

- [ ] Every question names its dimension and its blocking status.
- [ ] Every question carries 2–3 options, a recommendation, and a default.
- [ ] Every surviving finding passes the materiality test.
- [ ] No question asks what the repo already answers.
