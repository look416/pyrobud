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

class TestModule(BaseModule):
    name = "Test"
    channelId = 1182022540
    disabled = False
    magicNumber = 82704650
    imageParser = FlagParser()

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if isinstance(event.message.peer_id, PeerChannel) and event.message.peer_id.channel_id == self.channelId:
            self.log.info(f"Received message: {event.message}")
            order = self.parseMessage(event.message.message)
            print(order)
            if event.message.media:
                filePath = str(Path(__file__).parent.joinpath("assets/test.jpg"))
                await self.bot.client.download_media(message=event.message, file=filePath)
                symbol = self.imageParser.detect_image(filePath)
                if symbol:
                    order.symbol = symbol
            
            await self.bot.client.send_message(PeerChannel(channel_id=self.debugChannel), f"Attempted Order {self.name}:{order}")
            if order.symbol and order.type:
                await self.order(order)
            await self.db.inc("messages_received")
