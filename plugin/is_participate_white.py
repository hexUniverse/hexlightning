from plugin import db_tools

mongo = db_tools.use_mongo()


def is_participate_white(bot, update, specfic=None):
    if specfic:
        chat_id, user_id = specfic
    else:
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
    query = {'chat.id': chat_id, 'chat.white_participate': {'$in': [user_id]}}
    return bool(mongo.group.find_one(query))
