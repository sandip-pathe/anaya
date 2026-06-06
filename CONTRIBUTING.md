# Contributing To Anaya

Thanks for helping make Anaya useful and trustworthy.

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .[dev]
```

On macOS/Linux, use:

```bash
python -m venv .venv
./.venv/bin/python -m pip install -e '.[dev]'
```

## Checks

```bash
python -m pytest
python -m pytest --cov
python -m ruff check .
python -m ruff format .
```

## Rule Pack Contributions

Anaya is policy-pack agnostic. Built-in and user-authored packs use the same YAML schema.

For every rule, include:

- one dirty fixture that should trigger
- one clean fixture that should pass
- one edge case, such as suppression or placeholder values

See [docs/PACK_AUTHORING.md](docs/PACK_AUTHORING.md).

## Security

Never commit secrets, private keys, or `.env` files. See [SECURITY.md](SECURITY.md).

## Pull Request Expectations

- Keep changes scoped.
- Add or update tests for behavior changes.
- Run tests and Ruff before sending.
- Prefer deterministic scanner behavior over OpenAI-assisted checks.
