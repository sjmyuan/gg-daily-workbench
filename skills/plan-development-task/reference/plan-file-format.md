# Plan File Format and Template

Single template for every plan this skill generates. **execute-plan** consumes the step block
unchanged — its `step-tracking-format.md` mirrors this template. Never invent a variant.

One artifact, one job: `index.md` = state · `context.md` = charter · `plan.md` = execution ·
`rework-<date>.md` = delta · git/PR = record. Budgets: **doc-budgets**.

## plan.md template

```markdown
# Plan: <feature-name> — <outcome in one line>
**Type**: bug-fix | feature | refactor | poc | restore
**Branch**: `<branch>` off `<base>`
**Test strategy**: test-first | characterization-first | type/config-only | none (mechanical) — <one-line why it fits; name the unit that departs>
**Gate**: build=`<cmd>` · test=`<cmd>` · lint-type=`<cmd>`
**Gate waiver**: <scope> — <named failures> — ratified by <user> on <date>   (only when ratified)
**ADR**: `adr-<name>.md` · **Option**: <option>            (POC only)
**Success criteria**: <user review checklist>            (POC only, optional)

## Scope Boundary
**May change**: <observable behaviors and contracts this plan may alter>
**Must match**: <path> @ <pinned ref>                    (restore/port only)
**Expected files**: <likely files> (advisory)
**Must not change**: <observable behaviors and contracts to preserve>
**Protected zones**: <additions to the default set, or "none added">

## Risk
- <assumption the code will test> → <step that tests it or the fallback>
- **Expected to break first**: Step N — <why>

## Decisions
- <decision> — <reason>                                  (only when context.md points to it)

## Steps

### Step 1: Prepare environment ⏳
**Objective**: <one sentence: what the step achieves>
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: <branch, dirt, and dependency checks>
**Validation**: <the gate commands from `Gate` run on the base — `baseline: green` or named failures>
**Status**: ⏳ Pending

### Step 2: <step title> ⏳
**Objective**: <one sentence>
**Files**: <created, modified, or deleted files>
**Source**: <no-op|base|port|copy|edit|generate> · <pinned ref, origin path, or n/a> · <equality mode>
**Implementation**: <approach in prose — one line; never code>
**Validation**: <test or equality proof — one line>
**Status**: ⏳ Pending

### Step N: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `<build>` && `<test>` && `<lint-type>` — all exit 0, zero failures.
**Status**: ⏳ Pending
```

`**Status**` carries the record: the executor appends its one-line outcome there — receipt, counts,
or a deviation. What landed is the commit and its diff; never restate it in `plan.md`.

## Template rules

| Element | Rule |
|---|---|
| Title | `# Plan: <feature> — <outcome>`; one line. |
| Metadata | `Type` (`bug-fix` · `feature` · `refactor` · `poc` · `restore`); `Branch` as `<branch>` off `<base>`; `Test strategy` (`test-first` · `characterization-first` · `type/config-only` · `none (mechanical)`) + why it fits; `ADR`/`Option`/`Success criteria` only for POC. |
| Gate | One `**Gate**` line — `build=` · `test=` · `lint-type=`, each evidence-backed (`file:line`); monorepos repeat the line per module. `**Gate waiver**` only when user-ratified (see **exit-gate**). |
| Order | Title → metadata → `## Scope Boundary` → `## Risk` → `## Decisions` (optional) → `## Steps`. |
| Scope Boundary | Zone order fixed per **scope-boundary**; write `Protected zones: none added` when nothing is added. |
| Steps | One `### Step N: <title> <status>` block per step, in file order; all six field lines, in order. |
| Objective | One sentence, ≤20 words, imperative. |
| Files | Concrete paths where known; `none` for no-edit steps. |
| Source | Every step names `Source · Ref · Equality` per **change-provenance** — `no-op · n/a · n/a` when nothing changes; `generate` states its justification in `Implementation`, ratified when the user confirms the plan. |
| Implementation | The **approach** in prose — which seam moves, what behavior results — one line. Never source code, a diff hunk, a signature, a file dump, or a TODO list; the only literals are a git operation for `base`/`port` or a path or identifier. Frozen — the executor never rewrites it. |
| Validation | Behavioral or `Must match` equality; the exit gate's pass rule is every gate command exit 0 — never a commit hash. |
| Status | Generated plans use `⏳`; the executor owns `🔄 ✅ ❌ 🚫`; the planner sets `⏭` only. `**Status**` is canonical — the heading glyph mirrors it. |
| Step shape | A step is a **unit with one verdict**, never a phase. Test, implement, refactor, and cleanup fold into the unit they serve; a step earns existence only when its `Validation` differs from its neighbour's. |
| Open by design | A step whose shape depends on unread code states the check that closes it plus a fallback, and appears in `## Risk` — never a guessed change. |
| Risk | Two or three assumptions, each naming the step that tests it; plus the step expected to break first. Six lines maximum. |
| Exit gate | Final step, six fields, `Source: no-op · n/a · n/a`; its `Status` line carries the receipt — commands, exit codes, and counts. Never abandoned or deferred — only a ratified waiver removes it. |
| Amendment | Append the next number or insert `3a`; never renumber (see **plan-amendment**). |

Not in `plan.md`: requirement narrative, background, consolidation prose, per-step rationale, issue history, "key characteristics", source code, diffs, snippets, signatures. Root cause → `context.md` **Why**; strategy rationale → the `Test strategy` line; decisions `context.md` must not restate → `## Decisions`; risk → `## Risk`.

## rework-<date>.md template

Written when executed behavior must change; `plan.md` stays frozen (see **rework-plan-convention**).

```markdown
# Rework <date> — <one-line trigger>
**Mode**: pre-merge | post-merge · **Cell**: <cell>
**Branch**: `<branch>` off `<base>`
**Test strategy**: <inherited from plan.md, or the strategy for the delta> — <one-line why>
**ADR focus**: `<adr path>`
**Gate**: <inherited from `plan.md`, or discovered for the delta>

## Scope Boundary
**May change**: <original May change, tightened or extended>
**Must match**: <path> @ <pinned ref>                    (restore/port only)
**Expected files**: <delta files> (advisory)
**Must not change**: <original Must not change, plus any tightened item>
**Protected zones**: <additions, or "none added">

## Done means
| Criterion | Verification | Pass rule |
|---|---|---|
| <delta criterion> | <test or diff check> | <pass rule> |

## Risk
- **Expected to break first**: Step N — <why>

## Steps

### Step 1: <delta step> ⏳
**Objective**: <one sentence>
**Files**: <files>
**Source**: <source> · <ref> · <equality>
**Implementation**: <delta approach in prose — one line; never code>
**Validation**: <proof — one line>
**Status**: ⏳ Pending
```

Rework step numbers restart at 1 in the rework file; the frozen `plan.md` numbering is untouched.
The file carries only the delta and inherits `context.md` by reference.

## context.md

The cell's charter — why, must-hold invariants, unknowns, done criteria, pointers, state.
Target **40–60 lines**; hard cap **8,000 chars / 120 lines**. Template, section order, and
admission test: **doc-budgets**.

Not in `context.md`: Scope Boundary, steps, TDD rationale, branch/base, plan decisions (all in
`plan.md`); feature status, wave, PR (`index.md`); pre-flight evidence, commit tables, test
matrices, deviations, incidents (git/PR are the history).

`## Execution` is written by **execute-plan**, latest round only — never appended.
Template and admission test: **[doc-budgets.md](doc-budgets.md)**.
