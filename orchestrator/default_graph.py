from uuid import uuid4

from orchestrator.graph import Graph, GraphNode, Topic

topics: list[Topic] = [
    Topic(
        topic_id=str(uuid4()),
        title="Структуры данных",
        topic_content="Массив, Связаный список, Хеш-таблица, Множество, Стек, Очередь, Куча",
    ),
    Topic(
        topic_id=str(uuid4()),
        title="Основные алгоритмы",
        topic_content="Сложность алгоритма, Грубая Сила, Бинарный поиск, Разделяй и властвуй",
    ),
    Topic(
        topic_id=str(uuid4()),
        title="Динамическое программирование",
        topic_content="Мемоизация, 1dp, 2dp",
    ),
]


def create_graph() -> Graph:
    graph_nodes = [
        GraphNode(
            node_id=str(uuid4()),
            topic_id=topic.topic_id,
            is_studied=False,
            is_major=False,
            prev_node=None,
            next_node=None,
        )
        for topic in topics
    ]
    for i, node in enumerate(graph_nodes):
        if i != 0:
            node.prev_node = graph_nodes[i - 1].node_id
        if i != len(graph_nodes) - 1:
            node.next_node = graph_nodes[i + 1].node_id
    return Graph(graph_id=str(uuid4()), first_node_id=graph_nodes[0].node_id)
