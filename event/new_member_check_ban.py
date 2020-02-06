import time
import logging
import coloredlogs

from plugin import db_parse, db_tools, gatejieitai
from plugin import to_string
from locales import i18n

from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest

mongo = db_tools.use_mongo()
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def new_member_check_ban(bot, update, new_member):
    i18n(update).loads.install(True)
    if gatejieitai(bot, update, specfic=(update.message.chat.id, new_member.id)):
        user = db_parse.user()
        group = db_parse.group()
        query_user = mongo.user.find_one({'chat.id': new_member.id})
        query_group = mongo.group.find_one({'chat.id': update.message.chat.id})
        user.parse(query_user)
        group.parse(query_group)

        try:
            update.message.delete()
        except BadRequest:
            pass

        if user.current.evidence == None:
            user.current.evidence = 2
        text = _('名字：{fullname}\n'
                 'UID：{uid}\n'
                 '證據：https://t.me/hexevidence/{evidence}\n'
                 '標籤：{tags}\n'
                 '因為 <code>{reason}</code>\n'
                 '封鎖至 <code>{until}</code>\n'
                 '處刑人：{execser}\n'
                 '有任何問題請至 @hexjudge 詢問').format(
                     fullname=new_member.mention_html(),
                     uid=new_member.id,
                     evidence=user.current.evidence,
                     tags=to_string(user.current.tags),
                     reason=user.current.reason,
                     until=user.current.date_text,
                     execser=user.current.opid)
        try:
            sent = bot.send_message(
                update.message.chat.id, text, parse_mode='html').result()
        except BadRequest as e:
            if e.message == 'Have no rights to send a message':
                pass
            logger.warn(e.message)
        time.sleep(5)
        try:
            sent.delete()
        except BadRequest as e:
            logger.warn(e.message)
        try:
            bot.kick_chat_member(update.message.chat.id, new_member.id)
        except BadRequest as e:
            if e.message == 'Not enough rights to restrict/unrestrict chat member':
                text = _('因權限不足無法踢除 {fullname}\n'
                         '⚠️為bot正常運作，請給予admin權限⚠️').format(fullname=new_member.mention_html())
                bot.send_message(text, parse_mode='html')
        return True
    return False
