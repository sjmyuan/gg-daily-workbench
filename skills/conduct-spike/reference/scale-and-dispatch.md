# Scale and Dispatch

Loaded by **scale-routing** when a spike may use sub-agents, or when an area session returns. Owns the threshold, the agent each role resolves to, the brief, the return contract, and the verification depth.

## Default: in-session

Run the spike in the orchestrating session unless a threshold below is met.
Dispatching a spike that fits in one session costs a brief, a return, and a verification seat for work the orchestrator could have done while holding the context.

| Condition | Route |
|---|---|
| One problem, evidence under ~10 files | In-session — the fast path |
| One problem, evidence over ~10 files or 2+ independent subsystems | One area session |
| 2+ areas | One area session per area, dispatched concurrently |
| Cross-area constraint needs synthesis | In-session by the orchestrator after the returns |

The threshold is reading volume and context pressure, not artifact count. When unsure, start in-session; dispatch when the second read starts crowding out the decision.

## What never dispatches

- Scope definition — the orchestrator holds the cross-state every brief depends on.
- The ADR review — the user is the reviewer.
- Verification of a return whose claims the orchestrator can check with one read.

## Role resolution

Resolution starts only after the threshold above justifies the dispatch — a matching agent never makes a dispatch worth doing. Resolve each role once per spike.

| Rung | Use when | Target |
|---|---|---|
| 1 | The project's agent registry has an agent whose domain matches the area and whose permissions let it write ADR files — a read-only agent investigates but never authors, and an area is never split | That **project agent** |
| 2 | The platform exposes the role's named agent | **code-analyst** (area session, rewrite, independent check) · **solution-doc-writer** (overview) |
| 3 | Neither exists, but the platform has a default agent | The **default agent**, with the role's skill and write boundary named in the brief |
| 4 | No target can carry the role | **Run it in-session** under the same gate and write boundary — tell the user if the volume makes that unsafe |

Role skill: area session → **investigate-code** + **draft-adr** · rewrite → **draft-adr** (`adr-rewrite`) · independent check → **question-everything** · overview → **write-solution-doc**.

- The **role contract travels with the dispatch**: name the role skill and the boundary (`adrs/adr-<area>-<NN>-<problem>.md` only). An unqualified dispatch lands on the default agent, which drafts a document that misses the gate and may prompt the user itself.
- **Independence**: the check seat is a fresh instance, never the area session that wrote the ADRs — even when both resolve to one project agent.

## Area brief

One brief per area. Every path absolute. Fill every bracket; a brief that carries only a goal and an output name makes the agent re-derive scope and repeat searches.

```markdown
# Area brief — <area>

## Mode
`adr` — write the ADRs, nothing else.

## Mission
Settle <area>'s problems with ADRs that pass the acceptance gate, then return once.

## Context
- Spike question: <one sentence>
- Scope file: <absolute path> — problems <P1, P2>
- Boundaries: <inside> · out: <sibling areas>
- Accepted assumptions: <A1 → value> — a premise the ADRs may rely on
- Sibling decisions: <area → ADR path, chosen option> — inherit, never contradict

## Inputs
- Drivers (mandatory): <P1: driver, metric, threshold; …> — never infer one
- Known locations: <symbol / file:line already found>
- Already searched: <query + root + outcome>
- Candidate / rejected options: <named, with why rejected>
- Notes (re-dispatch only): <absolute path> — verified claims are settled

## Tasks
1. Investigate to sufficiency per the evidence-sufficiency reference.
2. Draft one ADR per problem with `draft-adr`, headlessly, from the drivers above.
3. Run the acceptance gate on each ADR; fix the ADR, not the gate.
4. Return once, after the gate.

## Return
- ADR paths, per problem: chosen option, the drivers it wins, what is unverified
- Gate result per ADR (`ACCEPT` or `REVISE` + failing IDs)
- Gaps, cross-area conflicts, and anything contradicting another area
- Options the evidence ruled out, and why

## Constraints
- Write only `adrs/adr-<area>-<NN>-<problem>.md`.
- Never write `scope.md`, `solution.md`, code, config, or tests.
- Never prompt the user; the orchestrator owns the review.
- Never verify your own output and never dispatch a sub-agent.
```

## Rewrite brief

A settled decision only needs its ADR rewritten. Hand over the digest and the target path — no investigation task, no scope file, no re-evaluation.

```markdown
# Rewrite brief — <ADR>

## Mode
`adr-rewrite` — rewrite in place, never investigate.

## Decision
- Chosen option: <Option N> — the drivers it wins, with metric and threshold
- Evidence: <file:line> per driver-impact row
- Still unverified: <claim → what would settle it>

## Task
Rewrite <absolute ADR path> in place with `draft-adr`, in template order, from the decision above.
Re-run the acceptance gate on the changed sections only.

## Constraints
- Never investigate; every claim above is settled input.
- Never add an option this digest does not name.
- Never write `scope.md`, `solution.md`, code, config, or tests.
- Never prompt the user, never spawn a sub-agent, and never verify your own output.

## Return
ADR path · sections changed · gate result on the changed sections · unverified claims
```

The digest is the question. A brief with no chosen option means the decision is not settled — run the spike instead.

## Return contract

An area session returns once, after the ADRs are written. The ADRs are the durable state; a receipt is supplementary and a lost session resumes from the files.

| Field | Required |
|---|---|
| ADR paths + chosen option per problem | Yes |
| Gate result per ADR | Yes |
| Unverified claims and what would settle them | Yes |
| Cross-area conflicts, gaps | When present |
| Options ruled out and why | Yes — prevents a sibling re-proposing them |

## Verification depth

| Claim | Depth |
|---|---|
| An ADR's decision-flipping claim | Full check against the primary source; a **DISAGREE** goes back to a new area session with the verdict and the ADR path |
| Supporting claim | Check the cited `file:line` exists and says what is claimed |
| Cross-area constraint | Check both sides; a conflict is surfaced to the user, never silently resolved |

Verification is per claim; a stale `file:line` or an inference presented as verified is a defect worth a re-dispatch, a formatting nit is not.

## Re-dispatch

Re-dispatch the same session (or a new analyst with the files) with:

1. the written ADR paths,
2. the failing gate IDs or the verification verdicts,
3. the specific claims to repair.

Never rebuild evidence by re-investigating; never re-verify a claim the re-dispatch did not touch.
