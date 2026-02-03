from pydantic import BaseModel


class Topic(BaseModel):
    topic_id: int
    title: str
    context: str


class Graph(BaseModel):
    graph_id: int
    title: str
    topics: list[tuple[Topic, bool]]
