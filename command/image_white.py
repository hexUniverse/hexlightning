import io
from plugin import imagehash
from plugin import db_tools, sage
from telegram.ext.dispatcher import run_async


@run_async
def image_white(bot, update):
    if sage.michael(update.message.from_user.id) or sage.lucifer(update.message.from_user.id):
        mongo = db_tools.use_mongo()
        file = bytes(
            update.message.reply_to_message.photo[-1].get_file().download_as_bytearray())
        bio = io.BytesIO(file)
        i = imagehash.hashing(bio)
        hashing = i.phash()

        update_xmedia = {
            '$set': {'photo.hash': hashing, 'photo.is_white': True, 'photo.indexing': i.indexing()}}
        mongo.xmedia.find_one_and_update(
            {'photo.hash': hashing}, update_xmedia, upsert=True)
        update.message.reply_text('Done')
