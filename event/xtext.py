import re
import time
import logging
import coloredlogs

from dateutil import tz
from datetime import datetime, timedelta

import locales
from plugin import db_tools, db_parse, config, excalibur, homicide
from plugin import druation, is_admin, is_participate_white, sage, to_emoji
from event.xtext_filter import _, extend_links


from telegram.ext import Filters
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
taiwan_country = tz.gettz('Asia/Taipei')
redis = db_tools.use_redis()
mongo = db_tools.use_mongo()


class xtext_rules:
    def __init__(self, data):
        self.rule = None
        self.name = None
        self.match = None
        self.tags = None
        self.action = None
        self.parse(data)

    def parse(self, data):
        if 'rule' in data.keys():
            self.rules = data['rule']
        if 'name' in data.keys():
            self.name = data['name']
        if 'match' in data.keys():
            self.match = data['match']
        if 'tags' in data.keys():
            self.tags = data['tags']
        if 'action' in data.keys():
            self.action = data['action']


def xfilter_refresh():
    redis = db_tools.use_redis()
    mongo = db_tools.use_mongo()

    result = mongo.xtext_filter.find()
    redis.delete('xtext_filter')
    for x in list(result):
        redis.lpush('xtext_filter', x['rule'])
    return True


class excute_:
    def __init__(self):
        self.tags = []  # list
        self.name = ''  # string
        self.action = []  # list

    def parse(self, data):
        self.name += f'{data.name} '
        if data.action:
            self.action.extend(data.action)
        self.tags.extend(data.tags)


@run_async
def xtext(bot, update):
    locales.i18n(update).loads.install(True)
    # Filters photo, documents
    if Filters.text(update.message):
        text = update.message.text_html
    else:
        text = update.message.caption_html

    if sage.in_shield(update.message.from_user.id):
        return
    if is_participate_white(bot, update):
        return
    if is_admin(bot, update):
        return

    cache = redis.lrange('xtext_filter', 0, -1)
    if len(cache) == 0:
        xfilter_refresh()
        cache = redis.lrange('xtext_filter', 0, -1)

    extend = extend_links(bot, update, text).result()
    excute = excute_()

    if not extend:
        for rule in cache:
            checker = re.findall(rule.decode(), text)
            if checker:
                query_xtext = mongo.xtext_filter.find_one(
                    {'rule': rule.decode()})
                rule_result = xtext_rules(query_xtext)
                if rule_result.match <= len(checker):
                    try:
                        evidence = update.message.forward(
                            config.getint('log', 'evidence')).message_id
                    except BaseException:
                        evidence = 2
                    else:
                        send_text = f'Sender: {update.message.from_user.mention_html()}\n' +\
                                    f'ID: {update.message.from_user.id}'
                        bot.send_message(
                            config.getint(
                                'log',
                                'evidence'),
                            send_text,
                            reply_to_message_id=send_text.message_id)
                    excute.parse(rule_result)
                else:
                    return False
    else:
        return

    if excute.name == '':
        return

    day = druation(list(dict.fromkeys(excute.tags)))
    tags = list(list(dict.fromkeys(excute.tags)))
    action = to_emoji(list(dict.fromkeys(excute.action)))
    query_group = mongo.group.find_one({'chat.id': update.message.chat.id})

    if query_group:
        group = db_parse.group()
        group.parse(query_group)
        if bool(set(group.config.sub_ban_list).intersection(
                list(to_emoji(tags)))):
            pass
        else:
            return
    else:
        return

    right = False
    if 'delete' in action or tags:
        try:
            update.message.delete()
        except BadRequest as e:
            if e.message == "Message can't be deleted":
                right = True
    if 'restrict' in action:
        try:
            bot.restrict_chat_member(
                update.message.chat.id, update.message.from_user.id)
        except BadRequest as e:
            if e.message == 'Not enough rights to restrict/unrestrict chat member':
                right = True
    if 'alert' in action:
        try:
            pass
        except BadRequest as e:
            text = f'#error #{__name__}\n'
            f'message: {e.message}\n'
            bot.send_message(config.getint('log', 'error'))
    text = _('偵測到 <code>{rule}</code> 規則漢堡罐頭\n'.format(rule=excute.name))
    if right:
        text += _('⚠️權限不足無法操作⚠️\n')
    if excute.tags:
        text += _('依照契約內容已吞噬 Sammer\n')
    text += _('名字：{full_name}\n' +
              'UID：<code>{user_id}</code>\n' +
              '標籤：<code>{tags}</code>').format(
                  full_name=update.message.from_user.mention_html(),
                  user_id=update.message.from_user.id,
                  tags=', '.join(tags)
    )
    if day == 0:
        until = 0
    else:
        until = (datetime.now(taiwan_country) +
                 timedelta(days=day)).timestamp()
    excalibur(
        bot,
        update,
        update.message.from_user.id,
        tags,
        bot.id,
        until=until,
        reason=f'hex auto.{excute.name}',
        evidence=evidence)
    sent = update.message.reply_html(text).result()
    time.sleep(10)
    sent.delete()
    homicide(bot, update, update.message.from_user.id)


# dataset = {'name': 'adx.cc',
#           'rulte': 'qqweqwe',
#           'match': 3,
#           'tags': ['porn', 'ads'],
#           'action': 'delete'}
'''
action
alert, delete, restrict #, ban
'''
