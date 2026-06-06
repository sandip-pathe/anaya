# Changelog

All notable changes to Anaya will be documented in this file.

The format follows Keep a Changelog, and this project uses semantic versioning once public releases begin.

## [Unreleased]

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

### Changed

- Anaya product direction locked to OpenAI for future optional LLM support.
- Starter `anaya.yml` now includes all default OSS generic packs.

### Security

- Fresh Anaya repository initialized without committed runtime secrets.
