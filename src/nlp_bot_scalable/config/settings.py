from pathlib import Path

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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
