# Step Tracking Format

Record each step in the plan file using this format (each line one fact):

```
### Step N[letter]: [Step Title] [Status Emoji]
**Objective**: [What this step achieves — 1 sentence]
**Files**: [Files created, modified, or deleted]
**Source**: [no-op | base | port | copy | edit | generate] · [pinned ref, origin path, or n/a] · [equality mode]
**Implementation**: [Approach in prose — the seam that moves and the behavior it yields, 1 line; never code]
**Validation**: [Equality proof / test results — 1 line]
**Status**: [Status emoji] [Status description — 1 line]
```

## Status emojis

| Status | Emoji | Meaning |
|---|---|---|
| Pending | ⏳ | Not yet started |
| In Progress | 🔄 | Currently being worked on |
| Completed | ✅ | Successfully finished |
| Failed | ❌ | Encountered errors (include error details) |
| Blocked | 🚫 | Cannot proceed (include blocker details) |
| Abandoned | ⏭ | Deliberately not executed (reason required, no commit); ignored by completion checks |

`[letter]` appears only for amendment insertions (`Step 3a`); file order is execution order.

When a step is abandoned by an approved amendment, keep its number and record `**Status**: ⏭ Abandoned — <reason>`; it has no commit and is skipped on resume.

## Implementation and status

`**Implementation**` is the planner's approach, in prose: the seam that moves and the behavior it yields. It never carries source code, a diff, a signature, or a TODO list, and it stays frozen — the executor reads it and never rewrites it.

What execution produces goes in two places, never a third: the **commit and its diff** are the change, and the step's `**Status**` line carries the one-line outcome — receipt, counts, or a deviation. The six fields never change.
