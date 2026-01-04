import os
from functools import wraps

from flask import Blueprint, jsonify, request

from server.db import session_scope
from server.models.message import Message
from server.utils.tokens import TOKEN_STORE

admin_bp = Blueprint("admin", __name__)

TOKEN_TTL = int(os.getenv("ADMIN_TOKEN_TTL", "86400"))


def require_admin(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth.replace("Bearer ", "") if auth else ""
        if not TOKEN_STORE.validate(token):
            return jsonify({"error": "unauthorized"}), 401
        return view(*args, **kwargs)

    return wrapper


@admin_bp.post("/api/admin/login")
def admin_login():
    password = request.json.get("password") if request.is_json else None
    if password != os.getenv("ADMIN_PASSWORD"):
        return jsonify({"error": "invalid_credentials"}), 401
    token = TOKEN_STORE.create_token(TOKEN_TTL)
    return jsonify({"token": token, "expires_in": TOKEN_TTL})


@admin_bp.get("/api/admin/summary")
@require_admin
def admin_summary():
    with session_scope() as session:
        pending_count = session.query(Message).filter(Message.status == "pending").count()
        approved_count = session.query(Message).filter(Message.status == "approved").count()
        deleted_count = session.query(Message).filter(Message.status == "deleted").count()
    return jsonify(
        {
            "pending": pending_count,
            "approved": approved_count,
            "deleted": deleted_count,
        }
    )
