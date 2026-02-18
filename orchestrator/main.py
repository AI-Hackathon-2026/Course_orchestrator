from orchestrator.mongo_init import mongo_init
from orchestrator.rest_handler import start_rest


if __name__ == "__main__":
    mongo_init()
    start_rest()
