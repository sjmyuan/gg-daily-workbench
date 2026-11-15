# Review Briefing Skeleton

Used by **brief-before-review** (steps 3–4) and **record-review-state** (step 1). One briefing per unit; the artifact is attached below it, never summarized in it.

## Skeleton

```markdown
**Decision**: <the single decision this unit asks for>

**Start here** — <N> stops, in order:
1. `<path>:<from>-<to>` — <mechanism> — notice <what to notice>
2. ...

**Predict first**: <the expectation to commit to> — my read: <your read>

**Check yourself** (<2 min): <action> → expect <result>; wrong if <falsifier>

**Then**: <the checkpoint's original question, unchanged>

<artifact>
```

## Field order and ceilings

| Field | Required | Ceiling | Owner |
|---|---|---|---|
| `Decision` | Always | 1 line | Names the choice, not the artifact |
| `Start here` | Code claims and no authored area | 5 stops (2 familiar, 0 authored) | **plan-orientation-route** |
| `Predict first` | When a live hypothesis exists | 1 line plus your read | **brief-before-review** step 5 |
| `Check yourself` | When the artifact rests on a code claim | 1 check, 2 minutes | **design-self-check** |
| `Then` | Always | The existing question, verbatim | The calling checkpoint |
| Whole briefing | Always | ≤15 lines above the artifact | **dose-control** |

## Recording the state

| State | Trigger | Carried where |
|---|---|---|
| `reviewed` | The reviewer reports which stops they opened, or answers the prediction | The unit's existing status field |
| `waived` | The reviewer declines, skips, or says "just proceed" | The same field, with the unread claim named once |

Never label the state `ACCEPTED` — that word belongs to the intake gate and records permission, not comprehension.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| A route that lists the artifact's own sections | Stops that carry the mechanism in the code |
| "Let me explain the architecture first" | A route the reviewer walks themselves |
| A prediction with no expectation asked of the reviewer | Elicit, then reveal |
| A self-check that cannot fail | Pick a claim whose failure changes the decision |
| Bundling three areas behind one question | One unit per turn |
| A summary above the artifact restating its content | A route; the artifact stays the payload |
| Recording `reviewed` from silence | `waived`, stated aloud |
