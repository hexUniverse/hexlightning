
import locales
import time
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async

from plugin import config
from plugin import db_parse, db_tools, to_emoji
from plugin.spam_name import _, ad82cc, dexcoin_spam, halal, mdfk_ads, porn_1861, qqspam, scam, testnet
from plugin.excalibur import excalibur
checker_list = [dexcoin_spam, mdfk_ads,
                porn_1861, qqspam, scam, testnet, halal, ad82cc]


@run_async
def checker(bot, update, new_member):
    # halal 合併 /name
    # i18n(update).loads.install(True)
    locales.i18n(update).loads.install(True)
    mongo = db_tools.use_mongo()
    user = db_parse.user()
    group = db_parse.group()
    query_user = mongo.user.find_one({'chat.id': new_member.id})
    query_group = mongo.group.find_one({'chat.id': update.message.chat.id})
    user.parse(query_user)
    group.parse(query_group)
    for check in checker_list:
        do_check = check()
        # return (True, 'QQ_Spam', result)
        checker_result, checker_name, checker_match = do_check.detect(
            new_member.full_name.lower())
        # print(do_check.detect(new_member.full_name.lower()))
        if group.config is None:
            # 無心市政
            # 城市不築 敗事有瑜
            return

        tags_result = bool(
            set(group.config.sub_ban_list).intersection(to_emoji(do_check.tags)))

        if checker_result and tags_result:
            # halal 先上標籤啦
            if checker_name in ['halal_arabic', 'halal_cyrillic']:
                excalibur(bot, update, new_member.id, tags=['halal'],
                          opid=bot.id, reason='花瓜 呱呱呱')

            try:
                update.message.delete()
            except BaseException:
                pass
            try:
                bot.restrict_chat_member(
                    update.message.chat_id,
                    new_member.id,
                    until_date=None,
                    can_send_messages=None,
                    can_send_media_messages=None,
                    can_send_other_messages=None)
            except BadRequest:
                text = _('海克斯希貝兒先知系統偵測到一個<code>心靈指數過高用戶</code>，請給予相應權限作出處理。\n') + \
                    _(f'名稱：{new_member.mention_html()}\n') + \
                    _(f'UID：<code>{new_member.id}</code>\n') + \
                    _(f'偵查：<code>{checker_name}</code>')
                update.message.reply_text(text, parse_mode='html')
                break
            else:
                '''
                Name: 虎虎
                UID: 123123
                因為 {checker name} 導致 心靈指數 指數過高，主宰者 切換至 摧毀分解 模式。
                若有誤判請至 @hexjudge 報告 希貝兒先知系統 存在問題
                案件追蹤 ID：update_id
                '''
                record_msg = f'Name：{new_member.mention_html()}\n' \
                    f'UID：<code>{new_member.id}</code>\n' \
                    f'Checker：{checker_name}\n' \
                    f'Group Name：<code>{update.message.chat.title}</code>\n' \
                    f'Group ID：<code>{update.message.chat.id}</code>\n' \
                    f'Group Username：{"@{update.message.chat.username}" if update.message.chat.username else None}\n' \
                    f'#{checker_name} #tracker_{update.update_id}'
                bot.send_message(config.getint('log', 'abyss'),
                                 record_msg, parse_mode='html')

                tmp = _(f'名稱：{new_member.mention_html()}\n') + \
                    _(f'UID：<code>{new_member.id}</code>\n') + \
                    _(f'因為 <code>{checker_name}</code> 導致<code>心靈指數</code>過高，<code>主宰者</code>切換至摧毀分解模式。\n') + \
                    _(f'若有誤判請至 @hexjudge 報告海克斯希貝兒先知系統存在問題\n') + \
                    _(f'案件追蹤：#tracker_{update.update_id}')
                warn_msg = update.message.reply_text(tmp, parse_mode='html')
                time.sleep(10)
                bot.kick_chat_member(update.message.chat_id, new_member.id)
                try:
                    bot.delete_message(update.message.chat_id,
                                       warn_msg.result().message_id)
                except BadRequest:
                    pass

            return True
    return False
