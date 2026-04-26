from functools import lru_cache
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_env_filename() -> str:
    env = os.getenv("ENV")
    return f".env.{env}" if env else ".env"

class EnvironmentSettings(BaseSettings):
    API_VERSION: str
    APP_NAME: str
    FASTAPI_ENV: str
    DATABASE_DIALECT: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DEBUG_MODE: bool
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(env_file=get_env_filename())

@lru_cache
def get_environment_settings() -> EnvironmentSettings:
    return EnvironmentSettings()