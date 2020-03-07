import re


class qqspam:
    def __init__(self):
        self.tags = ['ads']

    def detect(self, full_name):
        '''
        ★加Q群537592562下载 253款破解版看片APP★免会员★免推广★无限看
        return:
            tuple (True, 'QQ_Spam', [result])
        '''
        pattern = '(无限看|免推广|免会员|看片APP|加Q群|537592562|破解版|请加Q|1943675344)'
        result = re.findall(pattern, full_name)
        if result:
            return (True, 'QQ_Spam', result)
        else:
            return (False, 'QQ_Spam', None)
