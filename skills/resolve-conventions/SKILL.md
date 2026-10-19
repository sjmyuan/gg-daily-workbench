---
name: resolve-conventions
description: Resolve a target repository's conventions for a named domain into an evidence-backed card. Use when resolving, discovering, or checking repo conventions before acting.
---

<when-to-use-this-skill>
- A workflow must follow a repo's pull-request, coding, testing, review, commit, branch, or docs conventions
- The repo's conventions are not recorded, stale, or conflicting
- A skill needs an evidence-backed convention card before it acts
- A recorded card must be checked against the current repo after a policy or remote change
- Do NOT load to apply a convention — the domain skill owns application
- Do NOT load when a current card for the repo and domain is already recorded — reuse it
</when-to-use-this-skill>

<knowledge>
<convention-domains>
| Domain | Fields |
|---|---|
| `pull-request` | base, title, body, labels, reviewers, draft, linked issue, disclosure, forbidden content, duplicate search |
| `coding` | formatter, linter, style, comments, naming, error handling |
| `testing` | framework, placement, naming, fixtures, coverage, commands |
| `review` | checklist, severity, approvals, required reviewers, comment style |
| `commit` | format, scope, ticket, sign-off, AI wording |
| `branch` | naming, base, protection |
| `docs` | location, format, front matter, links |

- A caller may request a subset of a domain's fields.
- Unknown domain: ask the user for its fields before resolving.
</convention-domains>

<convention-source-order>
Detect conventions in this order; the first source that answers a field wins.

| Priority | Source | Extract |
|---|---|---|
| 1 | Repo-local skills and agents | Domain procedure, required sections, prohibitions |
| 2 | Templates and configs | PR/MR templates, issue templates, linter, formatter, test, review configs |
| 3 | Repo docs and rules | `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING*`, domain docs, `CODEOWNERS`, branch protection |
| 4 | Recent practice | Recent requests, commits, branches, reviews (≤10 each) |
| 5 | Ask the user | Gaps, conflicts, or no history |

- A hard prohibition in any source always applies, even when a lower-priority source conflicts.
- Never assume a field outside the requested domain profile.
</convention-source-order>

<convention-card>
One card per repo and domain.

| Field | Value | Evidence |
|---|---|---|
| Domain | requested domain | caller |
| Resolved fields | value or `unknown` | path, `file:line`, request number, or sample size |
| Conflicts | unresolved conflicts | both sources |
| Prohibitions | hard prohibitions found | path or request |

- Every field has a value or `unknown`.
- Expand **Resolved fields** into one row per domain field.
- `unknown` is valid; a guess is not.
</convention-card>

<conflict-handling>
- Ask the user for every unresolved conflict or `unknown`; never choose silently.
- Never default a value from another repo, framework, or personal habit.
</conflict-handling>

<domain-lifecycle>
- Re-resolve only when the repo, remote, or policy changes.
</domain-lifecycle>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Resolving a domain and needing exact sources | Domain hints, discovery commands, extraction rules, conflict nuances | [reference/domain-and-discovery.md](reference/domain-and-discovery.md) |
| Resolving pull-request conventions | PR domain card walkthrough | [examples/resolve-pull-request-conventions.md](examples/resolve-pull-request-conventions.md) |
| Resolving coding conventions | Coding domain card walkthrough | [examples/resolve-coding-conventions.md](examples/resolve-coding-conventions.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<resolve-conventions>
**Objective**: Produce an evidence-backed convention card for one repository and domain.

1. Resolve the target repo (upstream/base, not a fork) from the working directory and its remotes.
2. Select the requested domain from **convention-domains** and confirm its fields.
3. Read sources in **convention-source-order** priority until every field has evidence.
4. Extract each field and record its evidence; list conflicts.
5. Resolve conflicts per **conflict-handling** before returning.
6. Return the card; the caller keeps it for the domain skill.
7. Validate against **convention-card**.
</resolve-conventions>
</capabilities>

<rules>
<rule> When a domain convention is missing, stale, or conflicting, apply **resolve-conventions**. </rule>
<rule> Never apply a convention from this skill — return the card to the domain skill. </rule>
</rules>
