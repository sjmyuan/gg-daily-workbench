# Script and CLI Policy

Used by **create-skill-scripts**, **validate-created-skill** (tooling step), and **review-skill-file** (tooling step).

Prefer a maintained CLI. Add a script only when no CLI produces the result.
A script is code the reviewer trusts but nobody tests.

## Preferred means

| Rank | Means | Use when | Cost to accept |
|---|---|---|---|
| 1 | Installed CLI (`git`, `gh`, `jq`, `python3`, `docker`, platform tools) | It exists, is installed, and its flags are documented | Install/auth, version drift |
| 2 | Inline `python3 -c` one-liner | ≤5 statements, one-off, never reused | Quoting, hard to review |
| 3 | `scripts/<verb>_<object>.py` | No CLI produces the result and a capability step runs it on every use | Maintenance, orphan risk |

## Justification tests

Add a script only when all four pass:

- No installed CLI produces the result — a char-vs-byte, exemption-aware size report has no CLI equivalent.
- A capability step runs it on every execution, not once during authoring.
- Its output must be deterministic and machine-checkable.
- The same logic would otherwise need >5 inline commands.

One failing test → use a CLI or an inline one-liner and leave no script behind.

## Language rule

- Scripts are Python 3, standard library only — no build step, no dependency install, portable.
- Exceptions — each must be stated in the capability step that runs it:

| Exception | Allowed when |
|---|---|
| Node | The only implementation lives in an npm package |
| POSIX `sh` | The whole task is ≤3 commands |
| OS-native tool | The capability is OS-locked by definition |

- Never ship a script that needs `pip install`, network access, a prompt, an absolute path, or secrets.

## Script contract

| Element | Requirement |
|---|---|
| Path and name | `scripts/<verb>_<object>.py`, snake_case |
| Shebang | `#!/usr/bin/env python3`; invoke as `python3 scripts/<name>.py` |
| Docstring | Usage line, exit codes, exemptions, assumptions |
| Entry point | `main(argv) -> int`; no work at import time |
| Exit codes | `0` pass, `1` findings, `2` usage error |
| Output | Sorted, stable field names, no timestamps or author-machine paths |
| Side effects | Read-only unless the capability declares a write |
| Size | ≤150 lines; larger means the task needs a real tool, not a skill script |
| No arguments | Prints the usage docstring and exits `2` |

- Field names are a contract: steps quote them (`chars`, `lines`, `budget`), so a rename renames every step.
- Provide a `--diff` or `--check` mode instead of shipping a second script.

## CLI contract

- Detect before use: check availability and the version floor, then run.
- Record the fallback for a missing CLI in the same step — alternate tool or manual procedure.
- Pass non-interactive flags; a capability step never waits for a prompt.
- Check the exit code; nonzero routes to the capability's failure step.

## Anti-patterns

| Anti-pattern | Severity |
|---|---|
| Script re-implements a standard CLI (`wc`, `git`, `jq`) | 🟡 Minor — replace or justify |
| Non-Python script with no stated exception | 🟡 Minor |
| Third-party dependency, network call, or prompt in a script | 🔴 Major |
| Script in `scripts/` that no capability step names (orphan) | 🔴 Major |
| Script path absent from the declared directory layout | 🟡 Minor |
| Capability step runs a CLI without detection or fallback | 🟡 Minor |
| Capability reports success without checking the exit code | 🔴 Major |
| Output fields consumed by steps but not documented | 🟡 Minor |
| Authoring-only script committed with the skill | 🟡 Minor — delete it |
