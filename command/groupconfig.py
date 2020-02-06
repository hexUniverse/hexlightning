import time
from html import escape
from telegram.ext.dispatcher import run_async

from plugin import db_tools, is_admin, sage
from locales import i18n
from inlinekeyboard import generate


@run_async
def groupconfig(bot, update):
    i18n(update).loads.install(True)
    mongo = db_tools.use_mongo()
    try:
        update.message.delete()
    except:
        pass
    users = bot.get_chat_member(
        update.message.chat.id, update.message.from_user.id)
    if is_admin(bot, update) == False or sage.lucifer(update.message.chat.id) == False:
        text = _('你不是管理員好嗎，請不要亂打擾我。')
        sent = update.message.reply_text(text).result()
        time.sleep(5)
        sent.delete()
        return
    text = f'<code>{escape(update.message.chat.title)}</code>\n' + \
        _('📋 訂閱黑名單列表\n') + \
        _('本清單預設開啟 "兒童色情內容" \n') + \
        _('✅ - 開啟訂閱\n') + \
        _('❌ - 關閉訂閱')
    keyboard = generate.inline_groupconfig(bot, update, 0)
    sent = update.message.reply_text(
        text, parse_mode='html', reply_markup=keyboard)
    mongo.group.find_one_and_update({'chat.id': update.message.chat.id}, {'$set': {
        'chat.config.configuring': sent.result().message_id}})
