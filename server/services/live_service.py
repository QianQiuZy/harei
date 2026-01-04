import asyncio
import logging
import os

from blivedm.clients.open_live import OpenLiveClient
from blivedm.handlers import BaseHandler

from server.services.captain_service import record_captain

logger = logging.getLogger("live")


class LiveHandler(BaseHandler):
    def _on_open_live_buy_guard(self, client, message):
        asyncio.create_task(
            asyncio.to_thread(
                record_captain,
                uid=message.uid,
                username=message.uname,
                gift_name=message.guard_name,
            )
        )

    def _on_open_live_start_live(self, client, message):
        logger.info("直播开始: room=%s", client.room_id)

    def _on_open_live_end_live(self, client, message):
        logger.info("直播结束: room=%s", client.room_id)


class LiveService:
    def __init__(self) -> None:
        self._access_key_id = os.getenv("BLIVE_ACCESS_KEY_ID")
        self._access_key_secret = os.getenv("BLIVE_ACCESS_KEY_SECRET")
        self._app_id = int(os.getenv("BLIVE_APP_ID", "0"))
        self._identity_code = os.getenv("BLIVE_IDENTITY_CODE")

    def run(self) -> None:
        if not all([self._access_key_id, self._access_key_secret, self._app_id, self._identity_code]):
            logger.warning("直播连接配置缺失，跳过连接")
            return
        asyncio.run(self._run_async())

    async def _run_async(self) -> None:
        client = OpenLiveClient(
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            app_id=self._app_id,
            room_owner_auth_code=self._identity_code,
        )
        client.set_handler(LiveHandler())
        await client.init_room()
        client.start()
        try:
            await client.join()
        finally:
            await client.stop_and_close()
