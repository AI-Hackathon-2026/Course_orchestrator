from bson import ObjectId

from orchestrator.mongo.mongo_interface import MongoInterface


class MongoMock(MongoInterface):
    def __init__(self):
        topics: list[dict] = [
            {
                "_id": ObjectId("507f1f77bcf86cd799439011"),
                "title": "Основы Python",
                "topic_content": "Переменные, циклы, функции, ООП, исключения.",
            }
        ]

        graph_nodes: list[dict] = [
            {
                "_id": ObjectId("507f1f77bcf86cd799439012"),
                "graph_id": "507f1f77bcf86cd799439013",
                "topic_id": "507f1f77bcf86cd799439011",
                "next_node_id": None,
            }
        ]

        graphs: list[dict] = [
            {
                "_id": ObjectId("507f1f77bcf86cd799439013"),
                "title": "Основной граф обучения",
                "nodes": [
                    {
                        "_id": ObjectId("507f1f77bcf86cd799439012"),
                        "topic_id": "507f1f77bcf86cd799439011",
                        "title": "Основы Python",
                        "is_studied": False,
                        "is_major": True,
                        "next_node_id": None,
                    }
                ],
            }
        ]
        fake_bd = {"topics": topics, "graph_nodes": graph_nodes, "graphs": graphs}
        self.fake_bd = fake_bd

    async def get_graphs(self, graphs_ids: list[ObjectId]) -> list[dict]:
        result = []
        for graph_id in graphs_ids:
            for graph in self.fake_bd["graphs"]:
                if graph["_id"] == graph_id:
                    result.append(graph)
        return result

    async def get_topic(self, topic_id: ObjectId) -> dict | None:
        for topic in self.fake_bd["topics"]:
            if topic["_id"] == topic_id:
                return topic
        return None

    async def get_all_topics(self) -> list[dict]:
        return self.fake_bd["topics"]

    async def add_graph_nodes(self, graph_nodes: list[dict]):
        self.fake_bd["graph_nodes"].extend(graph_nodes)

    async def add_graph(self, graph: dict):
        self.fake_bd["graphs"].extend(graph)

    async def set_node_as_ended(self, node_id: ObjectId, graph_id: ObjectId):
        for graph in self.fake_bd["graphs"]:
            if graph["_id"] == graph_id:
                for node in graph["nodes"]:
                    if node["_id"] == node_id:
                        node["is_studied"] = True
                return

    async def get_node(self, node_id: ObjectId) -> dict | None:
        for node in self.fake_bd["nodes"]:
            if node["_id"] == node_id:
                return node
        return None

    async def check_connection(self) -> bool:
        return True
