from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pass


class BackendConfig(BaseSettings):
    port: int = 8067
    host: str = "localhost"
    reload: bool = True


class GraphConfig(BaseSettings):
    topics: list[dict[str | int, str]] = [
        {
            "topic_id": 1,
            "title": "Структуры данных",
            "context": "Массив, Связаный список, Хеш-таблица, Множество, Стек, Очередь, Куча",
        },
        {
            "topic_id": 2,
            "title": "Основные алгоритмы",
            "context": "Сложность алгоритма, Грубая Сила, Бинарный поиск, Разделяй и властвуй",
        },
        {
            "topic_id": 3,
            "title": "Динамическое программирование",
            "context": "Мемоизация, 1dp, 2dp",
        },
    ]


backend_config = BackendConfig()
settings = Settings()
graphConfig = GraphConfig()
