from pydantic_settings import BaseSettings


class BackendConfig(BaseSettings):
    PORT: int = 8067
    HOST: str = "localhost"
    RELOAD: bool = False


class MongoDBConfig(BaseSettings):
    MONGO_HOST: str = "localhost"
    PORT: int = 27017
    MONGO_URL: str = f"mongodb://{MONGO_HOST}:{PORT}/"
    DATABASE: str = "courses"


backend_config = BackendConfig()
mongo_config = MongoDBConfig()
