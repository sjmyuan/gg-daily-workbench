# gg-daily-workbench
A collection of agents and skills used in my daily work

## Installing agents & skills

Use [`install-agents-skills.sh`](./install-agents-skills.sh) to install the
agents and skills in this repo into a workspace or your user profile for
**Copilot** (VS Code), **OpenCode**, and/or **Claude Code**:

```sh
./install-agents-skills.sh <target> <platform> [options]

# Install everything for all three tools into your user profile
./install-agents-skills.sh user all

# Install claude agents + skills into a specific project
./install-agents-skills.sh workspace claude --project ~/work/my-app

# Preview what would happen without changing anything
./install-agents-skills.sh user all --dry-run
```

- `<target>`: `user` | `workspace`
- `<platform>`: `copilot` | `opencode` | `claude` | `all`
- Options: `--project <path>` (workspace), `--scope agents|skills|all`,
  `--force`, `--dry-run`

Agents and skills are **symlinked as whole folders** into place (never copied),
so the repo remains the source of truth — `git pull` here updates every
installed agent and skill automatically. Targets already linked to this repo
are left alone; use `--force` to replace an existing target (e.g. a file copied
by an earlier version) with a link.

Source folders (linked whole): `copilot-agents/`, `opencode-agents/`,
`claude-agents/` for agents; `skills/` for skills.

## Project precedence: these skills are the fallback

These skills and agents are the general-purpose layer. A project's own copy for
the same task wins — same name or different — and this repo's copy is what
applies when the project has none.

### What each platform does on a name collision

| Platform | Skills | Agents |
|---|---|---|
| opencode | By ID, **last write wins** (`config/plugin/skill.ts:152-157`). Load order ends with the project, nearest ancestor last (`config.ts:368-378`, `config/discovery.ts:81,144-151`), so a project skill with the same ID **replaces** this copy — it is not a lower-priority fallback, the workspace text is gone. | By ID, **field-by-field merge** (`config/plugin/agent.ts:75-107`, `agent.ts:80-85`). Only declared fields override; `permissions` append and the last matching rule wins, so an omitted `permissions` block silently inherits these grants. |
| Claude Code, Copilot | Verify per install; do not rely on shadowing. | Same. |

Two consequences shape the policy:

- **Override by ID is free but total.** A project copy that shares a name must be
  complete, or the half it omits has no fallback to fall back to.
- **Differently-named equivalents are not resolved by any loader.** Both are
  listed, and the choice is made from `description` text alone — hence the
  clauses below.

### Override mode by the skill's purpose

| Skill purpose | Project copy should | Why |
|---|---|---|
| Produces or judges project artifacts — `conduct-spike`, `orchestrate-feature-delivery`, `plan-development-task`, `execute-plan`, `document-findings`, `write-solution-doc`, `draft-adr`, `resolve-artifact-location`, `resolve-conventions`, `create-pull-request`, `maintain-doc`, `review-code`, `investigate-code`, `question-everything`, `create-skill`, `review-skill`, `learn-from-history`, `craft-prompt`, `fan-out-agents`, `develop-miniprogram`, `draft-user-story` | **Same ID, complete file** | The project owns the templates, gates, and folder layout; a partial copy is worse than none. |
| Adds criteria to one of the above without replacing the workflow | **Distinct ID** (`acme-review`), named from the project's instruction file | Both stay visible; forking a body into a project drifts forever. |
| Language, media, and ideation — `correct-english`, `translate-en-cn`, `write-blog`, `draw-mermaid-diagrams`, `edit-svg`, `brainstorm-ideas`, `design-algorithm`, `clarify-request` | Leave alone, or override by ID if the project truly differs | No project-specific equivalent exists; a clause would only dilute the trigger. |

### How the rule is carried

- **`description` clause** — the 21 artifact skills above carry the sentence
  `Prefer the project's own equivalent when one exists.` immediately before their
  `Use when …` trigger, so the trigger stays last. It states precedence without
  adding trigger verbs. Check coverage with
  `grep -L "project's own equivalent" skills/*/SKILL.md`; the 8 language and
  ideation skills are expected in that output.
- **Agent context** — every agent in `opencode-agents/` and `claude-agents/`
  carries the same `**Resolution**` bullet in its `<project-context>` block, and
  every `copilot-agents/` agent carries the equivalent `<rule>`: a project skill
  or agent for the same task wins, under any name, and the agent plus the skills
  it applies are the fallback. It sits beside the existing `**Precedence**`
  bullet because it answers a different question — project-vs-workspace, not
  instructions-vs-agent.
