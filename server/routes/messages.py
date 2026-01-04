import os
from flask import Blueprint, jsonify, request

from server.db import session_scope
from server.models.message import Message
from server.models.message_image import MessageImage
from server.routes.admin import require_admin
from server.utils.images import save_image

messages_bp = Blueprint("messages", __name__)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")


def _file_to_url(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.startswith(UPLOAD_DIR):
        relative = normalized[len(UPLOAD_DIR) :].lstrip("/")
    else:
        relative = os.path.basename(normalized)
    return f"/uploads/{relative}"


@messages_bp.post("/api/messages")
def create_message():
    message_text = request.form.get("message_text") or ""
    tag = request.form.get("tag") or None
    if not message_text.strip():
        return jsonify({"error": "message_text_required"}), 400

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    with session_scope() as session:
        message = Message(message_text=message_text, tag=tag, status="pending", ip=ip)
        session.add(message)
        session.flush()

        images = request.files.getlist("images")
        for image in images:
            full_path, thumb_path = save_image(image, UPLOAD_DIR)
            session.add(
                MessageImage(
                    message_id=message.message_id,
                    image_path=full_path,
                    thumbnail_path=thumb_path,
                )
            )

        session.refresh(message)

        return jsonify(
            {
                "message_id": message.message_id,
                "status": message.status,
                "created_at": message.created_at.isoformat(),
            }
        )


@messages_bp.get("/api/messages")
@require_admin
def list_messages():
    status = request.args.get("status")
    tag = request.args.get("tag")
    page = int(request.args.get("page", "1"))
    size = int(request.args.get("size", "20"))

    with session_scope() as session:
        query = session.query(Message)
        if status:
            query = query.filter(Message.status == status)
        if tag:
            query = query.filter(Message.tag == tag)
        total = query.count()
        items = (
            query.order_by(Message.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )

        results = []
        for item in items:
            results.append(
                {
                    "message_id": item.message_id,
                    "message_text": item.message_text,
                    "tag": item.tag,
                    "status": item.status,
                    "created_at": item.created_at.isoformat(),
                    "ip": item.ip,
                    "images": [
                        {
                            "url": _file_to_url(image.image_path),
                            "thumbnail": _file_to_url(image.thumbnail_path),
                        }
                        for image in item.images
                    ],
                }
            )

    return jsonify({"total": total, "items": results})


@messages_bp.patch("/api/messages/<int:message_id>/status")
@require_admin
def update_message_status(message_id: int):
    status = request.json.get("status") if request.is_json else None
    if status not in {"pending", "approved", "rejected", "deleted"}:
        return jsonify({"error": "invalid_status"}), 400

    with session_scope() as session:
        message = session.query(Message).filter(Message.message_id == message_id).first()
        if not message:
            return jsonify({"error": "not_found"}), 404
        message.status = status
        session.add(message)

    return jsonify({"message_id": message_id, "status": status})


@messages_bp.get("/api/messages/history")
def message_history():
    tag = request.args.get("tag")
    with session_scope() as session:
        query = session.query(Message).filter(Message.status == "approved")
        if tag:
            query = query.filter(Message.tag == tag)
        items = query.order_by(Message.created_at.asc()).all()

        results = []
        for item in items:
            results.append(
                {
                    "message_id": item.message_id,
                    "message_text": item.message_text,
                    "tag": item.tag,
                    "created_at": item.created_at.isoformat(),
                    "images": [
                        {
                            "url": _file_to_url(image.image_path),
                            "thumbnail": _file_to_url(image.thumbnail_path),
                        }
                        for image in item.images
                    ],
                }
            )

    return jsonify({"items": results})


@messages_bp.get("/api/tags")
def list_tags():
    with session_scope() as session:
        tags = session.query(Message.tag).filter(Message.tag.isnot(None)).distinct().all()
    return jsonify({"items": [tag[0] for tag in tags]})


@messages_bp.get("/api/messages/history/tags")
def list_history_tags():
    return list_tags()
