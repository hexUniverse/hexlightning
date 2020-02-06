import logging
import coloredlogs
from html import escape

from telegram.error import _
from telegram.ext.dispatcher import run_async

from locales import i18n
from plugin import callabck_parse, emojitags, to_emoji
from plugin import db_parse, db_tools, sage, is_admin

from inlinekeyboard import generate

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def groupconfig_callback(bot, update):
    query = update.callback_query
    i18n(update).loads.install(True)

    mongo = db_tools.use_mongo()
    callback = callabck_parse.callback_parse(query.data)
    query_group = mongo.group.find_one({'chat.id': query.message.chat.id})
    group = db_parse.group()
    group.parse(query_group)
    if sage.lucifer(
        query.from_user.id) or is_admin(
        bot,
        update,
        (query.message.chat.id,
         query.from_user.id)):
        pass
    else:
        text = '你又不是管理員 😘'
        query.answer(text, show_alert=True)
        return

    if group.config is None:
        return

    if callback.qact == 'keyboard' and callback.qdata == 'close':
        text = _('<code>[設定完成]</code>\n\n') + \
            _(f'<code>{escape(query.message.chat.title)}</code>\n') + \
            _('📋 已訂閱黑名單列表：\n')
        emoji_list = emojitags().emoji_dict
        sub = ''
        plugin_ = ''
        for emoji in emoji_list:
            if emoji_list[emoji]['emoji'][0] in group.config.sub_ban_list:
                sub += '{title}\n'.format(
                    title=_(emoji_list[emoji]['title']))
        text += f'<pre>{sub}</pre>'

        for groupconfig_mcro in group.config_list_k:
            if groupconfig_mcro:
                plugin_ += '{title}\n'.format(
                    title=generate.groupconfig_dict(1)[groupconfig_mcro]['title'])
        if plugin_:
            text += _('⚙️ 已啟動附加功能：\n') + f'<pre>{plugin_}</pre>'

        query.edit_message_text(text=text, parse_mode='html')

    elif callback.qact == 'keyboard':
        if callback.qdata == '0':
            text = f'<code>{escape(query.message.chat.title)}</code>\n' + \
                _('📋 訂閱黑名單列表\n') + \
                _('本清單預設開啟 "兒童色情內容" \n') + \
                _('✅ - 開啟訂閱\n') + \
                _('❌ - 關閉訂閱')
            keyboard = generate.inline_groupconfig(bot, update, 0)
            query.edit_message_text(
                text=text, reply_markup=keyboard, parse_mode='html')

        elif callback.qdata == '1':
            text = f'<code>{escape(query.message.chat.title)}</code>\n' + \
                _('⚙️ 附加功能設定\n') + \
                _('✅ - 開啟訂閱\n') + \
                _('❌ - 關閉訂閱')
            keyboard = generate.inline_groupconfig(bot, update, 1)
            query.edit_message_text(
                text=text, reply_markup=keyboard, parse_mode='html')

        elif callback.qdata == '2':
            text = f'<code>{escape(query.message.chat.title)}</code>\n' + \
                '🌐 語言設定/Language Settings\n' + \
                _('✅ - Choosen\n')
            keyboard = generate.inline_groupconfig(bot, update, page=2)
            query.edit_message_text(
                text=text, reply_markup=keyboard, parse_mode='html')

    elif callback.qact == 'sub':
        # group.config.sub_ban_list
        click = to_emoji([callback.qdata])
        sub_total = len(emojitags().emoji_dict.keys()) - 1

        if click not in group.config.sub_ban_list and callback.qdata != 'spam':
            group.config.sub_ban_list.extend(click)
            if sub_total == len(group.config.sub_ban_list):
                group.config.sub_ban_list.append('💩')
            mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {'$set': {
                                            'chat.config.sub_ban_list': group.config.sub_ban_list}})
        elif click in group.config.sub_ban_list and callback.qdata != 'spam':
            group.config.sub_ban_list.remove(click[0])
            if sub_total == len(group.config.sub_ban_list):
                group.config.sub_ban_list.remove('💩')
            mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {'$set': {
                                            'chat.config.sub_ban_list': group.config.sub_ban_list}})

        if callback.qdata == 'spam':
            if sub_total > len(group.config.sub_ban_list):
                group.config.sub_ban_list = to_emoji(
                    list(emojitags().emoji_dict.keys()))
                mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {'$set': {
                    'chat.config.sub_ban_list': list(group.config.sub_ban_list)}})
            else:
                group.config.sub_ban_list = []
                mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {'$set': {
                    'chat.config.sub_ban_list': group.config.sub_ban_list}})

        keyboard = generate.inline_groupconfig(bot, update, 0)
        query.edit_message_reply_markup(reply_markup=keyboard)
        query.answer('Done.')

    elif callback.qact == 'set':
        # group.config.ml_nsfw
        if callback.qdata in group.config_list.keys():
            if group.config_list[callback.qdata]:
                mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {'$set': {
                                                f'chat.config.{callback.qdata}': False}}, upsert=True)
            else:
                mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {'$set': {
                                                f'chat.config.{callback.qdata}': True}}, upsert=True)
        else:
            if callback.qdata == 'all':
                group_config = query_group['chat']['config'].copy()
                for settings in generate.groupconfig_dict(1):
                    group_config[settings] = True
                if group_config == query_group['chat']['config']:
                    query.answer('>:(')
                    return
                mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {'$set': {
                    f'chat.config': group_config}}, upsert=True)
            else:
                mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {'$set': {
                    f'chat.config.{callback.qdata}': True}}, upsert=True)

        keyboard = generate.inline_groupconfig(bot, update, 1)
        try:
            query.edit_message_reply_markup(reply_markup=keyboard)
            query.answer('Done.')
        except Exception as e:
            logger.warning(e)

    elif callback.qact == 'langset':
        mongo.group.find_one_and_update({'chat.id': query.message.chat.id}, {
                                        '$set': {'chat.config.lang_code': callback.qdata}})
        keyboard = generate.inline_groupconfig(bot, update, 2)
        try:
            query.edit_message_reply_markup(reply_markup=keyboard)
            query.answer('Done.')
        except Exception as e:
            logger.warning(e)
