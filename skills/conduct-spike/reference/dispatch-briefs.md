# Dispatch Briefs

Brief index + the shared **structured brief shape**, known-context contract, and evidence-map input/output contract for dispatching spike work to sub-agents. The capability→agent mapping and dispatch rules live in **reference/multi-agent-orchestration.md**. Each ready-to-fill brief lives in its own file, loaded on demand:

| Capability → agent | Brief file |
|---|---|
| investigate-per-area → `code-investigator` | [investigation-brief.md](investigation-brief.md) |
| compile-findings-doc → `findings-doc-writer` | [findings-doc-brief.md](findings-doc-brief.md) |
| draft-problem-adrs → `adr-writer` | [adr-drafting-brief.md](adr-drafting-brief.md) |
| compile-solution-doc → `solution-doc-writer` | [solution-doc-brief.md](solution-doc-brief.md) |

Dispatch multiple work units concurrently, a single unit on its own. Fill each brief from its file per the **structured brief shape**, dispatch it to the mapped agent, then review each returned result against the capability's spike-specific checks (in its brief file). All briefs carry the shared known-context and evidence-map contracts below; a re-dispatched unit also carries the verification-result contract.

## Structured brief shape

Every dispatch brief follows the same 7-section skeleton so a filled brief is self-contained — the sub-agent follows the sections in order and never guesses. Each brief file (table above) is the ready-to-fill form: the orchestrator substitutes the `[bracketed]` fields and dispatches verbatim to the mapped agent.

| # | Section | Filled as |
|---|---|---|
| 1 | Mission | Who I am + the one-sentence deliverable |
| 2 | Context | Spike goal, scope-map slice (area/problems + boundaries), user-stated context, brownfield/greenfield |
| 3 | Inputs | Prior-artifact paths + established facts to load and how to use each |
| 4 | Tasks | Ordered actions to perform |
| 5 | Output contract | Exactly what to return and its format |
| 6 | Constraints | Guardrails — what never to do, including the write boundary |
| 7 | Report back | What to flag to the orchestrator |

## Known context in every brief

Everything the orchestrator already holds travels in the brief — a sub-agent never re-derives scope, constraints, or settled facts. Each field is filled in one of two modes, by where the info lives:

- **By reference** — the info is persisted in an artifact: fill in the **path + section** to load; never duplicate it inline.
- **Inline** — the info lives only in the orchestrator's or user's context, or the sub-agent must persist it into its output: fill in the **value** itself.

| Known-context item | Source | Mode |
|---|---|---|
| Spike goal, area problems | `scope.md` | Path |
| Findings doc pair (human + evidence), sibling pairs | `docs/findings-*.md` + `docs/evidence-*.md` | Path |
| Chosen options, decided sibling ADRs | `adrs/*.md` | Path |
| Area boundaries | scope dialog | Inline |
| User-stated constraints & facts | user dialog | Inline |
| Decision drivers, candidate options | user dialog | Inline |
| Investigation results (pre-findings-pair) | investigator's output | Inline |

- **Must-write → inline**: when the sub-agent writes the info into its output (drivers → ADR, investigation results → evidence doc), pass it inline.
- **Persist-once (optional)**: when unpersisted context is needed across several dispatches, persist it once and pass the path.
- A `[bracketed]` field is a **path** when an artifact holds it, a **value** otherwise — never leave either empty.

## Findings docs in every brief

An area's findings are **always passed as a pair** — the human doc (`docs/findings-<area>.md`) and the evidence doc (`docs/evidence-<area>.md`) together. Never pass one alone: the human doc orients (resource index, diagrams, TL;DRs, constraints), the evidence doc carries the claim ledger (`file:line`, confidence, searched-negatives).

- **Input — include the pair**: pass both docs so the sub-agent starts from verified `file:line` locations instead of scanning from scratch. Instruct it to treat the evidence ledger's **Verified** claims as settled and only dig into marked **Gap**s/**Inconsistencies** or **Inferred**/**Assumption** claims.
- **Output — require an evidence map back**: every investigation brief asks the sub-agent to return a per-area evidence map (entry points, key code locations with `file:line`, call chains, evidence verdicts, searched-negatives) alongside its narrative findings — the orchestrator records it in the area's evidence doc (see **compile-findings-doc**).
- **Searched-negatives travel with the evidence doc**: a documented "not found" tells the next sub-agent not to repeat the scan.
- **ADR-drafting briefs** include the area's findings pair so ADRs can cite evidence locations without re-reading code.
- **Verification briefs** carry the same contract — established `file:line`, the settled-vs-open claim split, and searched-negatives — so the verifier starts from evidence, not zero (see `question-everything`'s **reference/verification-protocol.md**).
- **First pass is the seed**: when no findings pair exists yet, briefs omit the input but still require the evidence-map output — the first investigation builds the map the evidence doc records.

## Verification results in a re-dispatch brief

A unit re-dispatched after a verification **DISAGREE** carries the **verification result** — never a blank re-run. Its **Inputs** add:

- **Open challenges (inline)**: the challenged claims, each challenge's verdict, and what the verifier disputed — resolve each and leave the settled work alone.
- **Priors to preserve (path)**: the prior result or its evidence map, once persisted — start from it, do not rebuild.
- **Re-dispatch scope**: which claims to re-examine and the round number (cap 2 — repair once, then confirm changed claims; per `question-everything`'s **verify-sub-agent-results**).

The result is inline (not yet an artifact); when a paused unit recorded open challenges in `scope.md` (see **scope-map-guide**), pass that section by path.

## Write boundary in every brief

Every brief's **Constraints** section carries the same boundary: writes are confined to the spike folder (`**/spikes/**`); never modify code, config, tests, or any file outside it. A sub-agent that finds implementation work needed flags it in **Report back** instead of making the change. Full doctrine and boundary check: **reference/write-boundary-guide.md**.
