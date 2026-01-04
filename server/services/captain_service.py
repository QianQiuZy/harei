import datetime

from server.db import session_scope
from server.models.captain_event import CaptainEvent


def record_captain(uid: str, username: str, gift_name: str | None) -> None:
    month_key = datetime.datetime.now().strftime("%Y-%m")
    with session_scope() as session:
        session.add(
            CaptainEvent(
                uid=str(uid),
                username=username,
                gift_name=gift_name,
                month_key=month_key,
            )
        )
