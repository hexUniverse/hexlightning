import gettext
import logging
import coloredlogs
from plugin import db_parse, db_tools, config
from plugin import to_emoji
from plugin.banyourwords import banyourwords
from locales import i18n

from dateutil import tz
from datetime import datetime

taiwan_country = tz.gettz('Asia/Taipei')
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
_ = gettext.gettext


def parser(
        uid,
        tags,
        opid,
        date=None,
        until=0,
        reason=None,
        evidence=0,
        user=None):
    tags = to_emoji(tags)
    if '💩'not in tags:
        tags = f'💩{tags}'
    else:
        tags = tags
    if date is None:
        date = int(datetime.now(taiwan_country).timestamp())

    current = {'date': date, 'until': until, 'opid': opid,
               'tags': tags, 'evidence': evidence}
    if reason:
        current['reason'] = reason
    return current


def announce(
        uid,
        tags,
        opid,
        date=None,
        until=0,
        reason=None,
        evidence=2,
        query_user=None,
        reply=False):
    if reason is None:
        reason = ', '.join(tags)

    text = ''
    if query_user:
        # user = db_parse.user()
        # user.parse(query_user)
        user = query_user
        if uid < 0:
            if query_user:
                text += _(f'頻道：<code>{user.fullname}</code>\n')
        else:
            if query_user:
                if user.fullname:
                    #
                    text += _(
                        f'名字：<a href="tg://user?id={user.id}">{user.fullname}</a>\n')
    tags_text = ', '.join(tags)
    until_text = datetime.fromtimestamp(until).astimezone(taiwan_country)
    text += _(f'UID：<code>{uid}</code>\n') + \
        _(f'標籤：<code>{tags_text}</code>\n') + \
        _(f'證據：https://t.me/hexevidence/{evidence}\n')
    if until == 0:
        text += _(banyourwords.forever.format(reason=reason))
    else:
        text += _(banyourwords.temp.format(reason=reason, date=until_text))
    return text


def excalibur(
        bot,
        update,
        uid,
        tags,
        opid,
        date=None,
        until=0,
        reason=None,
        evidence=2,
        user=None,
        reply=False):
    i18n(update).loads.install(True)
    mongo = db_tools.use_mongo()
    redis = db_tools.use_redis()

    query_user = mongo.user.find_one({'chat.id': uid})
    parse = parser(uid, tags, opid, date=date, until=until,
                   reason=reason, evidence=evidence, user=user)
    if query_user:
        user_ = db_parse.user()
        user_.parse(query_user)

        if user_.current:
            # 新增 current, 舊的移動到 history array
            user_update = {'$push': {'history': user_.current_raw},
                           '$set': {'current': parse}}
            mongo.user.find_one_and_update({'chat.id': uid}, user_update)

        elif user_.current is None:
            # 不是拉 警察這是我第一次拉
            # : 欸 我也是第一次開罰單啊 Q_Q
            # 辣我可以順便要你的電話嘛？ OS: 好 好...好可愛
            # : Q_Q 不要投訴我啦
            user_update = {'$set': {'current': parse}}
            mongo.user.find_one_and_update({'chat.id': uid}, user_update)

    else:
        if user:
            user_update = {'chat': user.to_dict(), 'current': parse}
            mongo.user.insert(user_update)
        else:
            user_update = {'chat': {'id': uid}, 'current': parse}
            mongo.user.insert(user_update)

    ban_cache = redis.lrange('ban_cache', 0, -1)
    if str(uid).encode() not in ban_cache:
        redis.lpush('ban_cache', uid)
    if query_user:
        return announce(
            uid,
            tags,
            opid,
            date=None,
            until=until,
            reason=reason,
            evidence=evidence,
            query_user=user_,
            reply=False)
    else:
        return announce(uid, tags, opid, date=None, until=until,
                        reason=reason, evidence=evidence)


def inherit_excalibur(bot, update, inherit_from: db_parse.user):
    '''
    inherit_from: db_parse.user
    inherit_to: user obj

    轉傳訊息
    '''
    mongo = db_tools.use_mongo()
    query_user = mongo.user.find_one({'chat.id': update.message.from_user.id})
    # user_ = db_parse.user()
    if query_user is None:
        user_update = {'chat': update.message.from_userto_dict()}
        mongo.user.insert(user_update)
        query_user = mongo.user.find_one(
            {'chat.id': update.message.from_user.id})

    user_ = db_parse.user()
    user_.parse(query_user)

    channel = config.getint('log', 'evidence')
    try:
        evidence = update.message.forward(channel).message_id
    except BaseException:
        evidence = 2

    current = inherit_from.current_raw
    update_user = {'inherit': {
        'id': inherit_from.id,
        'chat': {
            'id': update.message.chat.id
        },
        'evidence': inherit_from.current.evidence
    }}
    #current['inherit']['id'] = inherit_from.id
    #current['inherit']['chat']['id'] = update.message.chat.id
    #current['inherit']['evidence'] = inherit_from.current.evidence
    current['evidence'] = evidence
    current.update(update_user)
    logger.info(current)

    if user_.current:
        # 新增 current, 舊的移動到 history array
        user_update = {'$push': {'history': user_.current_raw},
                       '$set': {'current': current}}
        mongo.user.find_one_and_update(
            {'chat.id': update.message.from_user.id}, user_update)

    elif user_.current is None:
        # 不是拉 警察這是我第一次拉
        # : 欸 我也是第一次開罰單啊 Q_Q
        # 辣我可以順便要你的電話嘛？ OS: 好 好...好可愛
        # : Q_Q 不要投訴我啦
        user_update = {'$set': {'current': current}}
        mongo.user.find_one_and_update(
            {'chat.id': update.message.from_user.id}, user_update)
