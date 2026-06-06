"""FastAPI app factory for hosted Anaya."""

from __future__ import annotations

from collections.abc import Callable

from fastapi import FastAPI

from anaya.api.github import GitHubAppClient, github_client_from_settings
from anaya.api.health import router as health_router
from anaya.api.webhooks import ScanDispatcher, create_webhook_router
from anaya.config import Settings, load_settings


def create_app(
    *,
    settings: Settings | None = None,
    github_client_factory: Callable[[], GitHubAppClient] | None = None,
    dispatcher: ScanDispatcher | None = None,
) -> FastAPI:
    """Create the FastAPI application."""

    resolved_settings = settings or load_settings()
    app = FastAPI(title="Anaya", version="0.1.0")
    app.include_router(health_router)
    app.include_router(
        create_webhook_router(
            settings=resolved_settings,
            github_client_factory=github_client_factory
            or (lambda: github_client_from_settings(resolved_settings)),
            dispatcher=dispatcher,
        )
    )
    return app


app = create_app()
