import json
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


class user:
    def __init__(self):
        self.id = None
        self.first_name = None
        self.last_name = None
        # f'{self.first_name}{self.last_name}' if self.first_name else self.first_name
        self.fullname = None
        self.username = None
        self.is_bot = None
        self.language_code = None
        self.is_white = None
        self.participte = None
        self.history = None
        self.current = None

        #self.config_lang = None
        self.config = None

    def parse(self, data):
        user = data['chat']
        if 'config' in data.keys():
            self.config = self.config_(data['config'])

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
        if 'history' in user.keys():
            self.history = user['history']
        if 'current' in user.keys():
            self.current = user['current']

        # if 'config_lang' in user.keys():
        #    self.config_lang = user['config_lang']

    class config_:
        def __init__(self, data):
            self.data = data
            self.lang = None

            self.parse()

        def parse(self):
            if 'lang' in self.data.keys():
                self.lang = self.data['lang']


class group:
    def __init__(self):
        self.title = None
        self.id = None
        self.white_participate = None
        #self.config = self.config_()
        self.config = None

    def parse(data):
        try:
            self.data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.exception(e)
            return
        else:
            if 'config' in self.data:
                self.config = self.config_(data['config'])

    class config_:
        def __init__(self, config_data):
            self.data = config_data

        def sub_ban_list(self):
            if 'sub_ban_list' not in self.data.keys():
                return None
            return self.data['sub_ban_list']

        def configuring(self):
            pass

        def ml_nsfw(self):
            pass
