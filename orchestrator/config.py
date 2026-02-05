from pydantic_settings import BaseSettings


class BackendConfig(BaseSettings):
    port: int = 8067
    host: str = "127.0.0.1"
    reload: bool = True


backend_config = BackendConfig()
