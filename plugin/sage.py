from plugin import db_parse, db_tools

redis = db_tools.use_redis()
mongo = db_tools.use_mongo()


def refresh():
    result = mongo.class_level.find_one({})
    lucifer = result['lucifer']
    michael = result['michael']
    elf = result['elf']
    for sage_calling, sage_name in zip([elf, michael, lucifer], ['elf', 'michael', 'lucifer']):
        redis.delete(sage_name)
        for x in sage_calling:
            redis.lpush(sage_name, x)


def is_sage(user_id: 'str or int'):
    sages = []
    for x in ['elf', 'michael', 'lucifer']:
        tmp = redis.lrange(x, 0, -1)
        for get_id in tmp:
            sages.append(int(get_id.decode()))

    if int(user_id) in sages:
        return True
    else:
        return False


def elf(user_id: 'str or int'):
    query = redis.lrange('elf', 0, -1)
    if str(user_id).encode() in query:
        return True
    else:
        False


def michael(user_id: 'str or int'):
    query = redis.lrange('michael', 0, -1)
    if str(user_id).encode() in query:
        return True
    else:
        False


def lucifer(user_id: 'str or int'):
    query = redis.lrange('lucifer', 0, -1)
    print(query)
    if str(user_id).encode() in query:
        return True
    else:
        False
