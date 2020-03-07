import re


class scam:
    def __init__(self):
        self.tags = ['scam']

    def detect(self, full_name):
        '''
        银行卡|四件套|銀行儲蓄卡
        return:
            tuple (True, 'Scam_ads', [result])
        '''
        pattern = '(银行卡|四件套|銀行儲蓄卡|實力卡商|黑產指導|暗網資源)'
        result = re.findall(pattern, full_name)
        if result:
            return (True, 'Scam_ads', result)
        else:
            return (False, 'Scam_ads', None)
