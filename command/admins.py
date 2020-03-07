

from telegram.ext import Filters
from telegram import TelegramError

from plugin import config, db_parse, db_tools
from command import info
from inlinekeyboard import quickban
from locales import i18n


def sort_key(elem):
    return elem.user.id


def admins_text(bot, update, args=''):
    i18n(update).loads.install(True)
    if len(args) == 0:
        if Filters.group(update.message):
            mention = '目前群組：\n'
            creator = None  # Creator is not set now
            administrator = list()  # Administrators is not set now

            # Make sure Creator is not in list
            get_admins = bot.get_chat_administrators(
                update.message.chat.id).result()
            for u in get_admins:
                if u.status != 'creator':
                    administrator.append(u)
                else:
                    creator = u  # Set creator

            admins = [creator]  # Make creator in 0
            administrator.sort(key=sort_key)

            for u in administrator:
                admins.append(u)

            for users in admins:
                if users.status == 'creator':
                    mention += _('群主：') + users.user.mention_html() + '\n'
                    continue
                # List Permission
                if users.can_change_info is True:
                    mention += 'ℹ️'
                else:
                    mention += '🌚'
                if users.can_delete_messages is True:
                    mention += '🗑️'
                else:
                    mention += '🌚'
                if users.can_restrict_members is True:
                    mention += '🚫'
                else:
                    mention += '🌚'
                if users.can_pin_messages is True:
                    mention += '📌'
                else:
                    mention += '🌚'
                if users.can_invite_users is True:
                    mention += '🔗'
                else:
                    mention += '🌚'
                if users.can_promote_members is True:
                    mention += '➕'
                else:
                    mention += '🌚'

                mention += users.user.mention_html() + '\n'
            return mention
    elif len(args) == 1:
        if args[0].startswith('https://t.me/'):
            args[0] = args[0].replace('https://t.me/', '@')
        if args[0].startswith('@') or args[0].startswith('-100'):
            try:
                mention = _('群組內的管理員') + args[0] + '\n'
                creator = None
                administrator = list()

                for u in bot.get_chat_administrators(args[0]):
                    if u.status != 'creator':
                        administrator.append(u)
                    else:
                        creator = u

                admins = [creator]
                administrator.sort(key=sort_key)

                for u in administrator:
                    admins.append(u)

                for users in admins:
                    if users.status == 'creator':
                        mention += _('群主：') + users.user.mention_html() + '\n'
                        continue
                    if users.can_change_info is True:
                        mention += 'ℹ️'
                    else:
                        mention += '🌚'
                    if users.can_delete_messages is True:
                        mention += '🗑️'
                    else:
                        mention += '🌚'
                    if users.can_restrict_members is True:
                        mention += '🚫'
                    else:
                        mention += '🌚'
                    if users.can_pin_messages is True:
                        mention += '📌'
                    else:
                        mention += '🌚'
                    if users.can_invite_users is True:
                        mention += '🔗'
                    else:
                        mention += '🌚'
                    if users.can_promote_members is True:
                        mention += '➕'
                    else:
                        mention += '🌚'

                    mention += users.user.mention_html() + '\n'
                return mention
            except TelegramError:
                return '<b>錯誤</b> 檢查輸入的內容'
        else:
            return '傳送 <b>@groupname</b> 或群組 UID.'
    else:
        return '不要停！！嗯嗯 ... 你給太多參數了！恩...'


def admins(bot, update):
    mongo = db_tools.use_mongo()
    query_group = mongo.group.find_one({'chat.id': update.message.chat.id})
    if query_group == []:
        update.message.reply_text(_('請先執行設定，請在群組內發送 <code>!hex config</code>'))
        return
    group = db_parse.group()
    group.parse(query_group)
    if group.config.admin:
        admin_ = admins_text(bot, update)
        update.message.reply_html(admin_)
        if Filters.reply(update.message):
            text = '#report\n' + info(bot, update, gettext=True).result()
            sent = bot.forward_message(
                config.getint(
                    'admin',
                    'elf'),
                update.message.chat.id,
                update.message.reply_to_message.message_id)
            keyboard = quickban(bot, update, sent.message_id)
            bot.send_message(
                config.getint(
                    'admin',
                    'elf'),
                text,
                reply_to_message_id=sent.message_id,
                reply_markup=keyboard,
                parse_mode='html')