- **Dispatch** — no agent declares a `subagent` permission. `mode` decides what
  can be dispatched: the subagent tool rejects a `primary` target
  (`tool/plugin/subagent.ts:142`) and enforces a depth limit (`:136`), so any
  `subagent` or `all` agent is reachable, including one the project defines.
  What `mode` cannot do is keep a *specific* agent out. With no matching rule the
  action resolves through the agent's base `{ action: "*", resource: "*" }` allow
  (`schema/src/agent.ts:39-50`), so dispatch is silent unless a project or global
  rule narrows it.

### Verifying which copy won

`OPENCODE_LOG_LEVEL=debug` logs `skill source loaded` with each source and its
resolved IDs (`config/plugin/skill.ts:140-145`). A shadowed skill simply stops
appearing; opencode has no `skills` listing command.

## opencode-agents

Opencode-format copies of the agents in [`claude-agents/`](./claude-agents/).
Each file uses native **OpenCode V2** frontmatter per the
[V2 agents guide](https://opencode.ai/v2/docs/agents/) — no V1 fields
(`permission`, `tools`, `name`, `prompt`, `maxSteps`) remain.

> This folder is symlinked as a whole into `.opencode/agents` (or
> `~/.config/opencode/agents`) by `install-agents-skills.sh`, so it must contain
> **only** agent files — that is why this documentation lives here rather than
> as a `README.md` inside the folder.

### Files

| Agent | Purpose | Applies skill(s) |
|---|---|---|
| `algorithm-assistant.md` | **Primary** — conversational algorithm design assistant that clarifies, explores cases, brainstorms, explains, and designs algorithms bilingually | `design-algorithm` |
| `blog-assistant.md` | **Primary** — conversational blog-writing assistant that gathers ideas, fills gaps, and maintains the article document | `write-blog` |
| `english-corrector.md` | **Primary** — corrects English grammar, spelling, punctuation, and style while preserving meaning, tone, and format | `correct-english` |
| `translator.md` | **Primary** — translates text and Markdown blog posts between English and Chinese, preserving formatting and adapting idiom | `translate-en-cn` |
| `user-story-writer.md` | **Primary** — conversational user-story writer that drafts, refines, and updates user stories (incl. Jira/Azure DevOps) | `draft-user-story` |
| `prompt-engineer.md` | **Primary** — crafts and refines effective prompts and agent files by applying the SKR framework | `craft-prompt` |
| `skill-creator.md` | **Primary** — creates, edits, and reviews skills (SKILL.md) by applying the create-skill / review-skill workflows | `create-skill`, `review-skill` |
| `adr-writer.md` | Draft Architecture Decision Records | `draft-adr` |
| `code-investigator.md` | **Primary** — read-only codebase investigation | `investigate-code` |
| `code-reviewer.md` | **Primary** — read-only code review | `review-code` |
| `executor.md` | Execute an existing plan (never plans) | `execute-plan` |
| `learner.md` | Extract knowledge from history (self-dispatch for parallelism) | `learn-from-history` |
| `orchestrate-delivery.md` | **Primary** — delivery orchestrator: reads and reasons in-session, dispatches the plan/execute/spike/ADR/solution-doc sub-agents, tracks the delivery index | `orchestrate-feature-delivery` |
| `planner.md` | Diagnose the change, choose its evidence, and persist a plan an executor can run (never executes) | `plan-development-task`, `investigate-code` |
| `findings-doc-writer.md` | Compile question-style findings docs (resource index, topic blocks, `file:line` evidence ledger) | `document-findings` |
| `solution-doc-writer.md` | Compile solution documents (C4, sequence, RAID/RACI) | `write-solution-doc` |
| `spike-area-analyst.md` | One spike area end to end — investigate to sufficiency, draft problem ADRs, gate each ADR — in one session | `investigate-code`, `draft-adr` |
| `spike-conductor.md` | **Primary** — run decision-first spikes, dispatch area sessions at scale, verify results | `conduct-spike`, `question-everything` |
| `svg-assistant.md` | Create, edit, and upgrade PPT-quality SVG diagrams | `edit-svg` |

### Opencode V2 agent contract (summary)

- One markdown file per agent; **the filename becomes the agent ID** (e.g. `code-reviewer.md` → `code-reviewer`). There is no `name:` field.
- `description` explains the purpose; opencode shows it to the model choosing a subagent.
- `mode`: `primary` | `subagent` | `all` — V2 defaults a new custom agent to `primary`. `algorithm-assistant.md`, `blog-assistant.md`, `english-corrector.md`, `orchestrate-delivery.md`, `prompt-engineer.md`, `skill-creator.md`, `translator.md`, and `user-story-writer.md` are `primary`; `code-investigator.md`, `code-reviewer.md`, and `spike-conductor.md` are `all` (usable as primary or dispatched); `adr-writer.md`, `executor.md`, `findings-doc-writer.md`, `learner.md`, `planner.md`, `solution-doc-writer.md`, `spike-area-analyst.md`, and `svg-assistant.md` are `subagent` (dispatch targets only).
- `permissions` is an **ordered list** of `{ action, resource, effect }` rules; the **last matching rule wins**, so broad rules precede exceptions.
- Action names are V2 strings: `read`, `edit`, `glob`, `grep`, `shell`, `subagent`, `skill`, `question`, `webfetch`, `websearch`, `external_directory`, MCP tools. `bash`, `task`, `write`, `patch` are V1 names; `list`, `lsp`, and `todowrite` are not V2 permission actions.
- The markdown body is the agent's system prompt.

### Permission rules in these files

Each agent declares its tool set explicitly — `read`, `glob`, `grep`, `edit`, `shell`, `webfetch`, `websearch`, and `skill` — so the frontmatter states the agent's access instead of leaving it to inherited defaults. `subagent` is deliberately left undeclared: `mode` decides who is dispatchable. `webfetch` and `websearch` are denied everywhere: no agent reaches the network.

| Agent pattern | Rules |
|---|---|
| Doc-only writers — `adr-writer`, `findings-doc-writer`, `planner`, `solution-doc-writer` | `edit *` deny, then `edit *.md` allow; everything else allowed |
| Read-only — `code-investigator`, `code-reviewer` | `edit *` deny; discovery, shell, skills allowed |
| Text-only — `english-corrector`, `translator` | `edit *` and `shell *` denied; discovery and skills allowed |
| Folder-scoped writers — `orchestrate-delivery` (`deliveries`), `spike-conductor` and `spike-area-analyst` (`spikes`) | `edit *` deny, then `edit */deliveries/*` allow (V1 `**/deliveries/**` translated literally; same for `spikes`), plus a `deliveries/*` / `spikes/*` allow for in-project paths |
| Dispatch — every agent | no `subagent` rule: `mode` decides (`primary` cannot be dispatched, `subagent` and `all` can); an unmatched action resolves through the base `*` allow |
| No network — **every** agent | `webfetch *` and `websearch *` deny |
| Full access — `executor`, `learner` | every action above allowed; `learner` also dispatches its own copies, which it reaches through `mode` |

- Per V2's base policy, actions not listed (`question`, `external_directory`, Code Mode's `execute`, MCP tools) remain allowed.

