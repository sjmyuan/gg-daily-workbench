# Example: Curating a Planning Workbook into a Cell Charter

**Scenario**: A planner has drafted `context.md` for a feature cell. The draft is 182 lines and
mixes background, plan rationale, investigation evidence, and execution history. The user asks:
"This doesn't tell me anything I need — what should actually be in it?"

**Applies**: **doc-budgets** · **export-plan**

## 1. Triage every section

| Draft section | Verdict | Destination |
|---|---|---|
| Takeaway (50-word sentence) | Rewrite | `Outcome` — one line |
| Why this cell exists | Keep, compress | `Why` — ≤3 lines |
| The corrected mechanism | Plan rationale | `plan.md` §Plan decisions (PD8) |
| Install-aware filter table | Implementation detail | `plan.md` steps + code |
| Hard constraints (user-cut) | Keep | `Must hold` |
| Plan decisions PD1–PD12 | Duplicate | `plan.md` §Plan decisions — delete |
| TDD rationale | Duplicate | `plan.md` §TDD variant — delete |
| Grounded pre-flight findings (32 lines) | Investigation | Resolved → plan decision; unresolved → `Unknowns`; raw table deleted |
| Success criteria → verification | Keep | `Done means` |
| Constraints for the executor | Keep | `Must hold` |
| Spike References (12) | Keep, trim | `Pointers` — cell-specific only |
| Reworks manifest | Keep | `Reworks` |
| Execution (72 lines) | History | `## Execution` latest only; git/PR are the history |

Rule: **pre-flight findings are not context**. A finding that changed the plan is already a
plan decision; a finding that still matters is an Unknown; the rest is noise.

## 2. Resulting charter

```markdown
# Context: F2 skill-auto-discovery-plugin — installed-only skill registration

**Outcome:** installed Claude cache/marketplace skills register through one transform;
uninstalled plugins stay invisible.

## Why
Native discovery misses the Claude plugin cache/marketplace (F1 POC MR).
One config line reaches it but over-registers uninstalled plugins; install-aware filtering
is the differentiator. Option 3 adopted 2026-10-16 — do not re-litigate.

## Must hold
- V2-only (`v2.0.26`); no npm, Superpowers, embedding, or extra dependencies.
- No branch: small-step local commits on `main`; push needs the user.
- Never write `~/.config/opencode/**`; never touch the `:8888` service.

## Unknowns
- Setup-time snapshot may be incomplete → Step 5 measures; Step 6 contingency.
- F1 §4 row 3 (added skills unadvertised) did not reproduce → Step 9 stops if it recurs.
- No type-check exists → PD11 field set validated at runtime only.

## Done means
| Criterion | Verification | Pass rule |
|---|---|---|
| Installed skills register | `skill.list` | both present |
| Uninstalled stay absent | `skill.list` | both absent |
| No native shadowed | `uniq -d` | empty |
| Model-visible | `<available_skills>` | both announced |

## Pointers
- ADRs: `adr-plugin-port-01`, `adr-plugin-port-02`
- Evidence: F1 POC MR
- POC context: `../v2-skill-source-probe/context.md`

## Open concerns
- Precedence is the safety net, not the skip → verified by Step 9's shadowing assertion.

## State
| Field | Value |
|---|---|
| Active plan | `plan.md` · `rework-2026-10-16.md` |

## Execution
| Field | Value |
|---|---|
| Status | `DONE_WITH_CONCERNS` |
| Commits | `7ce6c4f..136a9b5` |
| PR | pending approval |
| Test evidence | `node --test` 11/11 pass |
| Review outcome | clean; 2 Major fixed |

## Reworks
| Date | Mode | Cell | Trigger | File | Status |
|---|---|---|---|---|---|
| 2026-10-16 | pre-merge | F2 | gate round 2: F-1, F-2 | rework-2026-10-16.md | done |
```

## 3. What changed

| Metric | Draft | Charter |
|---|---:|---:|
| Lines | 182 | 54 |
| Chars | 21,749 | ~1,900 |
| Duplicated plan content | 8 lines | 0 |
| Pre-flight evidence | 32 lines | 0 |
| Execution history | 72 lines | 6 rows |

Nothing needed to execute is lost: the mechanism and decisions are in `plan.md`; the feature
state is in `index.md`; git and the PR are the history; the charter keeps only why, invariants,
unknowns, done criteria, pointers, concerns, and state.

## 4. Responsibility check

| Artifact | Answers | Holds |
|---|---|---|
| `index.md` | Where is the epic now? | feature rows, waves, cell status |
| `context.md` | Why, what must hold, what is unknown, how done is judged | charter + latest handoff |
| `plan.md` | How, in what order | scope, TDD, decisions, steps |
| `rework-<date>.md` | What changed after delivery | delta steps + fix criteria |
| Git / PR / CI | What happened, and can it be reproduced? | commits, diff, test logs |
