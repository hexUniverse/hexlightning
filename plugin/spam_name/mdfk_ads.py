import re
import telegram
from telegram.ext import run_async


class mdfk_ads:
    def __init__(self):
        self.tags = ['ads']

    def detect(self, full_name):
        '''
        ★加Q群537592562下载 253款破解版看片APP★免会员★免推广★无限看
        return: 
            tuple (True, 'QQ_Spam', [result])
        '''
        pattern = '(軟件定製|機器人軟件|炸群服務|招代理|股票決策|廣告代發|推廣極速|價格極低|免費看黃|福利視頻|ais20|拉中文用戶|拉國外用戶)'
        result = re.findall(pattern, full_name)
        if result:
            return (True, 'mdfk_ads', result)
        else:
            return (False, 'mdfk_ads', None)
