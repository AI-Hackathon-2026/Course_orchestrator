from pydantic_settings import BaseSettings


class BackendConfig(BaseSettings):
    PORT: int = 8067
    HOST: str = "127.0.0.1"
    RELOAD: bool = True


class Settings(BaseSettings):
    LANGFUSE_SERVER: str = "https://cloud.langfuse.com"


backend_config = BackendConfig()
settings = Settings()
