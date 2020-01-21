import logging

import coloredlogs

from locales import i18n

from telegram.ext import run_async

logger = logging.getLevelName(__name__)
coloredlogs.install(level='INFO')


@run_async
def eula(bot, update):
    i18n(update).loads.install(True)
    text = _('<pre>'
             '"海克斯真香協議" 初版\n'
             '@DingChen_Tsai 編訂此協議，並由 "海克斯" 宇宙成員們同意。'
             '只要你看到這個協議檔案，不管你有沒有打開看，只要使用了 "海克斯" 任何程式碼做'
             '任何事表示皆接受 "踢低吸真香" 此共識，並且將此協議文本保留在該專案底下，加入'
             '本協議可以隨時修改不再另行通知。未來有一天與我們任何一成員相遇了你可以買咖'
             '啡請當事人。 \n\n'
             '- @allen0099 @bestpika @DingChen_Tsai @smailzhu \n'
             '</pre>')
    update.message.reply_text(text, parse_mode='html')