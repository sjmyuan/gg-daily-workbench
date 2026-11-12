---
name: fan-out-agents
description: Dispatch several independent, similar read-only sub-tasks as parallel copies of the same agent and merge their reports into one answer. Use when parallelizing, splitting, scaling out, or fanning out broad read-only work across same-type sub-agents; not for cross-role pipelines or work that writes shared state.
---

<when-to-use-this-skill>
- A task decomposes into several independent, similar sub-tasks (modules, entry points, repos, or candidates) that one agent would otherwise cover serially
- The agent wants to parallelize a broad read-only investigation or review by dispatching parallel copies of itself, then merging the reports
- Mid-task the agent notices several independent things it can do in parallel and fans out on its own, without being asked
- The agent merges the returned reports of several same-type sub-agents into one coherent answer
- Do NOT load when the sub-tasks are genuinely serial, each result feeds the next, or too small to justify fan-out — run them directly
- Do NOT load when another pipeline owns orchestration (e.g. `conduct-spike` per-area dispatch, `orchestrate-feature-delivery` waves) — those orchestrate already
</when-to-use-this-skill>

<knowledge>

<fan-out-model>
A **fan-out** runs several independent, similar units of work as parallel copies of the host agent, then merges the reports into one answer.
It is not heterogeneous orchestration: cross-role pipelines (spike per-area dispatch, feature-delivery waves) own their dispatch and never route here.
Fan-out is **read-only / report-producing** — clones never mutate shared files or state.
Work that writes shared targets runs directly or in a pipeline that owns conflict handling.
Fan-out leaves no artifacts, index, or tracking file.
One level deep — clones are leaf tasks and never re-fan-out.
</fan-out-model>

<trigger-signals>
Fan out when all four hold:

- **separable targets** — ≥2 modules, entry points, repos, or candidate lists
- **independent answers** — one area's findings cannot change another's conclusion
- **similar work** — same capability and reporting doctrine across areas
- **enough effort** — a serial sweep would be long and shallow

Skip on any anti-signal: a serial dependency between areas, one small lookup, a tightly coupled slice, or a shared-write target.
Also skip when the platform cannot spawn same-type sub-agents — run the task directly.
</trigger-signals>

<auto-split-principle>
Splitting is fully automatic — never ask the user to pre-decompose or confirm areas.
Partition the task into disjoint areas that together cover the whole task.
Cut along the strongest seams (repo → module/package → entry point → file cluster), one area per seam, boundaries where code touches least.
Prefer 2–4 areas, since more raises overlap and merge cost.

Check before dispatch: every part of the task is claimed by at least one area, and no target is claimed twice.
Fix a failure by re-partitioning; when you cannot form confidently disjoint, covering areas, run the task directly — a guessed split wastes parallel reads and silently drops coverage.
</auto-split-principle>

<inline-brief-contract>
The host authors each clone's brief inline from generic invariants — no fixed template file.
Every brief is **self-contained** — clones inherit neither the host's session history nor each other's context, so the brief carries every fact a clone needs.
Each states the area's scope boundary (in/out), the sub-question, the return contract per the host's own reporting doctrine, and a leaf instruction.
Name the clone's model where the platform allows choosing one — an omitted model inherits the host's, often the most expensive.
Match the model to area complexity: cheap for mechanical lookups, capable for subtle reasoning.
Briefs are the only deconfliction between clones, which never see each other.
</inline-brief-contract>

<merge-discipline>
Merging is where quality is won or lost.
The host reads short reports and never redoes a clone's reads.
Deduplicate overlapping claims: one claim, both locations.
Reconcile shared boundaries with a direct spot-check.
Spot-check at least one claim per area against primary sources — clones can make systematic errors, not just boundary overlaps.
Surface conflicts rather than hiding them; never present a coherent whole that papers over a contradiction.
Close with a coverage summary: areas covered, per-area returns, unresolved conflicts, searched-negatives.
Presentation stays in the host's own doctrine — this skill imposes none.
</merge-discipline>

<platform-dispatch>
Detect whether the platform lets the host spawn copies of itself as sub-agents.
When it does, dispatch all clones **in one response** — batched dispatches run in parallel; one per turn runs serially.
When it does not, run the same split serially — still better than an unplanned sweep.
</platform-dispatch>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Walking a broad codebase question fanned across three investigation clones | Host split, briefs, clone reports, merged answer | [examples/fan-out-investigation.md](examples/fan-out-investigation.md) |
| Walking a large multi-module review fanned across review clones | Host split of a PR, merged findings by severity | [examples/fan-out-review.md](examples/fan-out-review.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<fan-out-tasks>
**Objective**: Run several independent similar sub-tasks as parallel clones and merge their reports into one answer.

1. Detect fan-out-ability against **trigger-signals**. Run the task directly when a signal fails, dispatch is unavailable, or no safe split exists.
2. Split into disjoint covering areas per **auto-split-principle**.
3. Compose one inline brief per area per **inline-brief-contract**, model included.
4. Dispatch all clones concurrently per **platform-dispatch** — all dispatches in one response.
5. Keep local work moving while clones run — never poll on short timeouts.
6. Collect each report as it returns, and chase any clone that finishes without reporting.
7. Merge and reconcile the reports per **merge-discipline**.
8. Present the single merged answer using the host's reporting doctrine, with a coverage summary listing unresolved cross-area conflicts.
9. Validate — areas disjoint and covering, every report used, conflicts surfaced, the answer addresses the original task.
10. Gate — an unreturned area or a target claimed twice fails validation → dispatch the missing area, or state it as an explicit gap.
</fan-out-tasks>

</capabilities>

<rules>
<rule>When a task splits into several independent, similar, read-only sub-tasks, apply **fan-out-tasks**.</rule>
<rule>Never fan out work that writes shared files or state — clones are read-only and leave no artifact.</rule>
<rule>Never let a clone re-fan-out — fan-out is one level deep.</rule>
</rules>

