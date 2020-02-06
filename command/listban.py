import time
import logging
from html import escape
from datetime import datetime, timedelta

from munch import Munch
from dateutil import tz
from parse import search

import telegram
from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest, Unauthorized


class bang:
    def __init__(self, inherit):
        logger = logging.getLogger(__name__)
        self.logger = inherit.logger
        self.db = inherit.db
        self.config = inherit.config
        self.paradise = inherit.paradise
        self.emojitags = inherit.emojitags
        self.tags = self.emojitags.emoji_dict.keys()
        self.taiwan_is_an_independence_country = inherit.taiwan_is_an_independence_country

        # cache list
        self.ban_cache = inherit.ban_cache
        self.white_cache = inherit.white_cache
        self.group_whitelist = inherit.group_whitelist

    @run_async
    def boom(self, bot, update, uid):
        '''
        kick user from all off chat.participate
        '''
        query_user = self.db.user.find_one({'chat.id': uid})
        ban = Munch(query_user['current'])

        if 'evidence' not in ban.keys():
            ban['evidence'] = 2
        if 'reason' not in ban.keys():
            reason = self.emojitags.to_string(ban.tags)
        if 'reason' in ban.keys():
            reason = ban.reason
        if 'first_name' in query_user['chat'].keys():
            name = f'Name: <code>{query_user["chat"]["first_name"]}</code>'
        else:
            name = ''
        tags_str = self.emojitags.to_string(ban.tags)
        text = f'{name}\n' \
            f'UID: <code>{uid}</code>\n' \
            f'證據: https://t.me/{self.config.get("log", "evidence_url")}/{ban.evidence}\n' \
            f'tag: <code>{tags_str}</code>\n'
        if ban.until:
            readble = datetime.fromtimestamp(int(ban.until)).astimezone(
                self.taiwan_is_an_independence_country)
            text += f'因為 <code>{reason}</code> \n封禁至 <code>{readble}</code>'
        else:
            text += f'因為 <code>{reason}</code> 而被惠惠當作練習目標，被 <code>EXPLOSION</code> 至永不超生。\n '
        # 名單沒有任何群組。
        if 'participate' not in query_user['chat']:
            self.logger.debug('not thing in the chat.participate')
        # find in chat.participate
        else:
            participate = query_user['chat']['participate']
            for chat_id in participate:
                # check white group list
                if str(chat_id) in self.group_whitelist.keys():
                    if uid in self.group_whitelist[str(chat_id)]:
                        return
                query_group = self.db.group.find_one({
                    '$and': [
                        {'chat.id': int(chat_id)},
                        {'chat.config.sub_ban_list': {'$exists': True}}
                    ]})
                if query_group:
                    trigger = False
                    group_result = query_group['chat']['config']['sub_ban_list']
                    # for 群組 sub ban list 看有沒有在 user.current 裡面
                    for x in group_result:
                        if x in ban.tags:
                            trigger = True
                            break
                    if trigger == False:
                        return
                # 開工ㄌ。
                try:
                    bot.kick_chat_member(chat_id, uid, until_date=ban.until)
                    # 拔掉 chat.participate
                    self.db.user.find_one_and_update(
                        {'chat.id': uid},
                        {'$pull': {'chat.participate': chat_id},
                         '$push': {'chat.banned_participate': chat_id}},
                        upsert=True
                    )
                except (BadRequest, Unauthorized) as e:
                    if e.message == 'User is an administrator of the chat':
                        pass
                    elif e.message == 'Not enough rights to restrict/unrestrict chat member':
                        tmp_text = text+'因權限不足，而無法從本群組踢飛。'
                        #bot.send_message(chat_id, tmp_text, parse_mode='html', disable_web_page_preview=True)
                    elif e.message == 'Forbidden: bot is not a member of the supergroup chat':
                        self.db.group.find_one_and_delete(
                            {'chat.id': update.message.chat_id}
                        )
                        return

                finally:
                    tmp_text = text + \
                        f'\n{"="*23}\n處刑人：<code>{ban.opid}</code>\n有任何問題請至 @hexjudge 詢問'
                    try:
                        sent = bot.send_message(
                            chat_id, tmp_text, parse_mode='html', disable_web_page_preview=True)
                        time.sleep(10)
                        bot.delete_message(chat_id, sent.result().message_id)
                    except:
                        pass

    @run_async
    def listban(self, bot, update):
        day = search('ban={:d}d', update.message.text)
        reason = search('r={:S}', update.message.text)
        tag = search('t={:S}', update.message.text)
        list_uid = search('u={:S}', update.message.text)

        bang_uid_list = []
        if list_uid == None or tag == None:
            update.message.reply_text('缺少必要參數。')
            return
        # prevent injection
        if reason:
            reason = escape(reason[0])
            if len(reason) > telegram.constants.MAX_MESSAGE_LENGTH:
                update.message.reply_text('啊...恩...理由..頂...頂到.啊....支氣管了。')
                return
        tmp_tag = ['spam']
        for tag_split in tag[0].split(','):
            if tag_split not in self.tags:
                update.message.reply_text(
                    f'找不到相符的 tags，限用文字。\n<code>Error Code: 767 {tag_split}</code>', parse_mode='html')
                return
            tmp_tag.append(tag_split)
        tags_emoji = self.emojitags.to_emoji(tmp_tag)
        tags_str = self.emojitags.to_string(tags_emoji)

        # check uid 合乎規範。
        for ex_uid in list_uid[0].split(','):
            try:
                bang_uid_list.append(int(ex_uid))
            except ValueError:
                update.message.reply_text(
                    f'你 (´眼ω幹`) ? \n<code>{ex_uid}</code>', parse_mode='html')
                return
            else:
                if ex_uid == bot.id:
                    update.message.reply_text(f'你檢查一下不要自攻自受R XDDDD\n{ex_uid}')
                    return
                elif ex_uid in list(set(self.paradise.lucifer+self.paradise.michael)):
                    update.message.reply_text(f'連對方是天使都想濫掉(？▽？)\n{ex_uid}')
                    return
                elif ex_uid in self.white_cache:
                    update.message.reply_text(f'他有白天使護體\n{ex_uid}')
                    return

        # 非重複處理
        if reason == None:
            reason = tags_str
        if day:
            if day[0] > 365:
                update.message.reply_text(f'WAT ARE YOU DOING??\n{day[0]}')
                return
            until = int((datetime.now().astimezone(
                tz.gettz('UTC')) + timedelta(days=day[0])).timestamp())
            readble = datetime.fromtimestamp(int(until)).astimezone(
                self.taiwan_is_an_independence_country)
            druation = f'因為 <code>{reason}</code> \n封禁至 <code>{readble}</code>'
        else:
            until = 0
            druation = f'因為 <code>{reason}</code> 而被惠惠當作練習目標，被 <code>EXPLOSION</code> 至永不超生。 '
        for uid in bang_uid_list:
            try:
                query = self.db.user.find_one({'chat.id': uid})
            except:
                update.message.reply_text(f'你提供的uid頂到肺了。{uid}')
                return
            # db something
            query_update = {
                '$set': {
                    'current': {
                        'date': int(datetime.now().astimezone(tz.gettz('UTC')).timestamp()),
                        'opid': update.message.from_user.id,
                        'until': until,
                        'reason': reason,
                        'tags': tags_emoji
                    }
                }
            }
            if query == None:
                pass
            elif 'current' in query.keys() and 'history' in query.keys():
                query_update['$push'] = {'history': query['current']}
            elif 'current' in query.keys() and 'history' not in query.keys():
                query_update['$addToSet'] = {'history': query['current']}

            self.db.user.find_one_and_update(
                {'chat.id': uid},
                query_update,
                upsert=True
            )

        text = f'UID: <code>{", ".join(str(e) for e in bang_uid_list)}</code>\n' \
            f'tag: <code>{tags_str}</code>\n' \
            f'{druation}\n'
        if len(text) >= telegram.constants.MAX_MESSAGE_LENGTH:
            text = 'UID: <code>太多ㄌ</code>\n' \
                f'tag: <code>{tags_str}</code>\n' \
                f'{druation}\n'
            update.message.reply_text(text, parse_mode='html')
        else:
            update.message.reply_text(text, parse_mode='html')
        # boom all user participate chat
        self.boom(bot, update, uid)
        # update ban cache
        return bang_uid_list
