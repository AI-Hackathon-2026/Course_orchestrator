import uuid

from orchestrator.data_base import data_base
from orchestrator.default_graph import graph_nodes
from orchestrator.dto import (
    CreateCourseRequest,
    CreateCourseResponse,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
)
from orchestrator.graph import Graph, Topic


async def get_graphs(request: GetGraphsRequest) -> GetGraphsResponse:
    graphs = data_base.get_graphs(
        [graph_item.graph_id for graph_item in request.message]
    )
    if graphs:
        return GetGraphsResponse(request_id=request.request_id, message=graphs)
    else:
        return GetGraphsResponse(
            request_id=request.request_id, message="There are no graphs with such ids"
        )


async def get_topic(request: GetTopicRequest) -> GetTopicResponse:
    topic: Topic = data_base.get_topic_from_node(
        node_id=request.message.topic_id, graph_id=request.message.graph_id
    )
    if topic:
        return GetTopicResponse(request_id=request.request_id, message=topic)
    else:
        return GetTopicResponse(
            request_id=request.request_id, message="There are no such topic"
        )


async def create_new_course(request: CreateCourseRequest) -> CreateCourseResponse:
    new_course = Graph(
        **{
            "graph_id": str(uuid.uuid4()),
            "nodes": [node.model_dump() for node in graph_nodes],
        }
    )
    data_base.add_graph(new_course)
    return CreateCourseResponse(request_id=request.request_id, message=200)
