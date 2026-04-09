from pydantic_settings import BaseSettings


class BackendConfig(BaseSettings):
    PORT: int = 8067
    HOST: str = "127.0.0.1"
    RELOAD: bool = False


class MongoDBConfig(BaseSettings):
    MONGO_HOST: str = "127.0.0.1"
    PORT: int = 27017
    MONGO_URL: str = f"mongodb://{MONGO_HOST}:{PORT}/"
    DATABASE: str = "courses"


backend_config = BackendConfig()
mongo_config = MongoDBConfig()
