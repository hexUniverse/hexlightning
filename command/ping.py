from telegram.ext.dispatcher import run_async

from locales import i18n

# (」・ω・)」うー！(／・ω・)／にゃー！


@run_async
def ping(bot, update):
    i18n(update).loads.install(True)
    update.message.reply_text(_('pong'))
