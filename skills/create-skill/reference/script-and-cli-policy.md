# Script and CLI Policy

Scope: choosing and shaping the automation this skill ships. The reviewer owns the
anti-pattern severity table; this copy carries the decision order and the contract.

Prefer a maintained CLI. Add a script only when no CLI produces the result.

## Preferred means

| Rank | Means | Use when |
|---|---|---|
| 1 | Installed CLI (`git`, `gh`, `jq`, `python3`, platform tools) | It exists, is installed, flags are documented |
| 2 | Inline `python3 -c` one-liner | ≤5 statements, one-off, never reused |
| 3 | `scripts/<verb>_<object>.py` | No CLI produces the result and a capability step runs it every time |

## Justification tests

All four must pass, or use a CLI and ship no script:

- No installed CLI produces the result.
- A capability step runs it on every execution.
- Its output must be deterministic and machine-checkable.
- The logic would otherwise need >5 inline commands.

## Contract

| Element | Requirement |
|---|---|
| Path and name | `scripts/<verb>_<object>.py`, snake_case |
| Shebang | `#!/usr/bin/env python3`; invoked as `python3 scripts/<name>.py` |
| Docstring | Usage, exit codes, exemptions, assumptions |
| Entry point | `main(argv) -> int`; no work at import time |
| Exit codes | `0` pass, `1` findings, `2` usage error |
| Output | Sorted, stable field names, no timestamps or author-machine paths |
| Side effects | Read-only unless the capability declares a write |
| Size | ≤150 lines |
| No arguments | Print usage, exit `2` |

Python 3 standard library only. Never ship a script needing `pip install`, network
access, a prompt, an absolute path, or secrets. Exceptions (Node, POSIX `sh`, OS-native
tool) must be stated in the capability step that runs it.

Field names are a contract: steps quote them, so renaming one renames every reference.
Prefer a `--check` or `--diff` mode over shipping a second script.

## CLI contract

- Detect availability and version before use; record the fallback in the same step.
- Pass non-interactive flags; never wait for a prompt.
- Check the exit code; nonzero routes to the failure step.
