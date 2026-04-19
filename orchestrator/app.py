from bson import ObjectId
from pymongo.errors import PyMongoError

from orchestrator.data_base import MongoClient
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
from orchestrator.graph import Graph, GraphPreview, MLTopic, Topic
from orchestrator.mongo_trans import MongoTrans


class App:
    def __init__(self, mongo_client: MongoClient) -> None:
        self.mongo_client = mongo_client

    async def get_graphs(self, request: GetGraphsRequest) -> GetGraphsResponse:
        try:
            graphs = await self.mongo_client.get_graphs(
                [ObjectId(graph_item.graph_id) for graph_item in request.message]
            )
            graphs = [MongoTrans.mongo_to_pydantic(Graph, graph) for graph in graphs]
            return GetGraphsResponse(
                request_id=request.request_id, message=graphs, status=ResponseCodes.OK
            )
        except PyMongoError:
            return GetGraphsResponse(
                request_id=request.request_id,
                message=None,
                status=ResponseCodes.INTERNAL_ERROR,
            )

    async def get_topic(self, request: GetTopicRequest) -> GetTopicResponse:
        try:
            topic = await self.mongo_client.get_topic(
                topic_id=ObjectId(request.message.topic_id)
            )
            if topic is not None:
                topic = MongoTrans.mongo_to_pydantic(MLTopic, topic)
            topic = topic.model_dump()
            topic.pop("context")
            topic = Topic(**topic)
            return GetTopicResponse(
                request_id=request.request_id, message=topic, status=ResponseCodes.OK
            )
        except PyMongoError:
            return GetTopicResponse(
                request_id=request.request_id,
                message=None,
                status=ResponseCodes.INTERNAL_ERROR,
            )

    async def create_new_course(
        self, request: CreateCourseRequest
    ) -> CreateCourseResponse:
        try:
            graph_id = str(ObjectId())
            topics = await self.mongo_client.get_all_topics()
            topics = [MongoTrans.mongo_to_pydantic(MLTopic, topic) for topic in topics]
            graph_nodes = DefaultGraph.create_graph_nodes(graph_id, topics)
            await self.mongo_client.add_graph_nodes(
                [MongoTrans.pydantic_to_mongo(graph_node) for graph_node in graph_nodes]
            )

            new_course = Graph(
                graph_id=str(ObjectId()),
                nodes=DefaultGraph.create_users_graph_nodes(graph_nodes),
                title=DefaultGraph.default_title,
            )
            await self.mongo_client.add_graph(MongoTrans.pydantic_to_mongo(new_course))

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
        self,
        request: GetGraphsPreviewRequest,
    ) -> GetGraphsPreviewResponse:
        try:
            graphs = (
                await self.get_graphs(
                    GetGraphsRequest(request_id="", message=request.message)
                )
            ).message
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
