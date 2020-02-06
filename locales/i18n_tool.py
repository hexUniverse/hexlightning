import gettext


from plugin import db_tools, db_parse


class i18n_tool:
    def __init__(self):
        self.zh_cn = None
        self.en = None
        try:
            self.zh_cn = gettext.translation(
                'zh_CN', 'locales', languages=['zh_CN'])
        except FileNotFoundError:
            pass
        self.zh_tw = gettext.translation(
            'zh_TW', 'locales', languages=['zh_TW'])
        self.en = gettext.translation('en', 'locales', languages=['en'])

        self.lang = {
            'zh_tw': self.zh_tw,
            'zh-hant': self.zh_tw,
            'zh_cn': self.zh_cn,
            'zh-hans': self.zh_cn,
            'None': self.en,
            'en': self.en}


class i18n(i18n_tool):
    def __init__(self, update):
        self.mongo = db_tools.use_mongo()
        self.update = update
        self.lang = i18n_tool().lang
        self.loads = self.loads_()

    def loads_(self):

        # if Filters.group(self.update.message):
        #    self.query = self.mongo.user.find_one(
        #        {'chat.id': self.update.message.chat.id})
        # else:
        self.query = self.mongo.user.find_one(
            {'chat.id': self.update.message.from_user.id})

        # if self.query:
        user = db_parse.user()
        user.parse(self.query)
        if user.config.lang:
            # print(user.config.lang)
            if user.config.lang.lower() in self.lang.keys():
                return self.lang[user.config.lang]  # .install(True)
            else:
                print(self.lang.keys())
                print('not in ')

            # self.lang[user.lang_code].install(True)
