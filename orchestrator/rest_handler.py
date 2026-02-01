import uvicorn
from fastapi import FastAPI

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
async def get_graph(request: GetGraphRequest):
    print(request)
    return GetGraphResponse(zaglushka=1)


@app.get("/get_topic", response_model=GetTopicResponse)
async def get_topic(request: GetTopicRequest):
    print(request)
    return GetTopicResponse(zaglushka=1)


@app.post("/new_course", response_model=NewCourseResponse)
async def new_course(request: NewCourseRequest):
    print(request)
    return NewCourseResponse(zaglushka=1)


if __name__ == "__main__":
    uvicorn.run(
        "rest_handler:app",
        host=backend_config.host,
        port=backend_config.port,
        reload=backend_config.reload,
    )
