---
name: review-code
description: Code and document reviews across files, diffs, commits, PRs, and branches. Evaluates correctness, security, performance, and blast radius with line-precise findings. Use when requesting reviews, feedback, or bug hunting.
---

<when-to-use-this-skill>
- A user or another agent requests a code review
- User submits files, folders, diffs, commits, or pull requests for review
- User asks for feedback on code quality, security, performance, or maintainability
- User supplies one branch name (diff against current branch) or two branch names (diff between them)
- User asks to review a document (README, design doc, ADR, specification, runbook, etc.) for clarity, completeness, or structure
- User asks whether a change is safe, or wants potential bugs and failure modes surfaced
</when-to-use-this-skill>

<knowledge>

<context-loading-guide>
Load on demand. `branch-diff-review.md` demonstrates **gathering-review-context**, `pull-request-review.md` demonstrates **preparing-review-checkout**; others show the output phase.

| Load when | Provides | File |
|---|---|---|
| Before starting a review | Reviewer conduct rules — read-only, evidence-based findings, calibration, plan alignment, self-contained context | [reference/reviewer-conduct.md](reference/reviewer-conduct.md) |
| About to apply review dimensions to code | 10-dimension checklist plus adversarial stance, failure-mode enumeration, and negative-space prompts | [reference/review-dimensions.md](reference/review-dimensions.md) |
| About to categorize findings by severity | Severity rubric (🚫 Blocker, 🔴 Major, 🟡 Minor, 🟢 Nit, ⚠️ Inconsistency) with criteria for each level | [reference/severity-levels.md](reference/severity-levels.md) |
| About to anchor a finding location | Anchor rules — single `path:LINE`, code preview, missing-code anchors, PR-inline output | [reference/finding-anchors.md](reference/finding-anchors.md) |
| About to write review output | Review output template, formatting guidelines, and the plain-language Issue/Impact/Recommendation contract | [reference/review-output-format.md](reference/review-output-format.md) |
| Scoping a review under time pressure | Efficiency strategies — risk ordering, whole-file reading, call-graph bounding | [reference/review-efficiency.md](reference/review-efficiency.md) |
| Probing a code change for hidden bugs | Worked example of blast-radius tracing and failure-mode enumeration | [examples/change-context-probe.md](examples/change-context-probe.md) |
| About to review a diff, commit, or bug fix | Output structure example for diff/commit reviews | [examples/diff-commit-review.md](examples/diff-commit-review.md) |
| Retrieving the code to review (branches, PR, uncommitted) | Worktree location, PR refspecs, merge-base diffing | [reference/review-checkout.md](reference/review-checkout.md) |
| User supplies one or two branch names for comparison | Output structure example for branch diff reviews | [examples/branch-diff-review.md](examples/branch-diff-review.md) |
| Reviewing a pull request | Worked example of fetching the PR branch into a worktree | [examples/pull-request-review.md](examples/pull-request-review.md) |
| Reviewing a performance optimization or slow-code change | Output structure example for performance-focused reviews | [examples/performance-improvement.md](examples/performance-improvement.md) |
| Reviewing a document (README, ADR, design doc, specification, runbook) | Output structure example for document reviews | [examples/doc-review.md](examples/doc-review.md) |
| Reviewing a PR that adds a migration, new service endpoint, or cache layer | Output structure example for observability and deployment safety reviews | [examples/deployment-safety-review.md](examples/deployment-safety-review.md) |
| Writing or checking plain-language, actionable findings | Before/after example (terse → explained review findings) | [examples/plain-language-findings.md](examples/plain-language-findings.md) |
</context-loading-guide>

<finding-anchors>
Anchor every finding to one `path/file.ext:LINE` with the verbatim line quoted beneath it — never a range. Rules: **reference/finding-anchors.md**.
</finding-anchors>

<adversarial-stance>
Assume the change is wrong until the code proves it right; name the evidence behind every "safe" verdict. Prompts: **reference/review-dimensions.md**.
</adversarial-stance>
</knowledge>

<capabilities>

<gathering-review-context>
**Objective**: Establish clear understanding of what to review and why.

**Process**:
1. **Identify review scope**:
   - Single file review: Focus on that file in isolation
   - Multiple files: Consider interactions and integration points
   - Diff/commit: Review the full changed files plus every caller and callee of changed symbols, not just the changed hunks
   - Folder/module: Review module cohesion, interfaces, and architecture
   - Branch diff or pull request: Obtain the checkout first (see **preparing-review-checkout**)
   
2. **Understand intent and context**:
   - What changed and why (bug fix, feature, refactor, optimization)
   - Expected behavior and requirements
   - Related files or systems that may be affected
   
3. **Gather necessary context**:
   - Read referenced files to understand dependencies
   - Check tests to understand expected behavior
   - Review related documentation if available
   - If critical context is missing, ask the user before proceeding

4. **Prioritize review focus**:
   - For bug fixes: Focus on correctness, edge cases, and test coverage
   - For features: Focus on requirements alignment, API design, and extensibility
   - For refactors: Focus on maintainability, test preservation, and behavior equivalence
   - For optimizations: Focus on performance validation, benchmarks, and edge case handling
   - For documents: Focus on structure, clarity, completeness, accuracy, and target-audience alignment
