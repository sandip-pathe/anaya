# Azure VM Deployment Runbook

This runbook deploys the hosted Anaya GitHub App API on the existing Azure VM.
Use it after the public repository has been pushed and the GitHub App has fresh
secrets.

## Current Resource Shape

From the Azure portal screenshot:

- VM: `anaya-vm`
- Resource group: `anaya-rg`
- Public IP resource: `anaya-vm-ip`
- Network security group: `anaya-vm-nsg`
- Region/network: Central India resources

## Strategy

Do not delete the VM to replace the old app. Stop the old service, archive the
old directory, deploy Anaya into `/opt/anaya`, then switch Nginx/systemd traffic
after `/health` passes.

## VM Prerequisites

On the VM:

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv git nginx certbot python3-certbot-nginx
```

Azure networking:

- Allow inbound `80` and `443` from the internet.
- Restrict `22` to your own IP where possible.
- Point your domain, for example `app.anaya.dev`, to the VM public IP.

## Stop And Archive The Old Service

Replace `old-anaya.service` and `/opt/old-anaya` with the actual service and
directory names from the VM:

```bash
sudo systemctl stop old-anaya.service || true
sudo systemctl disable old-anaya.service || true
sudo mkdir -p /opt/archive
sudo cp -a /opt/old-anaya /opt/archive/old-anaya-2026-06-08
```

Keep the archive until the new GitHub App has processed real PR webhooks.

## Deploy Code

```bash
sudo mkdir -p /opt/anaya
sudo chown "$USER":"$USER" /opt/anaya
git clone https://github.com/sandip-pathe/anaya.git /opt/anaya
cd /opt/anaya
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[server,llm]"
```

## Configure Secrets

Create a dedicated config directory:

```bash
sudo mkdir -p /etc/anaya
sudo chmod 750 /etc/anaya
```

Put the GitHub App private key here:

```bash
sudo nano /etc/anaya/github-app.private-key.pem
sudo chmod 600 /etc/anaya/github-app.private-key.pem
```

Create `/etc/anaya/anaya.env`:

```bash
ANAYA_GITHUB_APP_ID=replace-me
ANAYA_GITHUB_PRIVATE_KEY_PATH=/etc/anaya/github-app.private-key.pem
ANAYA_GITHUB_WEBHOOK_SECRET=replace-me
ANAYA_OPENAI_API_KEY=replace-me
ANAYA_ENABLE_SARIF_UPLOAD=false
```

If OpenAI rules are not enabled in a repository's `anaya.yml`, the OpenAI key is
not used by scans.

## systemd Service

Create `/etc/systemd/system/anaya.service`:

```ini
[Unit]
Description=Anaya GitHub App API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/anaya
EnvironmentFile=/etc/anaya/anaya.env
ExecStart=/opt/anaya/.venv/bin/uvicorn anaya.api.app:app --host 127.0.0.1 --port 3000 --proxy-headers
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now anaya.service
sudo systemctl status anaya.service
curl http://127.0.0.1:3000/health
```

## Nginx

Create `/etc/nginx/sites-available/anaya`:

```nginx
server {
    listen 80;
    server_name app.anaya.dev;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/anaya /etc/nginx/sites-enabled/anaya
sudo nginx -t
sudo systemctl reload nginx
```

Add TLS:

```bash
sudo certbot --nginx -d app.anaya.dev
```

Verify:

```bash
curl https://app.anaya.dev/health
```

## GitHub App Settings

Set the app webhook URL to:

```text
https://app.anaya.dev/webhook
```

Minimum repository permissions:

- Metadata: read
- Contents: read
- Pull requests: read
- Checks: read/write
- Code scanning alerts or security events: write, only when SARIF upload is enabled

Subscribe to:

- Pull request
- Installation

## Production Gaps Before Marketplace

Before public GitHub Marketplace submission, harden:

- Retry/backoff for transient GitHub API failures.
- Failure-path Check Run updates so checks do not remain in progress.
- Background queue, for example Redis/Celery, instead of in-process background tasks.
- Installation-token cache.
- Privacy policy, terms, support page, status page, and Marketplace plan webhooks.
