from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from locales import i18n


@run_async
def guide(bot, update):
    # install guide
    i18n(update).loads.install(True)
    '''
    安裝指南
    **注意**
    ⚠️這個安裝指引沒有回到上一頁的功能⚠️
    ------
    安裝指南

    給予 bot (ban, delete 權限)
    <a href="" 操作指南 a>
    ------
    安裝指南

    在群內發送 `!hex config` 進行訂閱黑名單。
    ------
    恭喜你安裝完成！
    若有其他問題可到 @hexjudge 內詢問
    以及可以參考說明手冊。
    本訊指引將在 N 秒後自動消失。
    ------
    '''
    tmp = '<code>安裝指南</code>\n' + \
        '**注意**\n' + \
        '⚠️這個安裝指引沒有回到上一頁的功能⚠️\n\n' + \
        '<code>Install Guide</code>\n' + \
        '**ATTENTION**\n' + \
        '⚠️This install guide only show once WITHOUT previous step button⚠️'
    keyboard = [[InlineKeyboardButton(
        'Next ⏭', callback_data=f'guide keyboard 1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(update.message.chat_id, tmp, parse_mode='html',
                     disable_web_page_preview=True, reply_markup=reply_markup)
