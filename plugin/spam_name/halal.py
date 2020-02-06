from plugin import langdetec


class halal:
    def __init__(self):
        self.tags = ['halal']
        self.halal = langdetec()

    def detect(self, full_name):
        self.halal.detecor(full_name)
        if self.halal.result:
            return (True, f'halal_{self.halal.max}', '花瓜')
        else:
            return (False, f'halal_{self.halal.max}', None)
