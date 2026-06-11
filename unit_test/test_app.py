from orchestrator.app import App
from orchestrator.dto import (
    CreateCourseData,
    CreateCourseRequest,
    CreateCourseResponse,
    GetGraphsPreviewRequest,
    GetGraphsPreviewResponse,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
    Graph,
    GraphItem,
    GraphPreview,
    NodeItem,
    ResponseCodes,
    SetNodeAsEndedRequest,
    SetNodeAsEndedResponse,
    Topic,
    TopicItem,
    UsersGraph,
)
from orchestrator.graph import UsersGraphNode
from unit_test.mongo_mock import MongoMock

app = App(mongo_client=MongoMock())


class TestGetGraphs:
    @staticmethod
    async def test_void_ids():
        res = await app.get_graphs(request=GetGraphsRequest(request_id="1", message=[]))
        assert res == GetGraphsResponse(
            request_id="1", message=[], status=ResponseCodes.OK
        )

    @staticmethod
    async def test_incorrect_ids():
        res = await app.get_graphs(
            request=GetGraphsRequest(
                request_id="1", message=[GraphItem(graph_id="123")]
            )
        )
        assert res == GetGraphsResponse(
            request_id="1", message=None, status=ResponseCodes.BAD_REQUEST
        )

    @staticmethod
    async def test_not_exists_ids():
        res = await app.get_graphs(
            request=GetGraphsRequest(
                request_id="1", message=[GraphItem(graph_id="507f1f77bcf86cd799439099")]
            )
        )
        assert res == GetGraphsResponse(
            request_id="1", message=[], status=ResponseCodes.OK
        )

    @staticmethod
    async def test_exists_ids():
        res = await app.get_graphs(
            request=GetGraphsRequest(
                request_id="1", message=[GraphItem(graph_id="507f1f77bcf86cd799439013")]
            )
        )
        assert res == GetGraphsResponse(
            request_id="1",
            message=[
                Graph(
                    graph_id="507f1f77bcf86cd799439013",
                    title="Основной граф обучения",
                    nodes=[
                        UsersGraphNode(
                            node_id="507f1f77bcf86cd799439012",
                            topic_id="507f1f77bcf86cd799439011",
                            title="Основы Python",
                            is_studied=False,
                            is_major=True,
                            next_node_id=None,
                        )
                    ],
                )
            ],
            status=ResponseCodes.OK,
        )

    @staticmethod
    async def test_not_exists_and_exists_ids():
        res = await app.get_graphs(
            request=GetGraphsRequest(
                request_id="1",
                message=[
                    GraphItem(graph_id="507f1f77bcf86cd799439013"),
                    GraphItem(graph_id="507f1f77bcf86cd799439099"),
                ],
            )
        )
        assert res == GetGraphsResponse(
            request_id="1",
            message=[
                Graph(
                    graph_id="507f1f77bcf86cd799439013",
                    title="Основной граф обучения",
                    nodes=[
                        UsersGraphNode(
                            node_id="507f1f77bcf86cd799439012",
                            topic_id="507f1f77bcf86cd799439011",
                            title="Основы Python",
                            is_studied=False,
                            is_major=True,
                            next_node_id=None,
                        )
                    ],
                )
            ],
            status=ResponseCodes.OK,
        )


class TestGetTopic:
    @staticmethod
    async def test_incorrect_id():
        res = await app.get_topic(
            request=GetTopicRequest(request_id="1", message=TopicItem(topic_id="123"))
        )
        assert res == GetTopicResponse(
            request_id="1", message=None, status=ResponseCodes.BAD_REQUEST
        )

    @staticmethod
    async def test_exists_id():
        res = await app.get_topic(
            request=GetTopicRequest(
                request_id="1", message=TopicItem(topic_id="507f1f77bcf86cd799439011")
            )
        )
        assert res == GetTopicResponse(
            request_id="1",
            message=Topic(
                topic_id="507f1f77bcf86cd799439011",
                title="Основы Python",
                topic_content="Переменные, циклы, функции, ООП, исключения.",
            ),
            status=ResponseCodes.OK,
        )

    @staticmethod
    async def test_get_not_exists_id():
        res = await app.get_topic(
            request=GetTopicRequest(
                request_id="1", message=TopicItem(topic_id="507f1f77bcf86cd799439099")
            )
        )
        assert res == GetTopicResponse(
            request_id="1", message=None, status=ResponseCodes.OK
        )


