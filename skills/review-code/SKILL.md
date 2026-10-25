---
name: review-code
description: Review code and documents for correctness, security, performance, and blast radius; raise unreasonable changes as blocking challenges. Use when requesting reviews, bug hunting, or checking changes against repo conventions.
---

<when-to-use-this-skill>
- A user or another agent requests a code review of files, folders, diffs, commits, or pull requests
- User asks for feedback on code quality, security, performance, or maintainability
- User supplies one or two branch names for comparison
- User asks to review a document (README, design doc, ADR, specification, runbook)
- User asks whether a change is safe, or wants potential bugs and failure modes surfaced
- A change looks unreasonable — misplaced, misnamed, out of scope, or restructured without evidence
- A review must apply the target repo's own conventions, ADRs, or known constraints
</when-to-use-this-skill>

<knowledge>
<named-standards>
| Standard | Rule | Details |
|---|---|---|
| **referent-grounding** | Every path, package, symbol, flag, and config key resolves in the tree or is labeled `unverified`. | **reference/referent-grounding.md** |
| **challenge-taxonomy** | An assumption adopted to keep reviewing becomes a challenge, never a silent premise. | **reference/challenge-taxonomy.md** |
| **repo-expertise** | The repo's documented rules outrank reviewer taste; silent sources are reported, never guessed. | **reference/repo-expertise.md** |
| **finding-anchors** | Every finding anchors to one `path:LINE` with the verbatim line quoted beneath it. | **reference/finding-anchors.md** |
| **severity-and-confidence** | Severity per the rubric; Confidence on its own axis; a blocking challenge overrides the verdict. | **reference/severity-levels.md** |
</named-standards>

<context-loading-guide>
Load on demand — one row per trigger.

| Load when | Provides | File |
|---|---|---|
| Before starting a review | Conduct rules | [reference/reviewer-conduct.md](reference/reviewer-conduct.md) |
| Surveying the repo's own rules | Source priority, evidence card | [reference/repo-expertise.md](reference/repo-expertise.md) |
| About to name a path, move, or destination | Referent ledger, move proof | [reference/referent-grounding.md](reference/referent-grounding.md) |
| About to judge whether a change is reasonable | Probes, challenge record, blocking | [reference/challenge-taxonomy.md](reference/challenge-taxonomy.md) |
| About to apply review dimensions | 10 dimensions, failure modes | [reference/review-dimensions.md](reference/review-dimensions.md) |
| About to assign severity or confidence | Severity and confidence rubric | [reference/severity-levels.md](reference/severity-levels.md) |
| About to anchor a finding | One-line anchors, PR-inline mode | [reference/finding-anchors.md](reference/finding-anchors.md) |
| About to write the report | Report and challenge template | [reference/review-output-format.md](reference/review-output-format.md) |
| Scoping a review under time pressure | Risk ordering, call-graph bounding | [reference/review-efficiency.md](reference/review-efficiency.md) |
| Retrieving branches, PRs, or uncommitted code | Worktree, refspecs, merge base | [reference/review-checkout.md](reference/review-checkout.md) |
| Probing a change for hidden bugs | Blast-radius and failure-mode example | [examples/change-context-probe.md](examples/change-context-probe.md) |
| Challenging a move, placement, or restructure | Worked challenge on an invented path | [examples/unreasonable-change-challenge.md](examples/unreasonable-change-challenge.md) |
| A change may violate documented repo rules | Worked card that changes a severity | [examples/repo-expertise-grounding.md](examples/repo-expertise-grounding.md) |
| Reviewing a diff, commit, or bug fix | Output example | [examples/diff-commit-review.md](examples/diff-commit-review.md) |
| Comparing two branches | Output example | [examples/branch-diff-review.md](examples/branch-diff-review.md) |
| Reviewing a pull request | PR worktree example | [examples/pull-request-review.md](examples/pull-request-review.md) |
| Reviewing a performance change | Output example | [examples/performance-improvement.md](examples/performance-improvement.md) |
| Reviewing a document | Output example | [examples/doc-review.md](examples/doc-review.md) |
| Reviewing a migration, endpoint, or cache | Deployment-safety example | [examples/deployment-safety-review.md](examples/deployment-safety-review.md) |
| Writing plain-language findings | Terse → explained example | [examples/plain-language-findings.md](examples/plain-language-findings.md) |
</context-loading-guide>

</knowledge>

<capabilities>
<gathering-review-context>
**Objective**: Establish what to review, why, and under which interpretation.

**Steps**:
1. Classify the scope: single file, files with integration points, diff with callers, or a folder's interfaces.
2. Obtain the checkout for a branch diff or pull request per **preparing-review-checkout**.
3. State the intent — fix, feature, refactor, optimization, document — and where it came from.
4. Read the referenced files, tests, and documentation the change depends on.
5. Prioritize by change type — correctness, requirements, equivalence, benchmarks, structure.
6. **Validate**: scope, intent, and missing context are written before analysis; each gap becomes a challenge.
</gathering-review-context>

<preparing-review-checkout>
**Objective**: Materialize the code under review in a dedicated worktree so the review sees the whole change.

