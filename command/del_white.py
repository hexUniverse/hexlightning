from plugin import db_parse, db_tools, is_admin
from locales import i18n

from telegram.ext.dispatcher import run_async


@run_async
def del_white(bot, update, args):
    i18n(update).loads.install(True)
    if len(args) == 0:
        try:
            update.message.delete()
        except:
            pass
        return
    admins = bot.get_chat_member(
        update.message.chat.id, update.message.from_user.id)
    if is_admin(bot, update) == False:
        try:
            update.message.delete()
        except:
            pass
        text = '此指令只允許管理員操作。'
        update.message.reply_text(text)
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

    query_group = mongo.group.find_one({'chat.id': update.message.chat.id})
    if query_group:
        group = db_parse.group()
        group.parse(query_group)
        if group.white_participate:
            if uid in group.white_participate:
                mongo.group.update_one(
                    {'chat.id': group.id}, {'$pull': {'chat.white_participate': uid}},)
                text = _('已更新白名單 ✅')
                update.message.reply_text(text)
        else:
            text = _(f'<code>{uid}</code> 並不在群組白名單內')
            update.message.reply_html(text)

    else:
        text = _('似乎發生了點問題...?\n') + \
            _('請先使用 <code>!hex config</code> 設定群組試試？')
        update.message.reply_html(text)
