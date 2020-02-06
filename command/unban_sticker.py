from plugin import db_tools, db_parse
from telegram.ext import Filters
from parse import search
mongo = db_tools.use_mongo()


def unban_sticker(bot, update):
    if Filters.reply(update.message):
        if update.message.reply_to_message.sticker.set_name is None:
            return
        elif update.message.reply_to_message.sticker.set_name:
            set_name = update.message.reply_to_message.sticker.set_name
    else:
        set_name = search('s={:S}', update.message.text)
        if set_name is None:
            update.message.reply_text('缺少 <code>s=</code> 參數')
            return
        else:
            set_name = set_name[0]

        query_sticker = mongo.sticker.find_one(
            {'sticker.set_name': set_name})
        if bool(query_sticker) == False:
            return
        sticker = db_parse.sticker()
        sticker.parse(query_sticker)
        mongo.sticker.delete_one(
            {'sticker.set_name': set_name})
        text = '已解除貼圖封鎖。'
        update.message.reply_text(text)
