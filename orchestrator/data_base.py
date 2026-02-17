from orchestrator.graph import Graph, GraphNode, Topic


class Mongo:
    pass


class DataBaseAgent:
    def __init__(self):
        pass

    async def get_graphs(self, graph_ids: list[str]) -> list[Graph]:
        pass

    def add_default_topics(self):
        pass

    async def get_topic_from_node(self, node_id: int, graph_id: str) -> Topic | None:
        pass

    async def add_graph_nodes(self, graph_nodes: list[GraphNode]):
        pass

    async def add_graph(self, graph: Graph):
        pass


data_base_agent = DataBaseAgent()
