# Example: Classify Mixed Content Before Writing Sections

**Scenario**: A user supplies a support-triage agent prompt whose bullet lists mix facts, procedures, and prohibitions. The content must be sorted before any section is written — the form the source used says nothing about the class.

**Applies**: **classify-skill-content**

## Input / Context
Source excerpt, supplied unclassified:

- Escalation goes to the on-call rota in channel `#support-oncall`.
- Never close a ticket without a customer-visible reply.
- Score severity 1–4 with the matrix; 1 = outage, 4 = question.
- Handle billing questions as appropriate.
- Tickets older than 72 hours are breaching.
- When a ticket duplicates another, merge it into the parent and notify the reporter.

## Step 2 — Classify each claim

| # | Claim | Class | Decision-order hit |
|---|---|---|---|
| 1 | On-call channel `#support-oncall` | fact | holds without an actor |
| 2 | Never close without a customer-visible reply | routing+guard | decides whether an action is allowed |
| 3 | Score severity 1–4 with the matrix | procedure | ordered steps produce a value |
| 4 | Handle billing as appropriate | procedure | ordered steps, no decidable action |
| 5 | 72 hours is breaching | fact | holds without an actor |
| 6 | Duplicate → merge and notify | two classes | rule decides when; steps do the work |

Claim 3 is the trap: the source writes the matrix as a numbered list, so a shape-first read makes it a "capability" of four numbered facts. Claim 1 is the reverse trap: it reads like an instruction ("escalate to #support-oncall") but states a value the agent cannot infer.

## Step 3 — Split and route

| Claim | Route | Destination |
|---|---|---|
| 1, 5 | fact | knowledge — channel and threshold values |
| 2 | guard | rules: "Never close a ticket without a customer-visible reply" |
| 3 | procedure | capability `<score-severity>`; the 1–4 matrix is a fact → `reference/severity-matrix.md` |
| 4 | procedure, not decidable | back to the user as an open question — never invented |
| 6 | split | rule "When a ticket duplicates another → use **merge-ticket**" plus its capability steps |

## Expected Output

| Section | Holds |
|---|---|
| knowledge | `#support-oncall`, 72-hour threshold, severity matrix (routed to `reference/`) |
| capabilities | `<score-severity>`, `<merge-ticket>`, `<resolve-ticket>` |
| rules | routing for all three capabilities; one guard (claim 2) |

Validation after routing:
- Claim 4 is reported to the user, not filled in — an undecidable step is an adequacy failure, not a licence to guess.
- No fact sits in a capability step; no capability decides its own trigger.
- Each capability has one route; the one known misapplication has one guard.
