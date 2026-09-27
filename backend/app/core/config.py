from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "Saudi Investment AI"
    api_v1_prefix: str = "/api/v1"

    sahmk_api_key: str = ""
    sahmk_base_url: str = "https://api.sahmk.sa/api/v1"
    sahmk_plan: str = "pro"
    sahmk_timeout_seconds: int = 20

    database_url: str = "postgresql+psycopg://saudi_ai:change_me@localhost:5432/saudi_investment_ai"
    cors_origins: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
