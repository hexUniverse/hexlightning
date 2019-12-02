import gettext
import time
import logging
import coloredlogs

from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest

from plugin import db_parse, db_tools, gatejieitai, sage, homicide, inherit_excalibur
from plugin.excalibur import announce

from locales import i18n
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
mongo = db_tools.use_mongo()
redis = db_tools.use_redis()

_ = gettext.gettext


@run_async
def last_exlie(bot, update):
    # i18n(update).loads.install(True)
    # i18n(update).loads.install(True)
    forward = None
    if update.message.forward_from:
        forward = update.message.forward_from
    elif update.message.forward_from_chat:
        forward = update.message.forward_from_chat
    # 檢證流程需要更改。
    '''
    check forward content
        - ban
        - pass
    - check user
        - ban
        - pass

    '''
    inherit = None
    forward_check = None
    if forward:
        forward_check = gatejieitai(bot, update, specfic=(
            update.message.chat.id, forward.id))
        if sage.in_shield(update.message.from_user.id):
            return
        query_group_white = redis.lrange(
            f'white:{str(update.message.from_user.id)}', 0, -1)
        if str(update.message.from_user.id).encode() in query_group_white:
            logger.info(f'{update.message.from_user.id} in group white cache')
            return

        if forward_check and forward_check.current:
            # try:
            #    update.message.delete()
            # except:
            #    pass
            keeps = False
            try:
                update.message.from_user.fullname = update.message.from_user.full_name
                msg = _(announce(update.message.from_user.id, forward_check.current.tags_list, forward_check.current.opid, until=forward_check.current.until,
                                 reason=forward_check.current.reason, evidence=forward_check.current.evidence, query_user=update.message.from_user))
                bot.restrict_chat_member(
                    update.message.chat.id, update.message.from_user.id)
            except BadRequest as e:
                if e.message == 'Not enough rights to restrict/unrestrict chat member':
                    keeps = True
                    text = _('⚠️權限不足無法處理⚠️\n') + msg
                elif e.message == 'User is an administrator of the chat':
                    text = _('已自動加入群組白名單內 ✅') + msg

            else:
                text = _('轉傳封鎖內容已自動處理\n'
                         '名字：{chat_title}\n'
                         'ID：<code>{chat_id}</code>\n'
                         '{spliter}'
                         '\n{msg}').format(
                             spliter='='*10,
                             chat_title='title',
                             chat_id=forward_check.id,
                             msg=msg)
            sent = update.message.reply_html(text).result()
            if keeps:
                return
            time.sleep(10)
            try:
                update.message.delete()
            except:
                pass
            try:
                sent.delete()
            except:
                pass
            try:
                bot.kick_chat_member(update.message.chat.id,
                                     update.message.from_user.id)
            except:
                pass
            else:
                update_user = {'$addToSet': {
                    'chat.banned_participate': update.message.chat.id}}
                mongo.user.find_one_and_update(
                    {'chat.id': forward_check.id}, update_user)

    user_check = gatejieitai(bot, update, specfic=(
        update.message.chat.id, update.message.from_user.id))

    # user has mark as spamming, to processed
    if user_check and user_check.current:
        try:
            update.message.delete()
        except:
            pass
        keeps = False
        try:
            msg = _(announce(user_check.id, user_check.current.tags_list, user_check.current.opid, until=user_check.current.until,
                             reason=user_check.current.reason, evidence=user_check.current.evidence, query_user=user_check))
            bot.restrict_chat_member(
                update.message.chat.id, update.message.from_user.id)
        except BadRequest as e:
            if e.message == 'Not enough rights to restrict/unrestrict chat member':
                keeps = True
                text = _('⚠️權限不足無法處理⚠️\n') + msg
            elif e.message == 'User is an administrator of the chat':
                text = _('已自動加入群組白名單內 ✅') + msg

        else:
            text = msg
        sent = update.message.reply_html(text).result()
        if keeps:
            return
        time.sleep(10)
        try:
            sent.delete()
        except:
            pass
        try:
            bot.kick_chat_member(update.message.chat.id,
                                 update.message.from_user.id)
        except:
            pass
        else:
            update_user = {'$addToSet': {
                'chat.banned_participate': update.message.chat.id}}
            mongo.user.find_one_and_update(
                {'chat.id': user_check.id}, update_user)

    if forward_check:
        # 轉傳是 until 0
        # insert = False
        if forward_check.current.until == 0:
            # bot, update, inherit_from, inherit_to
            inherit_excalibur(bot, update, forward_check)

        # 轉傳不是 until 0
        else:
            if user_check and user_check.current:
                if forward_check.current.until > user_check.current.until:
                    logger.info(forward_check.current.until)
                    logger.info(user_check.current.until)
                    # update_user = {
                    #    '$set': {'current': forward_check.current_raw},
                    #    '$push': {'history': user_check.current_raw}}
                    inherit_excalibur(bot, update, forward_check)
            # 檢查 ban 比較久的有沒有被繼承
            # 這樣ㄛ！！
                else:
                    return
            elif user_check == False:
                # update_user = {
                #    '$set': {'current': forward_check.current_raw}}
                inherit_excalibur(bot, update, forward_check)
            # else:
            #    # 繼承
            #    insert = True
            #    forward_check.current_raw['inherit_id'] = forward_check.id
            #    forward_check.current_raw['inherit_chat'] = update.message.chat.id
            #    update_user = {'current': forward_check.current_raw}
            #    update_user.update(
            #        {'chat': update.message.from_user.to_dict()})
        # if update_user and insert:
        #    mongo.user.insert(update_user)
        # elif update_user:
        #    mongo.user.find_one_and_update(
        #        {'chat.id': update.message.from_user.id}, update_user)
        update_ban = {
            '$addToSet': {
                'chat.banned_participate': update.message.chat.id},
            '$pull': {'chat.participate': update.message.chat.id}
        }
        mongo.user.find_one_and_update(
            {'chat.id': update.message.from_user.id}, update_ban)
        query_ban_cache = redis.lrange('ban_cache', 0, -1)
        if str(update.message.from_user.id).encode() not in query_ban_cache:
            redis.lpush('ban_cache', update.message.from_user.id)
        homicide(bot, update, update.message.from_user.id)
