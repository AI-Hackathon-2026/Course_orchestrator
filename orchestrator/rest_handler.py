from typing import Annotated

from fastapi import Depends

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
from orchestrator.lifespan import create_app

api_app = create_app()


def get_app() -> App:
    return api_app.state.app


@api_app.get("/get_graphs", response_model=GetGraphsResponse)
async def get_graph_api(
    request: GetGraphsRequest, app: Annotated[App, Depends(get_app)]
):
    return await app.get_graphs(request)


@api_app.get("/get_topic", response_model=GetTopicResponse)
async def get_topic_api(
    request: GetTopicRequest, app: Annotated[App, Depends(get_app)]
):
    return await app.get_topic(request)


@api_app.post("/create_new_course", response_model=CreateCourseResponse)
async def new_course_api(
    request: CreateCourseRequest, app: Annotated[App, Depends(get_app)]
):
    return await app.create_new_course(request)


@api_app.get("/get_graph_previews", response_model=GetGraphsPreviewResponse)
async def get_graph_previews_api(
    request: GetGraphsPreviewRequest, app: Annotated[App, Depends(get_app)]
):
    return await app.get_graph_previews(request)


@api_app.patch("/set_node_as_ended", response_model=SetNodeAsEndedResponse)
async def set_node_as_ended_api(
    request: SetNodeAsEndedRequest, app: Annotated[App, Depends(get_app)]
):
    return await app.set_node_as_ended(request)
