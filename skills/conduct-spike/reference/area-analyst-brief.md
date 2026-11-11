# Area-Analyst Brief

Ready-to-fill structured brief for a spike area → `spike-area-analyst` — the single session that investigates the area, compiles its findings pair, and drafts its problem ADRs. Loaded on demand when dispatching an area. Fills the **structured brief shape**; carries the shared context-inventory, fill-mode, intake-record, and session contracts: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching area [name] to a spike-area-analyst sub-agent (single return)."

One brief per area. Every path is absolute.

## 1. Mission
You are the `spike-area-analyst`. Deliver for **[area]** in one session and one return: its findings doc pair and one ADR per problem, in that order, then stop.

## 2. Context
- Spike goal **(path + digest)**: `<artifact-root>/spikes/<spike-name>/scope.md` — **[1–3 lines: the question to settle and what completion looks like]**
- Area: **[name]** — **[description]**
- Problems **(path)**: `scope.md` — this area's "How to …?" rows; one ADR each
- Boundaries **(inline)**: **[modules/files/teams inside; what is out of scope — name the sibling areas]**
- Accepted assumptions **(digest, from `scope.md#accepted-assumptions`)**: **[A<N> → assumed value]** — carry each into the ledger as 💭 Assumption and into any decision that depends on it
- User-stated context **(inline)**: **[business context, constraints, facts, decisions, and domain details the user already gave]**
- Mode: **brownfield** (trace code) | **greenfield** (research approaches + comparable systems; see **greenfield-scenarios**)
- Cross-area constraints **(path + digest)**: sibling pairs `docs/findings-*.md` + `docs/evidence-*.md`, decided sibling ADRs — **[each constraint in one line]**

## 3. Inputs
- Intake record **(inline)**: system **[...]** · scope **[...]** · depth **[...]** · consumer **[...]** — the gate is already passed; adopt it, do not re-derive it.
- Return **(inline)**: once, after phase 3 — the written pair and the ADRs together. No intermediate return.
- Known locations **(digest)**: **[symbols / files / entry points / `file:line` already located]** — start here; do not re-discover them.
- Already searched **(digest)**: **[query + root + outcome, including "no matches"]** — do not repeat any listed search.
- Findings pair **(path, re-dispatch only)**: **[`docs/findings-<area>.md`] + [`docs/evidence-<area>.md`]** — the verified pair supplied on a re-dispatch; treat **Verified** claims as settled.
- Prior receipt **(inline, re-dispatch only)**: **[the receipt returned by the earlier session]** — the session's durable state; inherit it instead of rebuilding.
- Sibling unit results **(path + digest)**: **[area → verified pair path, or decision]** — inherit these; never re-scan code a sibling already covered.
- Pre-existing user findings **(inline)**: **[notes/findings the user supplied]** — treat as known; when they answer the area, skip phase 1 and start at phase 2, verifying only what they leave unresolved.
- Decision drivers **(inline, mandatory)**: **[drivers the orchestrator collected from the user]** — the ADR needs these; never infer them. A driver absent here is a question for the orchestrator, not a guess.
- Candidate / rejected options **(inline)**: **[options named by the user or earlier rounds; options already ruled out and why]** — seed the option list; do not re-propose a rejected option as new.
- Open verification challenges **(re-dispatch only, inline)**: **[challenged claims, verdicts, what the verifier disputed]** — resolve each; leave everything else settled.

## 4. Tasks
1. Run **phase 1 — investigate** (skip when §3 supplies pre-existing findings that answer the area): apply `investigate-code`; trace to `file:line`; build the evidence map (entry points, call chains, ledger verdicts, searched-negatives). Do not return here — continue into phase 2 so the evidence is persisted.
2. Run **phase 2 — compile the pair**: apply `document-findings`; derive the area's 3–7 topic questions; write `docs/findings-<area>.md` then `docs/evidence-<area>.md` per the skill's capability order; validate the pair.
3. Run **phase 3 — draft the ADRs**: apply `draft-adr` headlessly — drivers from §3 → considered options → evaluation (`detail-options-tech` when needed) → compilation; one ADR per problem, tagged **Area:**.
4. Return once, after phase 3, with the pair paths and the ADR paths in one receipt — never between phases.
5. Ground what the artifacts leave open with targeted reads — a gap they raise, or an option's tech details they do not cover; every new location joins the ledger. Never repeat a listed search or re-verify a **Verified** claim.

## 5. Output contract
| Item | Return |
|---|---|
| Pair | Pair paths, the topic list (for the orchestrator to confirm), ledger claim count, pair validation result |
| ADRs | ADR paths, per-problem chosen option + one-line rationale, cited evidence IDs, assumption-dependent decisions |
| Flags | Gaps and inconsistencies; cross-area conflicts; new facts the pair lacks; a split request when the area exceeded one pass |

One return, after the ADRs. Every receipt also carries the area and the artifact paths, so a re-dispatch resumes from the artifacts without re-reading the conversation.

## 6. Constraints
- Write only this area's `docs/findings-<area>.md`, `docs/evidence-<area>.md`, and `adrs/adr-<area>-NN-<problem>.md`; never `scope.md`, `solution.md`, code, config, or tests.
- Never prompt the user — the orchestrator owns every confirmation and the ADR dialog.
- Never verify your own output and never spawn a sub-agent — the orchestrator owns the verification seat.
- Keep the artifact boundary: the human findings doc is current-state only; the ADR is decision only.
- Never return early — the pair and the ADRs leave together, written; a re-dispatch continues from them, not from a receipt.
- Never add claims beyond the evidence; never alter a **Verified** verdict or an evidence `file:line` without new evidence.
- Never re-derive scope, re-ask, or search for your inputs — this brief is the gate result.
- Complete the pair before drafting any ADR — the evidence doc is what every decision cites.

## 7. Report back
- Flag every **Gap** / **Inconsistency** the pair does not already record, and anything contradicting another area.
- Flag every decision resting on an accepted assumption, and every driver you had to infer.
- Return the search log so the next area inherits it.
- Request a split when the area cannot be covered in one pass; do not thin the evidence.
