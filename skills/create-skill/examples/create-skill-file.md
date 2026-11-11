# Example: Create a Commit-Message Writer Skill

**Scenario**: Greenfield creation — the user asks for a brand-new copilot skill with no source material. Requirements are gathered from scratch, then a full SKILL.md is produced.

**Applies**: **collect-skill-requirements**, **classify-skill-content**, **create-skill-file**

## Input / Context
User request: "Create a skill that writes consistent git commit messages with conventional-commit prefixes and a 72-character subject line."

## Requirements Summary (collect-skill-requirements)
| Item | Confirmed value |
|---|---|
| Skill name | `write-commit-message` (imperative verb, kebab-case) |
| Description | "Write consistent git commit messages with conventional prefixes and a 72-char subject limit. Use when writing, fixing, or refining a commit message." |
| When-to-use scenarios | bug fix, feature, breaking change, refining an existing message |
| Capabilities | `<write-commit-message>` |
| Task regime | contractual — fixed literals and order per **empowerment-model** |
| Knowledge | prefix table, 72-char wrap rule, footer format |
| Rules | 1 rule routing commit-writing requests |
| Reference needs | none — rubrics are small |
| Gate state | `ACCEPTED-WITH-ASSUMPTIONS` — "consistent" inferred as subject-only, body only for breaking changes |
| Accepted assumptions | `Assumption (user-accepted, unverified)`: subject-only commits; body added only for breaking changes |

The gate ran before creation: the one inference was shown back in the restatement above and accepted, not assumed privately.

## Classification (classify-skill-content)
| Claim | Class | Route |
|---|---|---|
| 72-char subject limit | fact | knowledge |
| Conventional prefix table | fact | knowledge |
| Body and footer format for breaking changes | fact | knowledge, as a literal skeleton |
| "Add a body when needed" | procedure, not decidable | rewritten as "when the diff changes public behaviour" |
| Decide that a commit request is in scope | routing | the single rule |

Classification ran before any section was written; the undecidable step was fixed as content, not as style.

## Post-Write Checks
- Adequacy gates re-run per **content-model** — one owner per claim, every step decidable.
- Prescriptiveness checked per **empowerment-model** — every step passes the expert test.
- Prose written per **writing-style** — directive voice, BLUF, hard caps, no banned phrases.
- SKILL.md written within a per-section char budget, then measured per **size-limits** (≤12,000 chars / 150 lines); over-budget drafts fixed per **size-remediation** (lever order) before finalizing.

## Expected Output — `skills/write-commit-message/SKILL.md` (abridged)
```markdown
---
name: write-commit-message
description: Write consistent git commit messages with conventional prefixes and a 72-character subject limit. Use when writing, fixing, or refining a commit message.
---
<when-to-use-this-skill>
- User needs a commit message for a bug fix
- User needs a commit message for a feature
- User needs a commit message with a breaking change
- User needs to fix or refine an existing commit message
</when-to-use-this-skill>
<knowledge>
<commit-format>
... prefix table, wrap rule, footer format ...
</commit-format>
</knowledge>
<capabilities>
<write-commit-message>
1. Detect the change type from the diff.
2. Write the subject line within the 72-char limit.
3. Add a body and BREAKING CHANGE footer when the diff changes public behaviour.
4. Verify the subject is ≤72 characters and the footer matches the change type.
</write-commit-message>
</capabilities>
<rules>
<rule>When the user needs a commit message, use **write-commit-message**.</rule>
</rules>
```
