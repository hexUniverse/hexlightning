import time
import logging
import coloredlogs
from html import escape


from telegram.error import BadRequest, _
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


from plugin import config, db_parse, db_tools, gatejieitai
from plugin import banyourwords, checker
from event import guide  # , new_member_check_ban
from locales import i18n

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


def profile_pic(user):
    # 唯唯好嚴格喔~
    return '<code>true</code>' if user.get_profile_photos().total_count > 0 else '<code>false</code>'


@run_async
def new_chat_members(bot, update):
    i18n(update).loads.install(True)
    mongo = db_tools.use_mongo()
    redis = db_tools.use_redis()

    # bot got invite
    if len(
            update.message.new_chat_members) == 1 and update.message.new_chat_members[0].id == bot.id:
        # 處理紀錄
        if update.message.chat.type == 'group':
            update.message.reply_text(_('多比只為住在大房子(supergroup)的主人服務')).result()
            bot.leave_chat(update.message.chat.id)
            return
        from_user = update.message.from_user
        count = bot.get_chat_members_count(update.message.chat.id)
        tmp = '<b>Invited</b>\n' \
            f'Group Name: <code>{escape(update.message.chat.title)}</code> \n' \
            f'Group ID: <code>{update.message.chat.id}</code> \n' \
            f'Group Members Counts: {count}\n\n' \
            f'<b>Invited By</b>\n' \
            f'Name: {from_user.mention_html()}\n' \
            f'Username: @{from_user.username}\n' \
            f'UID: <code>{from_user.id}</code>\n' \
            f'lang_code: <code>{from_user.language_code}</code>'
        if str(from_user.id).encode() in redis.lrange('ban_cache', 0, -1):
            tmp = '<b>已退出></b>\n' + tmp
            bot.send_message(config.getint('log', 'invitelog'),
                             tmp, parse_mode='html')
            bot.leave_chat(update.message.chat.id)
            return

        keyboard = [[
            InlineKeyboardButton(
                '報警', callback_data=f'bot leave {update.message.chat.id}'),  # leave group
            InlineKeyboardButton('舔舔', callback_data=f'bot pass {update.message.chat.id}')]]  # keep in group
        keyboard = InlineKeyboardMarkup(keyboard)
        bot.send_message(config.getint('log', 'invitelog'),
                         tmp, parse_mode='html', reply_markup=keyboard)

        # 安裝指南
        guide(bot, update)

        # 記錄低逼
        group = {
            'chat': {
                'title': f'{update.message.chat.title}',
                'id': update.message.chat.id,
                'config': {
                    'sub_ban_list': ['👶'],
                    'ml_nsfw': False,
                    'lang_code': None,
                    'admins': True
                }
            }
        }
        # 重新邀請會導致group資料洗掉ㄛ
        mongo.group.find_one_and_update(
            {'chat.id': update.message.chat_id},
            {'$set': group},
            upsert=True
        )

    # elif update.message.from_user.id ==
    # update.message.new_chat_members[0].id:
    else:
        '''
        new chat member flow
        - 檢查白名單 & 群組白名單
        - 檢查紀錄
        - 檢查名稱
        - ads, halal name
            - kick, return
        - sent to abyss channel and record
        '''
        # update.message.from_user.id == update.message.new_chat_members[0].id
        for new_member in update.message.new_chat_members:
            border_keeper = gatejieitai(
                bot, update, (update.message.chat.id, new_member.id))
            if border_keeper:
                if border_keeper.current.evidence:
                    evidence = border_keeper.current.evidence
                else:
                    evidence = 2
                text = _('名稱：{fullname}\n'
                         'UID：<code>{user_id}</code>\n'
                         '證據：https://t.me/hexevidence/{evidence}\n'
                         '標籤：<code>{tags}</code>\n').format(
                    fullname=new_member.mention_html(),
                    user_id=new_member.id,
                    evidence=evidence,
                    tags=border_keeper.current.tags_text)
                if border_keeper.current.reason:
                    reason = border_keeper.current.reason
                else:
                    reason = border_keeper.current.tags_text
                if border_keeper.current.until == 0:
                    text += _(banyourwords.forever.format(reason=reason))
                else:
                    text += _(banyourwords.temp.format(reason=reason,
                                                       date=border_keeper.current.date_text))
                text += _(
                    '\n處刑人：<code>{uid}</code>\n'
                    '有任何問題請至 @hexjudge 詢問').format(
                    uid=border_keeper.current.opid)
                try:
                    update.message.delete()
                except BaseException:
                    pass
                try:
                    bot.restrict_chat_member(
                        update.message.chat.id, new_member.id)
                except BadRequest as e:
                    if e.message == 'Not enough rights to restrict/unrestrict chat member':
                        text = _('⚠️為bot正常運作，請給予admin權限⚠️\n') + \
                            text + \
                            _('\n⚠️為bot正常運作，請給予admin權限⚠️')
                        bot.send_message(update.message.chat.id,
                                         text, parse_mode='html')
                else:
                    try:
                        sent = bot.send_message(
                            update.message.chat.id, text, parse_mode='html')
                    except BaseException:
                        pass
                    time.sleep(15)
                    try:
                        bot.kick_chat_member(
                            update.message.chat.id, new_member.id)
                    except BaseException:
                        pass
                    bot.delete_message(update.message.chat.id,
                                       sent.result().message_id)

            else:
                checker(bot, update, new_member)

            from_user = update.message.from_user
            tmp = '<b>New</b>\n' \
                f'Group ID：<code>{update.message.chat_id}</code>\n' \
                f'Group Name：{escape(update.message.chat.title)}\n' \
                f'Group Username：{f"@{update.message.chat.username}" if update.message.chat.username else None}\n' \
                f'Name：{new_member.mention_html()}\n' \
                f'Username：@{new_member.username}\n' \
                f'UID：<code>{new_member.id}</code>\n' \
                f'lang_code：<code>{new_member.language_code}</code>\n' \
                f'Profile Pic：{profile_pic(new_member)}\n' \
                '=======================\n'
            keyboard = [[InlineKeyboardButton('炸他全家', callback_data=f'user bypass {update.message.chat_id}:-{new_member.id}'),  # kick new member
                         InlineKeyboardButton('他還只是個孩子啊', callback_data=f'user bypass {update.message.chat.id}:+{new_member.id}')]]  # keep new member
            if from_user.id != new_member.id:
                tmp += '<b>Invite By</b>\n' \
                    f'Name：{from_user.mention_html()}\n' \
                    f'Username：@{from_user.username}\n' \
                    f'UID：<code>{from_user.id}</code>\n' \
                    f'lang_code：<code>{from_user.language_code}</code>\n' \
                    f'Profile Pic：{profile_pic(from_user)}\n' \
                    '=======================\n'
                keyboard = [[InlineKeyboardButton("掐死被邀人", callback_data=f'user bypass {update.message.chat.id}:+{from_user.id}:-{new_member.id}'),  # kick from_user group
                             InlineKeyboardButton("掐死邀請人", callback_data=f'user bypass {update.message.chat.id}:-{from_user.id}:+{new_member.id}')],  # kick new_member group
                            [InlineKeyboardButton("先放過", callback_data=f'user bypass {update.message.chat.id}:+{from_user.id}:+{new_member.id}'),  # keep both
                             InlineKeyboardButton("殉情", callback_data=f'user bypass {update.message.chat.id}:-{from_user.id}:-{new_member.id}')]]   # kick both]

            # update participate group
            query_participate = mongo.user.find_one({'chat.id': new_member.id})
            part = db_parse.user()
            part.parse(query_participate)
            if part.participate:
                participate = part.participate
                if update.message.chat.id not in participate:
                    participate.append(update.message.chat.id)
            else:
                participate = [update.message.chat_id]

            update_user = {'$set': {
                'chat': {**new_member.to_dict()}}
            }
            update_user['$set']['chat'].update({'participate': participate})
            mongo.user.find_one_and_update({'chat.id': new_member.id},
                                           update_user,
                                           upsert=True)

            keyboard = InlineKeyboardMarkup(keyboard)
            bot.send_message(config.getint('log', 'namecheck'),
                             tmp, parse_mode='html', reply_markup=keyboard)
