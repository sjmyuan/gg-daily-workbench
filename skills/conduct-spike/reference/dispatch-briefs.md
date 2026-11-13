# Dispatch Briefs

Brief index + the shared **structured brief shape**, the **context inventory** gate, the three fill modes, the **callee intake record**, the **area-session contract**, and the verification-result contract. The capability→agent mapping and dispatch rules live in **reference/multi-agent-orchestration.md**. Each ready-to-fill brief lives in its own file, loaded on demand:

| Capability → agent | Brief file |
|---|---|
| investigate + pair + ADRs (single return) → `spike-area-analyst` | [area-analyst-brief.md](area-analyst-brief.md) |
| compile-solution-doc → `solution-doc-writer` | [solution-doc-brief.md](solution-doc-brief.md) |

Dispatch one brief per area and run all areas concurrently; each session returns once, carrying its written pair and ADRs — never a bare evidence map or an intermediate phase. Fill each brief from its file per the **structured brief shape**, then review the returned receipt against the capability's spike-specific checks (in its brief file). All briefs carry the shared contracts below; a re-dispatched unit also carries the verification-result contract.

## Structured brief shape

Every dispatch brief follows the same 7-section skeleton so a filled brief is self-contained — the sub-agent follows the sections in order and never guesses. Each brief file (table above) is the ready-to-fill form: the orchestrator substitutes the `[bracketed]` fields and dispatches verbatim to the mapped agent.

| # | Section | Filled as |
|---|---|---|
| 1 | Mission | Who I am + the one-sentence deliverable |
| 2 | Context | Spike goal, scope-map slice (area/problems + boundaries), user-stated context, brownfield/greenfield |
| 3 | Inputs | Prior-artifact paths, established facts, known locations, and prior searches — with how to use each |
| 4 | Tasks | Ordered actions, ending with the single return (pair + ADRs) |
| 5 | Output contract | Exactly what to return and its format |
| 6 | Constraints | Guardrails — what never to do, including the write boundary |
| 7 | Report back | What to flag to the orchestrator |

Every brief also states **Model** — the tier chosen per **dispatch-discipline**. An omitted model inherits the orchestrator's session model, which is usually the most expensive.

## Context inventory before every brief

A brief is complete when **nothing the orchestrator holds is missing from it**. Before filling a brief, inventory the orchestrator's own context — not only the artifacts on disk:

1. List every item: the user's ask and answers, `scope.md` contents, each prior receipt, the orchestrator's own file reads, located symbols, and searches, the project's conventions, and the resolved paths.
2. Classify each item by fill mode (below) and place it in §2 when it orients or §3 when it seeds work.
3. Drop an item only because the unit cannot need it — never because it is obvious, cheap to redo, or findable.
4. Fail the brief when an item has no home: add the field instead of dropping the item.

A path is a pointer, not knowledge. A sub-agent that receives only a path must open the file, re-read it, and re-derive what the orchestrator already concluded — the inventory exists to make that re-derivation unnecessary. Because one area session spans the chain in a single return, a brief covers the whole chain instead of four hops; the inventory shrinks accordingly.

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
- **Never the transcript**: a brief carries the accepted request, not its clarification — no gate state, inference list, or which round settled what. The sub-agent applies the request; it never adjudicates the dialogue.

## Known context in every brief

Everything the orchestrator already holds travels in the brief — a sub-agent never re-derives scope, constraints, or settled facts.

