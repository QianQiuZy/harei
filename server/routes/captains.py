import io

from flask import Blueprint, jsonify, request, send_file
from openpyxl import Workbook

from server.db import session_scope
from server.models.captain_event import CaptainEvent
from server.routes.admin import require_admin

captains_bp = Blueprint("captains", __name__)


@captains_bp.get("/api/captains")
@require_admin
def list_captains():
    month = request.args.get("month")
    with session_scope() as session:
        query = session.query(CaptainEvent)
        if month:
            query = query.filter(CaptainEvent.month_key == month)
        events = query.order_by(CaptainEvent.event_time.desc()).all()
        items = [
            {
                "uid": event.uid,
                "username": event.username,
                "gift_name": event.gift_name,
                "event_time": event.event_time.isoformat(),
                "month_key": event.month_key,
            }
            for event in events
        ]
    return jsonify({"items": items})


@captains_bp.get("/api/captains/export")
@require_admin
def export_captains():
    month = request.args.get("month")
    with session_scope() as session:
        query = session.query(CaptainEvent)
        if month:
            query = query.filter(CaptainEvent.month_key == month)
        events = query.order_by(CaptainEvent.event_time.desc()).all()

    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["UID", "用户名", "礼物", "时间", "月份"])
    for event in events:
        sheet.append(
            [event.uid, event.username, event.gift_name or "", event.event_time.isoformat(), event.month_key]
        )

    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    filename = f"captains-{month or 'all'}.xlsx"
    return send_file(buffer, as_attachment=True, download_name=filename)
