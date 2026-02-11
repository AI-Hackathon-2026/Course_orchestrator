from orchestrator.default_graph import topics
from orchestrator.graph import Graph, Topic
from orchestrator.config import redis_config

class AsyncRedisClient:
    def __init__(self):
        self.redis = {}

    async def set(self, name: str, value: redis_config.REDIS_VALUE_TYPE):
        self.redis[name] = value

    async def get(self, name: str) -> redis_config.REDIS_VALUE_TYPE:
        return self.redis.get(name)


class DataBaseAgent:
    def __init__(self):
        self.redis = AsyncRedisClient()

    async def get_graphs(self, graph_ids: list[str]) -> list[Graph]:
        graphs = []
        for graph_id in graph_ids:
            if graph := await self.redis.get(graph_id):
                graphs.append(Graph(**graph))
        return graphs

    async def add_default_topics(self):
        for topic in topics:
            await self.redis.set(topic.topic_id, topic.model_dump())

    async def get_topic_from_node(self, node_id: int, graph_id: str) -> Topic | None:
        graph = await self.redis.get(graph_id)
        if graph:
            next_node_id = graph["first_node_id"]
            node = await self.redis.get(next_node_id)
            while node:
                if node["node_id"] == node_id:
                    return await self.redis.get(node["topic_id"])
                next_node_id = node["next_node"]
                node = await self.redis.get(next_node_id)
        return None

    async def add_graph(self, graph: Graph):
        await self.redis.set(name=graph.graph_id, value=graph.model_dump())


data_base_agent = DataBaseAgent()
data_base_agent.add_default_topics()
