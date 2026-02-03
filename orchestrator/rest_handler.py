import uvicorn
from fastapi import FastAPI

from orchestrator.app import get_graph, get_topic, new_course
from orchestrator.config import backend_config
from orchestrator.dto import (
    GetGraphRequest,
    GetGraphResponse,
    GetTopicRequest,
    GetTopicResponse,
    NewCourseRequest,
    NewCourseResponse,
)

app = FastAPI()


@app.get("/get_graph", response_model=GetGraphResponse)
async def get_graph_api(request: GetGraphRequest):
    return await get_graph(request)


@app.get("/get_topic", response_model=GetTopicResponse)
async def get_topic_api(request: GetTopicRequest):
    return await get_topic(request)


@app.post("/new_course", response_model=NewCourseResponse)
async def new_course_api(request: NewCourseRequest):
    return await new_course(request)


if __name__ == "__main__":
    uvicorn.run(
        "rest_handler:app",
        host=backend_config.host,
        port=backend_config.port,
        reload=backend_config.reload,
    )
