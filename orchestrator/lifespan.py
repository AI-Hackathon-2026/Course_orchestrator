from contextlib import asynccontextmanager
from fastapi import FastAPI
from orchestrator.mongo_init import mongo_init
from pymongo import AsyncMongoClient
from config import mongo_config
from orchestrator.app import App
from orchestrator.data_base import MongoClient


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    mongo_init()
    mongo_connect = AsyncMongoClient(mongo_config.MONGO_URL)
    mongo_client = MongoClient(mongo_connection=mongo_connect)
    app = App(mongo_client=mongo_client)
    api_app.state.app = app
    yield
    await mongo_connect.close()
