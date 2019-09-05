import time

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext.dispatcher import run_async

from locales import i18n


@run_async
def cleancb(bot, update):
    i18n(update).loads.install(True)
    kb = ReplyKeyboardMarkup([[ReplyKeyboardRemove]])
    try:
        update.message.delete()
    except:
        pass
    sent = update.message.reply_text(
        _('已清除鍵盤'), reply_markup=ReplyKeyboardRemove(remove_keyboard=True)).result()
    time.sleep(5)
    try:
        sent.delete()
    except:
        pass
