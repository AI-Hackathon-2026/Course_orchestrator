from bson import ObjectId
from langfuse import Langfuse, observe

from orchestrator.config import langfuse_settings
from orchestrator.data_base import data_base_agent
from orchestrator.default_graph import DefaultGraph
from orchestrator.dto import (
    CreateCourseRequest,
    CreateCourseResponse,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
    ResponseCodes,
    UsersGraph,
)
from orchestrator.graph import Graph
from pymongo.errors import PyMongoError

langfuse = Langfuse(
    secret_key=langfuse_settings.SECRET_KEY,
    public_key=langfuse_settings.PUBLIC_KEY,
    host=langfuse_settings.LANGFUSE_SERVER,
)


@observe(name="get_graphs")
async def get_graphs(request: GetGraphsRequest) -> GetGraphsResponse:
    try:
        graphs = await data_base_agent.get_graphs(
            [graph_item.graph_id for graph_item in request.message]
        )
        return GetGraphsResponse(
            request_id=request.request_id, message=graphs, status=ResponseCodes.OK
        )
    except PyMongoError:
        return GetGraphsResponse(
            request_id=request.request_id, message=None, status=ResponseCodes.INTERNAL_ERROR
        )


@observe(name="get_topic")
async def get_topic(request: GetTopicRequest) -> GetTopicResponse:
    try:
        topic = await data_base_agent.get_topic(
            topic_id=request.message.topic_id
        )
        return GetTopicResponse(
            request_id=request.request_id, message=topic, status=ResponseCodes.OK
        )
    except PyMongoError:
        return GetTopicResponse(
            request_id=request.request_id, message=None, status=ResponseCodes.INTERNAL_ERROR
        )


@observe(name="create_new_course")
async def create_new_course(request: CreateCourseRequest) -> CreateCourseResponse:
    try:
        graph_nodes = await DefaultGraph.create_graph_nodes()
        await data_base_agent.add_graph_nodes(graph_nodes)

        new_course = Graph(
            graph_id=str(ObjectId()),
            nodes=await DefaultGraph.create_users_graph_nodes(graph_nodes),
        )
        await data_base_agent.add_graph(new_course)

        return CreateCourseResponse(
            request_id=request.request_id,
            status=ResponseCodes.OK,
            message=UsersGraph(
                username=request.message.username, graph_id=new_course.graph_id
            ),
        )
    except PyMongoError:
        return CreateCourseResponse(
            request_id=request.request_id,
            status=ResponseCodes.INTERNAL_ERROR,
            message=None
        )
