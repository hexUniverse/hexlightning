import io
import logging
import coloredlogs

from telegram.ext.dispatcher import run_async
from telegram.ext import Filters


from plugin import db_tools, db_parse, sage
from plugin import sticker_judge, imagehash
from plugin import druation
from locales import i18n

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
mongo = db_tools.use_mongo()


def banstat_chat(bot, update):
    i18n(update).loads.install(True)

    if Filters.forwarded(update.message.reply_to_message):
        if update.message.reply_to_message.forward_from_chat:
            query = mongo.user.find_one(
                {'chat.id': update.message.reply_to_message.forward_from_chat.id})
            if query:
                user = db_parse.user()
                user.parse(query)
                text = _(f'頻道名稱：<code>{update.message.reply_to_message.forward_from_chat.title}</code>\n') + \
                    _(f'UID：<code>{update.message.reply_to_message.forward_from_chat.id}</code>\n') + \
                    _(f'標籤：{user.current.tags}\n') + \
                    _(f'證據：https://t.me/hexevidence/{user.current.evidence}\n') + \
                    _(f'封鎖日：<code>{user.current.date_text}</code>\n') + \
                    _(f'封鎖到：<code>{user.current.until_text}</code>')
                if sage.is_sage(
                        update.message.from_user.id) or sage.is_sage(
                        update.message.reply_to_message.from_user.id):
                    excuse = mongo.user.find_one(
                        {'chat.id': user.current.opid})
                    execser = db_parse.user()
                    execser.parse(excuse)
                    text = text + \
                        _(f'\n處刑人: <a href="tg://user?id={user.current.opid}">{execser.fullname}</a>')
            else:
                text = _(f'頻道名稱：<code>{update.message.reply_to_message.forward_from_chat.title}</code>\n') + \
                    _(f'UID：<code>{update.message.reply_to_message.forward_from_chat.id}</code>\n') + \
                    _(f'頻道未被封鎖')
            return text
        else:
            if update.message.reply_to_message.forward_from:
                update.message.from_user = update.message.reply_to_message.forward_from
                return banstat_user(bot, update)
            else:
                return _('找不到目標！\n可能來源訊息沒有連結到發送者帳號。')

    else:
        update.message.from_user = update.message.reply_to_message.from_user
        return banstat_user(bot, update)


