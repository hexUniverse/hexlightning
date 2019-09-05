import re
import logging
import coloredlogs
import unicodedata

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


class langdetec:
    def __init__(self):
        logger.debug('Init')

    def detecor(self, text, ban=['arabic', 'cyrillic'], full=None):
        # pre process #
        text = ''.join(c for c in unicodedata.normalize(
            'NFC', text) if c <= '\uFFFF')
        text = re.sub('[\u2600-\u26FF\u200D]+| ', '', text)
        # pre process #
        total = len(text)
        cacu = {}

        for content in text:
            try:
                result = unicodedata.name(content).lower()  # 語系名稱
            except ValueError:
                result = 'error'
            category = result.split()[0]
            if category not in cacu.keys():
                cacu[category] = 1
            else:
                cacu[category] += 1
        for category in cacu:
            cacu[category] = cacu[category]/total
        sorted_ = sorted(cacu.items(), key=lambda kv: kv[1])

        self.confidence = sorted_[-1][1]
        self.max = sorted_[-1][0]
        self.full = sorted_
        if self.max in ban and self.confidence >= 0.3:
            self.result = True
        else:
            self.result = False
