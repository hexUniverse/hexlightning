import logging
import coloredlogs

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async

from locales import i18n
from plugin import config, callabck_parse, emojitags, to_emoji
from plugin import db_parse, db_tools

from inlinekeyboard import generate

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def hint(bot, update):
    query = update.callback_query
    i18n(query).loads.install(True)

    mongo = db_tools.use_mongo()
    callback = callabck_parse.callback_parse(query.data)

    if callback.qact in ['groupconfig', 'guide']:
        if callback.qdata in emojitags().emoji_dict.keys():
            answer = emojitags().emoji_dict[callback.qdata]['hint']
        elif callback.qdata in generate.groupconfig_dict(1).keys():
            answer = generate.groupconfig_dict(1)[callback.qdata]['hint']

        query.answer(_('{answer}'.format(answer=answer)), show_alert=True)
