from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from server.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    message_text = Column(Text, nullable=False)
    tag = Column(String(64), nullable=True)
    status = Column(String(32), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    ip = Column(String(64), nullable=True)
