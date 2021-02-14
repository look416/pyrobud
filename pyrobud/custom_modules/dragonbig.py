import asyncio
import io
from pathlib import PurePosixPath
from .base import BaseModule
from typing import IO
import dataclasses as dc

import telethon as tg
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import re
import decimal
from fxparser import ParserHelper


from .. import command, module, util, mt4


class DragonBigModule(BaseModule):
    name = "DragonBig"
    channelId = 1355656891
    fromChannelId = 1355656891
    disabled = False
    magicNumber = 82704663

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if isinstance(event.message.peer_id, PeerChannel) and event.message.peer_id.channel_id == self.channelId:
            self.log.info(f"Received message: {event.message}")
            if event.message.media == None and "TP’s / SL’s Measured by Proper Support / Resistance level & Always 1 TP / 1 SL." in event.message.message:
                order = self.parseMessage(event.message.message)
                await self.bot.client.send_message(PeerChannel(channel_id=self.debugChannel), f"Attempted Order {self.name}:{order}")
                if order.symbol:
                    await self.order(order)
            await self.db.inc("messages_received")


