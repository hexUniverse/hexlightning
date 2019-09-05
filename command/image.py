import io
import logging
import coloredlogs
from telegram.ext.dispatcher import run_async
from telegram.ext import Filters

from plugin import is_sage, db_tools, db_parse
from plugin import imagehash, nsfw_detect

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


@run_async
def image(bot, update):
    if is_sage(update.message.from_user.id) != True:
        return
    if Filters.photo(update.message.reply_to_message) != True:
        return
    mongo = db_tools.use_mongo()
    file = bytes(
        update.message.reply_to_message.photo[-1].get_file().download_as_bytearray())
    bio = io.BytesIO(file)
    i = imagehash.hashing(bio)
    hashing = i.phash()
    middle = i.indexing()

    nsfw = nsfw_detect(file)

    query_xmedia = list(mongo.xmedia.find(
        {'photo.indexing': {'$gte': middle-10, '$lte': middle+10}}))
    hash_media = ''
    hash_list = []
    for x in query_xmedia[-5:]:
        media = db_parse.media()
        media.parse(x)
        hash_list.append(media.hash)

    percent = i.plooks_like(hash_list)
    for y in percent:
        hash_media += f'<code>{y.hash}</code> - <code>{y.score}%</code>\n'

    text = f'hash：<code>{i.phash()}</code>\n' \
        f'NSFW Score：<code>{round(nsfw.score, 4)}</code>\n' \
        '==Compare==\n' \
        f'{hash_media}'
    update.message.reply_html(text)
