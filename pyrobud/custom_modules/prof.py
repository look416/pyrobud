import asyncio
import io
from pathlib import PurePosixPath
from typing import IO
import dataclasses as dc

import telethon as tg
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import re
import decimal
from fxparser import ParserHelper
from .base import BaseModule

from .. import command, module, util, mt4


class PPEModule(BaseModule):
    name = "PPE"
    channelId = 1474572570
    disabled = False
    magicNumber = 82704669
    allowMedia = True

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if isinstance(event.message.peer_id, PeerChannel) and event.message.peer_id.channel_id == self.channelId:
            self.log.info(f"Received message: {event.message}")
            order = self.parseMessage(event.message.message)
            await self.bot.client.send_message(PeerChannel(channel_id=self.debugChannel), f"Attempted Order {self.name}:{order}")
            if order.symbol and order.sl:
                await self.order(order)
            await self.db.inc("messages_received")
    
    async def on_message_edit(self, event: tg.events.NewMessage.Event) -> None:
        if isinstance(event.message.peer_id, PeerChannel) and event.message.peer_id.channel_id == self.channelId:
            self.log.info(f"Received edited message: {event.message}")
            order = self.parseMessage(event.message.message)
            await self.bot.client.send_message(PeerChannel(channel_id=self.debugChannel), f"Attempted Order {self.name}:{order}")
            if order.symbol and order.sl:
                await self.order(order)
            await self.db.inc("messages_received")
