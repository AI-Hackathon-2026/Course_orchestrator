from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from orchestrator.app import App
from orchestrator.config import mongo_config
from orchestrator.mongo.mongo_client import MongoClient
from orchestrator.mongo.mongo_init import mongo_init


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    api_app.state.is_ready = False
    mongo_init()
    mongo_connect = AsyncMongoClient(
        mongo_config.MONGO_URL,
        maxPoolSize=mongo_config.MAX_POOL_SIZE,
        minPoolSize=mongo_config.MIN_POOL_SIZE,
    )
    mongo_client = MongoClient(mongo_connection=mongo_connect)
    app = App(mongo_client=mongo_client)
    api_app.state.app = app
    api_app.state.is_ready = True
    yield
    await mongo_connect.close()


def create_app():
    app = FastAPI(lifespan=lifespan)
    return app
