from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pass


class BackendConfig(BaseSettings):
    port: int = 8067
    host: str = "localhost"
    reload: bool = True


backend_config = BackendConfig()
settings = Settings()
