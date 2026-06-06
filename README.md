# Anaya

Anaya is a policy-pack-agnostic compliance-as-code engine. The V1 direction is a shared deterministic engine with two product surfaces:

- CLI: local and CI usage through `anaya scan`; this is OSS, similar in spirit to Semgrep
- GitHub App: pull request checks, annotations, and SARIF output

This folder is the clean Anaya foundation. The older `rbi-compliance-scanner` folder remains a prototype/reference, mainly useful for GitHub App auth and webhook signature code.

## Current Scope

- Load rule packs from YAML
- Load built-in or user-authored external policy packs
- Run deterministic pattern rules against source files
- Emit table, JSON, or SARIF-style output from the CLI
- Ship five generic OSS packs for secrets, OWASP, PII handling, TLS, and audit logging
- Cover 26 built-in rules with Python and JavaScript fixture tests

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

## Status

This is the Phase 1/Phase 3/Phase 4 foundation from `ANAYA_SPEC.py`: engine models, rule loader, pattern scanner, repository config, reporters, tested generic packs, and OSS CLI. GitHub App, Check Runs, async workers, AST scanning, and OpenAI-based optional LLM fallback are intentionally not wired yet.

## Development

```bash
python -m pip install -e .[dev]
python -m pytest
python -m pytest --cov
python -m ruff check .
```

The same commands are wrapped in the repository `Makefile` for contributors who have `make` installed.

For human product checks after automated tests pass, see `docs/MANUAL_CHECKS.md`.
For GitHub Actions SARIF upload, see `docs/GITHUB_ACTION.md`.
