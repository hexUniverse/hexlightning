import logging

import telegram
from telegram.ext.dispatcher import run_async


class ping:
    def __init__(self, inherit):
        logger = logging.getLogger(__name__)
        self.logger = inherit.logger

    @run_async
    def pong(self, bot, update):
        update.message.reply_text('pong')
