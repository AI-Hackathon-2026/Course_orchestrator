from orchestrator.default_graph import topics
from orchestrator.graph import Graph, Topic


class Redis:
    def __init__(self):
        self.redis = {}
        for topic in topics:
            self.set(topic.topic_id, topic.model_dump())

    def set(self, name: str, value: str | int | dict | list | bool | None):
        self.redis[name] = value

    def get(self, name: str) -> str | int | dict | list | bool | None:
        return self.redis.get(name)


class DataBaseAgent:
    def __init__(self):
        self.redis = Redis()

    async def get_graphs(self, graph_ids: list[str]) -> list[Graph]:
        graphs = []
        for graph_id in graph_ids:
            if graph := self.redis.get(graph_id):
                graphs.append(Graph(**graph))
        return graphs

    async def get_topic_from_node(self, node_id: int, graph_id: str) -> Topic | None:
        graph = self.redis.get(graph_id)
        if graph:
            next_node_id = graph["first_node_id"]
            node = self.redis.get(next_node_id)
            while node:
                if node["node_id"] == node_id:
                    return self.redis.get(node["topic_id"])
                next_node_id = node["next_node"]
                node = self.redis.get(next_node_id)
        return None

    async def add_graph(self, graph: Graph):
        self.redis.set(name=graph.graph_id, value=graph.model_dump())


data_base_agent = DataBaseAgent()
