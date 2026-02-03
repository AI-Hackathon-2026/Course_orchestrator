from config import graphConfig
from dto import (
    GetGraphRequest,
    GetGraphResponse,
    GetTopicRequest,
    GetTopicResponse,
    NewCourseRequest,
    NewCourseResponse,
)
from graph import Graph, Topic

graphs_counter = 0
db: list[Graph] = []


def get_graph_db(graphs_id: list[int]) -> list[Graph] | None:
    graphs = []
    for graph in db:
        if graph.graph_id in graphs_id:
            graphs.append(graph)
    return graphs


def get_topic_db(topic_id: int, graph_id) -> Topic | None:
    for graph in db:
        if graph.graph_id == graph_id:
            for topic in graph.topics:
                if topic[0].topic_id == topic_id:
                    return topic[0]
    return None


def new_course_db() -> int | str:
    global graphs_counter
    topics = [(Topic(**topic), False) for topic in graphConfig.topics]
    new_graph = Graph(graph_id=graphs_counter, title="Алгоритмы", topics=topics)
    graphs_counter += 1
    db.append(new_graph)
    return 200


async def get_graph(request: GetGraphRequest) -> GetGraphResponse:
    graphs_ids = [graph.graph_id for graph in GetGraphRequest.message]
    graphs = get_graph_db(graphs_ids)
    if graphs is None:
        return GetGraphResponse(
            request_id=request.request_id, message="There are no graphs with such IDs"
        )
    else:
        return GetGraphResponse(request_id=request.request_id, message=graphs)


async def get_topic(request: GetTopicRequest) -> GetTopicResponse:
    topic = get_topic_db(request.message.topic_id, request.message.graph_id)
    if topic is None:
        return GetTopicResponse(
            request_id=request.request_id, message="There are no topic with such ID"
        )
    else:
        return GetTopicResponse(request_id=request.request_id, message=topic)


async def new_course(request: NewCourseRequest) -> NewCourseResponse:
    status = new_course_db()
    return NewCourseResponse(request_id=request.request_id, message=status)
