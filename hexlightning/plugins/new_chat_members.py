import logging
import coloredlogs

from pyrogram import Client, Message
from pyrogram.errors import BadRequest

from hexlightning.functions.i18n import i18n
from hexlightning.functions import configure


logger = logging.getLogger(__name__)
coloredlogs.install(level=configure.get('logging', 'status'), logger=logger)


@i18n()
def new_chat_members(client: Client, message: Message):
    """
    new_chat_members
     - 處理 new install (獨立處理 filter 處理？)
     - 處理是否已被黑名單 (banstat 先寫！)
       - 是否在群組白名單
     - 處理進群訊息是否要刪除
     - 處理進群驗證
    """
    pass
