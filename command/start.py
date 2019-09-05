from telegram.ext.dispatcher import run_async

from locales import i18n


@run_async
def start(bot, update):
    i18n(update).loads.install(True)
    tmp = _('Hi！我是 hexlightning 以下是我的常用指令 \n\n'
            '[群組管理員]\n'
            '!bang - 回覆時使用，將該訊息刪除以及剔除該名成員，並且自動回報給團隊。\n'
            '!hex config - 在群組內發送查看黑名單訂閱狀況。\n\n'
            '[一般成員]\n'
            '/report /spam @admin !admin - 回覆時使用，將訊息回報給團隊。\n'
            '/banstat <uid> - 可回覆時使用，也可單獨使用，查看有無被標記黑名單。\n'
            '/ping - pong，檢察網路狀況。\n'
            '/eula - 僅私訊時可用，查看 hex 使用者條款。\n'
            '/user - 回覆時使用，查看使用者 ID\n'
            '/help - 你知道你正在看嗎？')
    update.message.reply_text(tmp)
