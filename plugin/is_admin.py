def is_admin(bot, update, specfic=None):
    if specfic:
        chat = specfic[0]
        uid = specfic[1]
        user = bot.get_chat_member(chat, uid)
    elif update.callback_query:
        user = bot.get_chat_member(
            update.callback_query.message.chat.id, update.callback_query.message.from_user.id)
    else:
        user = bot.get_chat_member(
            update.message.chat.id, update.message.from_user.id)

    if user.status not in ['administrator', 'creator']:
        return False
    else:
        return True
