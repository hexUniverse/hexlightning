import re
import sys
import time
import logging
from datetime import datetime, timedelta

from dateutil import tz
from pymongo import ReturnDocument

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async
from telegram.error import *


class banstat:
    def __init__(self, inherit):
        logger = logging.getLogger(__name__)
        self.banquery = inherit.banquery
        self.logger = inherit.logger
        self.db = inherit.db
        self.paradise = inherit.paradise

    @run_async
    def check(self, bot, update):
        cmd = update.message.text.split(' ', 1)
        if len(cmd) == 1:
            target = update.message.from_user.id
        else:
            if cmd[1].isdigit():
                target = int(cmd[1])
            else:
                update.message.reply_text('啊...恩...ID..頂...頂到.啊....支氣管了。')
                return
        if update.message.from_user.id in list(set(self.paradise.lucifer+self.paradise.michael)):
            opid = True
        else:
            opid = False
        result = self.banquery.query(self, target, opid)
        if result:
            update.message.reply_text(result, parse_mode='html')
