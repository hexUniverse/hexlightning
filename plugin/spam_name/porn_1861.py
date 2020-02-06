import re


class porn_1861:
    def __init__(self):
        self.tags = ['porn', 'ads']

    def detect(self, full_name):
        '''
        return: 
            tuple (True, 'Coin_Dex_Spam', [result])
        '''
        pattern = '(1861\.app|1861app|xingtao\.app|1861点APP)'
        result = re.findall(pattern, full_name)
        if result:
            return (True, 'porn_ads_1861.app', result)
        else:
            return (False, 'porn_ads_1861.app', None)
