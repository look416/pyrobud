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


class ForexProsModule(BaseModule):
    name = "ForexPros"
    channelId = 1423236859
    disabled = False
    magicNumber = 82704665
    