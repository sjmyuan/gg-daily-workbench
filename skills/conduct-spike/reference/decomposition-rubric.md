# Problem Decomposition Rubric for Spikes

Rubric for **define-spike-scope**: a spike decomposes into **areas** (shared-subject groupings), each into **problems** ("How to …?" decisions). Areas define the evidence/findings boundary; problems define the decidable units, one ADR each. Validate the breakdown with this rubric, then record it in `scope.md`.

## Two-level structure

```
Area: Data storage
├── Problem: How to pick the database engine? → adr-database-01-…
└── Problem: How to migrate the schema?      → adr-database-02-…
Area: API layer
└── Problem: How to expose the API contract? → adr-api-01-…
```

- A problem belongs to exactly one area; a problem that "spans" areas signals mis-grouping.
- An area exists because it holds problems — no empty areas.
- Areas keep the findings pair `findings-<area>.md` + `evidence-<area>.md`; problems each get one ADR.

## Area heuristics

| Heuristic | Boundary | Example areas |
|---|---|---|
| **Layer separation** | Different architectural layers | "Storage layer", "API layer", "Frontend rendering" |
| **Risk isolation** | High-uncertainty subjects get their own area | "Migration strategy for legacy data" |
| **Team/owner boundaries** | Areas owned by different teams | "Auth service changes" vs. "Payment service changes" |
| **Technology domains** | Different stacks or domains | "Mobile client" vs. "Backend services" vs. "Infrastructure" |

Target 2–5 areas; a single area is valid when the whole spike shares one subject. More than 5 → narrow the scope.

## Problem heuristics

Within each area, enumerate the "How to …?" decisions:

| Heuristic | Rule |
|---|---|
| **Decision independence** | Each problem is decidable without another's outcome ("pick the DB engine" vs. "migrate the schema") |
| **One ADR per problem** | Each problem maps to exactly one ADR |
| **Shared evidence** | Problems in one area share its subject and evidence map |

Target 1–3 problems per area; more than ~8 total → narrow the goal, merge problems, or split into follow-up spikes.

## Quality criteria

| Criterion | Good | Needs Work | Bad |
|---|---|---|---|
| **Area cohesion** | One shared subject; its problems belong together | Some problems loosely related | Grab-bag of unrelated problems |
| **Problem granularity** | One clear "How to …" decision | Bundles 2 related decisions | Grab-bag of unrelated decisions |
| **Decision independence** | Decided independently | Partial dependency, proceeds on assumptions | One decision forces another |
| **Investigate-ability** | Code can be meaningfully explored | Partial codebase, poorly documented | No code exists (greenfield) |
| **Actionability** | Clear what a good outcome looks like; concrete options per ADR | Fuzzy but directionally clear | Nobody knows what "done" means |
| **Boundary clarity** | Clear what is inside vs. outside each area | Some grey edges | Scope completely unclear |

## Edge cases

### Single-area spike
One subject, one or two problems ("Should we migrate from MySQL to PostgreSQL?" → engine choice + schema migration). It runs the identical workflow and produces the identical artifact set: one area row in `scope.md`, one findings pair, one ADR per problem, `solution.md`. Nothing is added or omitted because the spike is small.

### Too many areas (>5) or problems (>~8)
The scope is too broad. Choose: **narrow** the goal to the highest-uncertainty areas first and defer the rest, **merge** areas sharing evidence or problems sharing drivers, or **split** into separate spikes for independent problem domains.

### Greenfield (no existing code)
Each area's `investigate-per-area` shifts to researching industry approaches, similar in-house systems, and documented benchmarks and operational constraints instead of tracing code. Never build proof-of-concept prototypes — any POC is delivered by `orchestrate-feature-delivery`, not the spike.
