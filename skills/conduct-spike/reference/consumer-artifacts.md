# Consumer Artifacts

Loaded by **produce-optional-artifact**, or when someone asks for investigation notes, an architecture overview, or the delivery handoff. Owns the consumer test, the notes shape, the overview brief, and the write boundary.

## The consumer test

Produce an artifact only when you can name who consumes it and what they will do differently.

| Artifact | Justified consumer | Not justified |
|---|---|---|
| `notes-<area>.md` | A later spike, a delivery cell needing current-state detail, a user asking what exists today | "For completeness"; the ADR already cites what it needs |
| `solution.md` | Delivery starts next and needs a target-state view; onboarding a team; the user asks for the architecture | The ADRs already answer the question and nothing follows |
| Either | A named person or skill that reads it | A hypothetical future reader |

No named consumer → produce nothing and say why. Silence is the correct output.

## Notes

Shape and rules live in **evidence-sufficiency.md** §Optional notes document. Spike-specific points:

- One file per area, `notes-<area>.md`, beside `scope.md`.
- The ADR cites it only when it adds a detail the ADR should not carry — never as the source of a decision.
- When a later fact changes a note, update the note in place; no versions, no dates in the body.

## Architecture overview

Target-state only, decision-referencing, produced by `write-solution-doc`.

1. Dispatch `solution-doc-writer` with: the ADR set paths, the cited evidence, the audience, and which C4 levels matter.
2. Instruct it to **reference** each ADR (`adr-<area>-<NN>-<problem>.md`, chosen option) rather than restate the decision; a restated decision is a second owner that will drift.
3. Verify fidelity to the ADRs — no new decision, no changed chosen option, no invented component.
4. Save as `<spike-folder>/solution.md`; link it from the handoff.

If the overview would only repeat the ADRs in different prose, do not produce it.

## Handoff

Only these cross into delivery; each by reference, never copied:

| From the spike | To delivery |
|---|---|
| ADR paths per problem | Index feature table `ADRs` column |
| `solution.md` when it exists | Index `## Spike References` |
| `notes-<area>.md` when it exists | Cell `context.md` `## Pointers` |
| `scope.md` question and drivers | Cell charter context, summarised in one line |

A fact discovered during delivery that changes a decision re-enters through **continue-spike**: rewrite the ADR, re-run the gate, then update the artifacts that cite it.
A delivery defect that changes no decision never touches the spike.

## Write boundary

Every write stays under `**/spikes/**`:

- `scope.md`, `adrs/adr-<area>-<NN>-<problem>.md`, `notes-<area>.md`, `solution.md`
- never code, config, tests, migrations, or a POC
- never a path outside the spike folder

After each write, list the paths written and confirm each sits inside the spike folder. On an outside path: stop, report it, and do not continue.
