import uvicorn

from orchestrator.config import backend_config

if __name__ == "__main__":
    uvicorn.run(
        "orchestrator.rest_handler:api_app",
        host=backend_config.HOST,
        port=backend_config.PORT,
        reload=backend_config.RELOAD,
    )
