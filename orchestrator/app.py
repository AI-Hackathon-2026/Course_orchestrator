from bson import ObjectId
from langfuse import Langfuse
from pymongo.errors import PyMongoError

from orchestrator.config import langfuse_settings
from orchestrator.data_base import data_base_agent
from orchestrator.default_graph import DefaultGraph
from orchestrator.dto import (
    CreateCourseRequest,
    CreateCourseResponse,
    GetGraphsPreviewRequest,
    GetGraphsPreviewResponse,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
    ResponseCodes,
    UsersGraph,
)
from orchestrator.graph import Graph, GraphPreview

langfuse = Langfuse(
    secret_key=langfuse_settings.SECRET_KEY,
    public_key=langfuse_settings.PUBLIC_KEY,
    host=langfuse_settings.LANGFUSE_SERVER,
)


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
            request_id=request.request_id,
            message=None,
            status=ResponseCodes.INTERNAL_ERROR,
        )


async def get_topic(request: GetTopicRequest) -> GetTopicResponse:
    try:
        topic = await data_base_agent.get_topic(topic_id=request.message.topic_id)
        return GetTopicResponse(
            request_id=request.request_id, message=topic, status=ResponseCodes.OK
        )
    except PyMongoError:
        return GetTopicResponse(
            request_id=request.request_id,
            message=None,
            status=ResponseCodes.INTERNAL_ERROR,
        )


async def create_new_course(request: CreateCourseRequest) -> CreateCourseResponse:
    try:
        graph_id = str(ObjectId())
        graph_nodes = DefaultGraph.create_graph_nodes(
            graph_id, await data_base_agent.get_all_topics()
        )
        await data_base_agent.add_graph_nodes(graph_nodes)

        new_course = Graph(
            graph_id=str(ObjectId()),
            nodes=DefaultGraph.create_users_graph_nodes(graph_nodes),
            title=DefaultGraph.default_title,
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
            message=None,
        )


async def get_graph_previews(
    request: GetGraphsPreviewRequest,
) -> GetGraphsPreviewResponse:
    try:
        graphs = await data_base_agent.get_graphs(
            [graph_item.graph_id for graph_item in request.message]
        )
        graphs_previews: list[GraphPreview] = [
            GraphPreview(
                graph_id=graph.graph_id,
                title=graph.title,
                progress=round(
                    sum(int(node.is_studied) for node in graph.nodes)
                    / len(graph.nodes)
                    * 100,
                    2,
                ),
            )
            for graph in graphs
        ]
        return GetGraphsPreviewResponse(
            request_id=request.request_id,
            message=graphs_previews,
            status=ResponseCodes.OK,
        )

    except PyMongoError:
        return GetGraphsPreviewResponse(
            request_id=request.request_id,
            status=ResponseCodes.INTERNAL_ERROR,
            message=None,
        )
