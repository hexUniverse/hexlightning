import re


class ad82cc:
    def __init__(self):
        self.tags = ['porn', 'ads']

    def detect(self, full_name):
        '''
        return: 
            tuple (True, 'Coin_Dex_Spam', [result])
        '''
        pattern = '(ad\d+.cc)'
        result = re.findall(pattern, full_name)
        if result:
            return (True, 'porn_ads_ad82.cc', result)
        else:
            return (False, 'porn_ads_1861.app', None)
