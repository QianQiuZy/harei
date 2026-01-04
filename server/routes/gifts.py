from flask import Blueprint, jsonify, request

from server.db import session_scope
from server.models.gift import Gift
from server.routes.admin import require_admin

gifts_bp = Blueprint("gifts", __name__)


@gifts_bp.get("/api/gifts")
@require_admin
def list_gifts():
    with session_scope() as session:
        gifts = session.query(Gift).order_by(Gift.name.asc()).all()
        items = [
            {"id": gift.id, "name": gift.name, "description": gift.description}
            for gift in gifts
        ]
    return jsonify({"items": items})


@gifts_bp.post("/api/gifts")
@require_admin
def create_gift():
    payload = request.json or {}
    name = payload.get("name")
    description = payload.get("description")
    if not name:
        return jsonify({"error": "name_required"}), 400

    with session_scope() as session:
        gift = Gift(name=name, description=description)
        session.add(gift)
        session.flush()
        return jsonify({"id": gift.id, "name": gift.name, "description": gift.description})
