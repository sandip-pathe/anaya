# Railway Deployment Runbook

Use Railway for the hosted GitHub App webhook/API while the CLI remains
published through PyPI.

## Why Railway First

For Anaya V1, the fastest production-like path is to host the GitHub webhook API
before publishing another PyPI release. The CLI can already be tested locally
from source; the hosted product needs a public HTTPS URL so GitHub can deliver
pull request webhooks.

## Deploy Shape

This repo includes:

- `Dockerfile` to install Anaya with the `llm` extra.
- `railway.json` to use the Dockerfile, healthcheck `/health`, and restart on crashes.
- FastAPI app entrypoint: `anaya.api.app:app`.

Railway provides the runtime `PORT` variable. The Dockerfile starts:

```bash
uvicorn anaya.api.app:app --host 0.0.0.0 --port ${PORT:-3000}
```

## Required Variables

Set these in the Railway service variables UI:

```bash
ANAYA_GITHUB_APP_ID=replace-me
ANAYA_GITHUB_PRIVATE_KEY=replace-me
ANAYA_GITHUB_WEBHOOK_SECRET=replace-me
ANAYA_GITHUB_UPLOAD_SARIF=false
ANAYA_OPENAI_API_KEY=replace-me
```

Optional tuning:

```bash
ANAYA_OPENAI_MODEL=gpt-4o-mini
ANAYA_OPENAI_MAX_TOKENS=300
ANAYA_OPENAI_TEMPERATURE=0.1
ANAYA_OPENAI_TIMEOUT_SECONDS=10
ANAYA_LOG_LEVEL=INFO
```

The OpenAI key variable name is `ANAYA_OPENAI_API_KEY`.

## Private Key Format

On Railway, prefer `ANAYA_GITHUB_PRIVATE_KEY` instead of a file path. Paste the
GitHub App private key as one value. If Railway preserves newlines, paste it
normally. If not, paste it with escaped newlines:

```text
-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----
```

Anaya accepts both raw PEM newlines and escaped `\n`.

## GitHub App Settings

After Railway deploys and gives you a domain, set the GitHub App webhook URL:

```text
https://your-service.up.railway.app/webhook
```

Minimum permissions:

- Metadata: read
- Contents: read
- Pull requests: read
- Checks: read/write
- Code scanning/security events: write only if `ANAYA_GITHUB_UPLOAD_SARIF=true`

Subscribe to:

- Pull request
- Installation

## Verify

Open:

```text
https://your-service.up.railway.app/health
```

Expected response:

```json
{"status":"ok","service":"anaya"}
```

Then open a test pull request in a repository where the GitHub App is installed.
The PR should get an `Anaya Policy Scan` Check Run.
