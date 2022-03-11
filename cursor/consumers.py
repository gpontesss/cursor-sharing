import json
import uuid
from functools import cached_property
from urllib.parse import parse_qs

import pydantic
from channels.generic.websocket import AsyncWebsocketConsumer
from pydantic.json import pydantic_encoder

cursors = {}


class Position(pydantic.BaseModel):
    """docs here."""

    x: int
    y: int


class CursorConsumer(AsyncWebsocketConsumer):
    """docs here."""

    groups = ("cursor",)
    cursor_id: str
    nickname: str
    current_position: Position

    @cached_property
    def qs(self):
        """docs here."""
        return parse_qs(self.scope["query_string"].decode())

    def get_nickname(self):
        """docs here."""
        return self.qs.get("nickname", ("anonymous",))[0]

    async def send_initial_positions(self):
        """docs here."""
        await self.send(
            json.dumps(
                {
                    "type": "cursor.initial.data",
                    "cursors": [
                        {
                            "id": cursor.cursor_id,
                            "nickname": cursor.nickname,
                            "position": cursor.current_position,
                        }
                        for cursor in cursors.values()
                    ],
                },
                default=pydantic_encoder,
            )
        )

    async def connect(self):
        """docs here."""
        self.cursor_id = str(uuid.uuid4())
        self.nickname = self.get_nickname()
        self.current_position = Position(x=0, y=0)
        cursors[self.cursor_id] = self
        await self.accept()
        await self.send_initial_positions()

    async def disconnect(self, code):
        """docs here."""
        del cursors[self.cursor_id]

    async def receive(self, text_data: str):
        """docs here."""
        try:
            self.current_position = Position.parse_raw(text_data)
        except pydantic.ValidationError:
            await self.close(1007)
        else:
            await self.channel_layer.group_send(
                "cursor",
                {
                    "type": "cursor.update",
                    "id": self.cursor_id,
                    "nickname": self.nickname,
                    "position": self.current_position,
                },
            )

    async def cursor_update(self, evt):
        """docs here."""
        await self.send(json.dumps(evt, default=pydantic_encoder))
