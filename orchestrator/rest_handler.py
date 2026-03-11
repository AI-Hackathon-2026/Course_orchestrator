import uvicorn
from fastapi import FastAPI

from orchestrator.app import create_new_course, get_graphs, get_topic
from orchestrator.config import backend_config
from orchestrator.dto import (
    CreateCourseRequest,
    CreateCourseResponse,
    GetGraphsRequest,
    GetGraphsResponse,
    GetTopicRequest,
    GetTopicResponse,
)

app = FastAPI()


@app.get("/get_graphs", response_model=GetGraphsResponse)
async def get_graph_api(request: GetGraphsRequest):
    return await get_graphs(request)


@app.get("/get_topic", response_model=GetTopicResponse)
async def get_topic_api(request: GetTopicRequest):
    return await get_topic(request)


@app.post("/create_new_course", response_model=CreateCourseResponse)
async def new_course_api(request: CreateCourseRequest):
    return await create_new_course(request)

def start_rest():
    uvicorn.run(
        "orchestrator.rest_handler:app",
        host=backend_config.HOST,
        port=backend_config.PORT,
        reload=backend_config.RELOAD,
    )
