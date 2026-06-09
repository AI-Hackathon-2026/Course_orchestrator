from pymongo import MongoClient

from orchestrator.config import mongo_config
from orchestrator.default_graph import DefaultGraph
from orchestrator.mongo.mongo_trans import MongoTrans


def mongo_init():
    with MongoClient(mongo_config.MONGO_URL) as client:
        courses_db = client[mongo_config.DATABASE]
        if "topics" not in courses_db.list_collection_names():
            topics_collection = courses_db["topics"]
            for topic in DefaultGraph.topics:
                topics_collection.insert_one(MongoTrans.pydantic_to_mongo(topic))
        if "graphs" not in courses_db.list_collection_names():
            courses_db.create_collection("graphs")
        if "nodes" not in courses_db.list_collection_names():
            courses_db.create_collection("nodes")
            courses_db["nodes"].create_index("graph_id")
