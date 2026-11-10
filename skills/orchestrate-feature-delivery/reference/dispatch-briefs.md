# Dispatch Briefs (Delivery)

Backs **agent-dispatch**, **orchestrate-delivery**, **resume-delivery**, **verify-cell**, and **triage-issue**. Every dispatched unit — planner, executor, verifier, investigator, spike conductor, ADR or solution-doc writer — receives a brief built from this contract. Cell-level content (feature, repo, scope, branch, plan location) is owned by **reference/delivery-index-format.md** (per-cell scope brief); this file owns how all known context reaches the agent.

## Why it matters here

The orchestrator holds state no dispatched agent can see: the index, the user's answers, L0/L1 findings, prior cells' delivered contracts, gate verdicts, and detected repo conventions. A brief that names only paths sends the agent back through the spike artifacts, the record, and the code to rediscover what is already settled — at full cost, in a context that cannot report it back.

## Context inventory before every brief

A brief is complete when **nothing the orchestrator holds is missing from it**.

1. List every item: the user's ask and answers (gate record, `Assumption (user-accepted, unverified)` lines), the index rows (statuses, dependencies, waves, cell brief), each spike artifact already read and what it established, L0/L1 answers, prior cells' delivered contracts and merge state, open gate findings, plan/rework state, detected repo conventions (branch prefix, test command, layout), and the resolved absolute paths.
2. Classify each item by fill mode (below) and place it in the brief.
3. Drop an item only when the unit cannot need it — never because it is findable or cheap to re-read.
4. Fail the brief when an item has no home: add the field instead of dropping the item.

## Three fill modes

| Mode | Use when | Filled as |
|---|---|---|
| **Path** | The item is persisted and the agent needs its full detail | Absolute path + the section anchor to load; the agent reads it once |
| **Digest** | The item is persisted **and** the orchestrator already holds a conclusion from it | That conclusion in 1–5 lines, marked `from <path#section>` — the agent acts on it and opens the file only to go deeper |
| **Inline** | The item lives only in conversation, or the agent must write it into its output | The value itself |

- **Digest is the anti-re-investigation mode**: located `file:line`, settled decisions, the contract surface a prior cell delivered, what a record read established, and what was ruled out at which rung.
- **Never replace a path with a digest** — pass both. The digest removes the re-read; the path keeps the full detail reachable.
- **Persist-once**: when unpersisted context is needed by several later dispatches, write it into the cell's `context.md` (planner-owned) or the index cell brief, then pass the path plus its digest.

## Context per dispatch target

| Target | Beyond the cell brief, it must receive | Mode |
|---|---|---|
| **planner** | Drivers and constraints, the dependency cells' delivered contract surface, known code locations from L1, acceptance assumptions | Digest + inline |
| **executor** | Verified plan path, base ref, active `rework-<date>.md`, branch name, prior-round gate findings | Path + inline |
| **verifier** | Cell digest (done means, decided behaviour), recorded `base7..head7`, governing ADR, prior-round verdicts | Digest + inline |
| **L1 investigator** | The question, the record artifacts already read and what they established, known locations, already-searched | Digest |
| **spike conductor (L3)** | Delta scope, the trigger that chose L3, prior artifacts and the findings they already cover | Path + digest |
| **adr-writer / solution-doc-writer** | Decision digest, affected sections, which cells the change governs | Digest + path |

## Self-locating brief

The agent starts in its own context with no shared state.

- **Absolute paths** for the feature folder, `plan.md`, `rework-<date>.md`, governing ADR, solution-doc section.
- **Name the repo root, base ref, and branch** — the executor must not re-detect the epic folder or the branch convention; the planner must not search for the feature folder.
- A sub-agent searching the filesystem for its inputs or re-detecting the repo's conventions is a brief defect, not agent behaviour.

## Callee intake records

Dispatched skills run their own intake gate and refuse to act on a private reading. Feed the gate:

| Agent | Fields it gates on |
|---|---|
| **planner** | Change type, expected behavior, triggering input, done criteria (plus the ref, for a restore) |
| **executor** | Plan path, active rework file, base ref, expected outcome |
| **code-investigator (L1)** | System, scope, depth, consumer |
| **spike-conductor (L3)** | Spike goal, affected areas or delta scope, boundaries, brownfield/greenfield |

A brief carrying these fields **is** the gate result: the agent adopts them, asks nothing, and explores only what they leave open. An unfilled field becomes the agent's guess and an extra pass.

## Cross-cell context

- **Dependencies travel as contract surface**: a later cell receives its dependency's delivered interfaces, exported types, endpoints, PR reference, and merge state as a digest — never re-derives a dependency's implementation.
- **Same-wave siblings** receive the agreed stubs and interface names (contract-first), not each other's code.
- **A rework** receives the cell charter by path plus the prior round's findings **inline**; implemented steps are never re-derived or re-read.
- **A resumed cell** receives the index state, the active plan/rework path, and what was already completed — never a from-scratch brief.

## Completeness check before dispatch

Run on every brief; a failed check stops the dispatch:

- Every inventory item has a home — nothing dropped for being findable.
- Every path is absolute and carries its section anchor; the branch and repo root are named.
- The callee's intake fields are filled.
- A digest is present wherever the orchestrator holds a conclusion (L0/L1 answer, gate verdict, recorded read).
- Any cell whose dependency is planned or done carries that dependency's contract surface.
