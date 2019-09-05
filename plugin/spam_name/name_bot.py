import re
import telegram
from telegram.ext import run_async


class name_bot:
    def __init__(self):
        self.tags = ['spam']

    def detect(self, full_name):
        '''
        information bot|dexinfo bot|announcement bot

        return: 
            tuple (True, 'Coin_Dex_Spam', [result])
        '''
        pattern = '(bot)'
        result = re.findall(pattern, full_name)
        if result:
            return (True, 'AutoReport_Bot_Name_', result)
        else:
            return (False, 'AutoReport_Bot_Name_', None)
