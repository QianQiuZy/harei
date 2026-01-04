import os
from flask import Blueprint, jsonify, send_from_directory

assets_bp = Blueprint("assets", __name__)

ASSETS_DIR = os.getenv("ASSETS_DIR", "assets")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
CACHE_TTL = 60 * 60 * 24 * 30


@assets_bp.get("/assets/<path:filename>")
def get_assets(filename: str):
    return send_from_directory(ASSETS_DIR, filename, cache_timeout=CACHE_TTL)


@assets_bp.get("/uploads/<path:filename>")
def get_uploads(filename: str):
    return send_from_directory(UPLOAD_DIR, filename, cache_timeout=CACHE_TTL)


@assets_bp.get("/api/backgrounds")
def list_backgrounds():
    backgrounds_dir = os.path.join(ASSETS_DIR, "backgrounds")
    if not os.path.isdir(backgrounds_dir):
        return jsonify({"items": []})
    items = [
        f"/assets/backgrounds/{name}"
        for name in sorted(os.listdir(backgrounds_dir))
        if name.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]
    return jsonify({"items": items})


@assets_bp.get("/")
@assets_bp.get("/<path:path>")
def serve_frontend(path: str | None = None):
    web_dir = os.getenv("WEB_DIST_DIR", "web/dist")
    file_path = os.path.join(web_dir, path or "")
    if path and os.path.isfile(file_path):
        return send_from_directory(web_dir, path)
    return send_from_directory(web_dir, "index.html")
