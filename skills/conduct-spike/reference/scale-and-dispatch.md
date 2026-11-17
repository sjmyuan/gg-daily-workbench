# Scale and Dispatch

Loaded by **scale-routing** when a spike may use sub-agents, or when an area session returns. Owns the threshold, the brief, the return contract, and the verification depth.

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

## Area brief

One brief per area. Every path absolute. Fill every bracket; a brief that carries only a goal and an output name makes the agent re-derive scope and repeat searches.

```markdown
# Area brief — <area>

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
- Write only `adrs/adr-<area>-<NN>-<problem>.md` and, if a consumer was named, `notes-<area>.md`.
- Never write `scope.md`, `solution.md`, code, config, or tests.
- Never prompt the user; the orchestrator owns the review.
- Never verify your own output and never dispatch a sub-agent.
```

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
