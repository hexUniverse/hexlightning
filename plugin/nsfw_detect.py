import logging
import coloredlogs
import requests
from plugin import config


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
ban_range = 0.89


class nsfw_detect:
    def __init__(self, file=None, url=None):
        self.file = file
        self.url = url
        self.result = None
        self.status = None
        self.reason = None
        self.score = None
        self.raw = None
        self.ban = None
        self.detect(file, url)

    def detect(self, file=None, url=None):
        '''
        sticker, photo, gif, video
        '''

        if file:
            file = {'file': file}
            r = requests.post(config.get('machine', 'nsfw'), files=file)

        elif url:
            data = {'url': url}
            r = requests.post(config.get('machine', 'nsfw'), data=data)

        if r.status_code in [400, 200]:
            result = r.json()
            self.raw = result
            if 'status' in result.keys():
                self.status = result['status']
            if 'score' in result.keys():
                self.score = result['score']
            if 'reason' in result.keys():
                self.reason = result['reason']
            if self.score:
                if self.score >= ban_range:
                    self.ban = True
                else:
                    self.ban = False
