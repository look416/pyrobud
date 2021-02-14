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


class PowerForexModule(BaseModule):
    name = "PowerForex"
    channelId = 1387172415
    disabled = False
    # pro channel id = 1253830187
    magicNumber = 82704668

