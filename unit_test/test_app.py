from orchestrator.app import App
from orchestrator.dto import (
    GetGraphsRequest,
    GetGraphsResponse,
    Graph,
    GraphItem,
    ResponseCodes,
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
