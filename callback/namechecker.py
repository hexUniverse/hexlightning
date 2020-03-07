import logging
import coloredlogs
from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError, Unauthorized
from telegram.ext.dispatcher import run_async

from plugin import config, callabck_parse

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def namechecker(bot, update):
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
    callback = callabck_parse.callback_parse(query.data)

    if query.message.text_html:
        edit_msg = query.message.text_html
    else:
        edit_msg = query.message.caption_html

    if callback.qtype == 'user':
        target_chat_id, *targets = callback.qdata.split(':')
        if callback.qact == 'bypass':
            callback_data = f'user back {target_chat_id}'
            for target in targets:
                target_act, target_id = target[:1], target[1:]
                if target_act == '+':  # keep in group
                    edit_msg += f'\npass <code>{target_id}</code> by: {query.from_user.mention_html()}'
                    if target_id:
                        callback_data += f':+{target_id}'
                else:
                    try:
                        bot.kick_chat_member(target_chat_id, target_id)
                        edit_msg += f'\nkicked by: {query.from_user.mention_html()}'
                    except (BadRequest, Unauthorized) as e:
                        callback_data += f':+{target_id}'
                        try:
                            edit_msg += f'\nfailed to kick <code>{target_id}</code> by: {query.from_user.mention_html()}'
                        except TypeError:
                            query.answer('bot 並不在該群。', show_alert=True)
                            callback_data = None
                            return
                        if e.message == 'User is an administrator of the chat':
                            query.answer('你嘗試 bang 掉 admin。',
                                         show_alert=True)
                        elif e.message == 'Not enough rights to restrict/unrestrict chat member':
                            query.answer('Bot 在該群組並非 admin。',
                                         show_alert=True)
                            leave_group_msg = f'偵測到 <a href="tg://user?id={target_id}">spam 帳號</a>\n' \
                                '為 bot 正常運作請給予 admin 權限，請給予必要權限後再嘗試使用。\n' \
                                '有問題請至 @hexjudge 詢問。'
                            try:
                                bot.send_message(
                                    target_chat_id, leave_group_msg, parse_mode='html').done.wait()
                            except TelegramError as e:
                                edit_msg += '\n' + e.message
                                if e.message == 'Have no rights to send a message':
                                    pass
                            callback_data = None
                        elif e.message == 'Forbidden: bot is not a member of the supergroup chat':
                            query.answer('bot 並不在該群。', show_alert=True)
                            callback_data = None
                        else:
                            query.answer('發生了一些錯誤，一群訓練有素的猴子們正在圍觀。')
                            bot.send_message(
                                config.getint(
                                    'log',
                                    'error'),
                                f'<code>{escape(e.message)}</code>',
                                parse_mode='html')

                if callback_data is None:
                    keyboard = None
                else:
                    keyboard = [[InlineKeyboardButton(
                        '回去', callback_data=callback_data), ]]
        elif callback.qact == 'back':
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
                callback_data = [
                    f'user bypass {target_chat_id}:+{targets[0][1:]}:-{targets[1][1:]}',
                    f'user bypass {target_chat_id}:-{targets[0][1:]}:+{targets[1][1:]}',
                    f'user bypass {target_chat_id}:+{targets[0][1:]}:+{targets[1][1:]}',
                    f'user bypass {target_chat_id}:-{targets[0][1:]}:-{targets[1][1:]}',
                ]
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
                callback_data = [
                    f'user bypass {target_chat_id}:-{targets[0][1:]}',
                    f'user bypass {target_chat_id}:+{targets[0][1:]}']
                keyboard = [
                    [
                        InlineKeyboardButton(
                            '阿拉花瓜',
                            callback_data=callback_data[0]),
                        InlineKeyboardButton(
                            '他還只是個孩子啊',
                            callback_data=callback_data[1])]]

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
