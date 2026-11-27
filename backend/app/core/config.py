from functools import lru_cache
from typing import Literal
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, model_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://admin:secretpassword@localhost:9001/accident_manager"
    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: Literal["HS256"] = "HS256"
    access_token_expire_minutes: int = Field(default=60, ge=5, le=1440)
    cors_origins: str = "http://localhost:5173"
    max_reports_per_hour: int = Field(default=5, ge=1, le=100)
    # AI Auto-Responder settings
    ai_enabled: bool = False
    gemini_api_key: SecretStr | None = None
    gemini_model: str = "gemini-3.5-flash-lite"
    ai_timeout_seconds: float = Field(default=5.0, gt=0, le=30)

    @model_validator(mode="after")
    def valid_key(self):
        if self.jwt_secret_key.startswith("REPLACE_WITH"):
            raise ValueError("Replace the example JWT_SECRET_KEY with a strong random secret")
        return self

@lru_cache
def get_settings() -> Settings:
    return Settings()