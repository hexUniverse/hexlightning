import time
import logging
import coloredlogs
import threading

from telegram.error import BadRequest

from plugin import db_parse, db_tools
from plugin import banyourwords, gatejieitai, sage
from locales import i18n
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


def extinguish(bot, update, target: 'input chat.id and uid with int in tuple'):
    redis = db_tools.use_redis()
    chat, user = target[0], target[1]
    query_redis = redis.lrange(f'msg:{chat}', 0, -1)
    for data in query_redis:
        user_, message_id = data.decode().split(',')
        if int(user) == int(user_):
            try:
                bot.delete_message(chat_id=chat, message_id=message_id)
            except BadRequest as e:
                logger.warning(e)
            else:
                redis.lrem(f'msg:{chat}', data, num=1)


# @run_async
def homicide(bot, update, target: 'input uid with int'):
    '''
    列舉 UID 所參與的群組，然後幹他
    Here's Johnny ~
    https://media.giphy.com/media/RoajqIorBfSE/giphy.gif
    '''
    i18n(update).loads.install(True)
    mongo = db_tools.use_mongo()
    user = db_parse.user()
    query_user = mongo.user.find_one({'chat.id': target})
    if query_user == []:
        logger.debug('query user not found')
        return
    user.parse(query_user)
    if user.participate is None or user.participate == []:
        return

    for group in user.participate:
        if gatejieitai(bot, update, specfic=(group, target)):
            update.message.chat.id = group
            try:
                bot.kick_chat_member(
                    group, user.id, until_date=user.current.until)
            except BadRequest as e:
                if e.message == 'Not enough rights to restrict/unrestrict chat member':
                    text = _('⚠️ 權限不足而無法處理 ⚠️\n') + \
                        _(f'名字：{user.mention_html}\n') + \
                        _(f'UID：{user.id}\n') + \
                        _(f'證據：https://t.me/hexevidence{user.current.evidence}\n') + \
                        _(f'標籤：{user.current.tags_text}\n')
                    if user.current.until_date.year < 2019:
                        if user.current.reason:
                            text += _(banyourwords.banyourwords.forever.format(
                                reason=user.current.reason))
                            #text += _(banyourwords.forever.format(reason=user.current.reason))
                        else:
                            text += _(banyourwords.banyourwords.forever.format(
                                reason=user.current.tags_text))
                    else:
                        if user.current.reason:
                            text += _(banyourwords.banyourwords.temp.format(
                                reason=user.current.reason))
                        else:
                            text += _(banyourwords.banyourwords.temp.format(
                                reason=user.current.tags_text))
                    text += _(f'處刑人：{user.current.opid}\n') + \
                        _(f'有任何問題請至 @hexjudge 詢問')
                    sent = bot.send_message(
                        group, text, parse_mode='html').result()
                    time.sleep(10)
                    bot.delete_message(group, sent.message_id)

                elif e.message == 'User is an administrator of the chat':
                    text = _('⚠️ 管理員被標記 ⚠️\n') + \
                        _(f'名字：{user.mention_html}\n') + \
                        _(f'UID：{user.id}\n') + \
                        _(f'證據：https://t.me/hexevidence{user.current.evidence}\n') + \
                        _(f'標籤：{user.current.tags_text}\n')
                    if user.current.until_date.year < 2019:
                        # text += '{text}'.format(_(text=config.get('word',
                        #
                        if user.current.reason:
                            text += _(banyourwords.banyourwords.forever.format(
                                reason=user.current.reason))
                        else:
                            text += _(banyourwords.banyourwords.forever.format(
                                reason=user.current.tags_text))
                    else:
                        if user.current.reason:
                            text += _(banyourwords.banyourwords.temp.format(
                                reason=user.current.reason))
                        else:
                            text += _(banyourwords.banyourwords.temp.format(
                                reason=user.current.tags_text))
                    text += _(f'處刑人：{user.current.opid}\n') + \
                        _(f'有任何問題請至 @hexjudge 詢問')

                    update_white = {'$addToSet': {
                        'chat.white_participate': target}}
                    mongo.group.up({'chat.id': group}, update_white)
                    sage.refresh()

            else:
                threading.Thread(
                    target=extinguish, name=f'{group}_del_msg', args=[
                        bot, update, (group, target)]).start()
                text = _(f'名字：{user.mention_html}\n') + \
                    _(f'UID：{user.id}\n') + \
                    _(f'證據：https://t.me/hexevidence{user.current.evidence}\n') + \
                    _(f'標籤：{user.current.tags_text}\n')
                if user.current.reason:
                    reason = user.current.reason
                else:
                    reason = user.current.tags_text
                if user.current.until_date.year < 2019:
                    # text += _('因為 <code>{reason}</code> 而被琦玉用 <code>普通連續拳</code> 永久揍飛於宇宙之外。').format(
                    #    reason=reason)
                    text += _(banyourwords.banyourwords.forever.format(reason=reason))
                else:
                    # text += _('因為 <code>{reason}</code> 而被琦玉用 <code>普通連續拳</code> 暫時揍飛於宇宙之外\n封鎖到：<code>{date}</code>').format(
                    #    reason=reason, date=user.current.until_text)
                    text += _(banyourwords.banyourwords.temp.format(reason=reason,
                                                                    date=user.current.until_text))
                text += _(f'\n處刑人：{user.current.opid}\n') + \
                    _(f'有任何問題請至 @hexjudge 詢問')
                sent = bot.send_message(
                    group, text, parse_mode='html').result()
                user_update = {'$pull': {'chat.participate': group},
                               '$push': {'chat.banned_participate': group}}
                mongo.user.find_one_and_update(
                    {'chat.id': user.id}, user_update)
                time.sleep(10)
                bot.delete_message(group, sent.message_id)
