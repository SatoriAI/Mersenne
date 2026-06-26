from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

EnvironmentType = Literal[
    "local",
    "production",
]


LogLevelType = Literal[
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]


class Settings(BaseSettings):
    app_name: str = "Mersenne"

    environment: EnvironmentType = "local"

    log_level: LogLevelType = "INFO"
    debug: bool = False

    swagger_enabled: bool = True
    swagger_endpoint: str = "/docs"

    # Operational ceiling on the Mersenne exponent to bound the cost of the
    # Lucas-Lehmer computation per request. Tunable per environment.
    max_mersenne_exponent: int = 20_000

    # database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/deckard"
    # database_echo: bool = False

    cors_allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # @field_validator("database_url", mode="after")
    # @classmethod
    # def _force_asyncpg_driver(cls, value: str) -> str:
    #     if value.startswith("postgres://"):
    #         return "postgresql+asyncpg://" + value.removeprefix("postgres://")
    #     if value.startswith("postgresql://"):
    #         return "postgresql+asyncpg://" + value.removeprefix("postgresql://")
    #     return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
