# Dispatch Briefs

Brief index + the shared **structured brief shape**, the **context inventory** gate, the three fill modes, the **callee intake record**, and the evidence-map input/output contract for dispatching spike work to sub-agents. The capability→agent mapping and dispatch rules live in **reference/multi-agent-orchestration.md**. Each ready-to-fill brief lives in its own file, loaded on demand:

| Capability → agent | Brief file |
|---|---|
| investigate-per-area → `code-investigator` | [investigation-brief.md](investigation-brief.md) |
| compile-findings-doc → `findings-doc-writer` | [findings-doc-brief.md](findings-doc-brief.md) |
| draft-problem-adrs → `adr-writer` | [adr-drafting-brief.md](adr-drafting-brief.md) |
| compile-solution-doc → `solution-doc-writer` | [solution-doc-brief.md](solution-doc-brief.md) |

Dispatch multiple work units concurrently, a single unit on its own. Fill each brief from its file per the **structured brief shape**, dispatch it to the mapped agent, then review each returned result against the capability's spike-specific checks (in its brief file). All briefs carry the shared contracts below; a re-dispatched unit also carries the verification-result contract.

## Structured brief shape

Every dispatch brief follows the same 7-section skeleton so a filled brief is self-contained — the sub-agent follows the sections in order and never guesses. Each brief file (table above) is the ready-to-fill form: the orchestrator substitutes the `[bracketed]` fields and dispatches verbatim to the mapped agent.

| # | Section | Filled as |
|---|---|---|
| 1 | Mission | Who I am + the one-sentence deliverable |
| 2 | Context | Spike goal, scope-map slice (area/problems + boundaries), user-stated context, brownfield/greenfield |
| 3 | Inputs | Prior-artifact paths, established facts, known locations, and prior searches — with how to use each |
| 4 | Tasks | Ordered actions to perform |
| 5 | Output contract | Exactly what to return and its format |
| 6 | Constraints | Guardrails — what never to do, including the write boundary |
| 7 | Report back | What to flag to the orchestrator |

## Context inventory before every brief

A brief is complete when **nothing the orchestrator holds is missing from it**. Before filling a brief, inventory the orchestrator's own context — not only the artifacts on disk:

1. List every item: the user's ask and answers, `scope.md` contents, each prior unit's returned result, the orchestrator's own file reads, located symbols, and searches, the project's conventions, and the resolved paths.
2. Classify each item by fill mode (below) and place it in §2 when it orients or §3 when it seeds work.
3. Drop an item only because the unit cannot need it — never because it is obvious, cheap to redo, or findable.
4. Fail the brief when an item has no home: add the field instead of dropping the item.

A path is a pointer, not knowledge. A sub-agent that receives only a path must open the file, re-read it, and re-derive what the orchestrator already concluded — the inventory exists to make that re-derivation unnecessary.

## Three fill modes

| Mode | Use when | Filled as |
|---|---|---|
| **Path** | The item is persisted and the sub-agent needs its full detail | Absolute path + the section anchor to load; the sub-agent reads it once |
| **Digest** | The item is persisted **and** the orchestrator already holds a conclusion from it | That conclusion in 1–5 lines, marked `from <path#section>` — the sub-agent acts on it and opens the file only to go deeper |
| **Inline** | The item lives only in conversation, or the sub-agent must write it into its output | The value itself |

- **Digest is the anti-re-search mode**: located entry points and `file:line`, the settled-vs-open split, what was searched and not found, and decisions already taken. It never replaces its path — it removes the re-read and the re-scan.
- **Must-write → inline**: when the sub-agent writes the info into its output (drivers → ADR, investigation results → evidence doc), pass it inline.
- **Persist-once (optional)**: when unpersisted context is needed across several dispatches, persist it once and pass the path plus its digest.
- A `[bracketed]` field is a **path** when an artifact holds it, a **digest** when the orchestrator concluded something from it, a **value** otherwise — never leave a required one empty; a `(re-dispatch only)` field is filled exactly when re-dispatching.

## Known context in every brief

Everything the orchestrator already holds travels in the brief — a sub-agent never re-derives scope, constraints, or settled facts.

| Known-context item | Source | Mode |
|---|---|---|
| Spike goal, area problems | `scope.md` | Path + digest |
| Gate record: restatement, inferences, accepted assumptions | `scope.md` `## Accepted assumptions` | Digest |
| Area boundaries, out-of-scope siblings | scope dialog | Inline |
| User-stated constraints, facts, decisions, rejected options | user dialog | Inline |
| Decision drivers, candidate options | user dialog | Inline |
| Resolved paths: artifact root, spike folder, target repo root | `resolve-artifact-location`, work dialog | Inline |
| Files, symbols, and `file:line` already located | orchestrator's own reads, prior units | Digest |
| Searches already run, with outcomes (incl. "no matches") | orchestrator's own searches, prior searched-negatives | Digest |
| Prior unit results not yet persisted | returned results | Inline |
| Findings doc pair (human + evidence), sibling pairs | `docs/findings-*.md` + `docs/evidence-*.md` | Path |
| Chosen options, decided sibling ADRs | `adrs/*.md` | Path + digest |
| Project conventions that shape the work (exploration commands, layout, naming) | project instructions | Inline |

