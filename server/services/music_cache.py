import datetime
import threading
import time
from typing import List

from server.db import session_scope
from server.models.music import MusicTrack


class MusicCache:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tracks: List[MusicTrack] = []
        self._last_refresh: datetime.date | None = None

    def start(self) -> None:
        thread = threading.Thread(target=self._refresh_loop, daemon=True)
        thread.start()

    def _refresh_loop(self) -> None:
        while True:
            today = datetime.date.today()
            if self._last_refresh != today:
                self.refresh()
            time.sleep(3600)

    def refresh(self) -> None:
        with session_scope() as session:
            tracks = session.query(MusicTrack).all()
        with self._lock:
            self._tracks = tracks
            self._last_refresh = datetime.date.today()

    def list_tracks(self) -> list[dict]:
        with self._lock:
            return [
                {
                    "id": track.id,
                    "title": track.title,
                    "artist": track.artist,
                    "url": track.url,
                }
                for track in self._tracks
            ]
