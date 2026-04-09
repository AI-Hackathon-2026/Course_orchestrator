from bson import ObjectId
from typing import Type
from orchestrator.graph import Graph, GraphNode, Topic


class MongoTrans:
    @classmethod
    def pydantic_to_mongo(cls, model: Graph | GraphNode | Topic) -> dict:
        model_class = type(model)
        if model_class is Graph:
            id_name = "graph_id"
        elif model_class is GraphNode:
            id_name = "node_id"
        else:
            id_name = "topic_id"
        model = model.model_dump()
        model["_id"] = ObjectId(model[id_name])
        model.pop(id_name)
        return model

    @classmethod
    def mongo_to_pydantic(cls, model_class: Type[Graph | GraphNode | Topic], mongo_dict: dict) -> Graph | GraphNode | Topic:
        if model_class is Graph:
            id_name = "graph_id"
        elif model_class is GraphNode:
            id_name = "node_id"
        else:
            id_name = "topic_id"
        mongo_dict[id_name] = str(mongo_dict["_id"])
        mongo_dict.pop("_id")
        return model_class(**mongo_dict)