# GitHub App Foundation

Anaya's hosted API is a FastAPI app that accepts GitHub webhooks, verifies
GitHub's HMAC signature, creates an in-progress Check Run, and runs an
in-process PR scan worker. A Redis/Celery deployment worker can replace the
in-process dispatcher in a later hardening milestone.

## Environment

```bash
ANAYA_GITHUB_APP_ID=123456
ANAYA_GITHUB_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
ANAYA_GITHUB_WEBHOOK_SECRET=your-webhook-secret
ANAYA_GITHUB_API_URL=https://api.github.com
ANAYA_GITHUB_UPLOAD_SARIF=false

# Optional OpenAI judge, used only when a repo's anaya.yml has llm.enabled: true
ANAYA_OPENAI_API_KEY=your-openai-api-key
ANAYA_OPENAI_MODEL=gpt-4o-mini
```

You can use `ANAYA_GITHUB_PRIVATE_KEY_PATH` instead of
`ANAYA_GITHUB_PRIVATE_KEY` when mounting a PEM file locally.

## Run Locally

```bash
python -m pip install -e .[dev]
uvicorn anaya.api.app:app --host 0.0.0.0 --port 3000
```

Health check:

```bash
curl http://localhost:3000/health
```

## GitHub App Settings

Webhook URL:

```text
https://YOUR-TUNNEL.example/webhook
```

Webhook secret:

```text
ANAYA_GITHUB_WEBHOOK_SECRET
```

Permissions:

- Checks: read and write
- Contents: read
- Pull requests: read
- Metadata: read
- Code scanning alerts / security events: write, once SARIF upload is enabled

Events:

- Pull request
- Installation

## Current Webhook Behavior

For `pull_request` events with action `opened`, `reopened`, or `synchronize`,
the API:

1. Verifies `X-Hub-Signature-256`.
2. Extracts owner, repo, PR number, head SHA, and installation ID.
3. Creates an installation access token.
4. Creates an in-progress Check Run named `Anaya Policy Scan`.
5. Fetches changed PR files from the head SHA.
6. Fetches `anaya.yml` and custom pack files from the base/default branch.
7. Runs the shared Anaya engine, including optional OpenAI rules only when
   `llm.enabled: true` is set in the trusted config.
8. Updates the Check Run with completed output and annotations.
9. Uploads SARIF when `ANAYA_GITHUB_UPLOAD_SARIF=true`.
10. Returns HTTP 202 before the background scan runs.

Other events or PR actions return HTTP 200 with `status: ignored`.

References:

- GitHub webhook signature docs: https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks
- GitHub App installation auth docs: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation
- GitHub Checks REST API docs: https://docs.github.com/v3/checks
