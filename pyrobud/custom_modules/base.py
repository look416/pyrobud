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


from .. import command, module, util, mt4

class BaseModule(module.Module):
    name = "BaseModel"
    zmqHost = "192.168.88.211"
    channelId = 1480231253
    debugChannel = 1347732970
    # tt = 1179400979 1480231253
    disabled = True
    magicNumber = 80000000
    parserHelper = ParserHelper()
    allowMedia = False

    db: util.db.AsyncDB

    async def on_load(self) -> None:
        self.db = self.bot.get_db(self.name.replace(" ","").lower())

    async def on_start(self, time_us: int) -> None:
        await self.bot.client.send_message(PeerChannel(channel_id=self.debugChannel), f"bot - {self.name} started....")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if isinstance(event.message.peer_id, PeerChannel) and event.message.peer_id.channel_id == self.channelId:
            self.log.info(f"Received message: {event.message}")
            if self.allowMedia or event.message.media == None:
                order = self.parseMessage(event.message.message)
                await self.bot.client.send_message(PeerChannel(channel_id=self.debugChannel), f"Attempted Order {self.name}:{order}")
                if order.symbol and order.type:
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

    def parseMessage(self, message):
        return self.parserHelper.parse_text(message)

    async def order(self, order):
        # get the base decimal numbers
        exponent = 1000 if 'JPY' in order.symbol else 100000
        if "GOLD" in order.symbol or "XAU" in order.symbol:
            exponent = 100

        tp = 0
        if len(order.tpList) > 0:
            tp = float(order.tpList[0])
        
        if order.price == 0.0:
            order.price = order.sl + (400 / exponent * (1 if order.type == 1 else -1))

        _zmq = mt4.DWX_ZeroMQ_Connector(_host=self.zmqHost)
        _trade = _zmq._generate_default_order_dict()
        _trade['_type'] = order.type - 1
        _trade['_TP'] = int(abs(order.price - tp) * exponent) if tp > 0 else 500
        _trade['_SL'] = int(abs(order.price - order.sl) * exponent) if order.sl > 0 else 500
        _trade['_lots'] = order.lotSize
        _trade['_symbol'] = order.symbol
        _trade['_comment'] = self.name
        _trade['_magic'] = self.magicNumber
        if not order.market:
            _trade["_price"] = order.price
        _zmq._DWX_MTX_NEW_TRADE_(_order=_trade)
        await self.bot.client.send_message(PeerChannel(channel_id=self.debugChannel), f"{_trade}")
        self.log.info(f"Order created: {_trade}")
