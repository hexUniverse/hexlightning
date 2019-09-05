import logging
import coloredlogs

from plugin import db_tools

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
redis = db_tools.use_redis()
mongo = db_tools.use_mongo()


def fresh_redis():
    logger.info(f'refresh redis started.')
    fulluser = list(mongo.user.find(
        {"current": {'$exists': True}, "current.date": {'$exists': True}}))
    redis.delete('ban_cache')
    for user in fulluser:
        redis.lpush('ban_cache', user['chat']['id'])
    logger.info(f'refresh redis finished.')
    logger.info(f'Redis Cached {len(fulluser)} Banned UID')
    return len(fulluser)
