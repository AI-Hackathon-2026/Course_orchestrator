import os
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from orchestrator.app import App


def get_app(request: Request) -> App:
    return request.app.state.app


def get_readiness(request: Request) -> bool:
    return request.app.state.is_ready


health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("/liveness")
async def liveness():
    return JSONResponse(
        status_code=200, content={"status": "alive", "pid": os.getpid()}
    )


@health_router.get("/readiness")
async def readiness(
    app: Annotated[App, Depends(get_app)],
    is_ready: Annotated[bool, Depends(get_readiness)],
):
    if not is_ready:
        return JSONResponse(status_code=503, content={"status": "initializing"})
    db_is_health = await app.check_mongo_connection()
    if db_is_health:
        return JSONResponse(status_code=200, content={"status": "healthy"})
    else:
        return JSONResponse(status_code=503, content={"status": "mongo is unavailable"})
