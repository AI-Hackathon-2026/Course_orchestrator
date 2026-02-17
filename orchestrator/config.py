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


class MongoDBConfig(BaseSettings):
    MONGO_HOST: str = "127.0.0.1"
    PORT: int = 27017
    MONGO_URL: str = f"mongodb://{MONGO_HOST}:{PORT}/"
    DATABASE: str = "courses"


backend_config = BackendConfig()
langfuse_settings = LangfuseSettings()
mongo_config = MongoDBConfig()
