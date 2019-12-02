import re
import time
import logging
import coloredlogs
from html import escape

from locales import i18n
from plugin import db_tools
from plugin.spam_name import checker

from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest


mongo = db_tools.use_mongo()
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def new_member_check_name(bot, update, new_member):
    checker(bot, update)
