import time
import logging
from html import escape

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import *
from telegram.ext.dispatcher import run_async

# custom module


class handler:
    def __init__(self, inherit):
        self.logger = inherit.logger
        self.config = inherit.config
        self.emojitags = inherit.emojitags
        self.errorlog = self.config.getint('log', 'errReport')
        self.db = inherit.client
        logger = logging.getLogger(__name__)

    @run_async
    def callbackQueryHandler(self, bot, update):
        '''
        set sub halal
        set hint halal
        '''
        query = update.callback_query
        qtype, qact, qdata = query.data.split()
        if qact == 'hint' or qact == 'sub':
            # all user
            if qact == 'hint':
                query.answer(
                    self.emojitags.emoji_dict[qdata]['hint'], show_alert=True)
                return

            # group admininstrator only
            else:
                user = bot.get_chat_member(
                    query.message.chat_id, query.from_user.id)
                if user.status not in ['creator', 'administrator']:
                    # 會觸犯到 flood
                    # query.answer('你不是admin啦，好大的官威啊。', show_alert=True)
                    return
                db_query = self.db.group.find_one(
                    {'chat.id': query.message.chat_id})
                if db_query == None:
                    query.answer('有什麼東西發生了錯誤，請聯絡開發者 @hexjudge',
                                 show_alert=True)
                    return
                if 'sub_ban_list' not in db_query['chat']['config'].keys():
                    current = []
                else:
                    current = db_query['chat']['config']['sub_ban_list']

                # 你給我便便我給你全世界
                if qdata == 'spam':
                    keyboard = []
                    if len(current) < len(self.emojitags.emoji_dict)-1:
                        current = ['🤡', '🔞', '👶', '😈', '💪', '👺', '🤖', '💰', '💩']
                    else:
                        current = []
                    self.db.group.find_one_and_update(
                        {'chat.id': query.message.chat_id},
                        {'$set': {'chat.config.sub_ban_list': current}},
                        upsert=True
                    )
                    query.answer('done')

                # 給你勾勾
                elif self.emojitags.to_emoji([qdata]) not in current:
                    current.append(self.emojitags.to_emoji([qdata]))
                    self.db.group.find_one_and_update(
                        {'chat.id': query.message.chat_id},
                        {'$set': {'chat.config.sub_ban_list': current}},
                        upsert=True
                    )
                    query.answer('done')
                # 把你勾勾拿掉
                elif self.emojitags.to_emoji([qdata]) in current:
                    result = self.db.group.find_one(
                        {'chat.id': query.message.chat_id}
                    )
                    if len(result['chat']['config']['sub_ban_list']) == len(self.emojitags.emoji_dict):
                        current.remove('💩')
                    current.remove(self.emojitags.to_emoji([qdata]))
                    self.db.group.find_one_and_update(
                        {'chat.id': query.message.chat_id},
                        {'$set': {'chat.config': {
                            'sub_ban_list': current}}},
                        upsert=True
                    )
                    query.answer('done')

                keyboard = []
                for emoji_list in self.emojitags.emoji_dict:
                    if self.emojitags.emoji_dict[emoji_list]['emoji'][0] in current:
                        check_box = '✅'
                    else:
                        check_box = '❌'
                    tmp_keyboard = [InlineKeyboardButton(f'{self.emojitags.emoji_dict[emoji_list]["tw"]}', callback_data=f'set hint {emoji_list}'),
                                    InlineKeyboardButton(
                                        check_box, callback_data=f'set sub {emoji_list}')
                                    ]
                    keyboard.append(tmp_keyboard)
                keyboard.append([InlineKeyboardButton(
                    '關閉鍵盤⌨️', callback_data='set close keyboard')])

                reply_markup = InlineKeyboardMarkup(keyboard)
                try:
                    query.edit_message_reply_markup(reply_markup=reply_markup)
                except BadRequest as e:
                    # 別問我為啥，真的有遇過。
                    if e.message == 'Message is not modified':
                        pass

        elif qact == 'close':
            current = self.db.group.find_one(
                {'chat.id': query.message.chat_id})['chat']['config']['sub_ban_list']
            keyboard = []
            for emoji_list in self.emojitags.emoji_dict:
                if self.emojitags.emoji_dict[emoji_list]['emoji'][0] in current:
                    check_box = '✅'
                else:
                    check_box = '❌'
                tmp_keyboard = [InlineKeyboardButton(f'{self.emojitags.emoji_dict[emoji_list]["tw"]}', callback_data=f'set hint {emoji_list}'),
                                InlineKeyboardButton(
                                    check_box, callback_data=f'set hint {emoji_list}')
                                ]
                keyboard.append(tmp_keyboard)

            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                query.edit_message_text(
                    f'[設定完成]\n<b>{"="*23}</b>\n'+query.message.text_html, reply_markup=reply_markup, parse_mode='html')
                self.db.group.find_one_and_update(
                    {'chat.id': query.message.chat_id},
                    {'$set': {'chat.config.configuring': False}},
                    upsert=True
                )
                time.sleep(10)
                bot.delete_message(query.message.chat_id,
                                   query.message.message_id)
            except (BadRequest, TimedOut) as e:
                if e.message == 'Message is not modified':
                    pass
                elif e.message == 'Timed out':
                    pass
                elif e.message == 'Message to delete not found':
                    pass
                else:
                    self.logger.exception(e)
