from uuid import uuid4

from orchestrator.graph import GraphNode, Topic, UsersGraphNode

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


def create_graph_nodes() -> list[GraphNode]:
    graph_nodes = [
        GraphNode(
            node_id=str(uuid4()),
            topic_id=topic.topic_id,
            is_studied=False,
            is_major=False,
            prev_node_id=None,
            next_node_id=None,
        )
        for topic in topics
    ]
    for i, node in enumerate(graph_nodes):
        if i != 0:
            node.prev_node_id = graph_nodes[i - 1].node_id
        if i != len(graph_nodes) - 1:
            node.next_node_id = graph_nodes[i + 1].node_id

    return graph_nodes


def create_users_graph_nodes(graph_nodes: list[GraphNode]) -> list[UsersGraphNode]:
    users_graph_nodes = []

    for node in graph_nodes:
        users_graph_nodes.append(
            UsersGraphNode(
                node_id=node.node_id,
                topic_id=node.topic_id,
                title=topics[0].title,
                is_studied=node.is_studied,
                is_major=node.is_major,
                next_node_id=node.next_node_id,
            )
        )

    return users_graph_nodes
