# Challenge Taxonomy

A challenge is a question the reviewer could not settle from the repo. It is not a finding and not
a risk bullet — it needs an answer from the requester before the verdict is trustworthy.

## Reasonableness probes

Run every probe against the change's **structure**, not only its behavior. A probe that passes needs
no output; a probe that fails or cannot be settled becomes a challenge.

| Probe | Question | Raise when |
|---|---|---|
| Placement | Does this code belong in this package, layer, and module? | A move or new directory has no cited rule |
| Path derivation | Was this path read, or completed from a feature name? | A segment matches the branch, not the tree |
| Naming | Does it use the domain language the repo already uses? | A synonym appears where the repo settled one term |
| Scope | Does the change do what its stated intent says, no more and no less? | Unrelated edits, or intent the diff does not deliver |
| Duplication | Does an equivalent already exist? | A second implementation of a solved problem |
| Abstraction | Is a new abstraction justified by more than one use? | An interface, base class, or option added for one caller |
| Data model | Is a new field, table, or state actually required? | Stored state that could be derived |
| Sequencing | Does it depend on something not yet merged or deployed? | A prerequisite absent from the change |
| Reversibility | Can this be undone without data loss? | A destructive or one-way operation inside a feature |
| Requirement conflict | Does it contradict a documented requirement or ADR? | The repo says otherwise |

## Challenge record

| Field | Content |
|---|---|
| `C<N>` | Sequential id; reuse **question-everything**'s id when that skill raised it |
| Question | One sentence the requester can answer |
| Why it looks unreasonable | The concrete signal, with `path:LINE` or the failed search |
| Assumed meanwhile | What the review did while unresolved, and which findings depend on it |
| Settles it | The document, rule, or answer that closes it |
| Blocking | `yes`, `no`, or `maybe` |

## Blocking rules

| Blocking | Verdict effect |
|---|---|
| `yes` | Verdict becomes `No` or `With fixes` until answered |
| `maybe` | Verdict may stand; state that the answer can still flip it |
| `no` | Advisory; listed, never dropped |

## Delegation

| The challenge questions | Hand off |
|---|---|
| A claim another agent returned — a report, a plan, a diagnosis | `question-everything` |
| The change under review itself | Keep it — this review owns it |
| A requirement the requester supplied | Ask the requester, never the author's agent |

## Never

- Raise a challenge about generated, vendored, or already-deprecated code
- Restate a finding as a challenge — a challenge has no known defect yet
- Soften a challenge because context is missing; missing context is the reason it is raised
- Drop an unanswered challenge, or answer it yourself when the repo is silent
- Present a restructure, move, or extraction as a finding without cited evidence

## Validation

- [ ] Every probe was run against structure, not only behavior
- [ ] Every unresolved premise appears exactly once, with an id
- [ ] Every challenge names what settles it
- [ ] Every `Blocking: yes` challenge is reflected in the verdict
- [ ] The assumed findings are named, so the requester can see what changes on an answer
