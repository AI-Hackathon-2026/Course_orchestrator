import asyncio

from bson import ObjectId
from pymongo import AsyncMongoClient

from orchestrator.config import mongo_config


class MongoClient:
    def __init__(self, mongo_connection: AsyncMongoClient):
        self.client = mongo_connection
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

    async def set_node_as_ended(self, node_id: ObjectId, graph_id: ObjectId):
        graphs_collection = self.data_base["graphs"]
        await graphs_collection.update_one(
            {"_id": graph_id, "nodes.node_id": node_id},
            {"$set": {"nodes.$.is_studied": True}},
        )

    async def get_node(self, node_id: ObjectId) -> dict:
        nodes_collection = self.data_base["nodes"]
        return await nodes_collection.find_one({"_id": node_id})

    async def check_connection(self) -> bool:
        try:
            await asyncio.wait_for(
                self.client.server_info(), mongo_config.HEALTH_CHECK_TIMEOUT
            )
            return True
        except Exception:
            return False
