from bson import ObjectId

from orchestrator.graph import Graph, GraphNode, Topic


class MongoTrans:
    @classmethod
    def topic_trans(cls, topic: Topic) -> dict:
        mongo_topic = topic.model_dump()
        mongo_topic["_id"] = ObjectId(mongo_topic["topic_id"])
        mongo_topic.pop("topic_id")
        return mongo_topic

    @classmethod
    def graph_trans(cls, graph: Graph) -> dict:
        mongo_graph = graph.model_dump()
        mongo_graph["_id"] = ObjectId(mongo_graph["graph_id"])
        mongo_graph.pop("graph_id")
        return mongo_graph

    @classmethod
    def node_trans(cls, node: GraphNode) -> dict:
        mongo_node = node.model_dump()
        mongo_node["_id"] = ObjectId(mongo_node["node_id"])
        mongo_node.pop("node_id")
        return mongo_node
