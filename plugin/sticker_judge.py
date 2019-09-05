from plugin import db_parse, db_tools
from plugin import sage
mongo = db_tools.use_mongo()
redis = db_tools.use_redis()


def refresh():
    query_sticker = mongo.sticker.find()
    redis.delete('sticker_cache')
    for query in query_sticker:
        sticker = db_parse.sticker()
        sticker.parse(query)
        if sticker.set_name:
            redis.lpush('sticker_cache', sticker.set_name)


def checker(bot, update, set_name=None):
    stickers = redis.lrange('sticker_cache', 0, -1)
    d = set_name.encode()
    if set_name and set_name.encode() in stickers:
        return True
    else:
        False
