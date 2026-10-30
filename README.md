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
| `orchestrate-delivery.md` | **Primary** — delivery orchestrator that dispatches the plan/execute/spike/ADR/solution-doc sub-agents and tracks the delivery index | `orchestrate-feature-delivery` |
| `planner.md` | Produce + persist a TDD plan (never executes) | `plan-development-task`, `investigate-code` |
| `findings-doc-writer.md` | Compile question-style findings docs (resource index, topic blocks, `file:line` evidence ledger) | `document-findings` |
| `solution-doc-writer.md` | Compile solution documents (C4, sequence, RAID/RACI) | `write-solution-doc` |
| `spike-conductor.md` | **Primary** — orchestrate spike investigations + verify sub-agent results | `conduct-spike`, `question-everything` |
| `svg-assistant.md` | Create, edit, and upgrade PPT-quality SVG diagrams | `edit-svg` |

### Opencode V2 agent contract (summary)

- One markdown file per agent; **the filename becomes the agent ID** (e.g. `code-reviewer.md` → `code-reviewer`). There is no `name:` field.
- `description` explains the purpose; opencode shows it to the model choosing a subagent.
- `mode`: `primary` | `subagent` | `all` — V2 defaults a new custom agent to `primary`. `algorithm-assistant.md`, `blog-assistant.md`, `english-corrector.md`, `orchestrate-delivery.md`, `prompt-engineer.md`, `skill-creator.md`, `translator.md`, and `user-story-writer.md` are `primary`; `code-investigator.md`, `code-reviewer.md`, and `spike-conductor.md` are `all` (usable as primary or dispatched); `adr-writer.md`, `executor.md`, `findings-doc-writer.md`, `learner.md`, `planner.md`, `solution-doc-writer.md`, and `svg-assistant.md` are `subagent` (dispatch targets only).
- `permissions` is an **ordered list** of `{ action, resource, effect }` rules; the **last matching rule wins**, so broad rules precede exceptions.
- Action names are V2 strings: `read`, `edit`, `glob`, `grep`, `shell`, `subagent`, `skill`, `question`, `webfetch`, `websearch`, `external_directory`, MCP tools. `bash`, `task`, `write`, `patch` are V1 names; `list`, `lsp`, and `todowrite` are not V2 permission actions.
- The markdown body is the agent's system prompt.

### Permission rules in these files

Each agent declares its tool set explicitly — `read`, `glob`, `grep`, `edit`, `shell`, `webfetch`, `websearch`, `skill`, and `subagent` — so the frontmatter states the agent's access instead of leaving it to inherited defaults:

| Agent pattern | Rules |
|---|---|
| Doc-only writers — `adr-writer`, `findings-doc-writer`, `planner`, `solution-doc-writer` | `edit *` deny, then `edit *.md` allow; everything else allowed |
| Read-only — `code-investigator`, `code-reviewer` | `edit *` deny; discovery, shell, web, skills allowed |
| Text-only — `english-corrector`, `translator` | `edit *`, `shell *`, `webfetch *`, `websearch *` denied; discovery and skills allowed |
| Folder-scoped writers — `orchestrate-delivery` (`deliveries`), `spike-conductor` (`spikes`) | `edit *` deny, then `edit */deliveries/*` allow (V1 `**/deliveries/**` translated literally; same for `spikes`) |
| Dispatch-restricted — `orchestrate-delivery`, `spike-conductor` | `subagent *` deny, then one `subagent <id>` allow per target |
| Web search off — six writing/authoring agents | `websearch *` deny |
| Full access — `executor`, `learner` | every action above allowed; `learner` also allows `subagent` for self-dispatch |

- Per V2's base policy, actions not listed (`question`, `external_directory`, Code Mode's `execute`, MCP tools) remain allowed.

- Every rule carries `resource: "*"`. V2 requires all three fields and the patterns are whole-value wildcards, so `"*"` means "every path, query, or agent ID".
- Agent rules are appended **after** global rules, so an explicit `allow` here also wins over a stricter global `ask` — the same precedence the V1 `permission` map had. Narrow a rule in the file, not only in `opencode.jsonc`, when an agent must be restricted.
- `todowrite` and `lsp` are gone: V2 has neither as a permission action, and todos are off unless `experimental.todo: true` is set in `opencode.jsonc`.
- V2 allows `external_directory` by default; add `{ action: "external_directory", resource: "*", effect: "ask" }` globally to restore the V1 prompt.

