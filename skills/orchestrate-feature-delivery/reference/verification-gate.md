# Verification Gate

Backs the **verify-cell** capability and the `verified` status in `orchestrate-feature-delivery`.
The gate is independent and owns three questions: **did it build what was decided** (spec), **is the report true** (trust), and **is it good engineering** (quality). One reviewer answers all three; splitting them across two agents produces two half-verdicts and nobody saying "merge this".

## Division of labor

| Layer | Owns | Does not |
|---|---|---|
| **execute-plan** | Self-check of its own diff before hand-off, bounded to the changed files; in-boundary fixes | A second full quality review, spec re-derivation, or `review-code` when a gate follows |
| **verify-cell** (orchestrator) | Independent spec compliance, trust, **and quality**; bounded fix loop; breaker | Code changes; re-deriving the spec |

`execute-plan` runs the full **review-code** pass only when it executes standalone — with no gate behind it. In a delivery cell the independent gate is that review, and paying for both is a duplicated cost per cell per rework round.

## Risk-proportioned gate

Size the review to what the diff can break. State the tier in the cell brief.

| Tier | Trigger | Gate |
|---|---|---|
| **Full** | Delivered contract, public API, schema, migration, auth, money, data deletion, or another cell depends on it | Fresh **code-reviewer**; spec + trust + quality; diff read end to end |
| **Sampled** | Internal, additive, behind a stable interface, covered by tests | Fresh **code-reviewer**; spec + trust; quality sampled — the 2–3 riskiest files, plus every file the plan's `## Risk` names |

A cell that touches a protected zone is **Full** regardless of size. When the tier is arguable, take Full — the cost of a missed contract break exceeds a review round.

## Handoff contract

No separate files — the gate reuses the feature folder's existing docs (`<feature-folder>` = `deliveries/<epic-name>/<repo>/<feature-name>/`).

| Artifact | Location | Written by | Content |
|---|---|---|---|
| **Brief** | dispatch prompt — the index cell row + this round's delta | orchestrator | Cell scope, paths (plan, ADR, solution-doc section), the cell digest (done means, decided behaviour, assumptions), gate tier — within the **dispatch-briefs** budget |
| **Step record** | `<feature-folder>/plan.md` (or `rework.md`) | executor | Per-step status and notes; commit range lives only in the handoff |
| **Execution handoff** | `<feature-folder>/context.md` → `## Execution` (latest round only) | executor | Return status (`DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`), commit range (`base7..head7`), PR reference, **one-line** gate receipt, **one-line** self-check (`clean | fixed:<n>`) |
| **Open concerns** | `<feature-folder>/context.md` → `## Open concerns` | executor | Persistent ≤5 deferred Minors/risks; delete when resolved. No raw log — history is git/PR |
| **Diff** | fetched from git by the code-reviewer over the recorded `base7..head7` | code-reviewer | Commit list + stat + full diff; never enters the orchestrator's context |
| **Findings** | dispatch prompt → **planner**; recorded in `rework.md` | orchestrator → planner | Gate findings handed straight to the planner — not stored in the index |

- Seed the brief from the index cell row; `context.md` carries the cell charter and is passed by path, never restated.
- Carry the **cell digest** per **reference/dispatch-briefs.md**: done means, decided behaviour, accepted assumptions, the plan's step list, the plan's `## Risk`, and any located `file:line`.
  The verifier gates the diff against the decision as stated — it never re-derives the spec from the spike artifacts or re-investigates the code.
- Use **absolute paths** for the feature folder, `plan.md`, `context.md`, the governing ADR, and the solution-doc section; the verifier fetches the diff itself from the recorded range.
- `context.md` is **planner- and executor-owned** — the orchestrator never writes it; the planner registers the rework in `context.md`.
- The index tracks **status only** — no findings record.
- The executor **overwrites** `## Execution` each round; deferred concerns persist in `## Open concerns`; no log is written — git/PR are the history.
- A POC cell is verified exactly like any other cell. The gate checks the implementation; it never measures or judges the option — the user evaluates the MR.
- The gate result travels **inline** to the fix-round planner — the unresolved findings are not yet an artifact.
  Once recorded in the rework file — including its `Gate findings:` line — later rounds pass that file by **path**.

## Gate inputs

