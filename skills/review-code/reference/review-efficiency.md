# Review Efficiency

Strategies for maximizing review value while respecting time constraints.

- **Prioritize by risk**: security, correctness, and data integrity first
- **Read changed files in full**: the enclosing function, class, and module hold the context the hunk omits
- **Bound by call graph, not by diff**: trace every caller and callee of a changed symbol; skip unrelated subsystems
- **Leverage existing validations**: note when linters and type-checkers already caught an issue
- **Batch similar findings**: replace 10 naming findings with one pattern finding carrying several anchors
- **Distinguish patterns from instances**: flag the pattern once with multiple examples
- **Skip overcrowded areas**: above 5 major issues in one area, flag it as needing a broader refactor
- **Balance depth vs. breadth**: deep-dive on critical sections, skim lower-risk areas
- **Trust tests**: when comprehensive tests exist and pass, shift focus to test quality
- **Scan the whole visible codebase for inconsistencies**: surface conflicting solutions to the same problem together
- **Treat all code as suspect**: existing code may be legacy, copy-pasted, or wrong — "it matches the existing code" is never a reason to approve