class TestCreateCourse:
    @staticmethod
    async def test_create_course():
        res = await app.create_new_course(
            request=CreateCourseRequest(
                request_id="1",
                message=CreateCourseData(
                    username="misha", requirements="oosd", links=[]
                ),
            )
        )
        graph_id = res.message.graph_id
        assert res == CreateCourseResponse(
            request_id="1",
            message=UsersGraph(username="misha", graph_id=graph_id),
            status=ResponseCodes.OK,
        )


class TestGetGraphPreviews:
    @staticmethod
    async def test_void_ids():
        res = await app.get_graph_previews(
            request=GetGraphsPreviewRequest(request_id="1", message=[])
        )
        assert res == GetGraphsPreviewResponse(
            request_id="1", message=[], status=ResponseCodes.OK
        )

    @staticmethod
    async def test_incorrect_ids():
        res = await app.get_graph_previews(
            request=GetGraphsPreviewRequest(
                request_id="1", message=[GraphItem(graph_id="123")]
            )
        )
        assert res == GetGraphsPreviewResponse(
            request_id="1", message=None, status=ResponseCodes.BAD_REQUEST
        )

    @staticmethod
    async def test_not_exists_ids():
        res = await app.get_graph_previews(
            request=GetGraphsPreviewRequest(
                request_id="1", message=[GraphItem(graph_id="507f1f77bcf86cd799439099")]
            )
        )
        assert res == GetGraphsPreviewResponse(
            request_id="1", message=[], status=ResponseCodes.OK
        )

    @staticmethod
    async def test_exists_ids():
        res = await app.get_graph_previews(
            request=GetGraphsPreviewRequest(
                request_id="1", message=[GraphItem(graph_id="507f1f77bcf86cd799439013")]
            )
        )
        assert res == GetGraphsPreviewResponse(
            request_id="1",
            message=[
                GraphPreview(
                    graph_id="507f1f77bcf86cd799439013",
                    title="Основной граф обучения",
                    progress=0,
                )
            ],
            status=ResponseCodes.OK,
        )

    @staticmethod
    async def test_not_exists_and_exists_ids():
        res = await app.get_graph_previews(
            request=GetGraphsPreviewRequest(
                request_id="1",
                message=[
                    GraphItem(graph_id="507f1f77bcf86cd799439013"),
                    GraphItem(graph_id="507f1f77bcf86cd799439099"),
                ],
            )
        )
        assert res == GetGraphsPreviewResponse(
            request_id="1",
            message=[
                GraphPreview(
                    graph_id="507f1f77bcf86cd799439013",
                    title="Основной граф обучения",
                    progress=0,
                )
            ],
            status=ResponseCodes.OK,
        )


class TestSetNodeEnded:
    @staticmethod
    async def test_incorrect_id():
        res = await app.set_node_as_ended(
            request=SetNodeAsEndedRequest(
                request_id="1", message=NodeItem(node_id="123")
            )
        )
        assert res == SetNodeAsEndedResponse(
            request_id="1", message=None, status=ResponseCodes.BAD_REQUEST
        )

    @staticmethod
    async def test_not_exists_id():
        res = await app.set_node_as_ended(
            request=SetNodeAsEndedRequest(
                request_id="1", message=NodeItem(node_id="507f1f77bcf86cd799439099")
            )
        )
        assert res == SetNodeAsEndedResponse(
            request_id="1", message=None, status=ResponseCodes.BAD_REQUEST
        )

    @staticmethod
    async def test_exists_id():
        res = await app.set_node_as_ended(
            request=SetNodeAsEndedRequest(
                request_id="1", message=NodeItem(node_id="507f1f77bcf86cd799439012")
            )
        )
        assert res == SetNodeAsEndedResponse(
            request_id="1", message=None, status=ResponseCodes.OK
        )
