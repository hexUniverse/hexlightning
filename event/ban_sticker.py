import time
import logging
import coloredlogs

from dateutil import tz
from datetime import datetime, timedelta

from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest

from plugin import db_parse, db_tools, excalibur, sage, sticker_judge
from plugin import config, homicide, is_admin
from plugin.excalibur import announce

from locales import i18n


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
mongo = db_tools.use_mongo()
redis = db_tools.use_redis()

taiwan_country = tz.gettz('Asia/Taipei')


@run_async
def ban_sticker(bot, update):
    i18n(update).loads.install(True)
    if update.message.forward_from:
        chat = update.message.forward_from
    elif update.message.forward_from_chat:
        chat = update.message.forward_from_chat
    else:
        chat = update.message.from_user
    if update.message.sticker.set_name is None:
        return
    if sage.in_shield(update.message.from_user.id):
        return
    group = db_parse.group()
    query_group = mongo.group.find_one({'chat.id': update.message.chat.id})
    group.parse(query_group)
    if group.white_participate:
        if update.message.from_user.id in group.white_participate:
            return
    if is_admin(
        bot,
        update,
        specfic=(
            update.message.chat.id,
            update.message.from_user.id)):
        return

    ban = sticker_judge.checker(
        bot, update, update.message.sticker.set_name)

    if ban:
        try:
            evidence = update.message.forward(config.getint('log', 'evidence'))
        except BaseException:
            evidence = 2

        if update.message.sticker.set_name:
            query_stiker = mongo.sticker.find_one(
                {'sticker.set_name': update.message.sticker.set_name})
        if query_stiker:
            sticker = db_parse.sticker()
            sticker.parse(query_stiker)
            query_user = mongo.user.find_one(
                {'chat.id': update.message.from_user.id})
            user = db_parse.user()
            user.parse(query_user)

            if sticker.day == 0:
                until = 0
            else:
                until = int((datetime.now(taiwan_country) +
                             timedelta(days=sticker.day)).timestamp())

            # check group sub with sticker ban
            check = bool(
                set(group.config.sub_ban_list).intersection(sticker.tags_list))
            logger.debug(
                f'sticker compare with group sub is {check}, should ban')

            if not check:
                return
            if until == 0:
                pass
            '''
            當 A 子在別的地方得到 mark as spam (ads), 在 B 群沒有訂閱 (ads) 而有訂閱 porn,
            而 A 在貼了 mark as porn 的貼圖。
            A 子會被踢出去，並且記錄在 banned_participate, 但不更新 ban.current
            '''
            single_ban = True
            if user.current and user.current.until != 0:
                single_ban = False
                update.message.from_user.fullname = update.message.from_user.full_name
                if evidence == 2:
                    evidence_ = sticker.evidence
                else:
                    evidence_ = evidence.message_id

                excalibur(
                    bot,
                    update,
                    update.message.from_user.id,
                    sticker.tags,
                    sticker.opid,
                    until=until,
                    reason=sticker.reason,
                    evidence=evidence_,
                    user=update.message.from_user)
                announce_ban = _(
                    announce(
                        update.message.from_user.id,
                        sticker.tags,
                        sticker.opid,
                        until=until,
                        reason=sticker.reason,
                        evidence=evidence_,
                        query_user=update.message.from_user))
            else:
                announce_ban = _(
                    '名字：{fullname}\n'
                    '傳送了 <code>{sticker}</code> 已被標記為 <code>{tags}</code> 的貼圖。').format(
                    fullname=user.mention_html,
                    sticker=sticker.set_name,
                    tags=sticker.tags_text)
            try:
                update.message.delete()
            except BaseException:
                pass
            try:
                bot.restrict_chat_member(
                    update.message.chat.id, update.message.from_user.id)
            except BadRequest as e:
                if e.message == 'User is an administrator of the chat':
                    return
                elif e.message == 'Not enough rights to restrict/unrestrict chat member':
                    text = _('⚠️權限不足⚠️\n') + announce_ban
                    update.message.reply_html(text)
                    return

            else:
                sent = update.message.reply_html(announce_ban).result()

            time.sleep(10)
            try:
                sent.delete()
            except BaseException:
                pass

            homicide(bot, update, update.message.from_user.id)


'''
forward sticker
'''