def banstat_user(bot, update):
    i18n(update).loads.install(True)
    query = mongo.user.find_one({'chat.id': update.message.from_user.id})
    user = db_parse.user()
    user.parse(query)
    if user.current:
        text = _(f'名字：{update.message.from_user.mention_html()}\n') + \
            _(f'UID：<code>{update.message.from_user.id}</code>\n') + \
            _(f'標籤：{user.current.tags}\n') + \
            _(f'證據：https://t.me/hexevidence/{user.current.evidence}\n')
        if user.current.reason:
            text += _(f'說明：<code>{user.current.reason}</code>\n')
        text += _(f'封鎖日：<code>{user.current.date_text}</code>\n') + \
            _(f'封鎖到：<code>{user.current.until_text}</code>\n')
        elfs = update.message.from_user.id
        if update.message.reply_to_message:
            elfs = update.message.reply_to_message.from_user.id
        if sage.is_sage(elfs):
            logger.info(user.current.opid)
            excuse = mongo.user.find_one({'chat.id': user.current.opid})
            execser = db_parse.user()
            execser.parse(excuse)
            text = text + \
                _(f'\n處刑人: {execser.mention_html}')
    elif user.current is None:
        text = _(f'名字：{update.message.from_user.mention_html()}\n') + \
            _(f'UID：<code>{update.message.from_user.id}</code>\n') + \
            _('並未被封鎖')

    if Filters.reply(
            update.message) and Filters.sticker(
            update.message.reply_to_message):
        judge = sticker_judge.checker(
            bot, update, set_name=update.message.reply_to_message.sticker.set_name)
        text_sticker = ''
        if judge:
            query_stiker = mongo.sticker.find_one(
                {'sticker.set_name': update.message.reply_to_message.sticker.set_name})
            sticker = db_parse.sticker()
            sticker.parse(query_stiker)
            text_sticker = _(f'貼圖：<code>{sticker.set_name}</code>\n') + \
                _(f'標籤：<code>{sticker.tags_text}</code>')
            text += f'\n<code>{"="*23}</code>\n' + text_sticker
        else:
            text_sticker = _(
                f'貼圖：<code>{update.message.reply_to_message.sticker.set_name}</code>\n') + _('貼圖並未被封鎖！')
            text += f'\n<code>{"="*23}</code>\n' + text_sticker

    if Filters.reply(
            update.message) and Filters.photo(
            update.message.reply_to_message):
        file = bytes(
            update.message.reply_to_message.photo[-1].get_file().download_as_bytearray())
        bio = io.BytesIO(file)
        i = imagehash.hashing(bio)
        hashing = i.phash()
        query_photo = mongo.xmedia.find_one({'photo.hash': hashing})
        if query_photo:
            media = db_parse.media()
            media.parse(query_photo)
            text_photo = _(f'圖片標記：<code>{media.hash}</code>\n') + \
                _(f'標籤：<code>{media.tags_text}</code>\n') + \
                _(f'天數：<code>{druation(media.tags_list)}</code>')
            if sage.is_sage(
                    update.message.from_user.id) or sage.is_sage(
                    update.message.reply_to_message.from_user.id):
                # add excutor
                execser = db_parse.user()
                excuse = mongo.user.find_one(
                    {'chat.id': media.opid})
                execser.parse(excuse)
                text_photo += _(f'\n處刑人：{execser.mention_html}')

            text += f'\n<code>{"="*23}</code>\n' + text_photo
        else:
            text_photo = _('圖片並未被封鎖！')
            text += f'\n<code>{"="*23}</code>\n' + text_photo
    return text


def banstat_user_args(bot, update, args):
    i18n(update).loads.install(True)
    try:
        uid = int(args[0])
    except ValueError as e:
        logger.warn(e)
        args = ' '.join(args)
        return _(f'<code>{args}</code> 啊...恩...啊...這..好像不是 UID')
    query = mongo.user.find_one({'chat.id': uid})
    text = ''
    if query:
        user = db_parse.user()
        user.parse(query)
        if user.current is None:
            text = _(f'UID：<code>{uid}</code>\n') + \
                _('並未被封鎖')
            return text
        text = ''
        if user.fullname:
            text += _(f'名字：<code>{user.fullname}</code>\n')
        text += _(f'UID：<code>{uid}</code>\n') + _(f'標籤：{user.current.tags}\n') + _(
            f'證據：https://t.me/hexevidence/{"2" if user.current.evidence == None else user.current.evidence}\n')
        if user.current.reason:
            text += _(f'說明：<code>{user.current.reason}</code>\n')
        text += _(f'封鎖日：<code>{user.current.date_text}</code>\n') + \
            _(f'封鎖到：<code>{user.current.until_text}</code>\n')
        if sage.is_sage(update.message.from_user.id):
            execser = db_parse.user()
            excuse = mongo.user.find_one(
                {'chat.id': user.current.opid})
            execser.parse(excuse)
            text = text + \
                _(f'\n處刑人：{execser.mention_html}')
        return text
    else:
        text = _(f'UID：<code>{uid}</code>\n') + \
            _('並未被封鎖')
        return text


@run_async
def banstat(bot, update, args=None):
    i18n(update).loads.install(True)
    if args:
        text = banstat_user_args(bot, update, args)
        update.message.reply_text(text, parse_mode='html')

    elif Filters.reply(update.message) != True:
        text = banstat_user(bot, update)
        update.message.reply_text(text, parse_mode='html')

    elif Filters.reply(update.message):
        text = banstat_chat(bot, update)
        update.message.reply_text(text, parse_mode='html')
