# Domain Hints and Discovery

Domain-specific sources, discovery commands, extraction rules, and conflict nuances for **resolve-conventions**.

## Domain hints

| Domain | Extra sources |
|---|---|
| `pull-request` | PR/MR templates, recent merged and open requests, `CODEOWNERS`, labeler config, release config |
| `coding` | `.editorconfig`, formatter and linter configs, `STYLE.md`, recent changes in the touched module |
| `testing` | test framework config, existing test tree, CI test commands, fixtures and builders |
| `review` | `CODEOWNERS`, review checklists, recent review comments, approval settings |
| `commit` | `commitlint` config, recent commit log, `CONTRIBUTING*`, sign-off rules |
| `branch` | branch protection, recent branch names, remote and base-branch settings |
| `docs` | docs tree, front matter, link checker, existing page structure |

## Discovery commands

Run one sweep in priority order; do not search repeatedly.

1. `find . -path '*/skills/*/SKILL.md'`; also scan `.github/agents`, `.claude/agents`, `.opencode/agents`, `.agents`.
2. `find . -iname '*template*' -o -iname '.editorconfig' -o -iname '*eslint*' -o -iname '*prettier*' -o -iname '*commitlint*'`.
3. Read `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CONTRIBUTING*`, `docs/**`, `.cursor/rules`, `CODEOWNERS`, and branch protection.
4. Sample recent requests, commits, branches, and reviews with the forge and VCS tooling.
5. Read only files that can change the requested domain; skip product documentation.

## Extraction rules

- Quote the rule that decides a field; record its path and line.
- Prefer a stated rule over an observed habit.
- Treat repeated recent practice as evidence only when no source states a rule.
- Ignore legacy outliers when the majority and the docs agree.
- Record the sample size for empirical fields (`7 of 9 commits`).
- A template placeholder is a required section, not sample content.
- Comments inside templates and configs are instructions; follow them.

## Conflict signals

| Signal | Resolution |
|---|---|
| Two same-priority sources disagree | Present both to the user with citations |
| Recent practice splits between two values | Present both; never vote by majority |
| No history and no template | Ask for the expected format |
| Stated rule differs from current practice | Apply the stated rule; report the divergence |
