from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from orchestrator.config import database_config
from orchestrator.graph import Graph, GraphNode, Topic
from orchestrator.sql_tables import DBGraph


class Postgres:
    def __init__(self):
        async_engine = create_async_engine(database_config.DATABASE_URL, echo=True)
        self.async_session = async_sessionmaker(async_engine, class_=AsyncSession)

    async def get_graphs(self, graph_ids: list[str]) -> list[Graph]:
        pass

    async def add_default_topics(self):
        pass

    async def get_topic_from_node(self, node_id: int, graph_id: str) -> Topic | None:
        pass

    async def add_graph_nodes(self, graph_nodes: list[GraphNode]):
        pass

    async def add_graph(self, graph: Graph):
        async with self.async_session() as session:
            graph = DBGraph()
            session.add(graph)


class DataBaseAgent:
    def __init__(self):
        self.postgres = Postgres()

    async def get_graphs(self, graph_ids: list[str]) -> list[Graph]:
        pass

    async def add_default_topics(self):
        pass

    async def get_topic_from_node(self, node_id: int, graph_id: str) -> Topic | None:
        pass

    async def add_graph_nodes(self, graph_nodes: list[GraphNode]):
        pass

    async def add_graph(self, graph: Graph):
        pass


data_base_agent = DataBaseAgent()
