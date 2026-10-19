# Example: Stop on an Open Duplicate

**Scenario**: A change adds retry handling to an API client. Before drafting, the agent checks whether another request already covers it. Demonstrates **find-related-pulls** with a duplicate-open outcome.

**Applies**: **find-related-pulls**

## Input / Context
Target repo `acme/order-service`. Planned change: retry transient gateway timeouts in `GatewayClient` and add backoff tests.

## Output

Applied **find-related-pulls**:

```
Search terms: "gateway timeout retry", "GatewayClient backoff", "transient retry"

Open:
  #812  feat(gateway): retry transient timeouts with backoff   (open, same module)
Closed:
  #701  fix(gateway): retry once on timeout                   (closed, superseded by #812)
Related:
  #655  test(gateway): flaky timeout coverage                 (closed, test-only)

Classification: duplicate-open (#812)
Decision: stop — do not create a second request.
```

Reported to the user:

> "#812 already implements retry with backoff in `GatewayClient`. This change
> looks duplicate. Options: (a) add the missing backoff tests to #812,
> (b) close #812 and open one combined PR, (c) continue only if the approach differs."

## Validation
- Both open and closed requests searched.
- The duplicate is named with its number and scope.
- No PR was composed or created.
