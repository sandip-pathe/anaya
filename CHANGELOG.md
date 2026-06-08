# Changelog

All notable changes to Anaya will be documented in this file.

The format follows Keep a Changelog, and this project uses semantic versioning once public releases begin.

## [Unreleased]

No unreleased changes.

## [1.1.1] - 2026-06-09

### Fixed

- Added `anaya --version` for predictable CLI/package verification.
- Escaped table output on legacy Windows console encodings instead of crashing
  when scanned files contain characters the active code page cannot print.
- Added `pytest-asyncio` to developer dependencies so GitHub App async tests run
  in CI.

### Added

- OSS Anaya CLI foundation.
- Policy-pack-agnostic rule loading.
- Built-in generic packs for secrets, OWASP patterns, PII handling, and TLS.
- External custom pack support.
- Table, JSON, and SARIF-style output.
- Security and implementation planning docs.
- Diff-file scanning with `anaya scan --diff REF`.
- Engine summary metadata for checked rules, skipped files, config path, and pack versions.
- Repository config validation for packs, thresholds, languages, ignored rules, and scan mode.
- Rule-pack validation for SemVer versions, duplicate rule IDs, references, tags, and languages.
- Config-driven language filtering and inline suppression variants.
- `anaya test-rule` for pack authoring and rule debugging.
- Generic audit logging pack.
- Expanded generic pack matrix to 5 packs and 26 deterministic rules.
- Python and JavaScript dirty/clean fixture matrix with exact expected rule ID tests.
- Table output metadata for config path, pack versions, skipped files, and no-finding scans.
- JSON and SARIF reporter contract tests.
- Audit JSON, GitHub Check Run, and PR comment reporters.
- SARIF automation details, invocation metadata, stable fingerprints, and schema contract validation.
- Python AST scanner for function-level missing-call rules.
- Structural audit rules for missing transaction, authentication, and deletion audit calls.
- GitHub Actions SARIF upload guide.
- FastAPI GitHub App foundation with health and webhook endpoints.
- GitHub webhook HMAC-SHA256 signature verification.
- GitHub App JWT, installation token, Check Run, PR file list, and content-fetch client helpers.
- Pull request webhook handling for opened, reopened, and synchronize events.
- GitHub App local setup documentation.
- In-process pull request scan worker for GitHub App mode.
- GitHub PR file fetching, trusted base-branch config loading, and custom pack fetching.
- Check Run completion updates with batched annotations.
- Optional SARIF upload through GitHub Code Scanning API.
- Optional OpenAI-backed `type: llm` rules with repository opt-in.
- LLM judge prompt/schema modules, structured JSON decisions, warning-only failure handling, and mocked tests.
- Scan warnings surfaced in table, audit JSON, PR comment, and Check Run outputs.
- Experimental `india/dpdp-privacy` pack with DPDP Act aligned privacy and data-protection signals.

### Changed

- Anaya product direction locked to OpenAI for future optional LLM support.
- Starter `anaya.yml` now includes all default OSS generic packs.
- Generic audit logging pack now includes both explicit-bypass pattern rules and Python structural rules.
- Runtime settings support raw `ANAYA_GITHUB_PRIVATE_KEY` as well as private-key file paths.
- Project metadata now targets the public AGPL-licensed OSS release line.

### Security

- Fresh Anaya repository initialized without committed runtime secrets.