## Self-locating brief

A dispatched agent starts in its own context with no shared state — it cannot see the orchestrator's working directory, spike folder, or conversation. Make every brief locatable:

- **Absolute paths everywhere** — `<artifact-root>/spikes/<spike-name>/scope.md`, never a bare `scope.md` or `docs/evidence-<area>.md`.
- **Name the target repo root and the working scope** — the directory the unit reads, and the boundary it stays inside.
- Never make a sub-agent search the filesystem to find its own inputs.

## Callee intake record

A dispatched agent's skill may run its own intake gate and refuse to search on a private reading. Feed the gate instead of letting the sub-agent infer it:

| Field | Filled as |
|---|---|
| **System** | Repo root + the module or service under study |
| **Scope** | The area boundary and the symbols/paths inside it |
| **Depth** | The evidence depth required — C4 level, call-chain depth, or "current state to `file:line`" |
| **Consumer** | What the result feeds — the area's findings doc, an ADR's options, the solution doc |

- A brief carrying the intake record **is** the gate result: the sub-agent adopts it, asks nothing, and explores only what it leaves open.
- An unfilled field becomes the sub-agent's guess and an extra exploration pass — fill all four, or state why one is unknowable.

## Findings docs in every brief

An area's findings are **always passed as a pair** — the human doc (`docs/findings-<area>.md`) and the evidence doc (`docs/evidence-<area>.md`) together. Never pass one alone: the human doc orients (resource index, diagrams, TL;DRs, constraints), the evidence doc carries the claim ledger (`file:line`, confidence, searched-negatives).

- **Input — include the pair**: pass both docs so the sub-agent starts from verified `file:line` locations instead of scanning from scratch. Instruct it to treat the ledger's **Verified** claims as settled and only dig into marked **Gap**s/**Inconsistencies** or **Inferred**/**Assumption** claims.
- **Output — require an evidence map back**: every investigation brief asks for a per-area evidence map (entry points, key code locations with `file:line`, call chains, evidence verdicts, searched-negatives) alongside the narrative findings — the orchestrator records it in the area's evidence doc (see **compile-findings-doc**).
- **Searched-negatives travel forward too**: a documented "not found" belongs in the next brief's **already searched** digest, so the next sub-agent never repeats the scan.
- **ADR-drafting briefs** include the area's findings pair so ADRs cite evidence locations without re-reading code.
- **Verification briefs** carry the same contract — established `file:line`, the settled-vs-open claim split, and searched-negatives — so the verifier starts from evidence, not zero (see **reference/multi-agent-orchestration.md**, Verification questions).
- **First pass is the seed**: with no pair yet, briefs omit the pair but still carry known locations, prior searches, and the evidence-map output — the first investigation builds the map the evidence doc records.

## Verification results in a re-dispatch brief

A unit re-dispatched after a verification **DISAGREE** carries the **verification result** — never a blank re-run. Its **Inputs** add:

- **Open challenges (inline)**: the challenged claims, each challenge's verdict, and what the verifier disputed — resolve each and leave the settled work alone.
- **Priors to preserve (path + digest)**: the prior result or its evidence map — start from it, do not rebuild.
- **Re-dispatch scope**: which claims to re-examine and the round number (cap 2 — repair once, then confirm changed claims; per `question-everything`'s **verify-sub-agent-results**).

The result is inline (not yet an artifact); when a paused unit recorded open challenges in `scope.md` (see **scope-map-guide**), pass that section by path.

## Write boundary in every brief

Every brief's **Constraints** section carries the same boundary: writes are confined to the spike folder (`**/spikes/**`); never modify code, config, tests, or any file outside it. A sub-agent that finds implementation work needed flags it in **Report back** instead of making the change. Full doctrine and boundary check: **reference/write-boundary-guide.md**.

## Completeness check before dispatch

Run on every filled brief; any failed check stops the dispatch:

- Every inventory item has a home — nothing was dropped for being obvious.
- Every path is absolute and carries its section anchor.
- The intake record's four fields are filled or explicitly declared unknowable.
- Known locations and already-searched items are present whenever the orchestrator has any.
- Unpersisted prior unit results are inline, not referenced as if they were files.
