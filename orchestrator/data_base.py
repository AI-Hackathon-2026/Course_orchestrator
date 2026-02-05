from orchestrator.default_graph import topics
from orchestrator.graph import Graph, Topic


class DataBase:
    _graphs_db: list[Graph]
    _topics_db: list[Topic]

    def __init__(self):
        super().__init__()
        self._graphs_db = []
        self._topics_db = topics

    def get_graphs(self, graphs_ids: list[str]) -> list[Graph] | None:
        graphs = []
        for graph in self._graphs_db:
            if graph.graph_id in graphs_ids:
                graphs.append(graph)
        return graphs if len(graphs) == len(graphs_ids) else None

    def _get_topic(self, topic_id: int) -> Topic | None:
        for topic in self._topics_db:
            if topic.topic_id == topic_id:
                return topic
        return None

    def get_topic_from_node(self, node_id: int, graph_id: str) -> Topic | None:
        graph = self.get_graphs([graph_id])[0]
        if graph:
            for node in graph.nodes:
                if node.node_id == node_id:
                    return self._get_topic(node.topic_id)
        return None

    def add_graph(self, graph: Graph):
        self._graphs_db.append(graph)
        # with open("file.txt", "a") as file:
        # file.write(str(graph) + '\n')


data_base = DataBase()
