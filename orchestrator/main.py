from fastapi import FastAPI
from orchestrator.config import backend_config
from orchestrator.lifespan import lifespan
import uvicorn
api_app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "orchestrator.rest_handler:api_app",
        host=backend_config.HOST,
        port=backend_config.PORT,
        reload=backend_config.RELOAD,
    )