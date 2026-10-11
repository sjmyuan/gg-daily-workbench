````markdown
# Example: Pull Request Review (Fetch the PR Branch into a Worktree)

**Scenario**: User asks to review pull request #482 in the `order-service` repository.

**Applies**: **preparing-review-checkout**, **conducting-code-review**

**Review Focus**: Blast radius, correctness, test coverage — read from the full branch, not the patch.

---

## Step 1 – Identify the PR and its base

```
Request:   "Review PR #482 in order-service"
Host:      detect from origin remote → git remote -v → github.com/acme/order-service
Base:      main
Head ref:  refs/pull/482/head
```

## Step 2 – Fetch the PR head

```bash
git fetch origin +pull/482/head:review/pr-482
# → * [new branch]      pull/482/head -> review/pr-482
```

## Step 3 – Detect the worktree pattern, then add the worktree

```
git worktree list
# /Users/dev/acme/order-service                          4a91c22 [main]
# /Users/dev/acme/order-service-worktrees/feature-login  c7d18be [feature/login]
```

The existing worktree sits in a `<repo>-worktrees/` directory beside the repository and is named after its branch. Follow that pattern rather than inventing a path.

```bash
git worktree add ../order-service-worktrees/pr-482 review/pr-482
```

The requester's checkout stays on their own branch — no stash, no HEAD move, no writes.

## Step 4 – Diff from the merge base

```bash
BASE=$(git merge-base origin/main review/pr-482)
git diff "$BASE"...review/pr-482 --stat
```

```
 src/order/OrderService.java        | 84 ++++++++++++++++-------
 src/order/dto/OrderRequest.java    | 12 ++--
 src/discount/DiscountRule.java     | 41 ++++++++++
 src/discount/DiscountRules.java    | 6 ++
 4 files changed, 118 insertions(+), 25 deletions(-)
```

## Step 5 – Review inside the worktree

What the worktree made visible — none of it appears in the patch:

| Check | Command | Found |
|---|---|---|
| Full changed file | `git -C ../order-service-worktrees/pr-482 diff` then read each file end to end | `applyDiscount()` kept a `switch` default that returns `ZERO` silently |
| Callers of the changed signature | search for `applyDiscount(` across the repo | two callers outside the diff, one in a scheduled job that passes a null code |
| Consumers of the changed DTO | search for `OrderRequest` | an OpenAPI spec still documents the removed `discountPercent` field |
| Tests | `git -C ../order-service-worktrees/pr-482 show "$BASE":src/test/.../OrderServiceTest.java` | the expiry test was deleted, not moved |
| Migrations and config | `git -C ... status --short` + inspect `db/migration` | no migration for the new `discount_rule` table |

## Step 6 – Findings

> Severity legend: 🚫 Blocker = must fix before merge · 🔴 Major = should fix · 🟡 Minor = nice to fix · 🟢 Nit = polish · ⚠️ Inconsistency = decision required

### 🚫 Blockers (Must Fix)

#### Scheduled job calls the changed signature with a null discount code
- **File**: `src/order/job/NightlyOrderReconciliation.java:88`
- **Related**: `src/order/OrderService.java:104`
- **Confidence**: Confirmed
```java
88 │     orderService.applyDiscount(order, null);
```
- **Issue**: The PR makes `discountCode` a required argument of `applyDiscount()`. This caller was not updated and passes `null`, which now reaches `DiscountRule.evaluate()` without a guard. The file is outside the diff, so the patch alone never showed it.
- **Impact**: Every nightly reconciliation run throws on the first order with a discount — the whole batch fails, and no orders are reconciled.
- **Recommendation**: Pass the request's discount code or guard the null case:
```java
String code = order.getDiscountCode();
if (code != null) orderService.applyDiscount(order, code);
```

### 🔴 Major Issues

#### Expiry test deleted rather than migrated
- **File**: `src/test/java/com/acme/order/OrderServiceTest.java:142 (after — restore the expiry test here)`
- **Confidence**: Confirmed
- **Issue**: The base revision contains `shouldRejectExpiredDiscountCode`; the PR head does not. The expiry logic moved into `DiscountRule`, and the test was dropped instead of moved with it.
- **Impact**: Expired discounts can silently be applied again — the exact regression the deleted test existed to catch.
- **Recommendation**: Port the test against `DiscountRule` and assert rejection for an expired rule.

#### No migration for the new rule table
- **File**: `db/migration/V31__discount_rule.sql (file absent — create here)`
- **Confidence**: Confirmed
- **Issue**: `DiscountRule` is a new JPA entity mapping a `discount_rule` table, but no migration adds it. The schema change is invisible in the diff.
- **Impact**: The application starts and then fails on the first discount lookup in any environment that has not been migrated by hand.
- **Recommendation**: Add the versioned migration and state its deploy order in the PR description.

### 🟡 Minor Issues

#### OpenAPI spec still documents the removed field
- **File**: `src/main/resources/openapi/order-api.yaml:74`
- **Confidence**: Confirmed
- **Issue**: `discountPercent` was removed from `OrderRequest` but is still in the published schema.
- **Impact**: Generated clients keep sending a field the service now ignores.
- **Recommendation**: Regenerate the spec from the DTO or remove the property.

---

## Failure Modes Checked

| Mode | Change under test | Result |
|---|---|---|
| Empty / null | `null` discount code | not verified — unguarded, see blocker |
| Scale | Nightly batch over all orders | not verified — one failure aborts the batch |
| Boundary | Rule expiry at the exact second | not verified — the covering test was deleted |
| Rollback / undo | Revert the release | not verified — no down-migration for `discount_rule` |

---

## Risks & Assumptions
- Assumes the scheduled job is deployed in the same service — confirm from the cron manifest in the worktree
- Assumes `discount_rule` is created outside this repo — check the shared schema repository before merging

---

## Step 7 – Clean up

```bash
git worktree remove ../order-service-worktrees/pr-482
git branch -D review/pr-482
```

````
