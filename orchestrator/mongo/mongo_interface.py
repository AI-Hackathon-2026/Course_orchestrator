from abc import ABC, abstractmethod

from bson import ObjectId


class MongoInterface(ABC):
    @abstractmethod
    async def get_graphs(self, graphs_ids: list[ObjectId]) -> list[dict]:
        pass

    @abstractmethod
    async def get_topic(self, topic_id: ObjectId) -> dict | None:
        pass

    @abstractmethod
    async def get_all_topics(self) -> list[dict]:
        pass

    @abstractmethod
    async def add_graph_nodes(self, graph_nodes: list[dict]):
        pass

    @abstractmethod
    async def add_graph(self, graph: dict):
        pass

    @abstractmethod
    async def set_node_as_ended(self, node_id: ObjectId, graph_id: ObjectId):
        pass

    @abstractmethod
    async def get_node(self, node_id: ObjectId) -> dict | None:
        pass

    @abstractmethod
    async def check_connection(self) -> bool:
        pass
