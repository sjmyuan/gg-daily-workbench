# Finding Anchors

Location rules for every review finding. One finding carries exactly one primary anchor — a single `path/file.ext:LINE`, never a range.

## Primary anchor

| Rule | Requirement |
|---|---|
| Single line | `path/file.ext:LINE` — one line number, no ranges |
| Code preview | Quote the anchored line verbatim under the anchor: `LINE │ <code>` |
| Pin the defect | Anchor the line that must change; for a multi-line construct, the first defective line |
| One anchor per finding | Never place two paths or two ranges in one `**File**` field |
| New-file numbering | In diff reviews use the post-change line number; add `(old: L42)` when the sides differ |
| Documents | Anchor the file line; add the section heading when the file is long |

## Missing or unwritten code

Anchor the nearest existing line and state the direction.

| Case | Anchor |
|---|---|
| Missing test | `path/EventPublisherImplTest.java:120 (after — insert the regression test here)` |
| Missing guard | `path/EventPublisherImpl.java:74 (before — add the duplicate check here)` |
| Missing file | `path/to/expected/DeployRunbook.md (file absent — create here)` |

## Secondary locations

Never concatenate locations. Attach extra places as their own field:

```markdown
- **File**: `src/pricing/DiscountCalculator.java:44`
- **Related**: `src/pricing/DiscountValidator.java:18`, `src/pricing/LegacyPricing.java:203`
```

Split into separate findings when each place needs its own fix.

## Machine-readable output

Emit one `location` line per finding when the requester needs parseable output:

```markdown
- **File**: `src/pricing/DiscountCalculator.java:44`
- **Location**: `src/pricing/DiscountCalculator.java:44`
```

`location` holds `path:LINE` only — the parsing target for tooling and CI checks.

## PR-inline output mode

Emit one inline comment per finding when the requester asks for PR-style feedback.

| Field | Value |
|---|---|
| `path` | File path exactly as the PR expects it |
| `line` | The anchored line |
| `side` | `RIGHT` for added or changed lines, `LEFT` for removed lines |
| `body` | Finding title, confidence, Issue, Impact, Recommendation |

Findings with no anchorable line — missing files, PR-description gaps — go into the review summary body instead.

## Before → after

| Before (imprecise) | After (precise) |
|---|---|
| `[EventPublisherImpl.java](EventPublisherImpl.java#L28-L30)` | `EventPublisherImpl.java:28` + `28 │ private final Set<String> publishedMessageIds = new HashSet<>();` |
| `**File**: Tests missing for [EventPublisherImpl.java](EventPublisherImpl.java#L68-L75)` | `EventPublisherImplTest.java:120 (after — insert the regression test here)` |
| `**File**: [a.java:10-20](…), [b.java:44-50](…)` | Two findings, or `**File**: a.java:10` plus `**Related**: b.java:44` |

## Validation

- [ ] Every finding has exactly one `path:LINE` primary anchor
- [ ] Every anchor is followed by the verbatim anchored line
- [ ] No `#L10-L15` range appears in a `**File**` field
- [ ] Missing-code findings carry a direction word (`before` / `after` / `file absent`)
- [ ] Every `**Location**` value matches its `**File**` anchor
