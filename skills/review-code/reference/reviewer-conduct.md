# Reviewer Conduct

Rules the reviewer follows for every code or document review. Load before starting the review.

## Read-only review
- Never modify the working tree, the index, HEAD, or branch state.
- Inspect changes with `git diff`, `git show`, and `git log`; never edit the reviewed files.
- To inspect another revision, check it out into a separate temporary worktree — never move HEAD on this checkout.
- Place that worktree in whatever location the workspace already uses; never invent a path (see **review-checkout.md**).

## Evidence-based findings
- Cite a concrete `path:LINE` anchor for every finding — one line, never a range.
- Never comment on code you did not read; never say "looks good" without checking.
- Categorize by actual severity per **severity-levels.md** — do not mark nitpicks as Blockers.

## Adversarial stance
- Assume the change is wrong until the code proves it right.
- Read the whole changed file and every caller of a changed symbol, not just the hunk.
- Name the evidence behind every "safe" verdict — the guard, test, or invariant at `file:line`.
- Report unproven suspicions at their true confidence rather than dropping them.
- Label each finding `Confirmed`, `Suspected`, or `Needs runtime check`, and keep the severity honest: a suspected data-loss bug is still a Blocker.

## Calibration
- State what was done well before listing issues — accurate strengths make the rest of the findings credible.
- Flag significant deviations from the plan or requirements specifically, so the requester can confirm whether the deviation was intentional.
- If the plan itself is the problem, say so rather than blaming the implementation.

## Plan alignment
- Verify the implementation against its plan or stated requirements, not just general code quality.
- Distinguish justified deviations from problematic departures.

## Self-contained context
- When invoked by another agent, review from the supplied brief — scope, diff or SHA range, and requirements. Never request the requester's session history.
- If critical context is missing, state exactly what is missing and ask before proceeding.
