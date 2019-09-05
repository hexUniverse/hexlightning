import logging
import coloredlogs
from html import escape

import telegram
from telegram.ext import Filters
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async


from command import info
from plugin import db_tools, db_parse, sage, config, sage, is_admin
from inlinekeyboard import quickban
from locales import i18n


@run_async
def bang(bot, update):
    '''
    - kick
    - forward
    - delete
    - send report 
    '''
    i18n(update).loads.install(True)

    try:
        update.message.delete()
    except:
        pass

    # right check
    if sage.is_sage(update.message.from_user.id):
        pass
    else:
        # user = bot.get_chat_member(
        #    update.message.chat.id, update.message.from_user.id)
        if is_admin(bot, update):
            pass
        else:
            return

    sent = bot.forward_message(config.getint(
        'admin', 'elf'), update.message.chat.id, update.message.reply_to_message.message_id)

    try:
        bot.delete_message(update.message.chat.id,
                           update.message.reply_to_message.message_id)
    except:
        pass

    try:
        bot.kick_chat_member(update.message.chat_id,
                             update.message.reply_to_message.from_user.id)
    except BadRequest as e:
        if e.message == 'User is an administrator of the chat':
            update.message.reply_text(
                _(f'目標 {update.message.reply_to_message.from_user.mention_html()} 為管理員。'), parse_mode='html')
        elif e.message == 'Not enough rights to restrict/unrestrict chat member':
            update.message.reply_text(
                _('指令處理失敗\n原因：<code>權限不足</code>'), parse_mode='html')
        else:
            update.message.reply_text(
                _(f'指令處理失敗\n原因：<code>{escape(e.message)}</code>'), parse_mode='html')

    # report to elf 鍵盤
    text = '#banglog #report\n' + info(bot, update, gettext=True).result()
    keyboard = quickban(bot, update, update.message.message_id)

    bot.send_message(config.getint('admin', 'elf'), text,
                     reply_markup=keyboard, reply_to_message_id=sent.message_id, parse_mode='html')
