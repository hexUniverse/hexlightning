import logging

import coloredlogs

from locales import i18n

from telegram.ext import run_async

logger = logging.getLevelName(__name__)
coloredlogs.install(level='INFO')


@run_async
def about(bot, update):
    i18n(update).loads.install(True)
    text = _('本Bot隸屬於 <a href="https://t.me/hexuniverse">hex</a> 旗下\n'
             '並由多名小精靈共同維護，若有合作需求請洽 @orangetofu \n\n'
             '使用本Bot視同同意<code>海克斯真香協議</code> (詳情 /eula 查看)\n'
             '主要開發人員：\n'
             '@hexlightning @DingChen_Tsai @smailzhu\n'
             '主要嘴砲人員：@bestpika\n'
             '看板虎(娘)：@allen0099\n'
             '人工智障奶子偵測器：@toy17 @NekoNymphJapari')

    update.message.reply_text(
        text, parse_mode='html', disable_web_page_preview=True)
