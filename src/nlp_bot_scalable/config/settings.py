from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "NLP Chatbot API"
    app_env: str = "development"
    debug: bool = False
    database_url: str = f"sqlite:///{PROJECT_ROOT / 'chatbot.db'}"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    jwt_secret: str = "change-me-in-production-use-a-long-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    cors_origins: list[str] = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            return [
                origin.strip()
                for origin in value.split(",")
                if origin.strip()
            ]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
