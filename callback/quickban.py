import logging
import coloredlogs
from datetime import datetime, timedelta
from dateutil import tz

from telegram.ext.dispatcher import run_async

from locales import i18n
from plugin import callabck_parse, config, druation, excalibur
from plugin import sage

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
taiwan_country = tz.gettz('Asia/Taipei')


@run_async
def quickban(bot, update):
    query = update.callback_query
    i18n(update).loads.install(True)
    callback = callabck_parse.callback_parse(query.data)
    user_id, msg_id = callback.qact.split(':')
    tags = callback.qdata

    if sage.michael(query.from_user.id) == False and sage.lucifer(query.from_user.id) == False:
        query.answer('權限不夠。')
        return
    if sage.in_shield(int(user_id)):
        text = query.message.text_html + '\n被保護ㄉ狀態。'
        query.edit_message_text(text, parse_mode='html')
        return
    try:
        # sent = bot.forward_message(config.getint(
        #    'log', 'evidence'), config.getint('admin', 'elf'), int(msg_id))
        sent = update.message.forward(config.getint('log', 'evidence'))
    except:
        sent = 2

    days = druation([tags])
    if days != 0:
        until = int((datetime.now(taiwan_country) +
                     timedelta(days=days)).timestamp())
    else:
        until = 0
    excalibur(bot, update, int(user_id), [
              tags], query.from_user.id, until=until, reason=tags)
    text = query.message.text_html + \
        f'\n{"="*23}' + \
        _(f'\n處刑人：{query.from_user.mention_html()}\n') + \
        _(f'標籤：<code>{tags}</code>')
    query.edit_message_text(text, parse_mode='html')
