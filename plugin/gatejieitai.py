import logging
import coloredlogs
#import pysnooper
from datetime import datetime, timedelta
from dateutil import tz

from telegram.ext.dispatcher import run_async
from plugin import db_parse, db_tools, sage

taiwan_country = tz.gettz('Asia/Taipei')
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


# @run_async
def gatejieitai(bot, update, specfic=False):
    # compare from_user and chat.id and tags if banned in group
    # return True if need action
    mongo = db_tools.use_mongo()
    redis = db_tools.use_redis()

    user = db_parse.user()
    group = db_parse.group()

    # check cache
    query_redis = redis.lrange('ban_cache', 0, -1)
    query_white = redis.lrange('white_cache', 0, -1)
    # logger.info(specfic)
    if specfic:
        specfic_chat, specfic_id = specfic
    else:
        specfic_chat, specfic_id = update.message.chat.id, update.message.from_user.id
    if str(specfic_id).encode() not in query_redis:
        logger.debug(f'{specfic_id} not in redis cache')
        return False
    if str(specfic_id).encode() in query_white:
        logger.debug(f'{specfic_id} in white cache')
        return False
    if sage.is_sage(specfic_id):
        logger.debug(f'{specfic_id} in sage')
        return False
    query_group_white = redis.lrange(f'white:{str(specfic_chat)}', 0, -1)
    if str(specfic_id).encode() in query_group_white:
        logger.debug(f'{specfic_id} in group white cache')
        return False

    else:
        user_query = mongo.user.find_one(
            {'chat.id': specfic_id})
        group_query = mongo.group.find_one({'chat.id': specfic_chat})
        user.parse(user_query)
        group.parse(group_query)
        if user.current == None:
            return False
        if group_query == None:
            return False
        date = datetime.fromtimestamp(
            user.current.until).astimezone(taiwan_country)
        now = datetime.now(taiwan_country)
        l = user.current.until - now.timestamp()
        if user.current.until - now.timestamp() > 0:
            # kick yout ass
            if group.config.sub_ban_list:
                # 比較兩者
                check = bool(
                    set(group.config.sub_ban_list).intersection(user.current.tags_list))
                if check:
                    return user
            else:
                # 沒有設定清單
                return False
        else:
            # bang for ever
            if date.year == 1970:
                # logger.info(date)
                # logger.info(group_query)
                if group.config and group.config.sub_ban_list:
                    check = bool(
                        set(group.config.sub_ban_list).intersection(user.current.tags_list))
                    if check:
                        #logger.info(f'user {check}')
                        return user
            # punishiment finished
            if user.current.until - now.timestamp() <= 0 and user.current.until != 0:
                logger.info('punishiment fin')
                mongo.user.find_one_and_update(
                    {'chat.id': specfic_id},
                    {'$set': {'chat.banned_participate': []}}
                )
                return False
