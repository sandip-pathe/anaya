"""GitHub webhook endpoint."""

from __future__ import annotations

from dataclasses import replace
import json
from typing import Any, Callable, Protocol

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request, Response, status

from anaya.api.github import GitHubAppClient, PullRequestScanRequest
from anaya.api.security import verify_webhook_signature
from anaya.config import Settings


PULL_REQUEST_SCAN_ACTIONS = {"opened", "reopened", "synchronize"}


class ScanDispatcher(Protocol):
    """Interface for handing accepted PR scans to a worker."""

    async def enqueue(self, request: PullRequestScanRequest) -> None:
        """Enqueue a PR scan."""


class NoopScanDispatcher:
    """Placeholder dispatcher until the async worker lands."""

    async def enqueue(self, request: PullRequestScanRequest) -> None:
        """Accept the request without side effects."""


GitHubClientFactory = Callable[[], GitHubAppClient]


def create_webhook_router(
    *,
    settings: Settings,
    github_client_factory: GitHubClientFactory,
    dispatcher: ScanDispatcher | None = None,
) -> APIRouter:
    """Create the GitHub webhook router."""

    router = APIRouter()
    scan_dispatcher = dispatcher or NoopScanDispatcher()

    @router.post("/webhook")
    async def github_webhook(
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
        x_github_event: str | None = Header(default=None, alias="X-GitHub-Event"),
        x_github_delivery: str | None = Header(default=None, alias="X-GitHub-Delivery"),
        x_hub_signature_256: str | None = Header(default=None, alias="X-Hub-Signature-256"),
    ) -> dict[str, Any]:
        body = await request.body()
        _verify_signature(body, x_hub_signature_256, settings)
        payload = _decode_payload(body)

        if x_github_event != "pull_request":
            return {"status": "ignored", "event": x_github_event, "delivery_id": x_github_delivery}

        action = payload.get("action")
        if action not in PULL_REQUEST_SCAN_ACTIONS:
            return {
                "status": "ignored",
                "event": x_github_event,
                "action": action,
                "delivery_id": x_github_delivery,
            }

        scan_request = extract_pull_request_scan_request(payload)
        client = github_client_factory()
        installation_token = await client.create_installation_token(scan_request.installation_id)
        check_run = await client.create_check_run(
            owner=scan_request.owner,
            repo=scan_request.repo,
            installation_token=installation_token,
            name="Anaya Policy Scan",
            head_sha=scan_request.head_sha,
            status="in_progress",
        )
        check_run_id = check_run.get("id")
        if isinstance(check_run_id, int):
            scan_request = replace(scan_request, check_run_id=check_run_id)
        background_tasks.add_task(scan_dispatcher.enqueue, scan_request)
        response.status_code = status.HTTP_202_ACCEPTED

        return {
            "status": "accepted",
            "delivery_id": x_github_delivery,
            "repository": f"{scan_request.owner}/{scan_request.repo}",
            "pull_number": scan_request.pull_number,
            "head_sha": scan_request.head_sha,
            "check_run_id": scan_request.check_run_id,
        }

    return router


def extract_pull_request_scan_request(payload: dict[str, Any]) -> PullRequestScanRequest:
    """Extract scan routing data from a pull_request webhook payload."""

    try:
        repository = payload["repository"]
        owner = repository["owner"]["login"]
        repo = repository["name"]
        pull_request = payload["pull_request"]
        pull_number = int(pull_request["number"])
        head_sha = str(pull_request["head"]["sha"])
        installation_id = int(payload["installation"]["id"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed pull_request webhook payload",
        ) from exc

    return PullRequestScanRequest(
        owner=str(owner),
        repo=str(repo),
        pull_number=pull_number,
        head_sha=head_sha,
        installation_id=installation_id,
    )


def _verify_signature(body: bytes, signature_header: str | None, settings: Settings) -> None:
    if not settings.github_webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ANAYA_GITHUB_WEBHOOK_SECRET is not configured",
        )
    if not verify_webhook_signature(body, signature_header, settings.github_webhook_secret):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid GitHub webhook signature",
        )


def _decode_payload(body: bytes) -> dict[str, Any]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malformed JSON") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Webhook payload must be an object")
    return payload
