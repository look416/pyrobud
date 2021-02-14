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


class DirectorFXModule(BaseModule):
    name = "DirectorFX"
    channelId = 1467194174
    disabled = False
    magicNumber = 82704662
