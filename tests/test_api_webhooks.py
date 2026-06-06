import json

from fastapi.testclient import TestClient

from anaya.api.app import create_app
from anaya.api.github import PullRequestScanRequest
from anaya.api.security import sign_webhook_body
from anaya.config import Settings


class FakeGitHubClient:
    def __init__(self):
        self.installation_ids: list[int] = []
        self.check_runs: list[dict[str, object]] = []

    async def create_installation_token(self, installation_id: int) -> str:
        self.installation_ids.append(installation_id)
        return "installation-token"

    async def create_check_run(self, **kwargs):
        self.check_runs.append(kwargs)
        return {"id": 1234}


class FakeDispatcher:
    def __init__(self):
        self.requests: list[PullRequestScanRequest] = []

    async def enqueue(self, request: PullRequestScanRequest) -> None:
        self.requests.append(request)


def _client(
    *,
    github: FakeGitHubClient | None = None,
    dispatcher: FakeDispatcher | None = None,
) -> TestClient:
    settings = Settings(github_webhook_secret="secret")
    fake_github = github or FakeGitHubClient()
    app = create_app(
        settings=settings,
        github_client_factory=lambda: fake_github,
        dispatcher=dispatcher,
    )
    return TestClient(app)


def _signed_headers(body: bytes, event: str = "pull_request") -> dict[str, str]:
    return {
        "X-GitHub-Event": event,
        "X-GitHub-Delivery": "delivery-1",
        "X-Hub-Signature-256": sign_webhook_body(body, "secret"),
        "Content-Type": "application/json",
    }


def _pull_request_payload(action: str = "opened") -> dict[str, object]:
    return {
        "action": action,
        "installation": {"id": 99},
        "repository": {
            "name": "repo",
            "owner": {"login": "octo"},
            "default_branch": "main",
        },
        "pull_request": {
            "number": 7,
            "head": {"sha": "abc123", "ref": "feature/anaya"},
            "base": {"ref": "main"},
        },
    }


def test_health_endpoint_returns_ok():
    response = _client().get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "anaya"}


def test_webhook_rejects_invalid_signature():
    body = json.dumps(_pull_request_payload()).encode("utf-8")
    headers = _signed_headers(body)
    headers["X-Hub-Signature-256"] = "sha256=bad"

    response = _client().post("/webhook", content=body, headers=headers)

    assert response.status_code == 403


def test_webhook_ignores_non_pull_request_event():
    body = b'{"zen":"Approachable is better than simple."}'

    response = _client().post("/webhook", content=body, headers=_signed_headers(body, "ping"))

    assert response.status_code == 200
    assert response.json()["status"] == "ignored"


def test_webhook_accepts_pull_request_and_creates_check_run():
    github = FakeGitHubClient()
    dispatcher = FakeDispatcher()
    body = json.dumps(_pull_request_payload("synchronize")).encode("utf-8")

    response = _client(github=github, dispatcher=dispatcher).post(
        "/webhook",
        content=body,
        headers=_signed_headers(body),
    )

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"
    assert response.json()["check_run_id"] == 1234
    assert github.installation_ids == [99]
    assert github.check_runs == [
        {
            "owner": "octo",
            "repo": "repo",
            "installation_token": "installation-token",
            "name": "Anaya Policy Scan",
            "head_sha": "abc123",
            "status": "in_progress",
        }
    ]
    assert dispatcher.requests == [
        PullRequestScanRequest(
            owner="octo",
            repo="repo",
            pull_number=7,
            head_sha="abc123",
            installation_id=99,
            check_run_id=1234,
            head_ref="feature/anaya",
            base_ref="main",
            default_branch="main",
        )
    ]


def test_webhook_ignores_unscannable_pull_request_action():
    body = json.dumps(_pull_request_payload("closed")).encode("utf-8")

    response = _client().post("/webhook", content=body, headers=_signed_headers(body))

    assert response.status_code == 200
    assert response.json()["status"] == "ignored"
    assert response.json()["action"] == "closed"
