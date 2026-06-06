import httpx
import pytest

from anaya.api.github import PullRequestScanRequest
from anaya.config import Settings
from anaya.worker.pr_scan import PullRequestScanner


class FakeGitHub:
    def __init__(self, *, config_text: str | None = None, custom_pack_text: str | None = None):
        self.config_text = config_text
        self.custom_pack_text = custom_pack_text
        self.updated_check_runs: list[dict[str, object]] = []
        self.uploads: list[dict[str, object]] = []
        self.content_requests: list[tuple[str, str]] = []

    async def create_installation_token(self, installation_id: int) -> str:
        assert installation_id == 99
        return "installation-token"

    async def create_check_run(self, **kwargs):
        return {"id": 123}

    async def list_pull_request_files(self, **kwargs):
        return [
            {"filename": "src/app.py", "status": "modified"},
            {"filename": "README.md", "status": "modified"},
            {"filename": "old.py", "status": "removed"},
        ]

    async def get_file_content(self, *, path: str, ref: str, **kwargs):
        self.content_requests.append((path, ref))
        if path == "anaya.yml":
            if self.config_text is None:
                request = httpx.Request("GET", "https://api.github.test/contents/anaya.yml")
                response = httpx.Response(404, request=request)
                raise httpx.HTTPStatusError("not found", request=request, response=response)
            return self.config_text
        if path == "policies/custom.yml" and self.custom_pack_text is not None:
            return self.custom_pack_text
        if path == "src/app.py":
            return 'api_key = "sk_live_1234567890abcdef"\n'
        raise AssertionError(f"Unexpected content request: {path}")

    async def update_check_run(self, **kwargs):
        self.updated_check_runs.append(kwargs)
        return {"id": kwargs["check_run_id"], "status": "completed"}

    async def upload_sarif(self, **kwargs):
        self.uploads.append(kwargs)
        return {"id": "sarif-upload-id"}


def _request() -> PullRequestScanRequest:
    return PullRequestScanRequest(
        owner="octo",
        repo="repo",
        pull_number=7,
        head_sha="abc123",
        installation_id=99,
        check_run_id=42,
        head_ref="feature/anaya",
        base_ref="main",
        default_branch="main",
    )


@pytest.mark.asyncio
async def test_pull_request_scanner_fetches_files_scans_and_updates_check_run():
    github = FakeGitHub()
    scanner = PullRequestScanner(github=github, settings=Settings(github_upload_sarif=True))

    result = await scanner.scan_pull_request(_request())

    assert result.summary.total_violations == 1
    assert result.summary.results[0].file_path == "src/app.py"
    assert result.check_run_updates == 1
    assert result.sarif_upload_id == "sarif-upload-id"
    assert github.updated_check_runs[0]["check_run_id"] == 42
    assert github.updated_check_runs[0]["payload"]["status"] == "completed"
    assert github.updated_check_runs[0]["payload"]["conclusion"] == "failure"
    assert github.uploads[0]["commit_sha"] == "abc123"
    assert github.uploads[0]["ref"] == "refs/heads/feature/anaya"
    assert ("src/app.py", "abc123") in github.content_requests
    assert ("anaya.yml", "main") in github.content_requests


@pytest.mark.asyncio
async def test_pull_request_scanner_loads_custom_pack_from_base_ref():
    config_text = (
        "packs:\n"
        "  - policies/custom.yml\n"
        "thresholds:\n"
        "  fail_on: HIGH\n"
    )
    custom_pack_text = "\n".join(
        [
            "pack:",
            '  id: "custom/internal"',
            '  version: "1.0.0"',
            '  name: "Internal"',
            '  description: "Internal rules"',
            "rules:",
            '  - id: "CUSTOM-001"',
            '    name: "Hardcoded API Key"',
            '    description: "API key"',
            "    type: pattern",
            "    severity: HIGH",
            "    languages: [python]",
            "    patterns:",
            "      - regex: 'api_key\\s*=\\s*[\"''][A-Za-z0-9_\\-]{16,}[\"'']'",
            '    message: "API key at line {line}."',
            '    fix_hint: "Move it to secret storage."',
            "",
        ]
    )
    github = FakeGitHub(config_text=config_text, custom_pack_text=custom_pack_text)
    scanner = PullRequestScanner(github=github, settings=Settings())

    result = await scanner.scan_pull_request(_request())
    rule_ids = {
        violation.rule_id
        for scan_result in result.summary.results
        for violation in scan_result.violations
    }

    assert rule_ids == {"CUSTOM-001"}
    assert ("policies/custom.yml", "main") in github.content_requests
