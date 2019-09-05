from plugin import db_parse, db_tools, sage
from locales import i18n

from telegram.ext.dispatcher import run_async


@run_async
def del_wl(bot, update, args):
    i18n(update).loads.install(True)
    if len(args) == 0:
        try:
            update.message.delete()
        except:
            pass
        return
    if sage.is_sage(update.message.from_user.id):
        if sage.lucifer(update.message.from_user.id) == False:
            try:
                update.message.delete()
            except:
                pass
            text = '你等級不夠 🌚\n最低等級要求是 <code>Lucifer</code>'
            update.message.reply_html(text)
            return
    else:
        try:
            update.message.delete()
        except:
            pass
        return
    mongo = db_tools.use_mongo()
    if len(args) > 1:
        update.message.reply_text(_('傳入過多參數。'))
        return
    try:
        uid = int(args[0])
    except:
        update.message.reply_html(_(f'UID <code>{args[0]}</code> 解析錯誤 '))
        return
    if uid > 9999999999:
        update.message.reply_text(_('傳入怪怪的 UID 參數。'))
        return
    query_user = mongo.user.find_one({'chat.id': uid})
    if query_user:
        user = db_parse.user()
        user.parse(query_user)
        if user.is_white:
            mongo.user.find_one_and_update(
                {'chat.id': uid}, {'$set': {'chat.is_white': False}})
            text = _('已解除全域白名單 ✅')
            update.message.reply_text(text)
        else:
            text = _(f'<code>{uid}</code> 並沒有白名單紀錄')
            update.message.reply_html(text)
    else:
        text = _(f'<code>{uid}</code> 並沒有紀錄')
        update.message.reply_html(text)
