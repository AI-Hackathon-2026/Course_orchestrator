from bson import ObjectId
from pymongo import AsyncMongoClient

from orchestrator.config import mongo_config
from orchestrator.default_graph import DefaultGraph
from orchestrator.graph import Graph, GraphNode, Topic
from orchestrator.mongo_trans import MongoTrans


class Mongo:
    def __init__(self):
        self.client = AsyncMongoClient(mongo_config.MONGO_URL)
        self.data_base = self.client["courses"]

    async def get_graphs(self, graphs_ids: list[ObjectId]) -> list[dict]:
        result = (
            await self.data_base["graphs"].find({"_id": {"$in": graphs_ids}}).to_list()
        )
        return result

    async def get_topic(self, topic_id: ObjectId) -> dict | None:
        result = await self.data_base["topics"].find_one({"_id": topic_id})
        return result

    async def get_all_topics(self) -> list[dict]:
        result = await self.data_base["topics"].find().to_list()
        return result

    async def add_graph_nodes(self, graph_nodes: list[dict]):
        await self.data_base["nodes"].insert_many(graph_nodes)

    async def add_graph(self, graph: dict):
        await self.data_base["graphs"].insert_one(graph)

    async def recalculate_graph(self, graph_id):
        graph_nodes = (
            await self.data_base["nodes"].find({"graph_id": graph_id}).to_list()
        )

        nodes_mapping: dict[str, GraphNode] = {
            node["node_id"]: GraphNode(**node) for node in graph_nodes
        }
        cur_node_id = ""
        for node in graph_nodes:
            if node["prev_node_id"] is None:
                cur_node_id = node["node_id"]

        sorted_graph_nodes: list[GraphNode] = []
        while cur_node_id is not None:
            cur_node = nodes_mapping[cur_node_id]
            sorted_graph_nodes.append(cur_node)
            cur_node_id = cur_node.next_node_id

        graph_nodes = await DefaultGraph.create_users_graph_nodes(sorted_graph_nodes)
        graph_nodes = [node.model_dump() for node in graph_nodes]
        await self.data_base["graph"].update_one(
            {"graph_id": graph_id}, {"$set": {"nodes": graph_nodes}}
        )


class DataBaseAgent:
    def __init__(self):
        self.mongo = Mongo()

    async def get_graphs(self, graph_ids: list[str]) -> list[Graph]:
        graph_ids = [ObjectId(graph_id) for graph_id in graph_ids]
        result = await self.mongo.get_graphs(graph_ids)
        graphs = [MongoTrans.mongo_to_pydantic(Graph, graph) for graph in result]
        return graphs

    async def get_topic(self, topic_id: str) -> Topic | None:
        result = await self.mongo.get_topic(ObjectId(topic_id))
        return None if result is None else MongoTrans.mongo_to_pydantic(Topic, result)

    async def add_graph_nodes(self, graph_nodes: list[GraphNode]):
        graph_nodes = [MongoTrans.pydantic_to_mongo(node) for node in graph_nodes]
        await self.mongo.add_graph_nodes(graph_nodes)

    async def add_graph(self, graph: Graph):
        await self.mongo.add_graph(MongoTrans.pydantic_to_mongo(graph))

    async def get_all_topics(self) -> list[Topic]:
        topics = await self.mongo.get_all_topics()
        topics = [MongoTrans.mongo_to_pydantic(Topic, topic) for topic in topics]
        return topics

    async def recalculate_graph(self, graph_id):
        await self.mongo.recalculate_graph(graph_id=graph_id)


data_base_agent = DataBaseAgent()
