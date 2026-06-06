from anaya.config import load_settings


def test_settings_use_openai_env(monkeypatch):
    monkeypatch.setenv("ANAYA_OPENAI_API_KEY", "test-openai-key")

    settings = load_settings()

    assert settings.openai_api_key == "test-openai-key"
    assert not hasattr(settings, "gemini_api_key")
