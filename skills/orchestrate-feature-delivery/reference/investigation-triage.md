# Investigation Triage (L0–L3)

Backs **triage-issue**; consumed by **handle-post-implementation-issue**, **orchestrate-delivery**, and **resume-delivery**. Pick the cheapest rung that actually answers the question — the spike is the exception, not the default.

## Ladder

| Rung | Answers | Test | Action | Dispatches | Artifacts |
|---|---|---|---|---|---|
| **L-1 Clarify** | What is actually being asked? | Any inference was needed to make the ask decidable | Restate, show the inference list, ask `grill-user`'s **grill-the-ask** with options plus a recommendation | 0 | none |
| **L0 Answer** | What did we decide, why, or what is the status? | Index, `context.md`, plan/rework, ADR, findings/evidence, git log settle it | Read in-session and answer | 0 | none |
| **L1 Evidence** | Where or what is the code fact? | A code fact is missing or contradicted | One read-only `code-investigator`, artifacts by path | 1 | none |
| **L2 Decision** | Was exactly one ADR decision wrong or incomplete? | One decision changes; no new options | `adr-writer` revises in place; `solution-doc-writer` only if target state changes | 1–2 | ADR (+ solution section) |
| **L3 Spike** | Which option should we choose across decisions? | ≥2 decisions/areas, new options, or formal findings required | `spike-conductor`, **delta** scope | ≥3 | spike artifacts |

## Escalation rules

- L-1 is a precondition, not a rung: it costs nothing, runs before the ladder, and ends only when nothing was inferred.
- An assumption L-1 accepts is recorded in the index cell brief, labeled `Assumption (user-accepted, unverified)` — never in `context.md`, which the planner and executor own.
- Stop at the first rung that answers; never skip a rung without naming why it failed.
- State the question, rung, recorded evidence checked, and expected output before dispatching.
- Escalate one rung per attempt — L0 → L1 → L2 → L3.
- Ambiguous rung → ask the user with cost and latency per rung; recommend the cheapest sufficient one.
- L3 requires a stated trigger from the list below.

## L3 triggers (any one)

- The issue spans ≥2 decisions or areas.
- The fix needs option evaluation or a new ADR.
- The evidence is missing and spans multiple areas to gather.
- The user asks for formal findings or solution artifacts.
- A prior L2 revision failed to hold.

## L2 contract

- `adr-writer` rewrites the ADR in place (versionless); no scope map, no findings pair.
- `solution-doc-writer` only when the target state (C4, contracts, RAID) changes.
- Verify new code claims with one independent pass; no full loop unless the decision is irreversible.
- Record the revision trigger in the ADR context — no changelog, no version markers.

## L3 delta scope

- Pass the original `scope.md`, evidence docs, and governing ADR by path.
- Investigate only the delta; never rebuild unaffected findings or solution sections.
- The span rule is why L3 was chosen — if only one decision moved, drop to L2.

## Rework mapping

| Cell status | Usual rung | Note |
|---|---|---|
| **done** | L2 or L3 | L2 for one wrong decision; L3 when the decision space changed |
| **in-progress** | L1 or L2 | L3 only if the governing ADR is challenged |

## Anti-patterns

| Anti-pattern | Why it costs | Instead |
|---|---|---|
| "Investigate" always means `spike-conductor` | A full conductor for a one-line answer | L0 or L1 |
| Classifying an ambiguous report | The rung answers the wrong question | Restate expected versus actual first (L-1) |
| Deciding "is this ambiguous?" first | The misreading is what L-1 exists to catch | Count the inferences: zero → proceed, else show the list |
| Recording an assumption in `context.md` | Only the planner and executor write it | Record it in the index cell brief |
| Treating artifact reads as doing the work | The mandate forbids delivery work, not reading | Answer from the record at L0 |
| Running L2 through a full spike | Scope, findings pair, and solution rebuild for one ADR | `adr-writer` directly |
| L3 without a trigger | Weeks of artifacts for a local bug | State the trigger or drop a rung |
| Re-verifying the whole ADR at L2 | Cost with no new evidence | Verify only new code claims |

## Checklist

- [ ] Request restated, every inference itemized, and the list shown before any rung was chosen.
- [ ] Question stated in one sentence.
- [ ] Recorded artifacts checked before any dispatch.
- [ ] Rung and justification stated.
- [ ] L3 has a named trigger.
- [ ] Artifact scope matches the rung — none at L0/L1.
- [ ] Outcome recorded only when delivery state changed.
