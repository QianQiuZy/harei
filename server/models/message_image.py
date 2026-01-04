from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from server.models.base import Base


class MessageImage(Base):
    __tablename__ = "message_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("messages.message_id"), nullable=False)
    image_path = Column(String(256), nullable=False)
    thumbnail_path = Column(String(256), nullable=False)

    message = relationship("Message", backref="images")
