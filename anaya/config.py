"""Runtime settings for Anaya.

The core engine does not require these settings. Hosted GitHub App mode will use
them once the API and worker layers exist.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed runtime settings."""

    model_config = SettingsConfigDict(
        env_prefix="ANAYA_",
        env_file=".env",
        extra="ignore",
    )

    github_app_id: str | None = None
    github_private_key: str | None = None
    github_private_key_path: str | None = None
    github_webhook_secret: str | None = None
    github_api_url: str = "https://api.github.com"
    github_upload_sarif: bool = False
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str | None = None
    host: str = "0.0.0.0"
    port: int = 3000
    log_level: str = "INFO"


def load_settings() -> Settings:
    """Load settings from ANAYA_* environment variables."""

    return Settings()
