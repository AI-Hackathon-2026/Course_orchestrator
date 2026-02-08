from orchestrator.default_graph import topics
from orchestrator.graph import Graph, Topic


class Redis:
    def __init__(self):
        self._graphs_db = []
        self._topics_db = topics
        # with open("graphs.txt", "w") as file:
        # file.write('')
        # with open("topics.txt", "w") as file:
        # for topic in self._topics_db:
        # file.write(str(topic) + '\n')

    def get_graphs(self, graph_ids: list[str]) -> list[Graph]:
        graphs = []
        for graph in self._graphs_db:
            if graph.graph_id in graph_ids:
                graphs.append(graph)
        return graphs

    def get_topic(self, topic_id) -> Topic | None:
        for topic in self._topics_db:
            if topic.topic_id == topic_id:
                return topic
        return None

    def add_graph(self, graph: Graph):
        self._graphs_db.append(graph)
        # with open("graphs.txt", "a") as file:
        #   file.write(str(graph) + '\n')


class DataBase:
    def __init__(self):
        self.redis = Redis()

    def get_graphs(self, graph_ids: list[str]) -> list[Graph]:
        return self.redis.get_graphs(graph_ids)

    def get_topic_from_node(self, node_id: int, graph_id: str) -> Topic | None:
        graph = self.redis.get_graphs([graph_id])[0]
        if graph:
            node = graph.first_node
            while node:
                if node.node_id == node_id:
                    return self.redis.get_topic(node.topic_id)
                node = node.next_node
        return None

    def add_graph(self, graph: Graph):
        self.redis.add_graph(graph)


data_base = DataBase()
