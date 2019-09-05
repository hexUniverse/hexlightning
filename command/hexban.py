import io
import time
import logging
import coloredlogs

from parse import search

from dateutil import tz
from datetime import datetime, timedelta

from telegram.ext.dispatcher import run_async
from telegram.ext import Filters

from plugin import db_parse, db_tools, config, homicide, excalibur, imagehash
from plugin import sage, banyourwords, sticker_judge
from plugin import to_emoji, to_list, to_string, druation, emojitags
from locales import i18n
#import pysnooper
taiwan_country = tz.gettz('Asia/Taipei')
mongo = db_tools.use_mongo()
redis = db_tools.use_redis()

@run_async
def hexban_reply(bot, update):
    '''
    !hex ban ads,scam
    !hex ban u=123 t=scam r=ㄏㄏ
    '''
    i18n(update).loads.install(True)
    if sage.is_sage(update.message.from_user.id) == False:
        try:
            update.message.delete()
        except:
            return
        sent = update.message.reply_text('騷年，你渴望力量ㄇ？').result()
        time.sleep(5)
        sent.delete()
    if sage.elf(update.message.from_user.id):
        update.message.reply_text(_('等級不夠 🌚'))
        return
    args = update.message.text.split()
    if len(args) == 3:
        # !hex ban ads,scam
        tags = args[2].split(',')
        for tag in tags:
            if tag not in emojitags().emoji_dict.keys():
                text = _(f'找不到 <code>{tag}</code> 標籤')
                update.message.reply_html(text)
                return
        if 'spam' not in tags:
            tags.append('spam')

        day = druation(tags)
        now = datetime.now(taiwan_country)
        if day == 0:
            until = 0
        else:
            until = int((now + timedelta(days=day)).timestamp())
        tags_text = ', '.join(tags)
        opid = update.message.from_user.id

        bang = []
        if sage.in_shield(update.message.reply_to_message.from_user.id) == False:
            bang = [update.message.reply_to_message.from_user]
        if update.message.reply_to_message.forward_from:
            if sage.in_shield(update.message.reply_to_message.forward_from.id) == False:
                bang.append(update.message.reply_to_message.forward_from)
        if update.message.reply_to_message.forward_from_chat:
            if sage.in_shield(update.message.reply_to_message.forward_from_chat.id) == False:
                bang.append(update.message.reply_to_message.forward_from_chat)
        if bang:
            try:
                sent = bot.forward_message(config.getint('log', 'evidence'), update.message.reply_to_message.chat.id,
                                           update.message.reply_to_message.message_id)
            except:
                sent = None
            if sent:
                evidence = sent.message_id
            else:
                evidence = 2
        else:
            text = ''
            if sage.in_shield(update.message.reply_to_message.from_user.id):
                if sage.is_sage(update.message.reply_to_message.from_user.id):
                    text += _(f'<code>{update.message.reply_to_message.from_user.id}</code> 有精靈保護 🌚')
                else:
                    text += _(
                        f'<code>{update.message.reply_to_message.from_user.id}</code> 白色恐怖快逃R 🌚')
            if update.message.reply_to_message.forward_from:
                if sage.in_shield(update.message.reply_to_message.forward_from.id):
                    if sage.is_sage(update.message.reply_to_message.forward_from.id):
                        text += _(
                            f'<code>{update.message.reply_to_message.forward_from.id}</code> 有精靈保護 🌚')
                    else:
                        text += _(
                            f'<code>{update.message.reply_to_message.from_user.id}</code> 白色恐怖快逃R 🌚')
            if update.message.reply_to_message.forward_from_chat:
                if sage.in_shield(update.message.reply_to_message.forward_from_chat.id):
                    if sage.is_sage(update.message.reply_to_message.forward_from_chat.id):
                        text += _(
                            f'<code>{update.message.reply_to_message.forward_from_chat.id}</code> 有精靈保護 🌚')
                    else:
                        text += _(
                            f'<code>{update.message.reply_to_message.from_user.id}</code> 白色恐怖快逃R 🌚')
            update.message.reply_html(text)
            return

        if Filters.sticker(update.message.reply_to_message):
            if update.message.reply_to_message.sticker.set_name:
                update_sticker = {'$set':{'sticker': {'set_name': update.message.reply_to_message.sticker.set_name, 'tags':tags},'opid': update.message.from_user.id,'reason': tags_text, 'evidence': evidence}}
                mongo.sticker.find_one_and_update({'sticker.id': update.message.reply_to_message.sticker.file_id}, update_sticker, upsert=True)
                text = f'ID：<code>{update.message.reply_to_message.sticker.file_id}</code>\n'
                if update.message.reply_to_message.sticker.set_name:
                    # https://t.me/addstickers/nichijou
                    text += f'Set Name：https://t.me/addstickers/{update.message.reply_to_message.sticker.set_name}\n'
                text += _(f'標籤：<code>{tags_text}</code>')
                update.message.reply_html(text)
                sticker_judge.refresh()
        if Filters.photo(update.message.reply_to_message):
            file = bytes(update.message.reply_to_message.photo[-1].get_file().download_as_bytearray())
            bio = io.BytesIO(file)
            #hashing = str(imagehash.phash(bio))
            i = imagehash.hashing(bio)
            hashing = i.phash()
            
            query_photo = mongo.xmedia.find_one({'photo.hash': hashing})
            if query_photo:
                pass
            else:
                tmp_dict = {'photo':
                                {'hash': hashing,
                                'tags': to_emoji(tags),
                                'indexing': i.indexing()},
                            'evidence': evidence,
                            'opid': update.message.from_user.id,
                            'reason': tags_text}
                mongo.xmedia.insert_one(tmp_dict)
                text = f'hash：<code>{hashing}</code>\n' + \
                        _(f'標籤：<code>{tags_text}</code>\n') + \
                        _(f'標記：<code>{i.indexing()}</code>')
                update.message.reply_html(text)
                redis.lpush('photo_cache', hashing)

        for chat in bang:
            text = excalibur(bot, update, uid=chat.id, tags=tags, opid=opid,
                             until=until, reason=tags_text, user=chat, evidence=evidence)
            update.message.reply_html(text, web_page_preview=False)
            update_user = {'$set': {'chat': chat.to_dict()}}
            mongo.user.find_one_and_update({'chat.id': chat.id}, update_user)
            homicide(bot, update, chat.id)

    # !hex ban t=ads r=臭
    elif len(args) >= 4:
        day = search('ban={:d}d', update.message.text)
        reason = search('r={:S}', update.message.text)
        tags = search('t={:S}', update.message.text)
        uid = search('u={:d}', update.message.text)
        now = datetime.now(taiwan_country)

        if tags == None:
            text = f'缺少標籤參數。'
            update.message.reply_html(text)
            return
        else:
            tags = tags[0].split(',')
            if 'spam' not in tags:
                tags.append('spam')
        for tag in tags:
            if tag not in emojitags().emoji_dict.keys():
                text = f'找不到 <code>{tag}</code> 標籤'
                update.message.reply_html(text)
                return

        if day:
            if day[0] == 0:
                until = 0
            else:
                until = int((now + timedelta(days=day[0])).timestamp())
        else:
            day_ = druation(tags)
            if day_ == 0:
                until = 0
            else:
                until = int((now + timedelta(days=day_)).timestamp())
        tags_text = ', '.join(tags)

        opid = update.message.from_user.id
        if reason:
            reason = reason[0]
        else:
            reason = tags_text

        if uid:
            uid = uid[0]
            try:
                sent = bot.forward_message(config.getint('log', 'evidence'), update.message.reply_to_message.chat.id,
                                           update.message.reply_to_message.message_id)
            except:
                sent = None
            if sent:
                evidence = sent.message_id
            else:
                evidence = 2

            text = excalibur(bot, update, uid=uid, tags=tags,
                             opid=opid, until=until, reason=reason, evidence=evidence)

            update.message.reply_html(text)
            return

        if sage.in_shield(update.message.reply_to_message.from_user.id):
            bang = []
        else:
            bang = [update.message.reply_to_message.from_user]
        if update.message.reply_to_message.forward_from:
            if sage.in_shield(update.message.reply_to_message.forward_from.id) == False:
                bang.append(update.message.reply_to_message.forward_from)
        if update.message.reply_to_message.forward_from_chat:
            if sage.in_shield(update.message.reply_to_message.forward_from_chat.id) == False:
                bang.append(update.message.reply_to_message.forward_from_chat)

        if bang:
            try:
                sent = bot.forward_message(config.getint('log', 'evidence'), update.message.reply_to_message.chat.id,
                                           update.message.reply_to_message.message_id)
            except:
                sent = None
            if sent:
                evidence = sent.message_id
            else:
                evidence = 2
        else:
            text = ''
            if update.message.reply_to_message.forward_from:
                if sage.is_sage(update.message.reply_to_message.forward_from.id):
                    text += f'<code>{update.message.reply_to_message.forward_from.id}</code> 有精靈護體 🌚'
                else:
                    text += f'<code>{update.message.reply_to_message.forward_from.id}</code> 白色恐怖快逃RRR 🌝'

            if update.message.reply_to_message.forward_from_chat:
                if sage.is_sage(update.message.reply_to_message.forward_from_chat):
                    text += f'<code>{update.message.reply_to_message.forward_from_chat.id}</code> 有精靈護體 🌚'
                else:
                    text += f'<code>{update.message.reply_to_message.forward_from_chat.id}</code> 白色恐怖快逃RRR 🌝'
            update.message.reply_html(text)
            

        if Filters.sticker(update.message.reply_to_message):
            if update.message.reply_to_message.sticker.set_name:
                update_sticker = {'$set':{'sticker': {'set_name': update.message.reply_to_message.sticker.set_name, 'tags':tags},'opid': update.message.from_user.id,'reason': tags_text, 'evidence': evidence}}
                mongo.sticker.find_one_and_update({'sticker.id': update.message.reply_to_message.sticker.file_id}, update_sticker, upsert=True)
                text = f'ID：<code>{update.message.reply_to_message.sticker.file_id}</code>\n'
                if update.message.reply_to_message.sticker.set_name:
                    # https://t.me/addstickers/nichijou
                    text += f'Set Name：https://t.me/addstickers/{update.message.reply_to_message.sticker.set_name}\n'
                text += _(f'標籤：<code>{tags_text}</code>')
                update.message.reply_html(text)
                sticker_judge.refresh()
        for chat in bang:
            update_user = {'$set': {'chat': chat.to_dict()}}
            mongo.user.find_one_and_update({'chat.id': chat.id}, update_user)
            text = excalibur(bot, update, uid=chat.id, opid=opid,
                             until=until, reason=reason, tags=tags, user=chat, evidence=evidence)
            update.message.reply_html(text, web_page_preview=False)


