"""Worker dispatch adapters."""

from __future__ import annotations

from collections.abc import Callable

from anaya.api.github import GitHubAppClient, PullRequestScanRequest
from anaya.config import Settings
from anaya.worker.pr_scan import PullRequestScanner


class InProcessScanDispatcher:
    """Run PR scans as FastAPI background tasks in the current process."""

    def __init__(
        self,
        *,
        settings: Settings,
        github_client_factory: Callable[[], GitHubAppClient],
    ):
        self.settings = settings
        self.github_client_factory = github_client_factory

    async def enqueue(self, request: PullRequestScanRequest) -> None:
        """Run the PR scan."""

        scanner = PullRequestScanner(
            github=self.github_client_factory(),
            settings=self.settings,
        )
        await scanner.scan_pull_request(request)
