import logging
import coloredlogs

from pyrogram import Client, Message
from pyrogram.errors import BadRequest

from hexlightning.functions.i18n import i18n
from hexlightning.functions import configure


logger = logging.getLogger(__name__)
coloredlogs.install(level=configure.get('logging', 'status'), logger=logger)


@i18n()
def about(client: Client, message: Message):
    """
    about 宣示主權，形同 LICENSE
    """
    try:
        text = _('本Bot隸屬於 <a href="https://t.me/hexuniverse">hex</a> 旗下\n'
                 '並由多名小精靈共同維護，若有合作需求請洽 @orangetofu \n\n'
                 '使用本Bot視同同意<code>海克斯真香協議</code> (詳情 /eula 查看)\n'
                 '主要開發人員：\n'
                 '@hexlightning @Shawn_N @smailzhu\n'
                 '主要嘴砲人員：@bestpika\n'
                 '看板虎(娘)：@allen0099\n'
                 '人工智障奶子偵測器：@toy17 @NekoNymphJapari')
        message.reply_html(text)
    except BadRequest as e:
        logger.exception(e.message)
    except Exception as e:
        logger.exception(e)
