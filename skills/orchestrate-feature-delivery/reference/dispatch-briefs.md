# Dispatch Briefs (Delivery)

Backs **agent-dispatch**, **orchestrate-delivery**, **resume-delivery**, **verify-cell**, and **triage-issue**.
Every dispatched unit — planner, executor, verifier, investigator, spike conductor, ADR or solution-doc writer — receives a brief built from this contract.
Cell-level content (feature, repo, scope, branch, plan location) is owned by **reference/delivery-index-format.md** (per-cell scope brief); this file owns how all known context reaches the agent.

## Why it matters here

A brief that names only paths sends the agent back through the spike artifacts, the record, and the code to rediscover what is settled — at full cost, in a context that cannot report it back.
The opposite failure costs the same: a brief that carries everything makes every dispatch pay to compose, send, and re-read facts that change nothing. **Both are brief defects.**

## Brief budget

| Brief | Cap | When over |
|---|---|---|
| Plan · execute · verify | ≤40 lines / 2,500 chars | Move the detail into the cell's `context.md`; pass the path |
| Repair round (`Fix class: mechanical`) | ≤12 lines | Keep the labelled findings inline; drop what the plan already states |

- The brief is a **delta**: the index cell row + the plan or rework path + what changed this round. `plan.md` and `context.md` are opened, never restated.
- Compose **once per cell**; each dispatch changes only its delta.
- Hard fields never leave the brief: absolute paths, intake fields, gate tier, `Fix class`, `Mode`/`Push`, the dependency contract surface.

## What earns a place

An item enters only if it can change this unit's next action. In order:

1. Would the agent act differently without it? No → leave it out; a path in `context.md` covers discovery.
2. Is it already in a file the agent opens (`plan.md`, `context.md`, the ADR, the index row)? → a path and anchor, never prose.
3. Can the agent not open it (a prior verdict, a settled user answer, a merged cell's contract surface)? → a digest.
4. Does it belong to another cell's dispatch? → not this brief's business.

**Nothing irrelevant**, not "nothing missing", is the test. A missing hard field fails the check; a missing nicety does not.

## Three fill modes

| Mode | Use when | Filled as |
|---|---|---|
| **Path** | The item is persisted and the agent needs its full detail | Absolute path + section anchor |
| **Digest** | The fact cannot be opened, or the conclusion differs from the file's text | 1–5 lines, marked `from <path#section>` |
| **Inline** | It lives only in conversation, or the agent must write it into its output | The value itself |

- **Digest is the anti-re-investigation mode** for what cannot be read: located `file:line`, a gate verdict, a settled decision, a delivered contract surface.
- **A digest never accompanies a path the agent will read** — that is double payment; the path alone suffices.
- **Persist-once**: context several later dispatches need goes into the cell's `context.md` (planner-owned) or the index cell brief, then travels as a path.

## Context per dispatch target

| Target | Beyond the cell brief | Mode |
|---|---|---|
| **planner** | Drivers and constraints, dependency contract surface, known locations, acceptance assumptions, the review budget | Digest + inline |
| **executor** | Plan path, base ref, active `rework.md`, branch, prior-round findings, gate tier, `Fix class` on a repair round, push mode | Path + inline |
| **verifier** | Cell digest (done means, decided behaviour), recorded `base7..head7`, ADR path + decision digest, prior verdicts | Digest + inline |
| **L1 investigator** | The question, what the record already established, known locations, already-searched | Digest |
| **spike conductor (L3)** | Delta scope, the trigger that chose L3, prior artifacts and the findings they cover | Path + digest |
| **code-analyst (`adr-rewrite` / `findings`) / solution-doc-writer** | Decision digest, affected sections, governed cells, the `Output` mode | Digest + path + mode |

## Self-locating brief

- **Absolute paths** for the feature folder, `plan.md`, `rework.md`, governing ADR, solution-doc section.
- **Repo root, base ref, branch** — the executor must not re-detect the epic folder or the branch convention; the planner must not search for the feature folder.
- **`Mode: delivery`** — every dispatched planner and executor carries it. It forbids the interactive ritual: no user question, no plan quiz, no ratification pause, no per-cell push prompt. A planner persists and returns the path with its three-line risk report; an executor returns the branch and commit range. A question the record cannot settle returns as `NEEDS_CONTEXT` with options — never blocks on the user.
- A sub-agent searching the filesystem for its inputs or re-detecting the repo's conventions is a brief defect, not agent behaviour.

## Callee intake records

Dispatched skills run their own intake gate and refuse to act on a private reading. Feed the gate:

| Agent | Fields it gates on |
|---|---|
| **planner** | Change type, expected behavior, triggering input, done criteria (plus the ref, for a restore) |
| **executor** | Plan path, active rework file, base ref, expected outcome |
| **code-analyst (`investigate`, L1)** | System, scope, depth, consumer |
| **spike-conductor (L3)** | Spike goal, affected areas or delta scope, boundaries, brownfield/greenfield |

A brief carrying these fields **is** the gate result: the agent adopts them, asks nothing, and explores only what they leave open. An unfilled field becomes the agent's guess and an extra pass.

## Cross-cell context

- **Dependencies travel as contract surface**: interfaces, exported types, endpoints, PR reference, merge state — as a digest. Never the dependency's implementation.
- **Same-wave siblings** receive the agreed stubs and interface names (contract-first), not each other's code.
- **A rework** receives the charter by path plus the prior findings **inline**; implemented steps are never re-read.
- **A resumed cell** receives the index state, the active plan/rework path, and what was completed — never a from-scratch brief.

## Completeness check before dispatch

Run on every brief; a failed hard field stops the dispatch:

- Every item that can change this unit's action is present; nothing else is.
- Within budget: ≤40 lines; a repair round ≤12.
- Paths are absolute with anchors; the repo root and branch are named.
- The callee's intake fields are filled.
- `Mode: delivery` is stated; push handling is `Push: batched` unless the user asked per cell.
- The gate tier is stated (`Full`/`Sampled`), and the executor is told an independent gate follows — self-check only, no `review-code` pass.
- A repair dispatch states `Fix class: mechanical` and carries the labelled findings inline; a design round names the `rework.md` path.
- The resolved agent and its role skill are named — a default agent standing in for a role never arrives unlabeled.
- Any dependency that is planned or done carries its contract surface.
