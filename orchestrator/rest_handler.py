from typing import Annotated

from fastapi import Depends, Request

from orchestrator.app import App
from orchestrator.dto import (
    CreateCourseRequest,
    CreateCourseResponse,
    GetGraphsPreviewRequest,
    GetGraphsPreviewResponse,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
    SetNodeAsEndedRequest,
    SetNodeAsEndedResponse,
)
from orchestrator.health_ceck import health_router
from orchestrator.lifespan import create_app

api_app = create_app()
api_app.include_router(health_router)


def get_app(request: Request) -> App:
    return request.app.state.app


@api_app.get("/get_graphs", response_model=GetGraphsResponse)
async def get_graph(request: GetGraphsRequest, app: Annotated[App, Depends(get_app)]):
    return await app.get_graphs(request)


@api_app.get("/get_topic", response_model=GetTopicResponse)
async def get_topic(request: GetTopicRequest, app: Annotated[App, Depends(get_app)]):
    return await app.get_topic(request)


@api_app.post("/create_new_course", response_model=CreateCourseResponse)
async def new_course(
    request: CreateCourseRequest, app: Annotated[App, Depends(get_app)]
):
    return await app.create_new_course(request)


@api_app.get("/get_graph_previews", response_model=GetGraphsPreviewResponse)
async def get_graph_previews(
    request: GetGraphsPreviewRequest, app: Annotated[App, Depends(get_app)]
):
    return await app.get_graph_previews(request)


@api_app.patch("/set_node_as_ended", response_model=SetNodeAsEndedResponse)
async def set_node_as_ended(
    request: SetNodeAsEndedRequest, app: Annotated[App, Depends(get_app)]
):
    return await app.set_node_as_ended(request)
