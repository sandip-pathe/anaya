# GitHub Action Usage

Use this workflow when you want to run the OSS Anaya CLI in GitHub Actions and
upload SARIF to GitHub Code Scanning.

```yaml
name: Anaya

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  anaya:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Anaya
        run: python -m pip install -e .[dev]

      - name: Run Anaya
        run: anaya scan . --diff origin/main --format sarif -o anaya.sarif

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v4
        with:
          sarif_file: anaya.sarif
```

Notes:

- `fetch-depth: 0` lets `--diff origin/main` compare against the base branch.
- `security-events: write` is required for SARIF upload.
- For repositories where `origin/main` is not available, replace the diff ref
  with a branch or SHA available in the workflow checkout.
