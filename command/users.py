from telegram.ext.dispatcher import run_async
from locales import i18n


@run_async
def users(bot, update):
    # reply only
    i18n(update).loads.install(True)
    text = ''
    if update.message.reply_to_message.forward_from:
        uid = update.message.reply_to_message.forward_from.id
        text += _(f'被回覆人：<code>{uid}</code>')
    else:
        uid = update.message.reply_to_message.from_user.id
        text += _(f'被回覆人：<code>{uid}</code>')
    if uid:
        update.message.reply_html(text)
