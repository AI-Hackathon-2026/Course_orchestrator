from pydantic_settings import BaseSettings


class BackendConfig(BaseSettings):
    PORT: int = 8067
    HOST: str = "0.0.0.0"
    RELOAD: bool = False


class MongoDBConfig(BaseSettings):
    MONGO_HOST: str = "mongo_db"
    PORT: int = 27017
    MONGO_URL: str = f"mongodb://{MONGO_HOST}:{PORT}/"
    DATABASE: str = "courses"
    MAX_POOL_SIZE: int = 200
    MIN_POOL_SIZE: int = 50
    HEALTH_CHECK_TIMEOUT: int = 1


backend_config = BackendConfig()
mongo_config = MongoDBConfig()
