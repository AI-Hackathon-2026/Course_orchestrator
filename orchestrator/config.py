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


class DatabaseConfig(BaseSettings):
    DATABASE_HOST: str = "127.0.0.1"
    PORT: int = 5432
    DATABASE: str = "tmp"
    DATABASE_URL: str = (
        f"postgresql://{os.environ.get('DATABASE_USER')}:"
        f"{os.environ.get('DATABASE_USER_PASSWORD')}@{DATABASE_HOST}:{PORT}/{DATABASE}"
    )


backend_config = BackendConfig()
langfuse_settings = LangfuseSettings()
database_config = DatabaseConfig()