### How the conversion was done

- Claude frontmatter (`name:` / `tools:` / `model: inherit`) → opencode `mode:` + `permissions:`; the Claude tool list maps to V2 actions: `Glob/Grep/Read` → `glob`/`grep`/`read`, `Write/Edit` → `edit`, `Bash/KillShell/BashOutput` → `shell`, `WebFetch` → `webfetch`, `WebSearch` → `websearch`, skill tool → `skill`.
- V1 → V2: `permission:` map → ordered `permissions:` list; `bash` → `shell`; `task` → `subagent`; `write`/`patch` → `edit`; `list`, `lsp`, `todowrite` dropped.
- Every V1 `allow`/`deny` is carried over 1:1, including `executor` and `learner`, which previously listed no tools and now spell out their set (from their `claude-agents/` tool list and prior behavior).
- V1 path globs translate literally, one rule per V1 pattern: `"*": deny` + `"*.md": allow`, and `**/deliveries/**` → `*/deliveries/*` (both `*`s collapse to the same "any characters" wildcard). Every file is an exact permission translation — verified rule by rule against `git show HEAD`.
- Because V2 resolves in-project write paths as Location-relative, `*/deliveries/*` does not match `deliveries/<epic>/index.md` when the artifact base is the project root. That reproduces V1's behavior; to allow it, add `{ action: "edit", resource: "deliveries/*", effect: "allow" }` (after the deny) to `orchestrate-delivery.md`.
- Claude paths → opencode: `CLAUDE.md` → `AGENTS.md`, `.claude/agents/` → `.opencode/agents/`, `.claude/skills/` → `.opencode/skills/`, `.claude/rules/` → project instructions.

### Notes

- Skills must be discoverable by opencode (`.opencode/skills/<name>/SKILL.md`, `.claude/skills/`, `.agents/skills/`, or the matching global locations) for the `skill` tool to load them.
- Subagent dispatch tables (in `spike-conductor.md` and `learner.md`) reference agents by name — those names resolve to the other files in this folder once installed.
- Every agent in `opencode-agents/` **and** `claude-agents/` loads project context from **both** toolchains via **load-project-context**: instructions (`AGENTS.md`, `CLAUDE.md`), agents, skills, rules, and commands under `.opencode/` and `.claude/`, plus `.agents/skills/`. The path mapping above applies to frontmatter and the agent's own defaults, not to context discovery — a project set up for either tool wins over conflicting agent defaults.

## Agent dispatch per platform

An agent that dispatches sub-agents must declare the capability in its frontmatter, or the dispatch silently fails on that platform:

| Platform | Mechanism | Declaration |
|---|---|---|
| opencode | `subagent` permission allowlist | `{ action: "subagent", resource: "*", effect: "deny" }` then `{ action: "subagent", resource: "<agent>", effect: "allow" }` |
| Claude Code | `Task` tool (renamed `Agent`; `Task` remains an alias) | include `Task` (or `Agent`) in the comma-separated `tools:` list |
| VS Code Copilot | `agents` list + the `agent` tool | `agents: ['planner', ...]` (omit `tools` to keep all tools) |

Dispatching agents and their targets:

| Agent | Dispatches |
|---|---|
| `orchestrate-delivery` | code-investigator, planner, executor, code-reviewer, spike-conductor, adr-writer, solution-doc-writer |
| `spike-conductor` | code-investigator, findings-doc-writer, adr-writer, solution-doc-writer |
| `learner` | learner (self-dispatch) |
| `code-reviewer` | code-reviewer (fan-out) |
| `code-investigator` | code-investigator (fan-out) |

- **Self-dispatch / fan-out**: opencode and Claude allow an agent to invoke itself; a V2 `subagent *` deny blocks it, so self-dispatching agents must allow their own ID. VS Code Copilot requires the `chat.subagents.allowInvocationsFromSubagents` setting for a self-referential `agents` entry.
- opencode V2 allows unspecified actions by default; explicit `subagent` allowlists exist only where dispatch is restricted (`orchestrate-delivery`, `spike-conductor`).


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