- Every rule carries `resource: "*"`. V2 requires all three fields and the patterns are whole-value wildcards, so `"*"` means "every path, query, or agent ID".
- Agent rules are appended **after** global rules, so an explicit `allow` here also wins over a stricter global `ask` — the same precedence the V1 `permission` map had. Narrow a rule in the file, not only in `opencode.jsonc`, when an agent must be restricted.
- `todowrite` and `lsp` are gone: V2 has neither as a permission action, and todos are off unless `experimental.todo: true` is set in `opencode.jsonc`.
- V2 allows `external_directory` by default; add `{ action: "external_directory", resource: "*", effect: "ask" }` globally to restore the V1 prompt.

### Work-dir adoption (target repo)

Adoption belongs to the **dispatching parent**, not to the agent doing the work. No agent in `opencode-agents/` carries a work-dir capability or moves its own session.

- **Why it matters**: V2 resolves skills, instructions (`AGENTS.md`), agent definitions, project config, shell cwd, and the internal/external file-access boundary from the **session location**, not from path arguments. A child starts at its parent's location, so the parent must place it at the target repo.
- **Parent's job**: set the session location (via the dispatch `directory` argument, or `tools.opencode.session_move` in the parent's own call) before the unit starts work, and keep its own location when its `*/deliveries/*` and `*/spikes/*` rules must match the artifact base.
- **Child's job**: read the project context where it was placed, and report when that location is clearly the wrong repo instead of relocating itself.
- **Dispatched briefs**: name the target repo root absolutely so the child never has to guess between equally plausible repos.
- **Artifacts stay absolute**: the resolved base (often `my-work`, outside the repo) is written by absolute path. V2 wildcards compile `*` to `.*`, so `*/deliveries/*` and `*/spikes/*` still match an external absolute path.
- `claude-agents/` is unchanged: work-dir adoption is an opencode V2 concept (`tools.opencode.session_move`); Claude Code has no session work dir to switch.

### How the conversion was done

