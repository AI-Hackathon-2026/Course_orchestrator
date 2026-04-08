from orchestrator.main import api_app
from orchestrator.dto import (
    CreateCourseRequest,
    CreateCourseResponse,
    GetGraphsPreviewRequest,
    GetGraphsPreviewResponse,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
)

@api_app.post("/get_graphs", response_model=GetGraphsResponse)
async def get_graph_api(request: GetGraphsRequest):
    return await api_app.state.app.get_graphs(request)


@api_app.post("/get_topic", response_model=GetTopicResponse)
async def get_topic_api(request: GetTopicRequest):
    return await api_app.state.app.get_topic(request)

@api_app.post("/create_new_course", response_model=CreateCourseResponse)
async def new_course_api(request: CreateCourseRequest):
    return await api_app.state.app.create_new_course(request)


@api_app.post("/get_graph_previews", response_model=GetGraphsPreviewResponse)
async def get_graph_previews_api(request: GetGraphsPreviewRequest):
    return await api_app.state.app.get_graph_previews(request)
