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


class PremiumDegramModule(BaseModule):
    name = "PremiumDegram"
    channelId = 1220540048
    disabled = False
    magicNumber = 82704661
