import logging
import coloredlogs

from plugin import db_tools
from plugin.spam_name import checker

from telegram.ext.dispatcher import run_async


mongo = db_tools.use_mongo()
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def new_member_check_name(bot, update, new_member):
    checker(bot, update, new_member)
