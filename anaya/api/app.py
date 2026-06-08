"""FastAPI app factory for hosted Anaya."""

from __future__ import annotations

from collections.abc import Callable

from fastapi import FastAPI

from anaya import __version__
from anaya.api.github import GitHubAppClient, github_client_from_settings
from anaya.api.health import router as health_router
from anaya.api.webhooks import ScanDispatcher, create_webhook_router
from anaya.config import Settings, load_settings
from anaya.worker.tasks import InProcessScanDispatcher


def create_app(
    *,
    settings: Settings | None = None,
    github_client_factory: Callable[[], GitHubAppClient] | None = None,
    dispatcher: ScanDispatcher | None = None,
) -> FastAPI:
    """Create the FastAPI application."""

    resolved_settings = settings or load_settings()
    resolved_github_client_factory = github_client_factory or (
        lambda: github_client_from_settings(resolved_settings)
    )
    resolved_dispatcher = dispatcher or InProcessScanDispatcher(
        settings=resolved_settings,
        github_client_factory=resolved_github_client_factory,
    )
    app = FastAPI(title="Anaya", version=__version__)
    app.include_router(health_router)
    app.include_router(
        create_webhook_router(
            settings=resolved_settings,
            github_client_factory=resolved_github_client_factory,
            dispatcher=resolved_dispatcher,
        )
    )
    return app


app = create_app()
