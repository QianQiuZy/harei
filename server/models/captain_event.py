from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from server.models.base import Base


class CaptainEvent(Base):
    __tablename__ = "captain_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(64), nullable=False)
    username = Column(String(128), nullable=False)
    gift_name = Column(String(128), nullable=True)
    event_time = Column(DateTime, nullable=False, server_default=func.now())
    month_key = Column(String(16), nullable=False)
