import os

from pydantic_settings import BaseSettings


class BackendConfig(BaseSettings):
    PORT: int = 8067
    HOST: str = "0.0.0.0"
    RELOAD: bool = False


class LangfuseSettings(BaseSettings):
    LANGFUSE_SERVER: str = "https://cloud.langfuse.com"
    SECRET_KEY: str = os.environ.get("LANGFUSE_SECRET_KEY")
    PUBLIC_KEY: str = os.environ.get("LANGFUSE_PUBLIC_KEY")


class RedisConfig:
    REDIS_VALUE_TYPE = str | int | float | dict | list | bool | set | None


backend_config = BackendConfig()
langfuse_settings = LangfuseSettings()
redis_config = RedisConfig()
