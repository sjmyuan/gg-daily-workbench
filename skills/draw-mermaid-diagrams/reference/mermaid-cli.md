# Mermaid CLI Setup

Used by **ensure-mermaid-cli** (steps 2–3) and **validate-diagram-syntax** (step 1).

## Detect

```
mmdc --version
```

Exit 0 means the CLI is ready; report the version and continue.

## Install options

| Option | Command | Use when |
|---|---|---|
| Global install | `npm i -g @mermaid-js/mermaid-cli` | Normal developer machine |
| No install | `npx -p @mermaid-js/mermaid-cli mmdc -i in.mmd -o out.svg` | No global write access |
| Docker | `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/data minlag/mermaid-cli -i in.mmd -o out.svg` | No Node, or CI images |
| Local project | `npm i @mermaid-js/mermaid-cli && ./node_modules/.bin/mmdc …` | Repo-pinned version |

Global install downloads Node dependencies plus a Chromium build (~300 MB on first run). Say so before proposing it.

## Consent rules

- Never install silently; a global install changes the user's machine.
- Ask with the exact command, the approximate download, and the alternatives.
- Offer three choices: install now, user runs the command, use npx/Docker for this run.
- Continue with the chosen runner and report which one is in effect.

## Verify

```
mmdc --version
printf 'flowchart TD\n    A([Start]) --> B([End])\n' | mmdc -i - -o /tmp/probe.svg
```

Both must succeed before validating real diagrams.

## Linux and CI sandbox

If rendering fails with a Chromium sandbox error, write `puppeteer.json`:

```json
{ "args": ["--no-sandbox"] }
```

Then rerun with `-p puppeteer.json`. Mention the security trade-off; do not bake `--no-sandbox` into local runs.

## Reading failures

- Non-zero exit code = parse failure; no output and exit 0 = success.
- Parse errors report a line number relative to the block, not the document.
- Exit 1 with a browser error is an environment problem, not a diagram problem — fix setup first.
