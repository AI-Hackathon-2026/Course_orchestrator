from bson import ObjectId
from pymongo import AsyncMongoClient

from orchestrator.default_graph import DefaultGraph
from orchestrator.graph import GraphNode


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

    async def recalculate_graph(self, graph_id):
        graph_nodes: list[dict] = (
            await self.data_base["nodes"].find({"graph_id": graph_id}).to_list()
        )

        nodes_mapping: dict[str, GraphNode] = {}

        for node in graph_nodes:
            node["node_id"] = str(node["_id"])
            node.pop("_id")
            nodes_mapping[node["node_id"]] = GraphNode(**node)
        cur_node_id = ""
        for node in graph_nodes:
            if node["prev_node_id"] is None:
                cur_node_id = node["node_id"]

        sorted_graph_nodes: list[GraphNode] = []
        while cur_node_id is not None:
            cur_node = nodes_mapping[cur_node_id]
            sorted_graph_nodes.append(cur_node)
            cur_node_id = cur_node.next_node_id

        graph_nodes = DefaultGraph.create_users_graph_nodes(sorted_graph_nodes)
        graph_nodes = [node.model_dump() for node in graph_nodes]
        await self.data_base["graph"].update_one(
            {"graph_id": graph_id}, {"$set": {"nodes": graph_nodes}}
        )

    async def set_node_as_ended(self, node_id: ObjectId):
        nodes_collection = self.data_base["nodes"]
        await nodes_collection.update_one(
            {"_id": node_id}, {"$set": {"is_studied": True}}
        )

    async def get_node(self, node_id: ObjectId):
        nodes_collection = self.data_base["nodes"]
        return await nodes_collection.find_one({"_id": node_id})
