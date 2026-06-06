"""Runtime settings for Anaya.

The core engine does not require these settings. Hosted GitHub App mode will use
them once the API and worker layers exist.
"""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    github_app_id: str | None = None
    github_private_key_path: str | None = None
    github_webhook_secret: str | None = None
    redis_url: str = "redis://localhost:6379/0"
    gemini_api_key: str | None = None
    host: str = "0.0.0.0"
    port: int = 3000
    log_level: str = "INFO"


def load_settings() -> Settings:
    """Load settings from ANAYA_* environment variables."""

    return Settings(
        github_app_id=os.getenv("ANAYA_GITHUB_APP_ID"),
        github_private_key_path=os.getenv("ANAYA_GITHUB_PRIVATE_KEY_PATH"),
        github_webhook_secret=os.getenv("ANAYA_GITHUB_WEBHOOK_SECRET"),
        redis_url=os.getenv("ANAYA_REDIS_URL", "redis://localhost:6379/0"),
        gemini_api_key=os.getenv("ANAYA_GEMINI_API_KEY"),
        host=os.getenv("ANAYA_HOST", "0.0.0.0"),
        port=int(os.getenv("ANAYA_PORT", "3000")),
        log_level=os.getenv("ANAYA_LOG_LEVEL", "INFO"),
    )
