import gettext

from telegram.ext import Filters

from plugin import db_tools, db_parse


class i8n_tool:
    def __init__(self):
        self.zh_cn = gettext.translation(
            'zh_CN', 'locale', languages=['zh_CN'])
        self.zh_tw = gettext.translation(
            'zh_TW', 'locale', languages=['zh_TW'])
        self.en = gettext.translation('en', 'locale', languages=['en'])

        self.lang = {'zh_tw': self.zh_tw, 'zh-hant': self.zh_tw,
                     'zh_cn': self.zh_cn, 'zh-hans': self.zh_cn,
                     'None': self.en, 'en': self.en}


class i8n(i8n_tool):
    def __init__(self):
        self.mongo = db_tools.use_mongo()

    def install(self, update):

        if Filters.group(update.message):
            self.query = self.mongo.user.find_one(
                {'chat.id': update.message.chat.id})
        else:
            self.query = self.mongo.user.find_one(
                {'chat.id': update.message.from_user.id})

        if self.query:
            user = db_parse.user()
            user.parse(self.query)
            if user.config.lang:
                pass
