from pymongo import MongoClient

from orchestrator.config import mongo_config
from orchestrator.default_graph import default_graph
from orchestrator.pydantic_to_mongo import MongoTrans
from orchestrator.rest_handler import start_rest

if __name__ == "__main__":
    with MongoClient(mongo_config.MONGO_URL) as client:
        courses_db = client[mongo_config.DATABASE]
        if "topics" not in courses_db.list_collection_names():
            topics_collection = courses_db["topics"]
            for topic in default_graph.topics:
                topics_collection.insert_one(MongoTrans.topic_trans(topic))
        if "graphs" not in courses_db.list_collection_names():
            courses_db.create_collection("graphs")
        if "nodes" not in courses_db.list_collection_names():
            courses_db.create_collection("nodes")
    start_rest()
