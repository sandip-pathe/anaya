# Anaya

Anaya is a policy-pack-agnostic compliance-as-code engine. The V1 direction is a shared deterministic engine with two product surfaces:

- CLI: local and CI usage through `anaya scan`; this is OSS, similar in spirit to Semgrep
- GitHub App: pull request checks, annotations, and SARIF output

The OSS repository is licensed under AGPL-3.0-or-later.

This folder is the clean Anaya foundation. The older `rbi-compliance-scanner` folder remains a prototype/reference, mainly useful for GitHub App auth and webhook signature code.

## Current Scope

- Load rule packs from YAML
- Load built-in or user-authored external policy packs
- Run deterministic pattern rules against source files
- Emit table, JSON, or SARIF-style output from the CLI
- Ship five generic OSS packs for secrets, OWASP, PII handling, TLS, and audit logging
- Include an experimental India DPDP privacy pack for early policy-pack testing
- Cover 29 built-in rules with Python and JavaScript fixture tests
- Provide a FastAPI GitHub App foundation with webhook verification, PR scanning, Check Run updates, and optional SARIF upload
- Support optional OpenAI-backed `type: llm` rules, disabled by default and guarded by repository opt-in

## Quick Start

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .[dev]
anaya scan . --no-config --format table
```

Without installing the console script:

```bash
python -m anaya.cli.main scan . --no-config --format json
```

## Commands

```bash
anaya scan PATH
anaya scan PATH --diff HEAD~1
anaya scan PATH --format sarif -o anaya.sarif
anaya scan PATH --format audit-json
anaya scan PATH --format check-run
anaya test-rule --rule ANAYA-SEC-001 --file app.py
anaya init
anaya validate-pack anaya\packs\generic\secrets-detection.yml
anaya validate-pack anaya\packs\india\dpdp-privacy.yml
anaya packs list
```

Custom packs are first-class:

```bash
anaya scan . --pack path\to\my-policy-pack.yml
```

Pack paths in `anaya.yml` are resolved relative to the config file.

Diff scans are supported for local Git worktrees:

```bash
anaya scan . --diff origin/main
```

## Repository Config

`anaya scan` auto-discovers `anaya.yml` from the scanned path or its parents.
Use `--config path\to\anaya.yml` to choose a specific config file.

Repository config can choose packs, thresholds, ignored paths, ignored rule IDs, and language filters:

```yaml
scan:
  languages: [python, javascript]

ignore:
  rules:
    - ANAYA-SEC-006
```

Configured packs, thresholds, languages, and ignored rule IDs are validated before scanning.

Optional OpenAI-backed rules require explicit repository opt-in:

```yaml
llm:
  enabled: true
```

LLM rules are skipped with a warning when OpenAI is not configured. See
`docs/LLM_RULES.md` for the rule schema, safety limits, and data-handling notes.

## Status

This is the Phase 1/Phase 3/Phase 4/Phase 5 foundation from `ANAYA_SPEC.py`: engine models, rule loader, pattern and Python AST scanners, repository config, reporters, tested generic packs, OSS CLI, in-process GitHub App PR scanning, and optional OpenAI-backed LLM judging. Redis/Celery hosted queueing, retry hardening, JavaScript AST scanning, and deployment/demo readiness are intentionally not wired yet.

## Development

```bash
python -m pip install -e .[dev]
python -m pytest
python -m pytest --cov
python -m ruff check .
```

The same commands are wrapped in the repository `Makefile` for contributors who have `make` installed.

For human product checks after automated tests pass, see `docs/MANUAL_CHECKS.md`.
For the full engineering handoff, see `docs/TECHNICAL_ARCHITECTURE.md`.
For GitHub Actions SARIF upload, see `docs/GITHUB_ACTION.md`.
For local GitHub App API setup, see `docs/GITHUB_APP.md`.
For optional OpenAI-backed rules, see `docs/LLM_RULES.md`.
For PyPI releases, see `docs/PYPI_RELEASE.md`.
For Azure VM hosting, see `docs/AZURE_VM_DEPLOYMENT.md`.
For Railway hosting, see `docs/RAILWAY_DEPLOYMENT.md`.
For the public/private repository split, see `docs/REPOSITORY_STRATEGY.md`.