| Known-context item | Source | Mode |
|---|---|---|
| Accepted request: goal, boundaries, constraints, done criteria, area problems | `scope.md` | Path + digest |
| Scope-owned premises (`A<n>`) | `scope.md` `## Accepted assumptions` | Digest |
| Area boundaries, out-of-scope siblings | `scope.md` + scope dialog | Digest + inline |
| Settled decisions and rejected options the artifacts must respect | user dialog | Inline |
| Decision drivers, candidate options | user dialog | Inline |
| Resolved paths: artifact root, spike folder, target repo root | `resolve-artifact-location`, work dialog | Inline |
| Files, symbols, and `file:line` already located | orchestrator's own reads, prior receipts | Digest |
| Searches already run, with outcomes (incl. "no matches") | orchestrator's own searches, prior searched-negatives | Digest |
| Prior receipt not yet persisted | returned receipt | Inline |
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
| **Consumer** | What the result feeds — the area's findings pair, an ADR's options, the solution doc |

- A brief carrying the intake record satisfies the callee's intake gate: the sub-agent adopts it, asks nothing, and explores only what it leaves open.
- An unfilled field becomes the sub-agent's guess and an extra exploration pass — fill all four, or state why one is unknowable.

## Area-session contract

One analyst session per area runs the whole chain and returns once; [area-analyst-brief.md](area-analyst-brief.md) owns its inputs and receipt.

- **One return** — the session investigates, writes the pair, drafts the ADRs, then returns. No intermediate return; the artifacts are the only handoff.
- **Drivers before dispatch** — the brief carries each problem's decision drivers; the analyst never infers one. Missing driver → the orchestrator asks the user before dispatching.
- **Pair before decisions** — the pair (human doc, then evidence doc per `document-findings`) is written before the ADRs, so every decision cites it.
- **Resume only to revise** — feedback or a repair re-dispatches with the written artifacts plus the verification result; never re-investigate to recover context.
- **Split, do not thin** — an area that cannot be covered in one pass returns a split request.

## Artifacts as inputs

- **The pair always travels together** — `docs/findings-<area>.md` (orients) plus `docs/evidence-<area>.md` (claim ledger, `file:line`, searched-negatives). Never pass one alone.
- **A re-dispatch receives its own pair** — the pair the same session authored, or the verified pair on a fresh dispatch. Instruct it to treat **Verified** claims as settled and dig only into marked **Gap**s/**Inconsistencies** or **Inferred**/**Assumption** claims.
- **Searched-negatives travel forward** — a documented "not found" belongs in the next brief's **already searched** digest, so no session repeats the scan.
- **Solution-doc briefs** receive every findings pair plus the decisions digest; verification briefs receive established `file:line`, the settled-vs-open split, and searched-negatives.

## Verification results in a re-dispatch brief

A unit re-dispatched after a verification **DISAGREE** carries the **verification result** — never a blank re-run. Its **Inputs** add:

- **Open challenges (inline)**: the challenged claims, each challenge's verdict, and what the verifier disputed — resolve each and leave the settled work alone.
- **Priors to preserve (path + digest)**: the prior artifacts — start from them, do not rebuild.
- **Re-dispatch scope**: which claims to re-examine and the round number (cap 2 — repair once, then confirm changed claims; per `question-everything`'s **verify-sub-agent-results**).

The receipt is inline (not yet an artifact); when a paused unit recorded open challenges in `scope.md` (see **scope-map-guide**), pass that section by path.

## Write boundary in every brief

Every brief's **Constraints** section carries the same boundary: writes are confined to the spike folder (`**/spikes/**`); never modify code, config, tests, or any file outside it. An area analyst writes only its pair and its ADRs — never `scope.md` or `solution.md`. A sub-agent that finds implementation work needed flags it in **Report back** instead of making the change. Full doctrine and boundary check: **reference/write-boundary-guide.md**.

## Completeness check before dispatch

Run on every filled brief; any failed check stops the dispatch:

- Every inventory item has a home — nothing was dropped for being obvious.
- Every path is absolute and carries its section anchor.
- The intake record's four fields are filled or explicitly declared unknowable.
- The brief states the single return (pair + ADRs) and carries every problem's drivers; a missing driver blocks the dispatch.
- Known locations and already-searched items are present whenever the orchestrator has any.
- Unpersisted prior receipts are inline, not referenced as if they were files.
