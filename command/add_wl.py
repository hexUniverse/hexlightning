from plugin import db_parse, db_tools, sage
from locales import i18n

from telegram.ext.dispatcher import run_async


@run_async
def add_wl(bot, update, args):
    i18n(update).loads.install(True)
    if len(args) == 0:
        try:
            update.message.delete()
        except BaseException:
            pass
        return
    if sage.is_sage(update.message.from_user.id):
        if sage.lucifer(update.message.from_user.id) == False:
            try:
                update.message.delete()
            except BaseException:
                pass
            text = '你等級不夠 🌚\n最低等級要求是 <code>Lucifer</code>'
            update.message.reply_html(text)
            return
    else:
        try:
            update.message.delete()
        except BaseException:
            pass
        return
    mongo = db_tools.use_mongo()

    if len(args) > 1:
        update.message.reply_text(_('傳入過多參數。'))
        return
    try:
        uid = int(args[0])
    except BaseException:
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
            text = _(f'<code>{uid}</code> 已在白名單內')
            update.message.reply_html(text)
        else:
            mongo.user.find_one_and_update(
                {'chat.id': uid}, {'$set': {'chat.is_white': True}})
            text = _('已更新全域白名單 ✅')
            update.message.reply_text(text)
    else:
        update_user = {'chat': {'id': uid, 'is_white': True}}
        mongo.user.insert(update_user)
        text = _('已更新全域白名單 ✅')
