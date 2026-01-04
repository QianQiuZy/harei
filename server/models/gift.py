from sqlalchemy import Column, Integer, String

from server.models.base import Base


class Gift(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(256), nullable=True)
