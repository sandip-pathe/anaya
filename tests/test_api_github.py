import base64
import gzip
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import httpx
import jwt
import pytest

from anaya.api.github import GitHubAppClient, create_app_jwt, encode_sarif_for_upload, load_private_key
from anaya.config import Settings


def _test_private_key() -> tuple[str, str]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    public_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")
    return private_pem, public_pem


def test_create_app_jwt_can_be_verified():
    private_pem, public_pem = _test_private_key()

    token = create_app_jwt("123", private_pem, now=1_700_000_000)
    payload = jwt.decode(
        token,
        public_pem,
        algorithms=["RS256"],
        issuer="123",
        options={"verify_exp": False},
    )

    assert payload["iss"] == "123"
    assert payload["exp"] - payload["iat"] == 600


def test_load_private_key_supports_env_text_and_path(tmp_path: Path):
    key_path = tmp_path / "key.pem"
    key_path.write_text("from-file", encoding="utf-8")

    assert load_private_key(Settings(github_private_key="line1\\nline2")) == "line1\nline2"
    assert load_private_key(Settings(github_private_key_path=str(key_path))) == "from-file"


@pytest.mark.asyncio
async def test_github_client_creates_token_check_run_and_fetches_content():
    requests: list[tuple[str, str, dict[str, object] | None]] = []
    encoded_content = base64.b64encode(b"print('hello')\n").decode("ascii")

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8")) if request.content else None
        requests.append((request.method, request.url.path, payload))
        if request.url.path.endswith("/access_tokens"):
            return httpx.Response(201, json={"token": "installation-token"})
        if request.url.path.endswith("/check-runs"):
            return httpx.Response(201, json={"id": 42})
        if request.url.path.endswith("/check-runs/42"):
            return httpx.Response(200, json={"id": 42, "status": "completed"})
        if request.url.path.endswith("/pulls/7/files"):
            return httpx.Response(200, json=[{"filename": "app.py", "status": "modified"}])
        if request.url.path.endswith("/contents/app.py"):
            return httpx.Response(200, json={"encoding": "base64", "content": encoded_content})
        if request.url.path.endswith("/code-scanning/sarifs"):
            return httpx.Response(202, json={"id": "sarif-upload-id"})
        return httpx.Response(404)

    private_pem, _ = _test_private_key()
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        github = GitHubAppClient(
            app_id="123",
            private_key_pem=private_pem,
            api_url="https://api.github.test",
            client=http_client,
        )

        token = await github.create_installation_token(99)
        check_run = await github.create_check_run(
            owner="octo",
            repo="repo",
            installation_token=token,
            name="Anaya Policy Scan",
            head_sha="abc123",
        )
        files = await github.list_pull_request_files(
            owner="octo",
            repo="repo",
            pull_number=7,
            installation_token=token,
        )
        content = await github.get_file_content(
            owner="octo",
            repo="repo",
            path="app.py",
            ref="abc123",
            installation_token=token,
        )
        updated = await github.update_check_run(
            owner="octo",
            repo="repo",
            check_run_id=42,
            installation_token=token,
            payload={"status": "completed", "conclusion": "success"},
        )
        sarif_upload = await github.upload_sarif(
            owner="octo",
            repo="repo",
            installation_token=token,
            commit_sha="abc123",
            ref="refs/heads/feature",
            sarif='{"version":"2.1.0"}',
        )

    assert token == "installation-token"
    assert check_run == {"id": 42}
    assert files == [{"filename": "app.py", "status": "modified"}]
    assert content == "print('hello')\n"
    assert updated == {"id": 42, "status": "completed"}
    assert sarif_upload == {"id": "sarif-upload-id"}
    assert requests[1][2] == {
        "name": "Anaya Policy Scan",
        "head_sha": "abc123",
        "status": "in_progress",
    }


def test_encode_sarif_for_upload_round_trips():
    encoded = encode_sarif_for_upload('{"version":"2.1.0"}')

    decoded = gzip.decompress(base64.b64decode(encoded)).decode("utf-8")
    assert decoded == '{"version":"2.1.0"}'
