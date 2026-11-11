````markdown
# Example: Document Review (README)

**Scenario**: Review of `services/payment-service/README.md` for a new microservice being onboarded to the platform.

**Applies**: **reviewing-document**

## Code Review Summary

**Scope**: `services/payment-service/README.md` — new microservice README
**Focus Areas**: Structure, completeness, accuracy, audience alignment
**Reviewed**: 1 file — `services/payment-service/README.md` (127 lines)
**Overall Assessment**: Needs work before the service is onboarded — critical setup steps are missing and one command is incorrect.
**Ready to merge?**: With fixes — the documented setup cannot succeed as written
**Repo expertise**: `CONTRIBUTING.md`, `services/payment-service/` sources
**Open challenges**: 0 open, 0 blocking · **Unverified referents**: 0

---

## Findings

> Severity legend: 🚫 Blocker = must fix before merge · 🔴 Major = should fix · 🟡 Minor = nice to fix · 🟢 Nit = polish · ⚠️ Inconsistency = decision required

### 🔴 Major Issues

#### Missing Prerequisites Section
- **File**: `services/payment-service/README.md:1 (after — add a Prerequisites section here)`
- **Confidence**: Confirmed
- **Issue**: No prerequisites section — the README jumps to "Getting Started" without listing Java 21, Docker, or the AWS CLI, so onboarding fails on cryptic tool errors.
- **Impact**: Onboarding friction; developers waste time debugging missing tools rather than running the service.
- **Recommendation**: Add a **Prerequisites** section before "Getting Started":
```markdown
## Prerequisites
- Java 21 (install via `sdk use java 21`)
- Docker ≥ 24.0
- AWS CLI v2 configured with the `dev` profile
- Access to the internal package registry (see [confluence/registry-access](…))
```

#### Incorrect `docker-compose` Command
- **File**: `services/payment-service/README.md:34`
- **Confidence**: Confirmed
```bash
34 │ docker-compose up -d
```
- **Issue**: The "Local Development" section uses `docker-compose up` but the project uses Compose V2 (`docker compose up`). The legacy command fails silently on macOS with Docker Desktop ≥ 4.18.
- **Impact**: Local setup fails on all modern developer machines; the error message is unrelated to the root cause.
- **Recommendation**: Replace every `docker-compose` occurrence with `docker compose` and add a note on the minimum Docker Desktop version required.

---

### 🟡 Minor Issues

#### Environment Variable Table Is Incomplete
- **File**: `services/payment-service/README.md:52`
- **Confidence**: Confirmed
- **Issue**: The table lists 8 variables; `application.yaml` declares 12 — `PAYMENT_RETRY_MAX_ATTEMPTS`, `PAYMENT_TIMEOUT_MS`, `STRIPE_WEBHOOK_SECRET`, `DB_POOL_SIZE` are absent.
- **Impact**: Developers miss required configuration and encounter startup failures with no guidance on what is missing.
- **Recommendation**: Audit `application.yaml` and synchronize the README table. Consider generating the table from code comments to prevent future drift.

#### "Deployment" Section Describes the Old Pipeline
- **File**: `services/payment-service/README.md:80`
- **Confidence**: Confirmed
- **Issue**: The deployment section references Jenkins pipeline steps, but the project migrated to GitHub Actions in Q3 2025. The Jenkins URL is no longer valid.
- **Impact**: Confusing for anyone following the deployment runbook; could lead to failed or duplicate deployments.
- **Recommendation**: Update to describe the GitHub Actions workflow (`.github/workflows/deploy.yml`) and remove all Jenkins references.

---

### 🟢 Nits / Suggestions

#### Architecture diagram is hard to scan at scale
- **File**: `services/payment-service/README.md:22`
- **Confidence**: Confirmed
- **Issue**: The ASCII diagram is unreadable on narrow screens and does not render in the wiki.
- **Impact**: Readers skip the only structural overview of the service.
- **Recommendation**: Replace it with a Mermaid diagram so GitHub and the wiki render it.

#### Section headings use mixed capitalization
- **File**: `services/payment-service/README.md:11`
- **Confidence**: Confirmed
- **Issue**: Headings vary between "Getting Started", "local development", and "API Reference".
- **Impact**: Cosmetic inconsistency only; navigation is unaffected.
- **Recommendation**: Standardize to title case throughout.

#### Contributing section may link to a stale target
- **File**: `services/payment-service/README.md:96`
- **Confidence**: Suspected
- **Issue**: The section is one line linking to a global `CONTRIBUTING.md`; the link was not followed.
- **Impact**: Onboarding readers hit a dead end if the global file moved.
- **Recommendation**: Verify the link resolves, then leave the pointer as is.

---

## Positive Highlights
- The API reference table (endpoints, methods, descriptions) is well-structured and covers all public routes.
- The troubleshooting section with common errors and fixes is a strong onboarding aid — this kind of section is frequently missing in microservice READMEs.
- Clear separation between "local development" and "integration testing" environments reduces confusion about which setup to follow.

---

## Risks & Assumptions
- Review is based on the README alone; accuracy of commands was cross-checked against `docker-compose.yml` and `application.yaml` but not against actual runtime behavior.
- The environment variable gap may indicate the README is not updated as part of the feature workflow — a process gap, not just a one-time fix.

---

## Recommended Next Steps
1. Add Prerequisites section (required before service onboarding)
2. Fix `docker-compose` → `docker compose` command (required — blocks local setup on modern machines)
3. Complete the environment variable table (required — blocks successful startup)
4. Update Deployment section to reflect the GitHub Actions pipeline (required)
5. Standardize heading capitalization (minor polish)
6. Consider adding a PR checklist item: "Did you update the README?" to prevent future drift

````
