# Step Tracking Format

Record each step in the plan file using this format (each line one fact):

```
### Step N[letter]: [Step Title] [Status Emoji]
**Objective**: [What this step achieves — 1 sentence]
**Files**: [Files created, modified, or deleted]
**Implementation**: [Key changes — 1 line]
**Validation**: [Test results / verification — 1 line]
**Status**: [Status emoji] [Status description — 1 line]
```

Status emojis per **step-status-definitions** (see the skill's knowledge section).

`[letter]` appears only for amendment insertions (`Step 3a`); file order is execution order.

When a step is abandoned by an approved amendment, keep its number and record `**Status**: ⏭ Abandoned — <reason>`; it has no commit and is skipped on resume.