**Steps**:
1. Identify the input variant — two branches, one branch, a pull request, or uncommitted changes.
2. Load [review-checkout.md](reference/review-checkout.md), detect the convention, and run that variant's commands.
3. Diff the head against its merge base, never the target tip; never move HEAD on the current checkout.
4. Review inside the worktree so full files, call sites, tests, and configuration are readable.
5. Remove the worktree and temporary branch when the review ends.
6. **Validate** against the checklist in [review-checkout.md](reference/review-checkout.md) before reporting.
</preparing-review-checkout>

<surveying-repo-expertise>
**Objective**: Build an evidence-backed card of the target repo's own rules before judging the change.

**Steps**:
1. List the repo's expertise sources in the priority order of **repo-expertise**.
2. Read only the sources governing the changed area — conventions, decisions, commands, known debt.
3. Record one card row per fact with its `path:LINE`; no source, no row.
4. Cite the card row when a finding rests on a convention, naming the rule, not "project style".
5. Record absent or silent sources as gaps and promote each gap per **challenge-taxonomy**.
6. **Validate**: every convention-based finding cites a card row; every gap is a challenge or labeled assumption.
</surveying-repo-expertise>

<challenging-the-change>
**Objective**: Convert every unverified premise into a visible, prioritized challenge instead of a silent guess.

**Steps**:
1. State the intent hypothesis — what the change appears to do, and which intent would invalidate the review.
2. Ground every referent per **referent-grounding**: resolve it, or label it `unverified` with the failed search.
3. Apply the **challenge-taxonomy** probes to the change's structure, not only its behavior.
4. Record a challenge per failing probe: question, why, assumption held, what settles it, `Blocking`.
5. Probe each challenge resting on a repo claim with `question-everything`'s six dimensions, keeping its `C<N>` ids.
6. Rank by blocking status, then impact; never drop a challenge for lack of context.
7. **Validate**: every assumption appears as a challenge; no move or placement recommendation lacks cited evidence.
</challenging-the-change>

<conducting-code-review>
**Objective**: Analyze code for correctness and risk by assuming the change is broken and its shape unproven.

**Steps**:
1. State the intent hypothesis and a failure hypothesis per changed behavior; read each changed file in full.
2. Load the expertise card per **surveying-repo-expertise** and record its gaps before judging placement.
3. Apply dimension 10 of [review-dimensions.md](reference/review-dimensions.md) — every caller, contract, consumer.
4. Walk each behavior through the **Failure-mode enumeration** and **Negative space** passes, naming each search.
5. Re-read once as an attacker and once as a careless maintainer; log one new hypothesis per changed function.
6. Apply dimensions 1–9 to every relevant ✓ item, prioritizing by risk per **review-efficiency**.
7. Apply **challenging-the-change** to the change's structure and record the resulting challenges.
8. Assign severity per **severity-and-confidence** and prepare Issue, Impact, Recommendation, and Confidence.
9. For dimension 8, capture both variants with anchors and trade-offs, then request a decision.
10. Anchor each finding per **finding-anchors**.
11. Format the report per [review-output-format.md](reference/review-output-format.md), loading a matching example.
12. **Validate**: (a) one anchor, quoted line, severity, and Confidence per finding; (b) every referent grounded;
    (c) blocking challenges set the verdict; (d) Failure Modes Checked and Positive Highlights present;
    (e) no empty severity sections; (f) non-expert test passed; (g) merge verdict present.
</conducting-code-review>

<reviewing-document>
**Objective**: Evaluate a document for clarity, completeness, structure, and accuracy.

**Steps**:
1. Read the full document; state its purpose, audience, and scope.
2. Evaluate structure, clarity, completeness, accuracy, and audience alignment against its type's sections.
3. Apply the correctness, maintainability, and inconsistency dimensions plus the **Negative space** pass.
4. Ground every path, command, version, and config key the document cites per **referent-grounding**.
5. Record claims the document makes about code you did not read as challenges.
6. Anchor per **finding-anchors** and **Validate** each finding carries a severity, Confidence, and Recommendation.
</reviewing-document>
</capabilities>

<rules>
<rule>When the user submits files, folders, diffs, or commits, apply **gathering-review-context**, then **conducting-code-review**.</rule>
<rule>When the user supplies branches, a pull request, or uncommitted changes, apply **preparing-review-checkout** then review inside it; skip no changed file.</rule>
<rule>When the subject is a document, apply **reviewing-document** instead of **conducting-code-review**.</rule>
<rule>When reviewing any repository, apply **surveying-repo-expertise** before judging conventions, placement, or severity.</rule>
<rule>When a change looks unreasonable or two readings would change the verdict, apply **challenging-the-change**; never normalize it silently.</rule>
<rule>When naming a path, package, symbol, flag, or config key, ground it per **referent-grounding** — never from a branch or ticket name.</rule>
<rule>When presenting findings, anchor each per **finding-anchors** and add a Confidence label, Issue, Impact, and Recommendation.</rule>
<rule>When a finding is suspected but unproven, report it at its true confidence, naming the evidence that would confirm or refute it.</rule>
<rule>When a challenge questions a claim returned by another agent rather than the change itself, hand the claim to `question-everything`.</rule>
<rule>When a large review spans independent modules or documents, apply `fan-out-agents` and merge the returned findings.</rule>
</rules>
