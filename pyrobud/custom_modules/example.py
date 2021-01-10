import asyncio
import io
from pathlib import PurePosixPath
from typing import IO

import telethon as tg
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

from .. import command, module, util


class ExampleModule(module.Module):
    name = "Info"
    disabled = False
    channelId = 1179400979

    db: util.db.AsyncDB

    async def on_load(self) -> None:
        self.db = self.bot.get_db("info")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if isinstance(event.message.peer_id, PeerChannel) and event.message.peer_id.channel_id == self.channelId:
            self.log.info(f"Received message: {event.message}")

    async def on_message_edit(self, event: tg.events.NewMessage.Event) -> None:
        if isinstance(event.message.peer_id, PeerChannel) and event.message.peer_id.channel_id == self.channelId:
            self.log.info(f"Received edited message: {event.message}")
