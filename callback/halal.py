import time
import logging
from html import escape

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import *
from telegram.ext.dispatcher import run_async


class handler:
    def __init__(self, inherit):
        self.logger = inherit.logger
        self.config = inherit.config
        self.errorlog = self.config.getint('log', 'errReport')
        logger = logging.getLogger(__name__)

    @run_async
    def callbackQueryHandler(self, bot, update):
        '''
        halal bypass chat_id:user_id
        halal ban chat_id:user_id
        '''
        query = update.callback_query

        if query.message.text_html:
            edit_msg = query.message.text_html
        else:
            edit_msg = query.message.caption_html

        qtype, qact, qdata = query.data.split()

        keyboard = None
        chat_id, uid = qdata.split(':')
        user_status = bot.get_chat_member(
            query.message.chat_id, query.from_user.id).status

        if user_status not in ['administrator', 'creator']:
            # query.answer('你是不是也想當歐搜馬？\nやめなさいよ。', show_alert=True)
            return
        if qact == 'bypass':
            try:
                bot.restrict_chat_member(chat_id, uid, can_send_messages=True)
            except (Unauthorized, BadRequest) as e:
                if e.message == 'Not enough rights to restrict/unrestrict chat member':
                    query.answer('阿西利伯妹妹根本就沒吃過歐搜馬好嗎。', show_alert=True)
                    return
            edit_msg += f'\nbypass by: {query.from_user.mention_html()}'
            query.answer('今天心情很好是吧？')

        elif qact == 'ban':
            try:
                bot.kick_chat_member(chat_id, uid)
            except (Unauthorized, BadRequest) as e:
                if e.message == 'Not enough rights to restrict/unrestrict chat member':
                    query.answer('阿西利伯妹妹力量不夠，吃不掉歐搜馬\nヒンナヒンナ無法。',
                                 show_alert=True)
                    return
            edit_msg += f'\nkick by: {query.from_user.mention_html()}'
            query.answer('今天很嗆是吧？')

        reply_markup = None if keyboard is None else InlineKeyboardMarkup(
            keyboard)
        try:
            bot.edit_message_caption(caption=edit_msg,
                                     parse_mode='html',
                                     chat_id=query.message.chat.id,
                                     reply_markup=reply_markup,
                                     message_id=query.message.message_id)
            time.sleep(10)
            bot.delete_message(query.message.chat_id, query.message.message_id)

            self.logger.debug('是圖片編輯')
        except BadRequest as e:
            if e.message == 'There is no caption in the message to edit':
                self.logger.debug('是文字編輯啦')
                bot.edit_message_text(text=edit_msg,
                                      parse_mode='html',
                                      chat_id=query.message.chat.id,
                                      reply_markup=reply_markup,
                                      message_id=query.message.message_id)
                time.sleep(10)
                try:
                    bot.delete_message(query.message.chat_id,
                                       query.message.message_id)
                except:
                    pass
