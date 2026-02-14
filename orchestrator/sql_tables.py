from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DBTopics(Base):
    __tablename__ = "topics"

    topic_id = Column(String(36), primary_key=True)
    title = Column(String(100), nullable=False)
    topic_content = Column(String(1500), nullable=False)

    def __repr__(self):
        return f"<Topic(topic_id={self.topic_id}, title={self.title}, topic_content={self.topic_content[:40]})>"


class DBGraphNode(Base):
    __tablename__ = "graph_node"

    node_id = Column(String(36), primary_key=True)
    topic_id = Column(String(36), nullable=False)
    is_studied = Column(Boolean, nullable=False)
    is_major = Column(Boolean, nullable=False)
    prev_node_id = Column(String, nullable=True)
    next_node_id = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<GraphNode(node_id={self.node_id}, topic_id={self.topic_id}, is_studied={self.is_studied}, "
            f"is_major={self.is_major},prev_node_id={self.prev_node_id}, next_node_id={self.next_node_id})>"
        )


class DBGraph(Base):
    __tablename__ = "graph"

    graph_id = Column(String(36), primary_key=True)
    nodes = Column(JSONB, nullable=False)

    def __repr__(self):
        return f"<Graph(graph_id={self.graph_id}, nodes={self.nodes})>"
