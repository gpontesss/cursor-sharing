import json
import uuid
from functools import cached_property
from urllib.parse import parse_qs

import pydantic
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from pydantic.json import pydantic_encoder


class Position(pydantic.BaseModel):
    """docs here."""

    x: int
    y: int


class CursorConsumer(AsyncWebsocketConsumer):
    """docs here."""

    groups = ("cursor",)
    cursor_id: str
    nickname: str

    @cached_property
    def qs(self):
        """docs here."""
        return parse_qs(self.scope["query_string"].decode())

    def get_nickname(self):
        """docs here."""
        return self.qs.get("nickname", ("anonymous",))[0]

    async def connect(self):
        """docs here."""
        self.cursor_id = str(uuid.uuid4())
        self.nickname = self.get_nickname()
        await self.accept()

    async def receive(self, text_data: str):
        """docs here."""
        try:
            position = Position.parse_raw(text_data)
        except pydantic.ValidationError:
            await self.close(1007)
        else:
            await self.channel_layer.group_send(
                "cursor",
                {
                    "type": "cursor.update",
                    "id": self.cursor_id,
                    "nickname": self.nickname,
                    "position": position,
                },
            )

    async def cursor_update(self, evt):
        """docs here."""
        await self.send(json.dumps(evt, default=pydantic_encoder))
