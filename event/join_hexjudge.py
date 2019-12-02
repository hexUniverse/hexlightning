import logging
import coloredlogs
from telegram.ext import run_async

from command import banstat

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def join_hexjudge(bot, update):
    banstat(bot, update)
