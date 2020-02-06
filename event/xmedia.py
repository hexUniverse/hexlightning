import io
import time
import gettext
import logging
import coloredlogs

import locales
from plugin import nsfw_detect, imagehash, homicide
from plugin import config, db_parse, db_tools, excalibur
from plugin import in_shield, is_admin, is_participate_white
from plugin import druation

from datetime import datetime, timedelta
from dateutil import tz
from telegram.ext import Filters, run_async
from telegram.error import BadRequest

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
redis = db_tools.use_redis()
mongo = db_tools.use_mongo()
taiwan_country = tz.gettz('Asia/Taipei')
_ = gettext.gettext


@run_async
def xmedia_refresh():
    redis.delete('photo_cache')
    query_photo = list(mongo.xmedia.find({}))
    for photo in query_photo:
        photo_parse = db_parse.media()
        photo_parse.parse(query_photo)
        redis.lpush('photo_cache', photo_parse.hash)
    return True


@run_async
def xmedia(bot, update):
    locales.i18n(update).loads.install(True)
    if in_shield(update.message.from_user.id):
        return
    if is_participate_white(bot, update):
        return

    query_user = mongo.user.find_one({'chat.id': update.message.from_user.id})
    if query_user:
        user = db_parse.user()
        user.parse(query_user)
        if user.current:
            if datetime.fromtimestamp(user.current.until).astimezone(
                    taiwan_country).year == 1970:
                return
    if is_admin(bot, update):
        return

    if Filters.photo(update.message):
        file = bytes(
            update.message.photo[-1].get_file().download_as_bytearray())

    bio = io.BytesIO(file)
    i = imagehash.hashing(bio)
    hashing = i.phash()
    middle = i.indexing()

    query_xmedia = list(mongo.xmedia.find(
        {'photo.indexing': {'$gte': middle - 10, '$lte': middle + 10}}))
    if query_xmedia == []:
        logger.info('no target found')
        # return
    if query_xmedia:
        compare_list = []
        for parse in query_xmedia:
            media = db_parse.media()
            media.parse(parse)
            compare_list.append(media.hash)

        compare_result = i.plooks_like(compare_list)
        if compare_result[-1].judge:

            query_photo = mongo.xmedia.find_one(
                {'photo.hash': compare_result[-1].hash})

            media = db_parse.media()
            media.parse(query_photo)
            if media.is_white:
                logger.debug(f'{hashing} in white list')
                return

            query_group = mongo.group.find_one(
                {'chat.id': update.message.chat.id})
            if query_group:
                group = db_parse.group()
                group.parse(query_group)
            else:
                return

            # query_xmedia = mongo.xmedia.find_one(
            #    {'photo.hash': compare_result[-1].hash})
            #media_ = db_parse.media()
            # media_.parse(query_xmedia)

            check = bool(
                set(group.config.sub_ban_list).intersection(list(media.tags)))
            # logger.info(media.tags)
            # update.message.reply_text(media.tags)
            if not check:
                pass
            else:
                # query_user = mongo.user.find_one(
                #    {'chat.id': update.message.from_user.id})
                try:
                    sent = update.message.forward(
                        config.getint('log', 'evidence')).message_id
                except BaseException:
                    sent = 2
                else:
                    until = druation(list(media.tags_list))
                    excalibur(
                        bot,
                        update,
                        update.message.from_user.id,
                        media.tags_list,
                        media.opid,
                        until=until,
                        reason=media.reason,
                        evidence=sent,
                        user=update.message.from_user)
                    announce_ban = _(
                        '名字：{fullname}\n'
                        '傳送了已被標記為 <code>{tags}</code> 的圖片，已進行處置。').format(
                        fullname=update.message.from_user.mention_html(),
                        tags=media.tags_text)
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
                        bot.delete_message(
                            update.message.chat.id, sent.message_id)
                    except BaseException:
                        pass
                    finally:
                        homicide(bot, update, update.message.from_user.id)
                    return

    # NSFW DETECT #
    query_group = mongo.group.find_one({'chat.id': update.message.chat.id})
    if query_group is None:
        return
    group = db_parse.group()
    group.parse(query_group)
    check = bool(
        set(group.config.sub_ban_list_text).intersection(['porn']))
    if not check:
        return
    if group.config.ml_nsfw in [None, False]:
        return

    nsfw = nsfw_detect(file=file)
    if nsfw.ban:
        abyss = config.getint('log', 'abyss')
        sent = update.message.forward(abyss)
        evidence = update.message.forward(config.getint('log', 'evidence'))
        record_msg = f'Name：{update.message.from_user.mention_html()}\n' \
            f'UID：<code>{update.message.from_user.id}</code>\n' \
            f'Checker：<code>NSFW</code>\n' \
            f'Group Name：<code>{update.message.chat.title}</code>\n' \
            f'Group ID：<code>{update.message.chat.id}</code>\n' \
            f'Group Username：{f"@{update.message.chat.username}" if update.message.chat.username else None}\n' \
            f'NSFW Score：<code>{nsfw.score}</code>\n' \
            f'#NSFW #tracker_{update.update_id}'
        bot.send_message(abyss, record_msg, parse_mode='html',
                         reply_to_message_id=sent.message_id)
        try:
            text = ''
            bot.restrict_chat_member(
                update.message.chat.id, update.message.from_user.id)
        except BadRequest as e:
            if e.message == 'Not enough rights to restrict/unrestrict chat member':
                text = _('⚠️權限不足⚠️\n')
        finally:
            text += _('淺行系統偵測到 <code>NSFW</code> 內容媒體，依照契約將吞食內容\n'
                      '名字：{fullname}\n'
                      'UID：<code>{uid}</code>\n'
                      '若有誤判請至 @hexjudge 報告 淺行系統 存在問題。\n'
                      '案件追蹤 ID：#tracker_{tracker_id}').format(
                          fullname=update.message.from_user.mention_html(),
                          uid=update.message.from_user.id,
                          tracker_id=update.update_id
            )
            try:
                update.message.delete()
            except BaseException:
                pass
            sent = update.message.reply_html(text).result()
            until = int((datetime.now(taiwan_country) +
                         timedelta(days=90)).timestamp())

            time.sleep(10)
            bot.delete_message(update.message.chat_id, sent.message_id)
            excalibur(
                bot,
                update,
                update.message.from_user.id,
                ['porn'],
                bot.id,
                until=until,
                reason='NSFW 自動偵測',
                evidence=evidence.message_id,
                user=update.message.from_user)

            homicide(bot, update, update.message.from_user.id)
