# Repository Strategy

Anaya should start with one public repository and split only when there is real
private product surface to protect.

## Now: One Public OSS Repo

Use `sandip-pathe/anaya` for:

- Policy engine
- CLI
- Rule-pack schema and loader
- Built-in OSS packs
- Reporters
- GitHub Action/SARIF integration
- GitHub App API foundation
- Public docs and examples

This keeps the engine credible and easy to adopt. The CLI is the wedge: users
can install Anaya, run `anaya scan .`, and author their own packs without asking
for hosted access.

## Later: Add A Private Platform Repo

Create a private `anaya-platform` repository when we add:

- Tenant/account model
- Billing and GitHub Marketplace plan handling
- Hosted dashboard
- Proprietary policy packs
- Customer-specific pack distribution
- Queue workers and operational infrastructure
- Admin/support tooling
- Private deployment manifests and secrets templates

The private platform should consume the public engine as a package dependency,
not copy engine code. If private changes expose missing engine extension points,
add those extension points back to the OSS repo intentionally.

## Boundary

Public AGPL repo:

- What the scanner is
- How policies are represented
- How findings are generated
- How developers can run it locally or in CI

Private platform repo:

- How Anaya is sold, operated, customized, and managed for customers
- Private packs and pack distribution controls
- Hosted multi-tenant concerns

This gives investors a clean story: open source drives trust and distribution;
the hosted platform monetizes convenience, governance, proprietary packs, and
enterprise workflow.
