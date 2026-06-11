from typing import Type

from bson import ObjectId

from orchestrator.graph import Graph, GraphNode, MLTopic


class MongoTrans:
    @classmethod
    def pydantic_to_mongo(cls, model: Graph | GraphNode | MLTopic) -> dict:
        model_class = type(model)
        if model_class is Graph:
            id_name = "graph_id"
        elif model_class is GraphNode:
            id_name = "node_id"
        else:
            id_name = "topic_id"
        model = model.model_dump()
        if model_class is Graph:
            for node in model["nodes"]:
                node["node_id"] = ObjectId(node["node_id"])
        model["_id"] = ObjectId(model[id_name])
        model.pop(id_name)
        return model

    @classmethod
    def mongo_to_pydantic(
        cls, model_class: Type[Graph | GraphNode | MLTopic], mongo_dict: dict
    ) -> Graph | GraphNode | MLTopic:
        if model_class is Graph:
            id_name = "graph_id"
        elif model_class is GraphNode:
            id_name = "node_id"
        else:
            id_name = "topic_id"
        if model_class is Graph:
            for node in mongo_dict["nodes"]:
                node["node_id"] = str(node["_id"])
        mongo_dict[id_name] = str(mongo_dict["_id"])
        mongo_dict.pop("_id")
        return model_class(**mongo_dict)
