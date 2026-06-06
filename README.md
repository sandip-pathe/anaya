# Anaya

Anaya is a policy-as-code engine for compliance scanning. The V1 direction is a shared deterministic engine with two product surfaces:

- CLI: local and CI usage through `anaya scan`
- GitHub App: pull request checks, annotations, and SARIF output

This folder is the clean Anaya foundation. The older `rbi-compliance-scanner` folder remains a prototype/reference, mainly useful for GitHub App auth and webhook signature code.

## Current Scope

- Load rule packs from YAML
- Run deterministic pattern rules against source files
- Emit table, JSON, or SARIF-style output from the CLI
- Ship one initial generic rule pack for secret detection

## Quick Start

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .[dev]
anaya scan ..\fintech-demo --format table
```

Without installing the console script:

```bash
python -m cli.main scan ..\fintech-demo --format json
```

## Commands

```bash
anaya scan PATH
anaya init
anaya validate-pack anaya\packs\generic\secrets-detection.yml
anaya packs list
```

## Repository Config

`anaya scan` auto-discovers `anaya.yml` from the scanned path or its parents.
Use `--config path\to\anaya.yml` to choose a specific config file.

## Status

This is the Phase 1/Phase 3 skeleton from `ANAYA_SPEC.py`: engine models, rule loader, pattern scanner, and CLI. GitHub App, Check Runs, async workers, AST scanning, and LLM fallback are intentionally not wired yet.