</gathering-review-context>

<preparing-review-checkout>
**Objective**: Materialize the code under review in a dedicated worktree so the review sees the whole change, not just the patch.

**Steps**:
1. Identify the input variant: two branches, one branch, a pull request, or uncommitted changes.
2. Load [reference/review-checkout.md](reference/review-checkout.md) via the **context-loading-guide**, detect the local worktree location convention, and run the fetch and worktree commands for that variant.
3. Diff the head against its merge base with the target branch, never against the target tip, and never move HEAD on the current checkout.
4. Review from inside the worktree so full files, call sites, tests, and configuration are readable.
5. Remove the worktree and the temporary branch when the review ends.
</preparing-review-checkout>

<conducting-code-review>
**Objective**: Systematically analyze code for correctness, quality, and risks by assuming the change is broken.

**Steps**:
1. Apply **adversarial-stance**: state a failure hypothesis per changed behavior, and read each changed file in full to diff behavior, not text.
2. Load [reference/review-dimensions.md](reference/review-dimensions.md) via the **context-loading-guide** and apply dimension 10 — enumerate every caller, implementation, contract, and downstream consumer of each changed symbol.
3. Walk each changed behavior through the dimension-10 **Failure-mode enumeration** table, marking every mode `verified` or `not verified` with the reason, then run the **Negative space** pass for omitted artifacts.
4. Re-read the change once as an attacker and once as a careless maintainer; log at least one new hypothesis per changed function.
5. Apply dimensions 1–9, evaluating every relevant ✓ item, and apply **review-efficiency** strategies to prioritize findings by risk and impact.
6. For each violation, load [reference/severity-levels.md](reference/severity-levels.md) via the **context-loading-guide**, assign a severity, and prepare a finding with a **Confidence** label plus Issue, Impact, and Recommendation fields.
7. For dimension 8 (Inconsistencies): capture every conflicting pattern with both variants and concrete anchors; note trade-offs and flag for a user decision — do not silently pick one.
8. Load [reference/finding-anchors.md](reference/finding-anchors.md) via the **context-loading-guide** and anchor every finding to exactly one `path:LINE` with the verbatim anchored line quoted beneath it.
9. Load [reference/review-output-format.md](reference/review-output-format.md) via the **context-loading-guide** and format all findings using the standard template.
10. Load the appropriate example from the **context-loading-guide** table for output structure guidance.
11. **Validate output**: Verify (a) every finding carries one `path:LINE` anchor, the quoted line, a severity label, and a Confidence label; (b) suspicions keep the evidence that would confirm or refute them; (c) Failure Modes Checked and Positive Highlights are present; (d) no empty severity sections; (e) each inconsistency entry includes both variants and a decision request; (f) every finding has a concrete Recommendation, Issue, and Impact passing the non-expert test; (g) the merge verdict is present.
</conducting-code-review>

<reviewing-document>
**Objective**: Evaluate a document (README, design doc, ADR, specification, runbook, etc.) for clarity, completeness, structure, and accuracy.

**Steps**:
1. Read the full document to understand its purpose, target audience, and scope.
2. Evaluate **structure**: clear logical flow, expected section order for the document type, consistent heading levels.
3. Evaluate **clarity**: unambiguous language, technical terms defined, examples for complex concepts.
4. Evaluate **completeness**: all required sections present (purpose, prerequisites, setup, usage) and no unexplained gaps or placeholders.
5. Evaluate **accuracy**: code samples match behavior; versions and commands are current.
6. Evaluate **audience alignment**: match the depth to the intended reader and keep jargon appropriate.
7. Apply the document-relevant **conducting-code-review** dimensions: correctness, maintainability, and inconsistencies.
8. Apply the **Negative space** pass to the document: name each section the document type requires but does not contain.
9. Anchor every finding to one line per **finding-anchors**, adding the section heading for long documents, then format findings per [reference/review-output-format.md](reference/review-output-format.md) and **examples/doc-review.md**.
10. **Validate output**: Verify every finding has an anchor, a severity, a Confidence label, and an actionable Recommendation, and that the document-level verdict is present.
</reviewing-document>

</capabilities>

<rules>
<rule>When the user submits files, folders, diffs, or commits for review, first apply **gathering-review-context**, then **conducting-code-review** with its change-context, failure-mode, and adversarial passes.</rule>
<rule>When the user supplies branch names, a pull request, or uncommitted changes, first apply **preparing-review-checkout** to materialize the full change in a worktree, then apply **conducting-code-review** from inside it. Always review every changed file — never skip any.</rule>
<rule>When the subject of review is a document (README, ADR, design doc, specification, runbook, etc.), use **reviewing-document** instead of **conducting-code-review**.</rule>
<rule>When presenting review findings, anchor each one to a single line per **finding-anchors** and give it a Confidence label plus concrete plain-language Issue, Impact, and Recommendation fields.</rule>
<rule>When a finding is suspected but unproven, still report it — label it Suspected or Needs runtime check with the evidence that would confirm or refute it.</rule>
<rule>When a large review spans several independent changed modules or documents, apply `fan-out-agents` to dispatch parallel review clones and merge their findings.</rule>
</rules>