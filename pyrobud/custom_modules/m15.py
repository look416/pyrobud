import asyncio
import io
from pathlib import Path, PurePosixPath
from .base import BaseModule
from typing import IO
import dataclasses as dc

import telethon as tg
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import re
import decimal
from fxparser import FlagParser


from .. import command, module, util, mt4

class M15Module(BaseModule):
    name = "M15"
    channelId = 1490464609
    disabled = False
    magicNumber = 82704672
    imageParser = FlagParser()

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if isinstance(event.message.peer_id, PeerChannel) and event.message.peer_id.channel_id == self.channelId:
            self.log.info(f"Received message: {event.message}")
            order = self.parseMessage(event.message.message)
            if event.message.media:
                filePath = str(Path(__file__).parent.joinpath("assets/test.jpg"))
                await self.bot.client.download_media(message=event.message, file=filePath)
                symbol = self.imageParser.detect_image(filePath)
                order.symbol = symbol
            
            await self.bot.client.send_message(PeerChannel(channel_id=self.debugChannel), f"Attempted Order {self.name}:{order}")
            if order.symbol and order.type:
                await self.order(order)
            await self.db.inc("messages_received")
