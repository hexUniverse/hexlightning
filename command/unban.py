import logging
import coloredlogs

from parse import search

from telegram.ext.dispatcher import run_async

from plugin import db_parse, db_tools, sage, fresh
from locales import i18n
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


def unban(bot, update):
    i18n(update).loads.install(True)
    # !hex unban u=123 r=噗噗噗
    if sage.michael(update.message.from_user.id) == False:
        update.message.reply_text('權限不足啦 🌚')
        return
    if sage.lucifer(update.message.from_user.id) == False:
        update.message.reply_text('權限不足啦 🌚')
        return

    args = update.message.text.split()
    if len(args) == 2:
        update.message.reply_text(_('缺少參數'))
        return
    reason = search('r={:S}', update.message.text)
    uid = search('u={:d}', update.message.text)

    if uid == None:
        update.message.reply_html(_('缺少 <code>u=</code> 參數'))
        return
    else:
        uid = uid[0]
    if reason == None:
        update.message.reply_html(_('缺少 <code>r=</code> 參數'))
        return
    else:
        reason = reason[0]

    mongo = db_tools.use_mongo()
    redis = db_tools.use_redis()
    query_user = mongo.user.find_one({'chat.id': uid})
    if query_user == None:
        update.message.reply_html(_('找不到這個人，失蹤了！！'))
        return

    user = db_parse.user()
    user.parse(query_user)
    if user.current == None:
        update.message.reply_html(_('這人沒有被封鎖過啊'))
        return

    user.current_raw['unban'] = reason
    update_user = {'$unset': {'current': ''},
                   '$addToSet': {'history': user.current_raw}}
    mongo.user.find_one_and_update({'chat.id': uid}, update_user)
    redis.lrem('ban_cache', uid, 0)

    if user.banned_participate == None or user.banned_participate == []:
        update.message.reply_text('解除封鎖完成。')
        return

    groups = ''
    for ban in user.banned_participate:
        try:
            user_ = bot.get_chat_member(ban, uid)
        except:
            groups += _('解封失敗\n') + \
                f'{ban}'
        else:
            if user_.status == 'kicked':
                try:
                    bot.unban_chat_member(ban, uid)
                except:
                    groups += _('解封失敗\n') + \
                        f'{ban}'
                else:
                    query_group = mongo.group.find_one({'chat.id': ban})
                    if query_group:
                        group = db_parse.group()
                        group.parse(query_group)
                        groups += f'<code>{group.title}</code>\n' + \
                            f'<code>{ban}</code>\n' + \
                            f'{"="*10}\n'
                    else:
                        groups += f'<code>{ban}</code>'

                    update_user = {'$pull': {'chat.banned_participate': ban}}
                    mongo.user.find_one_and_update(
                        {'chat.id': uid}, update_user)
    update.message.reply_html('[解封完成]\n'+groups)
