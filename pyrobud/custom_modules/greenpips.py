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

class DayFinanceModule(BaseModule):
    name = "GreenPips"
    channelId = 1169845503
    # tt = 1179400979 1480231253
    disabled = False
    magicNumber = 82704673

