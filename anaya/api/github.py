"""GitHub App authentication and REST client helpers."""

from __future__ import annotations

import base64
from dataclasses import dataclass
import gzip
from pathlib import Path
import time
from typing import Any

import httpx
import jwt

from anaya.config import Settings


GITHUB_API_VERSION = "2022-11-28"


class GitHubAppError(RuntimeError):
    """Raised when GitHub App configuration or API calls fail."""


@dataclass(frozen=True)
class PullRequestScanRequest:
    """Minimum data needed to enqueue a PR scan."""

    owner: str
    repo: str
    pull_number: int
    head_sha: str
    installation_id: int
    check_run_id: int | None = None
    head_ref: str | None = None
    base_ref: str | None = None
    default_branch: str | None = None


class GitHubAppClient:
    """Small async GitHub REST client for App-mode operations."""

    def __init__(
        self,
        *,
        app_id: str,
        private_key_pem: str,
        api_url: str = "https://api.github.com",
        client: httpx.AsyncClient | None = None,
    ):
        self.app_id = app_id
        self.private_key_pem = private_key_pem
        self.api_url = api_url.rstrip("/")
        self._client = client

    async def create_installation_token(self, installation_id: int) -> str:
        """Create a short-lived installation access token."""

        response = await self._request(
            "POST",
            f"/app/installations/{installation_id}/access_tokens",
            token=create_app_jwt(self.app_id, self.private_key_pem),
        )
        payload = response.json()
        token = payload.get("token")
        if not isinstance(token, str) or not token:
            raise GitHubAppError("GitHub did not return an installation token")
        return token

    async def create_check_run(
        self,
        *,
        owner: str,
        repo: str,
        installation_token: str,
        name: str,
        head_sha: str,
        status: str = "in_progress",
    ) -> dict[str, Any]:
        """Create a GitHub Check Run."""

        response = await self._request(
            "POST",
            f"/repos/{owner}/{repo}/check-runs",
            token=installation_token,
            json={"name": name, "head_sha": head_sha, "status": status},
        )
        return response.json()

    async def update_check_run(
        self,
        *,
        owner: str,
        repo: str,
        check_run_id: int,
        installation_token: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Update a GitHub Check Run."""

        response = await self._request(
            "PATCH",
            f"/repos/{owner}/{repo}/check-runs/{check_run_id}",
            token=installation_token,
            json=payload,
        )
        return response.json()

    async def list_pull_request_files(
        self,
        *,
        owner: str,
        repo: str,
        pull_number: int,
        installation_token: str,
    ) -> list[dict[str, Any]]:
        """List files changed by a pull request."""

        response = await self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls/{pull_number}/files",
            token=installation_token,
        )
        payload = response.json()
        if not isinstance(payload, list):
            raise GitHubAppError("GitHub did not return a pull request file list")
        return payload

    async def get_file_content(
        self,
        *,
        owner: str,
        repo: str,
        path: str,
        ref: str,
        installation_token: str,
    ) -> str:
        """Fetch and decode a file from repository contents."""

        response = await self._request(
            "GET",
            f"/repos/{owner}/{repo}/contents/{path}",
            token=installation_token,
            params={"ref": ref},
        )
        payload = response.json()
        content = payload.get("content")
        encoding = payload.get("encoding")
        if not isinstance(content, str) or encoding != "base64":
            raise GitHubAppError(f"GitHub did not return base64 file content for {path}")
        return base64.b64decode(content).decode("utf-8", errors="replace")

    async def upload_sarif(
        self,
        *,
        owner: str,
        repo: str,
        installation_token: str,
        commit_sha: str,
        ref: str,
        sarif: str,
    ) -> dict[str, Any]:
        """Upload SARIF to GitHub Code Scanning."""

        response = await self._request(
            "POST",
            f"/repos/{owner}/{repo}/code-scanning/sarifs",
            token=installation_token,
            json={
                "commit_sha": commit_sha,
                "ref": ref,
                "sarif": encode_sarif_for_upload(sarif),
            },
        )
        return response.json()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        token: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
        }
        if self._client is not None:
            response = await self._client.request(
                method,
                f"{self.api_url}{path}",
                headers=headers,
                json=json,
                params=params,
            )
        else:
            async with httpx.AsyncClient(base_url=self.api_url, timeout=15.0) as client:
                response = await client.request(
                    method,
                    path,
                    headers=headers,
                    json=json,
                    params=params,
                )
        response.raise_for_status()
        return response


def create_app_jwt(app_id: str, private_key_pem: str, *, now: int | None = None) -> str:
    """Create a GitHub App JWT."""

    issued_at = int(time.time() if now is None else now) - 60
    payload = {
        "iat": issued_at,
        "exp": issued_at + 600,
        "iss": app_id,
    }
    return jwt.encode(payload, private_key_pem, algorithm="RS256")


def encode_sarif_for_upload(sarif: str) -> str:
    """Return gzip-compressed, base64-encoded SARIF for GitHub upload."""

    compressed = gzip.compress(sarif.encode("utf-8"))
    return base64.b64encode(compressed).decode("ascii")


def load_private_key(settings: Settings) -> str:
    """Load a GitHub App private key from env text or a configured path."""

    if settings.github_private_key:
        return settings.github_private_key.replace("\\n", "\n")
    if settings.github_private_key_path:
        return Path(settings.github_private_key_path).read_text(encoding="utf-8")
    raise GitHubAppError("ANAYA_GITHUB_PRIVATE_KEY or ANAYA_GITHUB_PRIVATE_KEY_PATH is required")


def github_client_from_settings(settings: Settings) -> GitHubAppClient:
    """Create a GitHub client from runtime settings."""

    if not settings.github_app_id:
        raise GitHubAppError("ANAYA_GITHUB_APP_ID is required")
    return GitHubAppClient(
        app_id=settings.github_app_id,
        private_key_pem=load_private_key(settings),
        api_url=settings.github_api_url,
    )
