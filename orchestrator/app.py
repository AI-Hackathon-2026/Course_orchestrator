from langfuse import Langfuse, observe
from orchestrator.config import langfuse_settings
from orchestrator.data_base import data_base_agent
from orchestrator.default_graph import create_graph
from orchestrator.dto import (
    CreateCourseRequest,
    CreateCourseResponse,
    UsersGraph,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
)
from orchestrator.dto import ResponseCodes
langfuse = Langfuse(
    secret_key=langfuse_settings.SECRET_KEY,
    public_key=langfuse_settings.PUBLIC_KEY,
    host=langfuse_settings.LANGFUSE_SERVER,
)


@observe(name="get_graphs")
async def get_graphs(request: GetGraphsRequest) -> GetGraphsResponse:
    graphs = await data_base_agent.get_graphs(
        [graph_item.graph_id for graph_item in request.message]
    )
    return GetGraphsResponse(
        request_id=request.request_id, message=graphs, status=ResponseCodes.OK
    )


@observe(name="get_topic")
async def get_topic(request: GetTopicRequest) -> GetTopicResponse:
    topic = await data_base_agent.get_topic_from_node(
        node_id=request.message.topic_id, graph_id=request.message.graph_id
    )
    return GetTopicResponse(
        request_id=request.request_id, message=topic, status=ResponseCodes.OK
    )


@observe(name="create_new_course")
async def create_new_course(request: CreateCourseRequest) -> CreateCourseResponse:
    new_course = create_graph()
    await data_base_agent.add_graph(new_course)
    return CreateCourseResponse(
        request_id=request.request_id,
        status=ResponseCodes.OK,
        message=UsersGraph(
            username=request.message.username, graph_id=new_course.graph_id
        ),
    )
