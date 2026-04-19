from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from orchestrator.app import App
from orchestrator.config import mongo_config
from orchestrator.data_base import MongoClient
from orchestrator.mongo_init import mongo_init


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    mongo_init()
    mongo_connect = AsyncMongoClient(mongo_config.MONGO_URL)
    mongo_client = MongoClient(mongo_connection=mongo_connect)
    app = App(mongo_client=mongo_client)
    api_app.state.app = app
    yield
    await mongo_connect.close()


def create_app():
    app = FastAPI(lifespan=lifespan)
    return app
