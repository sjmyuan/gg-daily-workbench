# Example: Challenging an Invented Package Path

**Scenario**: PR `feature/order-discount` moves pricing logic "into the order-discount module". The PR
description and the branch name both say so; the tree does not contain that module.

**Applies**: **challenging-the-change**

## Input

- **Diff**: `src/orders/do-something/Pricing.java` modified (+64/-12); `src/orders/do-something/pricing.md` added.
- **PR description**: "Move pricing into the `order-discount` module and add coupon support."
- **Base**: `main`. **Head**: `feature/order-discount`.

The tempting output — the one this skill exists to prevent:

```markdown
#### Pricing logic lives outside its module
- **File**: `src/orders/order-discount/Pricing.java:31`
- **Recommendation**: Keep the new coupon code inside `src/orders/order-discount/` as the PR describes.
```

Every path there was composed from the branch name. Nothing was read.

## Step 1 — Intent hypothesis

> The change adds coupon support to the existing `do-something` package and calls the result the
> "order-discount module". If the intent is instead a new bounded context, the placement challenge and
> the currency finding both change.

## Step 2 — Referent grounding

| Referent | Status | Evidence |
|---|---|---|
| `src/orders/do-something/Pricing.java` | resolved | `git diff --name-status main...HEAD` → `M src/orders/do-something/Pricing.java` |
| `src/orders/order-discount/` | unverified | `git ls-tree -d main -- src/orders` → no `order-discount` directory |
| `src/orders/order-discount/Pricing.java` | unverified | `git ls-files 'src/orders/*Pricing.java'` → 1 path, the `do-something` one |

## Step 3 — Reasonableness probes

| Probe | Result |
|---|---|
| Placement | **Fails** — no ADR or `AGENTS.md` line mentions a feature-named package; `docs/adr/014-layout.md:9` says code stays in its domain package |
| Path derivation | **Fails** — the only source of `order-discount` is the branch and PR title |
| Naming | Passes — `Pricing`, `DiscountRule`, `Coupon` match the domain glossary |
| Scope | **Fails** — the PR adds `pricing.md` and reformats `README.md`, neither mentioned as intent |
| Duplication | Passes — no existing coupon implementation |
| Abstraction | Passes — one new class, one caller |
| Data model | Passes — coupon state already exists |
| Sequencing | Passes — no migration or config prerequisite |
| Reversibility | Passes — no destructive operation |
| Requirement conflict | **Fails** — ADR-014 forbids feature-named packages under `orders/` |

## Step 4 — Challenges

| # | Question | Why it looks unreasonable | Assumed meanwhile | Settles it | Blocking |
|---|---|---|---|---|---|
| C1 | Should pricing stay in `src/orders/do-something/` rather than move to a feature package? | The destination exists only in the branch name; ADR-014 puts code in its domain package | Reviewed as if the package stays put — the currency finding depends on it | The author confirming no new module is planned, or an ADR superseding 014 | yes |
| C2 | Are the `pricing.md` and README edits part of this change? | Neither appears in the stated intent, and the README edit reformats unrelated sections | Reviewed as unrelated noise, excluded from findings | The author confirming scope | maybe |

## Expected output (abridged)

````markdown
## Code Review Summary

**Scope**: `feature/order-discount` — coupon support in `src/orders/do-something/`
**Open challenges**: 2 open, 1 blocking · **Unverified referents**: 2
**Ready to merge?**: With fixes — one blocking placement question and one correctness bug remain

## ❓ Challenges & Questions

| # | Question | Why it looks unreasonable | Assumed meanwhile | Settles it | Blocking |
|---|---|---|---|---|---|
| C1 | Should pricing stay in `src/orders/do-something/`? | `src/orders/order-discount/` exists only in the branch name; `docs/adr/014-layout.md:9` keeps code in its domain package | Reviewed as if the package stays put; the currency finding assumes it | The author confirming no new module is planned, or a superseding ADR | yes |
| C2 | Are the `pricing.md` and README edits in scope? | Neither appears in the stated intent | Treated as noise, excluded from findings | The author confirming scope | maybe |

## Findings

### 🔴 Major Issues

#### Coupon currency is ignored when no currency is supplied
- **File**: `src/orders/do-something/Pricing.java:41`
- **Confidence**: Confirmed
```java
41 │     return basePrice - coupon.getAmount().doubleValue();
```
- **Issue**: The coupon amount is subtracted without converting it to the order currency, so a coupon
  issued in another currency subtracts a foreign amount.
- **Impact**: Orders in non-default currencies are mispriced — silent revenue loss on every coupon.
- **Recommendation**: Convert through the existing `FxRateService` before subtracting, and add a test
  with a cross-currency coupon.

## Referent Check

| Referent | Status | Evidence |
|---|---|---|
| `src/orders/do-something/Pricing.java` | resolved | `src/orders/do-something/Pricing.java:41` |
| `src/orders/order-discount/` | unverified | `git ls-tree -d main -- src/orders` → absent |
````

## Why this is better

- The invented path never reaches the report: it is labeled `unverified` with the failed lookup.
- The move becomes a **question the requester can answer**, not a recommendation the author must obey.
- The currency finding is stated together with the assumption it rests on, so an answer to `C1` visibly changes it.
- The verdict reflects the blocking challenge instead of hiding it below the findings.
