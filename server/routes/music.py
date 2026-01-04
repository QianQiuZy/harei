from flask import Blueprint, jsonify

from server.services.music_cache import MusicCache

music_bp = Blueprint("music", __name__)

_cache = MusicCache()
_cache.start()


@music_bp.get("/api/music")
def list_music():
    return jsonify({"items": _cache.list_tracks()})