Dispatch a **fresh code-reviewer** agent (**review-code**) with: the cell brief, the cell digest, the recorded `base7..head7`, and the plan/context/ADR paths with anchors, the decision digest, and the gate tier.
Global constraints only when they change the verdict.
The intake record is already in the brief, so the review starts from the decision, not from discovery.
The code-reviewer fetches the diff from git over the recorded range — no diff file, and plan/context are opened, not pasted.
Never the executor instance that produced the work.

## Verdicts

1. **Spec compliance** — Missing / Extra / Misunderstood against the brief and governing ADR.
2. **Trust check** — verify the executor's claimed self-check and gate receipt against the diff.
   A receipt matching an earlier head is stale → back to the executor.
   Do not re-run the suite locally; sample the claimed Blocker/Major fixes.
   The gate is local — never wait for or poll a remote pipeline, nor treat pipeline status as the receipt.
3. **Quality** — Blocker / Major / Minor against the code itself, ending in one **merge recommendation**: merge · merge after the named fixes · do not merge.
   Judge what the diff changes, not the whole module. A Major is a defect a reviewer would block on; taste is a Minor.

Every Blocker and Major carries a **`mechanical`** or **`design`** label: mechanical changes no behaviour and stays inside the Scope Boundary; anything else is design. The label routes the fix, not its severity.

All three land in one verdict. A cell with clean spec, a true receipt, and a Major quality finding is **not verified**.

## Bounded fix loop

| Round | Action |
|---|---|
| Pass | Mark the cell **verified** via **update-delivery-index** |
| All labelled **mechanical** | One **executor** dispatch with the labelled findings inline and `Fix class: mechanical` — it repairs in place and records a `Gate repair:` line per finding in `## Execution`; then a scoped re-review |
| Any **design** finding | Dispatch the **planner** with every finding — it writes a sibling `rework.md` (mechanical ones ride along); then the **executor**; then a scoped re-review |
| Cap (2 rounds) | Stop and escalate to the user — the cell cannot reach **verified** with an unresolved gap |
| Recurs after round 1 | The finding is structural — escalate immediately instead of spending the second round |

Never silently discard a finding.

- The fix-round brief carries the prior round's **verification result** — each unresolved/new finding with its verdict and `mechanical`/`design` label — so the planner or executor works against what failed, never a blank re-run. The planner records it as the rework header's `Gate findings:` line.
- The scoped **re-review** receives the prior findings (inline) plus the new `rework.md` (path) — or, for a gate repair, the findings and their `Gate repair:` lines. It confirms each is resolved and re-checks only the changed scope.
- A design fix is a **rework** — planned then executed, never a direct executor edit. A mechanical fix is a **gate repair** — no behaviour change, inside the boundary, recorded as a `Gate repair:` line, never a second plan artifact.
- The cell stays **in-progress** through the rework; the `rework.md` file is the record of a design fix, `## Execution` the record of a gate repair — never the index.
- Roll deferred Minors into the epic integration review.

## Epic integration review

When all cells are **done**, run one cross-cell review + integration test pass over the epic — this is the one review the orchestrator may do in-session or delegate, and it is the place cross-cell contracts are judged.
Triage the deferred Minors from each cell's `context.md` `## Open concerns`; surface residual load-bearing findings to the user.
Per-cell gates do not cover cross-cell interaction.

## Dispatch discipline

- **Model**: choose the cheapest capable model per dispatch and state it explicitly; escalate a stuck fix round.
- **Agent**: resolve the role per **reference/orchestration-guide.md** → *Role resolution*; name the resolved agent and its role skill in the brief. A default-agent stand-in never gets a **Sampled** gate.
- **Gate tier**: state it in the brief; an unstated tier defaults to Full.
- **Wait**: wait in bounded stretches; reconcile live children; chase any that finished silently.
- **No subagents**: a dispatched worker never spawns reviewers or helpers — the orchestrator owns every review seat.

## Checklist

- [ ] `plan.md` (or `rework.md`) shows every step ✅ or ⏭, with the **Exit gate** last.
- [ ] `context.md` `## Execution` is the latest round only — status, commit range, PR, one-line gate receipt, one-line self-check.
- [ ] The gate receipt matches `head7`, or a user-ratified waiver is recorded.
- [ ] Gate tier stated and justified; Full for any protected zone or contract surface.
- [ ] code-reviewer fetched the diff over the recorded range, and is a fresh instance.
- [ ] All three verdicts present: spec compliance, trust, quality — with one merge recommendation.
- [ ] Fix loop within 2 rounds; a recurring or unresolved finding escalated.
- [ ] Fix findings dispatched to the planner; the `rework.md` file is the record.