- Claude frontmatter (`name:` / `tools:` / `model: inherit`) → opencode `mode:` + `permissions:`; the Claude tool list maps to V2 actions: `Glob/Grep/Read` → `glob`/`grep`/`read`, `Write/Edit` → `edit`, `Bash/KillShell/BashOutput` → `shell`, `WebFetch` → `webfetch`, `WebSearch` → `websearch`, skill tool → `skill`.
- V1 → V2: `permission:` map → ordered `permissions:` list; `bash` → `shell`; `task` → `subagent`; `write`/`patch` → `edit`; `list`, `lsp`, `todowrite` dropped.
- Every V1 `allow`/`deny` was carried over 1:1 at conversion, including `executor` and `learner`, which previously listed no tools and now spell out their set (from their `claude-agents/` tool list and prior behavior). The `subagent` rules were removed afterwards: dispatch now follows `mode` alone, so a project-defined agent needs no allowlist entry.
- V1 path globs translate literally, one rule per V1 pattern: `"*": deny` + `"*.md": allow`, and `**/deliveries/**` → `*/deliveries/*` (both `*`s collapse to the same "any characters" wildcard). Every file is an exact permission translation — verified rule by rule against `git show HEAD`.
- Because V2 resolves in-project write paths as Location-relative, `*/deliveries/*` does not match `deliveries/<epic>/index.md` when the artifact base is the project root. That reproduces V1's behavior; to allow it, add `{ action: "edit", resource: "deliveries/*", effect: "allow" }` (after the deny) to `orchestrate-delivery.md`. The spike agents carry the equivalent `spikes/*` rule.
- Claude paths → opencode: `CLAUDE.md` → `AGENTS.md`, `.claude/agents/` → `.opencode/agents/`, `.claude/skills/` → `.opencode/skills/`, `.claude/rules/` → project instructions.

### Notes

- Skills must be discoverable by opencode (`.opencode/skills/<name>/SKILL.md`, `.claude/skills/`, `.agents/skills/`, or the matching global locations) for the `skill` tool to load them.
- Subagent dispatch tables (in `spike-conductor.md` and `learner.md`) reference agents by name — those names resolve to the other files in this folder once installed. With same-ID project overrides, that name resolves to the project's copy instead.
- Every agent in `opencode-agents/` **and** `claude-agents/` loads project context from **both** toolchains via **load-project-context**: instructions (`AGENTS.md`, `CLAUDE.md`), agents, skills, rules, and commands under `.opencode/` and `.claude/`, plus `.agents/skills/`. The path mapping above applies to frontmatter and the agent's own defaults, not to context discovery — a project set up for either tool wins over conflicting agent defaults. Neither toolchain's agents adopt a work dir themselves; the dispatching parent places each unit at the target repo (see above).

## Agent dispatch per platform

An agent that dispatches sub-agents must declare the capability in its frontmatter, or the dispatch silently fails on that platform:

| Platform | Mechanism | Declaration |
|---|---|---|
| opencode | agent `mode` — no permission rule | `mode: subagent` or `all` is dispatchable; `mode: primary` is rejected as a subagent target. No `subagent` rule means the base `*` allow applies, so dispatch does not prompt |
| Claude Code | `Task` tool (renamed `Agent`; `Task` remains an alias) | include `Task` (or `Agent`) in the comma-separated `tools:` list |
| VS Code Copilot | `agents` list + the `agent` tool | `agents: ['planner', ...]` (omit `tools` to keep all tools) |

Dispatching agents and their targets:

| Agent | Dispatches |
|---|---|
| `orchestrate-delivery` | code-investigator, planner, executor, code-reviewer, spike-conductor, adr-writer, solution-doc-writer |
| `spike-conductor` | spike-area-analyst, code-investigator, solution-doc-writer |
| `learner` | learner (self-dispatch) |
| `code-reviewer` | code-reviewer (fan-out) |
| `code-investigator` | code-investigator (fan-out) |

- **Self-dispatch / fan-out**: with no `subagent` rule, an agent can invoke itself; the depth limit is what stops recursion. VS Code Copilot still requires an `agents` entry and the `chat.subagents.allowInvocationsFromSubagents` setting for a self-referential dispatch.
- opencode V2 dispatches on `mode` alone; any `subagent` or `all` agent is a valid target, so a project-defined agent needs no edit to this repo. Only `spike-area-analyst` states "never spawn a sub-agent" in prose now — that is a rule the agent follows, not one the runtime enforces.
- Claude and Copilot still gate dispatch on a declared capability (`Task` in `tools:`, or the `agents` list); dropping those would disable dispatch rather than relax a rule. On Copilot a differently-named project agent must be added to `agents:` to be reachable.


## Skill self-containment

Every skill is installable on its own: each markdown link resolves **inside its own
skill folder**, and another skill is named, never deep-linked. Doctrine that several
skills need is duplicated as a scoped local slice, not shared by path.

["Skill doctrine registry"](./docs/skill-doctrine.md) maps each doctrine to its owning
copy and every mirror, so a change knows what to propagate.

```sh
# No link may leave its skill folder
python3 skills/review-skill/scripts/check_skill_links.py skills

# Same basename in several skills — a `differ` row is a slice to check against the registry
python3 skills/review-skill/scripts/check_skill_links.py --duplicates skills
```
