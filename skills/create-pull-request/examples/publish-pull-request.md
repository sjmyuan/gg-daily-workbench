# Example: Publish After Approval and Return the Reference

**Scenario**: The draft is complete on a GitLab-hosted repo. Demonstrates **publish-pull-request**: approval block, forge detection, creation, verification, handoff.

**Applies**: **publish-pull-request**

## Input / Context
Repo `acme/order-service`, remote `git@gitlab.com:acme/order-service.git`. Branch `feature/retry-timeouts` pushed at `e4f5g6h`, matching the reviewed head commit. Card loaded from **resolve-conventions** (`pull-request` domain): target `develop`, title `type(scope): summary`, labels `area/gateway`, reviewer `@gateway-team`.

## Output

Applied **publish-pull-request** step 2 — approval block:

```
Base:      develop
Title:     feat(gateway): retry transient timeouts with backoff
Labels:    area/gateway
Reviewers: @gateway-team
Draft:     no
Head:      e4f5g6h
Sources:   .gitlab/merge_request_templates/Default.md · CONTRIBUTING.md:12

Body:
<full composed body>
```

Step 3 — user replies "Approved."

Step 4 — forge detected as GitLab from `origin`; create:

```
glab mr create --target-branch develop \
  --title "feat(gateway): retry transient timeouts with backoff" \
  --description "$(cat /tmp/mr-body.md)" \
  --label area/gateway --reviewer gateway-team
```

Step 5 — verify: `glab mr view 118 --output json` returns target `develop`, title unchanged, URL `https://gitlab.com/acme/order-service/-/merge_requests/118`.

Step 6 — handoff record:

```
URL: https://gitlab.com/acme/order-service/-/merge_requests/118
Number: 118
Base: develop
Head: e4f5g6h
Labels: area/gateway
Sources: .gitlab/merge_request_templates/Default.md · CONTRIBUTING.md:12
```

The caller records `#118` and the head commit; the orchestrator marks the cell **done** only after the merge includes `e4f5g6h`.

## Validation
- Creation happened only after explicit approval.
- Base, title, and URL verified after creation.
- No merge, approval, or auto-merge was requested.
- The handoff omits nothing the caller records.
