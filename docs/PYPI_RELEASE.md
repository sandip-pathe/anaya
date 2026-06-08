# PyPI Release Runbook

Anaya publishes the OSS CLI package under the existing `anaya` PyPI project.
The old PyPI release is `1.0.0`; this repository starts the cleaned OSS engine
release line at `1.1.0` so normal `pip install anaya` resolution moves forward
without pretending this is already a mature `2.x` product.

## Repository Decision

- Public repo: `sandip-pathe/anaya`
- Package name: `anaya`
- License: AGPL-3.0-or-later
- Publish workflow: `.github/workflows/publish.yml`
- PyPI environment name: `pypi`

## One-Time PyPI Setup

1. Log in to PyPI as an owner of `anaya`.
2. Open `https://pypi.org/manage/project/anaya/releases/`.
3. Yank the old `1.0.0` release with a reason such as:
   `Superseded by the AGPL Anaya 1.1 policy-as-code engine.`
4. Open `https://pypi.org/manage/project/anaya/settings/publishing/`.
5. Add a GitHub Actions trusted publisher:
   - Owner: `sandip-pathe`
   - Repository name: `anaya`
   - Workflow filename: `publish.yml`
   - Environment name: `pypi`
6. In GitHub, create an environment named `pypi`.
7. Add required reviewers to the `pypi` environment before the first release.

Do not delete the PyPI project unless the package name is being abandoned.
Yanking keeps historical installs understandable while preventing normal new
installs from selecting the old release.

## Local Preflight

Run from the repository root:

```bash
python -m pip install -e ".[dev,llm]"
python -m ruff check .
python -m pytest --cov
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

Smoke-test the built wheel in a clean virtual environment if this is the first
release from a new machine:

```bash
python -m venv .release-test
.release-test\Scripts\python -m pip install dist\anaya-1.1.0-py3-none-any.whl
.release-test\Scripts\anaya packs list
```

## Release

1. Confirm `pyproject.toml` and `anaya/__init__.py` have the same version.
2. Commit all release changes.
3. Push `main`.
4. Create and push a tag:

```bash
git tag v1.1.0
git push origin v1.1.0
```

5. Create a GitHub Release for `v1.1.0`.
6. The `Publish to PyPI` workflow will build and publish after the `pypi`
   environment approval.
7. Verify:

```bash
pipx install anaya
anaya packs list
anaya scan . --no-config --format table
```

The base PyPI package is the CLI/engine install. Hosted GitHub App deployments
should install:

```bash
pip install "anaya[server,llm]"
```
