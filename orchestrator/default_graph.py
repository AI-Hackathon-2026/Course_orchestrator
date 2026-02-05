from orchestrator.graph import GraphNode, Topic

topics: list[Topic] = [
    Topic(
        topic_id=1,
        title="Структуры данных",
        topic_content="Массив, Связаный список, Хеш-таблица, Множество, Стек, Очередь, Куча",
    ),
    Topic(
        topic_id=2,
        title="Основные алгоритмы",
        topic_content="Сложность алгоритма, Грубая Сила, Бинарный поиск, Разделяй и властвуй",
    ),
    Topic(
        topic_id=3,
        title="Динамическое программирование",
        topic_content="Мемоизация, 1dp, 2dp",
    ),
]

graph_nodes: list[GraphNode] = [
    GraphNode(node_id=1, topic_id=1, studied=False),
    GraphNode(node_id=2, topic_id=2, studied=False),
    GraphNode(node_id=3, topic_id=3, studied=False),
]
