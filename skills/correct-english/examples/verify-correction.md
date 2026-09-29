# Example: Verifying a Draft That Changes Meaning

**Scenario**: A correction draft silently changes "next Friday" to "this Friday" and reformats the line.
The verify capability catches the meaning and formatting failures, then revises the draft.

**Applies**: **verify-correction**

## Input

Original text:

> the deadline is next friday — pls confirm by monday

Correction draft:

> The deadline is this Friday. Please confirm by Monday.

## Output

Checklist result:

| # | Criterion | Result |
|---|---|---|
| 1 | Grammar correct | Pass |
| 2 | Spelling correct | Pass |
| 3 | Punctuation correct | Pass |
| 4 | Meaning preserved | **Fail** — "next Friday" changed to "this Friday" |
| 5 | Tone preserved | Pass |
| 6 | Formatting preserved | **Fail** — em dash removed, line split |
| 7 | Clarity or conciseness improved | Pass |
| 8 | Output contract met | Pass |

Revised text:

> The deadline is next Friday — please confirm by Monday.
