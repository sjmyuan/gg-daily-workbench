# Example: Compose Against a Strict Template

**Scenario**: A repo template requires five sections and a truthful checklist. Demonstrates **compose-pull-request** filling every section with verified facts.

**Applies**: **compose-pull-request**

## Input / Context
Card loaded from **resolve-conventions** (`pull-request` domain): base `develop`; title `type(scope): summary`; template headings Problem, Change, Tests, Rollback, Checklist; disclosure required; labels `area/gateway`.

Plan and execution evidence: added retry with exponential backoff to `GatewayClient`; tests `GatewayClientTest` 12/12 pass; integration suite not run; rollback is revert of two commits; no linked issue.

## Output

```
Title: feat(gateway): retry transient timeouts with backoff
Base: develop
Labels: area/gateway

## Problem
Transient gateway timeouts surface as failed orders because `GatewayClient`
does not retry. Support ticket order-service#4821 records 37 failures in one week.

## Change
Add retry with exponential backoff to `GatewayClient`. Retries stop after
three attempts or 2 seconds. Non-transient errors fail immediately.

## Tests
- `GatewayClientTest` — 12/12 passing.
- Integration suite — not run; gateway sandbox unavailable.
- Manual check — retry observed for a 504, no retry for a 400.

## Rollback
Revert commits `a1b2c3d` and `e4f5g6h`. No schema or config change.

## Checklist
- [x] Tests added for the retry path
- [x] No unrelated changes
- [ ] Integration suite run — blocked by unavailable sandbox

## Disclosure
Agent: executor · Model: <model-id> · Harness: <harness>
```

## Validation
- Headings match the template exactly.
- Every claim traces to the diff, test run, or ticket.
- The unchecked integration box states why; it is not ticked falsely.
- No placeholder or empty section remains.
