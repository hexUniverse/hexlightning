import time
import logging
from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError, TimedOut, Unauthorized
from telegram.ext.dispatcher import run_async


class handler:
    def __init__(self, inherit):
        self.logger = inherit.logger
        self.config = inherit.config
        self.db = inherit.client
        self.errorlog = self.config.getint('log', 'errReport')
        logger = logging.getLogger(__name__)

    @run_async
    def callbackQueryHandler(self, bot, update):
        """
        query_data rule
        category action data:data2

        bot leave  -100123456789 # bot leave group
        bot pass -100123456789 # keep bot in group
        user kick {update.message.chat.id}:{new_member.id}
        user pass {update.message.chat.id}:{new_member.id}
        user bypass {update.message.chat.id}:+{from_user.id}:-{new_member.id}
        +: keep, -: kick
        user back {update.message.chat.id}:+{from_user.id}:-{new_member.id}
        +: nothing, -: unban
        """
        query = update.callback_query

        if query.message.text_html:
            edit_msg = query.message.text_html
        else:
            edit_msg = query.message.caption_html

        if len(query.data.split()) < 3:
            qtype = query.data
        else:
            qtype, qact, qdata = query.data.split()

        if qtype == 'user':
            target_chat_id, *targets = qdata.split(':')
            if qact == 'bypass':
                callback_data = f'user back {target_chat_id}'
                for target in targets:
                    target_act, target_id = target[:1], target[1:]
                    if target_act == '+':  # keep in group
                        edit_msg += f'\npass <code>{target_id}</code> by: {query.from_user.mention_html()}'
                        if target_id:
                            '''
                            2018-12-10 20:05:46,355 - __main__ - WARNING - Not enough rights to restrict/unrestrict chat member
                            2018-12-10 20:05:46,361 - telegram.utils.promise - ERROR - An uncaught error was
                                raised while running the promise                                               
                                Traceback (most recent call last):                                              
                                File "/usr/local/lib/python3.6/dist-packages/telegram/utils/promise.py", line 
                                57, in run                                                                      
                                    self._result = self.pooled_function(*self.args, **self.kwargs)              
                                File "/data/Drive/hexPort/hexlightning/callback.py", line 49, in callbackQuery
                                Handler                                                                         
                                    callback_data += f':+{target_id}'                                           
                                TypeError: unsupported operand type(s) for +=: 'NoneType' and 'str'
                            '''
                            callback_data += f':+{target_id}'
                    else:
                        try:
                            bot.kick_chat_member(target_chat_id, target_id)
                            callback_data += f':-{target_id}'
                            edit_msg += f'\nkicked by: {query.from_user.mention_html()}'
                            # 抹出 user.participate 紀錄
                            self.db.user.find_one_and_update(
                                {'chat.id': int(target_id)},
                                {'$pull': {
                                    'chat.participate': int(target_chat_id)}}
                            )
                        except (BadRequest, Unauthorized) as e:
                            try:
                                callback_data += f':+{target_id}'
                                edit_msg += f'\nfailed to kick <code>{target_id}</code> by: {query.from_user.mention_html()}'
                            except TypeError:
                                query.answer('bot 並不在該群。', show_alert=True)
                                callback_data = None
                            if e.message == 'User is an administrator of the chat':
                                query.answer('你嘗試 bang 掉 admin。',
                                             show_alert=True)
                            elif e.message == 'Not enough rights to restrict/unrestrict chat member':
                                query.answer('Bot 在該群組並非 admin。',
                                             show_alert=True)
                                leave_group_msg = f'偵測到 <a href="tg://user?id={target_id}">spam 相關帳號</a>\n' \
                                                  '為 bot 正常運作請給予 admin 權限，請給予必要權限後再嘗試使用。\n' \
                                                  '有問題請至 @hexjudge 詢問。'
                                try:
                                    bot.send_message(
                                        target_chat_id, leave_group_msg, parse_mode='html').done.wait()
                                except TelegramError as e:
                                    edit_msg += '\n' + e.message
                                    if e.message == 'Have no rights to send a message':
                                        pass
                                # bot.leave_chat(target_chat_id)
                                callback_data = None
                            elif e.message == 'Forbidden: bot is not a member of the supergroup chat':
                                query.answer('bot 並不在該群。', show_alert=True)
                                callback_data = None
                            else:
                                query.answer('發生了一些錯誤，一群訓練有素的猴子們正在圍觀。')
                                bot.send_message(
                                    self.errorlog, f'<code>{escape(e.message)}</code>', parse_mode='html')

                    if callback_data is None:
                        keyboard = None
                    else:
                        keyboard = [[InlineKeyboardButton(
                            '回去', callback_data=callback_data), ]]
            elif qact == 'back':
                edit_msg += f'\nback by: {query.from_user.mention_html()}'
                if len(targets) == 2:
                    for target in targets:
                        target_act, target_id = target[:1], target[1:]
                        if target_act == '-':
                            try:
                                bot.unban_chat_member(
                                    target_chat_id, target_id)
                            except BadRequest as e:
                                if e.message == 'Not enough rights to restrict/unrestrict chat member':
                                    query.answer('沒有力量去對那個人上下其手。')
                                    return
                    callback_data = [f'user bypass {target_chat_id}:+{targets[0][1:]}:-{targets[1][1:]}',
                                     f'user bypass {target_chat_id}:-{targets[0][1:]}:+{targets[1][1:]}',
                                     f'user bypass {target_chat_id}:+{targets[0][1:]}:+{targets[1][1:]}',
                                     f'user bypass {target_chat_id}:-{targets[0][1:]}:-{targets[1][1:]}', ]
                    keyboard = [
                        [InlineKeyboardButton("掐死被邀人", callback_data=callback_data[0]),  # kick from_user group
                         InlineKeyboardButton("掐死邀請人", callback_data=callback_data[1])],  # kick new_member group
                        [InlineKeyboardButton("先放過", callback_data=callback_data[2]),  # keep both
                         InlineKeyboardButton("殉情", callback_data=callback_data[3])]]  # kick both
                else:
                    for target in targets:
                        target_act, target_id = target[:1], target[1:]
                        if target_act == '-':
                            bot.unban_chat_member(target_chat_id, target_id)
                    callback_data = [f'user bypass {target_chat_id}:-{targets[0][1:]}',
                                     f'user bypass {target_chat_id}:+{targets[0][1:]}']
                    keyboard = [[InlineKeyboardButton('阿拉花瓜', callback_data=callback_data[0]),
                                 InlineKeyboardButton('他還只是個孩子啊', callback_data=callback_data[1])]]
            else:  # TODO raise?
                pass
        elif qtype == 'bot':
            keyboard = None
            # check cliker right
            if query.from_user.id not in [self.config.getint('admin', 'uid'), 297394549, 184805205]:
                query.answer('你沒有那個屁股最好別按ㄛ')
                return
            if qact == 'leave':
                try:
                    #bot.send_message(qdata, '本宮先行離開了。').result()
                    if bot.leave_chat(qdata):
                        edit_msg += f'\nleave by: {query.from_user.mention_html()}'
                        self.db.group.find_one_and_delete(
                            {'chat.id': int(qdata)}
                        )
                except BadRequest as e:
                    if e.message == 'Chat not found':
                        query.answer('可能已經被請出去了。')
                        edit_msg += f'\nfailed to leave group <code>{qdata}</code>'
            elif qact == 'pass':
                edit_msg += f'\npass by: {query.from_user.mention_html()}'
            else:
                # TODO raise error?
                pass
        reply_markup = None if keyboard is None else InlineKeyboardMarkup(
            keyboard)
        while True:
            try:
                bot.edit_message_text(text=edit_msg,
                                      parse_mode='html',
                                      chat_id=query.message.chat.id,
                                      reply_markup=reply_markup,
                                      message_id=query.message.message_id)
                break
            except TimedOut:
                time.sleep(5)