def hexban_long(bot, update):
    i18n(update).loads.install(True)
    if sage.is_sage(update.message.from_user.id) == False:
        try:
            update.message.delete()
        except:
            return
        sent = update.message.reply_text('騷年，你渴望力量ㄇ？').result()
        time.sleep(5)
        sent.delete()
        return
    if sage.elf(update.message.from_user.id):
        update.message.reply_text(_('等級不夠 🌚'))
        return
    # !hex ban u=123 t=spam

    day = search('ban={:d}d', update.message.text)
    reason = search('r={:S}', update.message.text)
    tags = search('t={:S}', update.message.text)
    uid = search('u={:d}', update.message.text)
    now = datetime.now(taiwan_country)

    if tags == None:
        update.message.reply_html(_('缺少 <code>標籤</code> 參數。'))
        return
    elif uid == None:
        update.message.reply_html(_('缺少 <code>UID</code> 參數。'))
        return

    if uid:
        uid = uid[0]
    if tags:
        tags = tags[0].split(',')
        if 'spam' not in tags:
            tags.append('spam')
        for tag in tags:
            if tag not in emojitags().emoji_dict.keys():
                text = _(f'找不到 <code>{tag}</code> 標籤')
                update.message.reply_html(text)
                return
    if day:
        if day[0] == 0:
            until = 0
        else:
            until = int((now + timedelta(days=day[0])).timestamp())
    else:
        day_ = druation(tags)
        if day_ == 0:
            until = 0
        else:
            until = int((now + timedelta(days=day_)).timestamp())

    if sage.in_shield(uid):
        if sage.is_sage(uid):
            text = '精靈保護 🌚'
        else:
            text = '白色恐怖ㄉ力量 🌝'
        update.message.reply_text(text)
        return

    until_text = datetime.fromtimestamp(until).astimezone(taiwan_country)
    opid = update.message.from_user.id

    tags_text = ', '.join(tags)

    evidence = 2
    opid = update.message.from_user.id
    if reason:
        reason = reason[0]
    else:
        reason = tags_text
    query_user = mongo.user.find_one({'chat.id': uid})

    excalibur(bot, update, uid=uid, tags=tags,
              opid=opid, until=until, reason=reason)

    text = ''
    if query_user:
        user = db_parse.user()
        user.parse(query_user)
        if user.fullname:
            if user.id < 0:
                text += _(f'頻道：<code>{user.fullname}</code>\n')
            else:
                text += _(f'名字：<code>{user.fullname}</code>\n')
    text += _(f'UID：<code>{uid}</code>\n') + \
        _(f'標籤：<code>{tags_text}</code>\n') + \
        _(f'證據：https://t.me/hexevidence/{evidence}\n')
    if until == 0:
        text += _(banyourwords.forever.format(reason=reason))
    else:
        text += _(banyourwords.temp.format(reason=reason, date=until_text))

    update.message.reply_html(text, web_page_preview=False)
