"""Pull request scan worker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tempfile

import httpx
import yaml

from anaya.api.github import GitHubAppClient, PullRequestScanRequest
from anaya.config import Settings
from anaya.engine.models import ScanSummary
from anaya.engine.orchestrator import ScanOrchestrator, resolve_pack_identifier
from anaya.engine.repo_config import RepositoryConfig, load_repository_config
from anaya.engine.scanners.pattern import detect_language
from anaya.reporter.check_run import build_check_run_payloads
from anaya.reporter.sarif import format_sarif


CONFIG_PATH = "anaya.yml"
REMOVED_FILE_STATUSES = {"removed"}


@dataclass(frozen=True)
class PullRequestScanResult:
    """Result of a completed PR scan."""

    summary: ScanSummary
    check_run_updates: int
    sarif_upload_id: str | None = None


class PullRequestScanner:
    """Fetch, scan, and report on a GitHub pull request."""

    def __init__(
        self,
        *,
        github: GitHubAppClient,
        settings: Settings,
    ):
        self.github = github
        self.settings = settings

    async def scan_pull_request(self, request: PullRequestScanRequest) -> PullRequestScanResult:
        """Run a PR scan and update the associated Check Run."""

        installation_token = await self.github.create_installation_token(request.installation_id)
        check_run_id = await self._ensure_check_run(request, installation_token)
        config_ref = request.base_ref or request.default_branch or "main"
        config, orchestrator = await self._load_config_and_orchestrator(
            request,
            installation_token,
            config_ref,
        )
        fetched_files = await self._fetch_changed_files(request, installation_token)
        summary = orchestrator.scan_contents(
            fetched_files,
            fail_on=config.thresholds.fail_on,
            warn_on=config.thresholds.warn_on,
            ignored_rules=config.ignore.rules,
            languages=config.languages,
            config_path=CONFIG_PATH,
        )
        check_run_updates = await self._update_check_run(
            request,
            installation_token,
            check_run_id,
            summary,
        )
        sarif_upload_id = None
        if self.settings.github_upload_sarif:
            upload = await self.github.upload_sarif(
                owner=request.owner,
                repo=request.repo,
                installation_token=installation_token,
                commit_sha=request.head_sha,
                ref=_git_ref(request),
                sarif=format_sarif(summary, automation_id=f"anaya/{request.owner}/{request.repo}"),
            )
            upload_id = upload.get("id")
            sarif_upload_id = str(upload_id) if upload_id is not None else None

        return PullRequestScanResult(
            summary=summary,
            check_run_updates=check_run_updates,
            sarif_upload_id=sarif_upload_id,
        )

    async def _ensure_check_run(
        self,
        request: PullRequestScanRequest,
        installation_token: str,
    ) -> int:
        if request.check_run_id is not None:
            return request.check_run_id
        check_run = await self.github.create_check_run(
            owner=request.owner,
            repo=request.repo,
            installation_token=installation_token,
            name="Anaya Policy Scan",
            head_sha=request.head_sha,
            status="in_progress",
        )
        check_run_id = check_run.get("id")
        if not isinstance(check_run_id, int):
            raise RuntimeError("GitHub did not return a check_run id")
        return check_run_id

    async def _fetch_changed_files(
        self,
        request: PullRequestScanRequest,
        installation_token: str,
    ) -> list[tuple[str, str]]:
        files = await self.github.list_pull_request_files(
            owner=request.owner,
            repo=request.repo,
            pull_number=request.pull_number,
            installation_token=installation_token,
        )
        fetched: list[tuple[str, str]] = []
        for file_info in files:
            filename = str(file_info.get("filename", ""))
            status = str(file_info.get("status", ""))
            if not filename or status in REMOVED_FILE_STATUSES or detect_language(filename) is None:
                continue
            content = await self.github.get_file_content(
                owner=request.owner,
                repo=request.repo,
                path=filename,
                ref=request.head_sha,
                installation_token=installation_token,
            )
            fetched.append((filename, content))
        return fetched

    async def _load_config_and_orchestrator(
        self,
        request: PullRequestScanRequest,
        installation_token: str,
        config_ref: str,
    ) -> tuple[RepositoryConfig, ScanOrchestrator]:
        with tempfile.TemporaryDirectory(prefix="anaya-pr-") as temp_dir:
            temp_root = Path(temp_dir)
            config_text = await self._fetch_optional_file(
                request,
                installation_token,
                CONFIG_PATH,
                config_ref,
            )
            config_path = temp_root / CONFIG_PATH
            if config_text is None:
                config = RepositoryConfig()
            else:
                config_path.write_text(config_text, encoding="utf-8")
                await self._fetch_custom_pack_files(
                    request,
                    installation_token,
                    config_ref,
                    config_text,
                    temp_root,
                )
                config = load_repository_config(config_path)

            pack_paths = [
                resolve_pack_identifier(pack_id, base_dir=temp_root)
                for pack_id in config.packs
            ]
            return config, ScanOrchestrator.from_pack_paths(pack_paths)

    async def _fetch_custom_pack_files(
        self,
        request: PullRequestScanRequest,
        installation_token: str,
        config_ref: str,
        config_text: str,
        temp_root: Path,
    ) -> None:
        for pack_path in _custom_pack_paths(config_text):
            destination = temp_root / pack_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            content = await self.github.get_file_content(
                owner=request.owner,
                repo=request.repo,
                path=pack_path,
                ref=config_ref,
                installation_token=installation_token,
            )
            destination.write_text(content, encoding="utf-8")

    async def _fetch_optional_file(
        self,
        request: PullRequestScanRequest,
        installation_token: str,
        path: str,
        ref: str,
    ) -> str | None:
        try:
            return await self.github.get_file_content(
                owner=request.owner,
                repo=request.repo,
                path=path,
                ref=ref,
                installation_token=installation_token,
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise

    async def _update_check_run(
        self,
        request: PullRequestScanRequest,
        installation_token: str,
        check_run_id: int,
        summary: ScanSummary,
    ) -> int:
        payloads = build_check_run_payloads(summary)
        for payload in payloads:
            await self.github.update_check_run(
                owner=request.owner,
                repo=request.repo,
                check_run_id=check_run_id,
                installation_token=installation_token,
                payload=payload,
            )
        return len(payloads)


def _custom_pack_paths(config_text: str) -> list[str]:
    raw = yaml.safe_load(config_text) or {}
    if not isinstance(raw, dict):
        return []
    packs = raw.get("packs", [])
    if not isinstance(packs, list):
        return []

    custom_paths: list[str] = []
    for item in packs:
        pack_id: str | None = None
        if isinstance(item, str):
            pack_id = item
        elif isinstance(item, dict) and isinstance(item.get("id"), str):
            pack_id = item["id"]
        if pack_id and not _is_builtin_pack_id(pack_id):
            custom_paths.append(pack_id)
    return custom_paths


def _is_builtin_pack_id(pack_id: str) -> bool:
    try:
        resolve_pack_identifier(pack_id)
    except FileNotFoundError:
        return False
    return True


def _git_ref(request: PullRequestScanRequest) -> str:
    if request.head_ref:
        return f"refs/heads/{request.head_ref}"
    return request.head_sha
