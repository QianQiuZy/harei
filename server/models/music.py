from sqlalchemy import Column, Integer, String

from server.models.base import Base


class MusicTrack(Base):
    __tablename__ = "music_tracks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    artist = Column(String(128), nullable=True)
    url = Column(String(256), nullable=True)
