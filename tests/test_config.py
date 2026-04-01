import pytest
from dataclasses import FrozenInstanceError
from src.config import Config


def test_from_env_returns_config_when_both_vars_set(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")

    config = Config.from_env()

    assert config.database_url == "postgresql://localhost/test"
    assert config.openai_api_key == "sk-test-key"


def test_from_env_raises_when_database_url_missing(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setattr("src.config.load_dotenv", lambda: None)

    with pytest.raises(ValueError, match="DATABASE_URL"):
        Config.from_env()


def test_from_env_raises_when_openai_api_key_missing(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("src.config.load_dotenv", lambda: None)

    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        Config.from_env()


def test_config_is_frozen():
    config = Config(database_url="test", openai_api_key="test")

    with pytest.raises(FrozenInstanceError):
        config.database_url = "new_value"
