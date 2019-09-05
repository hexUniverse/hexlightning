import logging
import coloredlogs
from html import escape

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import *
from telegram.ext.dispatcher import run_async

from plugin import config, callabck_parse

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def botinvite(bot, update):
    query = update.callback_query
    callback = callabck_parse.callback_parse(query.data)

    if query.message.text_html:
        edit_msg = query.message.text_html

    keyboard = None
    if callback.qact == 'leave':
        if bot.leave_chat(callback.qdata):
            edit_msg += f'\nleave by: {query.from_user.mention_html()}'
        else:
            edit_msg += f'\nfailed to leave group <code>{callback.qdata}</code>'
    elif callback.qact == 'pass':
        edit_msg += f'\npass by: {query.from_user.mention_html()}'
    else:
        pass

    try:
        reply_markup = None if keyboard is None else InlineKeyboardMarkup(
            keyboard)
    except UnboundLocalError:
        query.answer('這個按鈕似乎有問題...?')
        return

    bot.edit_message_text(text=edit_msg,
                          parse_mode='html',
                          chat_id=query.message.chat.id,
                          reply_markup=reply_markup,
                          message_id=query.message.message_id)
