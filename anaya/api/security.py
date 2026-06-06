"""Webhook security helpers."""

from __future__ import annotations

import hashlib
import hmac


SIGNATURE_PREFIX = "sha256="


def sign_webhook_body(body: bytes, secret: str) -> str:
    """Return GitHub's X-Hub-Signature-256 value for a request body."""

    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"{SIGNATURE_PREFIX}{digest}"


def verify_webhook_signature(body: bytes, signature_header: str | None, secret: str) -> bool:
    """Verify a GitHub webhook signature using HMAC-SHA256."""

    if not signature_header or not signature_header.startswith(SIGNATURE_PREFIX):
        return False
    expected = sign_webhook_body(body, secret)
    return hmac.compare_digest(expected, signature_header)
