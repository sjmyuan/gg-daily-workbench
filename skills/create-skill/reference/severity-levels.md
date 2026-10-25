# Severity Levels

Scope: labels for reporting a finding about an authored skill. The reviewer owns the
audit-side usage; this copy carries the legend.

| Level | Symbol | Use when |
|---|---|---|
| Blocker | 🚫 | The skill cannot load, activate, or produce correct output in most realistic scenarios |
| Major | 🔴 | The violation breaks the agent in at least one realistic scenario |
| Minor | 🟡 | Quality drops; the common case still works |
| Nit | 🟢 | Cosmetic — naming, wording, style |
| Inconsistency | ⚠️ | Two conflicting patterns; present both and ask the user |

- 🚫 Blocker: no capability, missing frontmatter, absent `<when-to-use-this-skill>`.
- 🔴 Major: breaks a specific but realistic scenario.
- Every finding carries a severity and an actionable fix.
