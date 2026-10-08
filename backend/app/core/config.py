from functools import lru_cache
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "LearnFirst AI"

    app_version: str = "0.1.0"

    app_env: str = "development"

    debug: bool = True

    api_v1_prefix: str = "/api/v1"

    log_level: str = "INFO"

    database_url: str = (
        "sqlite:///./learnfirst.db"
    )

    # ----------------------------------
    # LLM Configuration
    # ----------------------------------

    llm_provider: str = "mock"

    ollama_base_url: str = (
        "http://localhost:11434"
    )

    ollama_model: str = "llama3.2"

    ollama_timeout_seconds: float = 60.0

    llm_temperature: float = 0.2

    llm_max_tokens: int = 300

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()