from plugin import sage, db_tools
#import pysnooper


# @pysnooper.snoop()
def pregnant(bot, update, args):
    # /add 123 lucifer
    mongo = db_tools.use_mongo()
    if len(args) < 2:
        update.message.reply_text('參數過少。')
        return
    elif len(args) > 2:
        update.message.reply_text('參數過多。')
        return
    try:
        uid = int(args[0])
    except BaseException:
        update.message.reply_text('UID 參數錯誤')
        return
    else:
        level = args[1]
        if level not in ['elf', 'michael', 'lucifer']:
            update.message.reply_text('等級 參數錯誤')
            return
    if sage.lucifer(update.message.from_user.id):
        if sage.is_sage(uid):
            update.message.reply_text('已經有職位了。')
            return
        user = mongo.user.find_one({'chat.id': uid})
        if user is None:
            update.message.reply_text('我不認識這人啊 誰啊？')
            return

        mongo.class_level.find_one_and_update({}, {'$addToSet': {level: uid}})
        update.message.reply_text('🆙️ 升級完成').result()
        sage.refresh()


def marry(bot, update, args):
    # 結婚就是墳場
    mongo = db_tools.use_mongo()
    if len(args) < 2:
        update.message.reply_text('參數過少。')
        return
    elif len(args) > 2:
        update.message.reply_text('參數過多。')
        return
    try:
        uid = int(args[0])
    except BaseException:
        update.message.reply_text('UID 參數錯誤')
        return
    else:
        level = args[1]
        if level not in ['elf', 'michael', 'lucifer']:
            update.message.reply_text('等級 參數錯誤')
            return
    if sage.lucifer(update.message.from_user.id):
        if sage.is_sage(uid):
            mongo.class_level.find_one_and_update({}, {'$pull': {level: uid}})
            update.message.reply_text('拔掉頭環惹').result()
            sage.refresh()
            return
        else:
            update.message.reply_text('這不是天使吧？？')
            return
