import asyncio
import io
from pathlib import PurePosixPath
from typing import IO
import dataclasses as dc
from .base import BaseModule

import telethon as tg
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import re
import decimal
from fxparser import ParserHelper


from .. import command, module, util, mt4


class TradeSocietyModule(BaseModule):
    name = "TradeSociety"
    channelId = 1183694013
    disabled = False
    magicNumber = 82704670