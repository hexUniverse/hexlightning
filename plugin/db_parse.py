import json
import logging
import coloredlogs
from html import escape
from dateutil import tz
from datetime import datetime, timedelta

from plugin.emojitags import to_string, to_list, to_emoji, druation

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


class user:
    def __init__(self):
        self.id = None
        self.first_name = None
        self.last_name = None
        # f'{self.first_name}{self.last_name}' if self.first_name else self.first_name
        self.fullname = None
        self.mention_html = None
        self.username = None
        self.is_bot = None
        self.language_code = None
        self.is_white = None
        self.participate = None
        self.banned_participate = None
        self.current = None
        self.config = None
        self.history = None

    def parse(self, data):
        if data == None:
            return None
        self.parse_data = data
        user = data['chat']
        if 'config' in data.keys():
            self.config = self.config_(data['config'])
        if 'current' in data.keys():
            if 'date' in data['current']:
                self.current = self.current_(data['current'])
                self.current_raw = data['current']

        self.raw = data  # hmmm confused.
        self.id = user['id']
        # first_name: require
        # last_name: optional
        if 'first_name' in user.keys():
            self.first_name = user['first_name']
        if 'last_name' in user.keys():
            self.last_name = user['last_name']

        if self.first_name:
            self.fullname = self.first_name
            if self.last_name:
                self.fullname += f' {self.last_name}'
        if self.fullname:
            self.mention_html = f'<a href="tg://user?id={self.id}">{escape(self.fullname)}</a>'
        if 'username' in user.keys():
            self.username = user['username']
        if 'is_bot' in user.keys():
            self.is_bot = user['is_bot']
        if 'language_code' in user.keys():
            self.language_code = user['language_code']
        if 'is_white' in user.keys():
            self.is_white = user['is_white']
        if 'participate' in user.keys():
            self.participate = user['participate']
        if 'banned_participate' in user.keys():
            self.banned_participate = user['banned_participate']
        if 'history' in user.keys():
            self.history = user['history']
        if 'current' in user.keys():
            self.current = user['current']

        # if 'config_lang' in user.keys():
        #    self.config_lang = user['config_lang']

    class config_:
        def __init__(self, data):
            self.data = data
            self.lang_code = None
            self.parse()

        def parse(self):
            if 'lang' in self.data.keys():
                self.lang_code = self.data['lang']

    class current_:
        def __init__(self, data):
            self.data = data
            self.date = None
            self.until = None
            self.until_date = None
            self.opid = None
            self.reason = None
            self.tags = None
            self.evidence = None
            self.inherit = None
            self.parse()

        def parse(self):
            self.date = self.data['date']
            self.date_text = datetime.fromtimestamp(
                int(self.data['date'])).astimezone(tz.gettz("Asia/Taipei"))
            self.opid = self.data['opid']
            self.reason = self.data['reason']
            self.tags = self.data['tags']
            self.tags_list = list(self.data['tags'])
            self.tags_text = to_string(self.data['tags'])
            self.until = self.data['until']
            self.until_text = datetime.fromtimestamp(
                int(self.data['until'])).astimezone(tz.gettz("Asia/Taipei"))
            self.until_date = datetime.fromtimestamp(self.data['until'])

            if 'evidence' in self.data.keys():
                self.evidence = self.data['evidence']
            if 'inherit' in self.data.keys():
                self.inherit = self.inherit_(self.data['inherit'])

        class inherit_:
            def __init__(self, data):
                self.data = data
                self.id = None
                self.chat = None
                self.evidence = None
                self.parse()

            def parse(self):
                if 'id' in self.data.keys():
                    self.id = self.data['id']
                if 'chat' in self.data.keys():
                    self.chat = self.chat_(self.data['chat'])
                    # self.inherit = self.inherit_(self.data['inherit'])
                    #self.chat = self.data['chat']
                if 'evidence' in self.data.keys():
                    self.evidence = self.data['evidence']

            class chat_:
                def __init__(self, data):
                    self.data = data
                    self.id = None
                    self.title = None
                    self.parse()

                def parse(self):
                    if 'id' in self.data.keys():
                        self.id = self.data['id']


class group:
    def __init__(self):
        self.title = None
        self.id = None
        self.white_participate = None
        # self.config = self.config_()
        self.config = None
        self.config_list = {}
        self.config_list_k = {}

    def parse(self, data):
        if data == None:
            return None
        chat = data['chat']
        if 'config' in chat.keys():
            self.config = self.config_(chat['config'])

            for content in chat['config']:
                self.config_list[content] = chat['config'][content]
                # self.config_list.append(content)
                if content not in ['lang_code', 'configuring', 'sub_ban_list', 'all']:
                    self.config_list_k[content] = chat['config'][content]

        if 'title' in chat.keys():
            self.title = chat['title']
        if 'id' in chat.keys():
            self.id = chat['id']
        if 'white_participate' in chat.keys():
            if chat['white_participate']:
                self.white_participate = chat['white_participate']

    class config_:
        def __init__(self, config_data):
            self.data = config_data
            self.sub_ban_list = None
            self.configuring = None
            self.admin = None
            self.ml_nsfw = None
            self.lang_code = None

            self.parse()

        def parse(self):
            if 'sub_ban_list' in self.data.keys():
                self.sub_ban_list = self.data['sub_ban_list']
                self.sub_ban_list_text = to_list(self.sub_ban_list)
            if 'configuring' in self.data.keys():
                self.configuring = self.data['configuring']
            if 'ml_nsfw' in self.data.keys():
                self.ml_nsfw = self.data['ml_nsfw']
            if 'lang_code' in self.data.keys():
                self.lang_code = self.data['lang_code']
            if 'admins' in self.data.keys():
                self.admin = self.data['admins']


class sticker:
    def __init__(self):
        # self.id = None
        self.set_name = None
        self.tags = None
        self.tags_text = None
        self.reason = None
        self.opid = None
        self.evidence = None

    def parse(self, data):
        # if 'id' in data['sticker'].keys():
        #    self.id = data['sticker']['id']
        if 'set_name' in data['sticker'].keys():
            self.set_name = data['sticker']['set_name']
        if 'tags' in data['sticker'].keys():
            self.tags = data['sticker']['tags']
            self.tags_text = ', '.join(self.tags)
            self.tags_list = list(to_emoji(self.tags))
            self.day = druation(self.tags)
        if 'reason' in data.keys():
            self.reason = data['reason']
        if 'opid' in data.keys():
            self.opid = data['opid']
        if 'evidence' in data.keys():
            self.evidence = data['evidence']


class media:
    def __init__(self):
        self.hash = None
        self.score = None
        self.tags = None
        self.tags_text = None
        self.tags_list = None
        self.reason = None
        self.opid = None
        self.evidence = None
        self.is_white = None

    def parse(self, data):
        if 'hash' in data['photo'].keys():
            try:
                self.hash = data['photo']['hash']
            except:
                logger.critical(data)
        if 'score' in data['photo'].keys():
            self.score = data['photo']['score']
        if 'is_white' in data['photo'].keys():
            self.is_white = data['photo']['is_white']
        if 'tags' in data['photo'].keys():
            self.tags = data['photo']['tags']
            self.tags_list = to_list(self.tags)
            self.tags_text = ', '.join(self.tags_list)
        if 'reason' in data.keys():
            self.reason = data['reason']
        if 'opid' in data.keys():
            self.opid = data['opid']
        if 'evidence' in data.keys():
            self.evidence = data['evidence']
