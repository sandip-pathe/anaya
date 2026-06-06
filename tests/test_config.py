from anaya.config import load_settings


def test_settings_use_openai_env(monkeypatch):
    monkeypatch.setenv("ANAYA_OPENAI_API_KEY", "test-openai-key")

    settings = load_settings()

    assert settings.openai_api_key == "test-openai-key"
    assert settings.openai_model == "gpt-4o-mini"
    assert settings.openai_max_tokens == 300
    assert settings.openai_temperature == 0.1
    assert settings.openai_timeout_seconds == 10.0
    assert not hasattr(settings, "gemini_api_key")
