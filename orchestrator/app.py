import uuid

from langfuse import Langfuse, observe

from orchestrator.config import langfuse_settings
from orchestrator.data_base import data_base
from orchestrator.default_graph import create_graph
from orchestrator.dto import (
    CreateCourseRequest,
    CreateCourseResponse,
    CreateCourseResponseItem,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
)
from orchestrator.graph import Graph

langfuse = Langfuse(
    secret_key=langfuse_settings.SECRET_KEY,
    public_key=langfuse_settings.PUBLIC_KEY,
    host=langfuse_settings.LANGFUSE_SERVER,
)


@observe(name="get_graphs")
async def get_graphs(request: GetGraphsRequest) -> GetGraphsResponse:
    graphs = data_base.get_graphs(
        [graph_item.graph_id for graph_item in request.message]
    )
    return GetGraphsResponse(request_id=request.request_id, message=graphs, status="OK")


@observe(name="get_topic")
async def get_topic(request: GetTopicRequest) -> GetTopicResponse:
    topic = data_base.get_topic_from_node(
        node_id=request.message.topic_id, graph_id=request.message.graph_id
    )
    return GetTopicResponse(request_id=request.request_id, message=topic, status="OK")


@observe(name="create_new_course")
async def create_new_course(request: CreateCourseRequest) -> CreateCourseResponse:
    first_node = create_graph()
    new_course = Graph(
        **{
            "graph_id": str(uuid.uuid4()),
            "first_node": first_node.model_dump(),
        }
    )
    data_base.add_graph(new_course)
    return CreateCourseResponse(
        request_id=request.request_id,
        status="OK",
        message=CreateCourseResponseItem(
            username=request.message.username, graph_id=new_course.graph_id, code=200
        ),
    )
