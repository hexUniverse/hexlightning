import re


class dexcoin_spam:
    def __init__(self):
        self.tags = ['coin', 'spam']

    def detect(self, full_name):
        '''
        informationbot|dexinfobot|announcementbot

        return:
            tuple (True, 'Coin_Dex_Spam', [result])
        '''
        pattern = '(informationbot|dexinfobot|announcementbot|binanceairdropbot)'
        result = re.findall(pattern, full_name)
        if result:
            return (True, 'Coin_Dex_Spam', result)
        else:
            return (False, 'Coin_Dex_Spam', None)
