import asyncio

from sqlalchemy import create_engine

from orchestrator.config import database_config
from orchestrator.data_base import data_base_agent
from orchestrator.rest_handler import start_rest
from orchestrator.sql_tables import Base

if __name__ == "__main__":
    engine = create_engine(database_config.DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    asyncio.run(data_base_agent.add_default_topics())
    start_rest()
