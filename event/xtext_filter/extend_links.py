import re
import time
import gettext
import logging
import coloredlogs
from html import unescape

import requests
from dateutil import tz
from datetime import datetime, timedelta

from telegram.ext import run_async
from telegram.error import BadRequest

import locales
from plugin import druation, to_emoji, to_string, config, sage
from plugin import db_parse, db_tools, excalibur, homicide, in_shield, is_admin, is_participate_white

from event.xtext_filter import *


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
taiwan_country = tz.gettz('Asia/Taipei')
_ = gettext.gettext
check_list = [binance]


class checker_result:
    def __init__(self):
        self.tags = None
        self.name = None


@run_async
def extend_links(bot, update, inherit, cmd=None):
    # tinyurl, t.cn, bit.ly
    return False
    locales.i18n(update).loads.install(True)
    pattern = '(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)(tinyurl\.com|bit\.ly|t\.cn)(\/[a-z0-9]+)'
    result = re.findall(pattern, unescape(
        update.message.text_html), re.IGNORECASE)
    if len(result) == 0:
        return False
    #result = []
    extract_result = checker_result()
    extract_result.tags = []
    extract_result.name = ''

    for x in result:
        url = ''.join(x)
        # binance_shortcut.ico
        req = requests.get(url, allow_redirects=False)
        try:
            real_url = req.headers['Location']
        except Exception as e:
            logger.exception(e)

        ## Do All Checker ##
        for checker in check_list:
            result_ = checker(bot, update, real_url)
            # result.append(result_)
            if result_.name:
                extract_result.name += result_.name
                extract_result.tags.extend(result_.tags)
            else:
                return
        ## Do All Checker ##
    if sage.in_shield(update.message.from_user.id):
        return
    if is_participate_white(bot, update):
        return
    if is_admin(bot, update):
        return
    if extract_result.tags == []:
        logger.info('return with null tags')
        return
    day = druation(list(dict.fromkeys(extract_result.tags)))
    tags = list(dict.fromkeys(extract_result.tags))

    mongo = db_tools.use_mongo()

    query_group = mongo.group.find_one({'chat.id': update.message.chat.id})
    if query_group:
        group = db_parse.group()
        group.parse(query_group)
    else:
        return True
    if bool(set(group.config.sub_ban_list).intersection(list(to_emoji(tags)))):
        pass
    else:
        return

    evidence = 2
    try:
        fwd = update.message.forward(config.getint('log', 'evidence'))
    except BadRequest as e:
        pass
    else:
        evidence = fwd.message_id
    if day == 0:
        until = 0
    else:
        until = (datetime.now(taiwan_country) +
                 timedelta(days=day)).timestamp()
    excalibur(bot, update, update.message.from_user.id, tags,
              bot.id, until=until, reason=f'hex auto.{extract_result.name}', evidence=evidence)

    right = False
    try:
        update.message.delete()
    except:
        right = True
    try:
        bot.restrict_chat_member(
            update.message.chat.id, update.message.from_user.id)
    except:
        right = True

    text = _(
        '偵測到 <code>{checker}</code> 垃圾訊息\n').format(checker=extract_result.name)
    if right:
        text += _('⚠️權限不足無法操作⚠️\n')
    if extract_result.tags:
        text += _('依照契約內容已吞噬 <code>Sammer</code>\n')
    text += _('名字：{full_name}\n' +
              'UID：<code>{user_id}</code>\n' +
              '標籤：<code>{tags}</code>').format(
                  full_name=update.message.from_user.mention_html(),
                  user_id=update.message.from_user.id,
                  tags=', '.join(tags))
    sent = update.message.reply_html(text).result()
    time.sleep(10)
    sent.delete()
    homicide(bot, update, update.message.from_user.id)
