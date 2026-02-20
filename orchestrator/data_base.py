from bson import ObjectId
from pymongo import AsyncMongoClient

from orchestrator.config import mongo_config
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


data_base_agent = DataBaseAgent()
